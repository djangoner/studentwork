import json
import logging
# import asyncio
# import datetime
from asgiref.sync import async_to_sync

from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer
# from channels.generic.http import AsyncHttpConsumer

# import channels.layers
# from django.db.models import Q, F
# from django.utils import timezone

from . import models
from django.db.models import Q

log = logging.getLogger("Channels consumers")


def chat2json(chat, is_admin):
    last_msg = chat.get_last_message()
    if last_msg:
        last_message = msg2json(last_msg)
    else:
        last_message = {}
    return {
        "first_name": chat.user.first_name,
        "username": chat.user.username,
        "last_message": last_message,
        "unread_count": chat.get_unread_count(is_admin=is_admin),
        "id": chat.id,
    }

def msg2json(msg):
    return {
        "text": msg.text,
        "author": msg.author,
        "id": msg.id,
        "chat_id": msg.chat.id,
        "created": msg.created.timestamp(),
    }

def chat_history(chat, offset=0, limit=25):
    if limit > 100:
        limit = 100
    return list(map(msg2json, chat.messages.all()[offset:offset+limit:-1]))

def save_last_online(user):
    pass
    # user.last_online = timezone.now()
    # user.save()

import uuid
LAUNCH_TOKEN = str(uuid.uuid4())

def user2dict(user):
    return {
        "id": user.id, 
        "username": user.username, 
        "first_name": user.first_name,
    }

class ChatConsumer(WebsocketConsumer):
    group_name = "chat"
    group_name_f = "chat-{}"
    group_admin= "chat-all"
    online = []
    logout_initiator = False

    @property
    def is_admin(self):
        return models.is_admin(self.user)

    def connect(self):
        self.user = self.scope["user"]
        # Check other login
        if not self.user.is_authenticated: # If not authorized
            self.accept() # Accept and
            self.send_data({}, "logout") # send logout signal
            self.send({"close": True}) # and close socket
            return
        self.accept()
        self.upd_online(1)
        is_admin = self.is_admin
        # Connect to chat group
        try:
            chat = models.Chat.objects.get(user=self.user)
        except models.Chat.DoesNotExist:
            chat = models.Chat.objects.create(user=self.user)
            self.handle_new_chat(chat)

        self.group_name = self.group_admin if is_admin else f"chat-{chat.id}"
        log.debug("Connected new as: {self.group_name} ({self.user})")
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        #
        # if not self.user.IsActive:
        #     self.logout_user({'user_id': self.user.id})
        #     return
        #
        chats = []
        if is_admin:
            chats = [chat2json(chat, is_admin) for chat in models.Chat.objects.all()[:25] if chat.user.id != self.user.id]
        else:
            chats = [
                {
                    'id': chat.id,
                    'first_name': 'Admin',
                    'last_name': 'Admin',
                    'username': 'admin',
                    'last_message': '?'
                }
            ]
        D = {
            "token": LAUNCH_TOKEN,
            "chats": chats,
            "is_admin": self.is_admin,
            "you": {'first_name': 'Admin', 'last_name': 'Admin', 'username': 'admin'},
        }
        self.send_data(D, "connection_info")
        save_last_online(self.user) # Save last online


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
        self.upd_online(0)
        save_last_online(self.user) # Save last online


    def receive(self, text_data):
        def find_chat(chat_id):
            try:
                chats = models.Chat.objects
                if not self.is_admin:
                    chats = chats.filter(user=self.user)
                chat = chats.get(pk=chat_id)
            except models.Chat.DoesNotExist:
                self.send_data({
                    "result": "error",
                    "error": "chat_not_exists",
                }, "chat_data")
                return False
            else:
                return chat

        data = json.loads(text_data)
        type = data.get('type')
        log.debug(f"Received from client: {data}")

        if type == "send_message":
            chat_id = data["chat_id"]
            text    = data["text"]
            chat = find_chat(chat_id)
            # print("Message chat:", chat)
            if chat:
                # print("Message sended!")
                msg = models.ChatMessage.objects.create(chat=chat, author="user" if chat.user == self.user else "admin", text=text)
                msg.save()
                self.handle_new_message(msg)

        elif type == "request_chat":
            chat_id = data["chat_id"]
            chat = find_chat(chat_id)
            if chat:
                self.send_data({
                    "result": "ok",
                    "history": chat_history(chat, offset=data.get('offset', 0), limit=data.get('limit', 0)),
                    "request_info": data,
                }, "chat_data")

        elif type == "chat_readed":
            chat_id = data["chat_id"]
            chat = find_chat(chat_id)
            if chat:
                chat.mark_readed(is_admin=self.is_admin)
                # self.send_data({
                #     "result": "ok",
                # }, "cb_readed")
        elif type == "search_users":
            if not self.is_admin:
                self.send_data({
                    "result": "error",
                    "error": "access_denied",
                }, "cb")
                return
            #
            q = data["search"]
            results = models.Chat.objects.filter(Q(user__first_name__icontains=q) | Q(user__username__icontains=q) | Q(user__email__icontains=q))[:15]

            self.send_data({
                "result": "ok",
                "results":[ chat2json(c, is_admin=True) for c in results]
            }, "search_suggestions")

        else:
            log.debug(f"Unrecognized data type: {type}\n{data}")
        # async_to_sync(self.channel_layer.group_send)(
        #     self.group_name,
        #     {
        #         'type': 'new_record',
        #         'data': {}
        #     }
        # )
    def upd_online(self, val):
        pass

    def new_message(self, event):
        self.send_data({"message":event["message"]}, "new_message")

    def new_chat(self, event):
        self.send_data({"chat":event["chat"]}, "new_chat")

    ###-- Actions
    def send_data(self, data, type):
        if isinstance(data, dict):
            dt = data.copy()
            dt['type'] = type
        else:
            dt = data
        self.send(text_data=json.dumps(dt))

    def handle_new_message(self, msg):
        dt = {
                'type': 'new_message',
                "message": msg2json(msg)
            }
        async_to_sync(self.channel_layer.group_send)(self.group_name_f.format(msg.chat.id), dt)
        # if not self.is_admin:
        async_to_sync(self.channel_layer.group_send)(self.group_admin, dt)

    def handle_new_chat(self, chat):
        dt = {
                'type': 'new_chat',
                "chat": chat2json(chat, self.is_admin)
            }
        async_to_sync(self.channel_layer.group_send)(self.group_name_f.format(chat.id), dt)
        # if not self.is_admin:
        async_to_sync(self.channel_layer.group_send)(self.group_admin, dt)

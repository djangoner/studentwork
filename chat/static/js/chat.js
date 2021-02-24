const options = {

    moduleCache: {
      vue: Vue
    },

    async getFile(url) {
      const res = await fetch(url);
      if ( !res.ok )
        throw Object.assign(new Error(url+' '+res.statusText), { res });
      return await res.text();
    },

    addStyle(textContent) {
      const style = Object.assign(document.createElement('style'), { textContent });
      const ref = document.head.getElementsByTagName('style')[0] || null;
      document.head.insertBefore(style, ref);
    },
  }

  
  const { loadModule } = window['vue3-sfc-loader'];
  // Sockets
  
function scrollLastMessage(){
    var last = $(".messages-container .message").last()[0]
    if (last){
        last.scrollIntoView()
    }
}
var errors = 0;
var TOKEN = null;
function connect(){
    var protocol = (location.protocol == "http:") ? 'ws://' : "wss://"
    // console.log(protocol)
    const socket = new WebSocket(
        protocol
        + window.location.host
        + '/ws/chat'
    );
    window.socket = socket
    // console.log(socket)
    socket.onopen = function(){
        errors = 0
        console.log("Socket opened")
        app.connected = true;
    }
    socket.onmessage = function(e) {
        const data = JSON.parse(e.data)
        var type = data.type
        console.log("Socket msg:", type)

        // Handle messages from server
        if (type == "new_message") {
            console.log("MSG:", data)
            app.dialog.messages.push(data.message)
            // Find in users list
            usr = app.chats.filter((c)=>{return c.id===app.dialog.id})[0]
            if (usr){
                usr.last_message = data['message'].text
            }
            Vue.nextTick(()=>{
                scrollLastMessage()
            })
        
        } else if (type == "connection_info") {
            console.log(data)
            app.chats.length = 0
            app.chats = data.chats
            app.chats_loading = false
            app.is_admin = data.is_admin
            app.current_user = data.you
            // console.log(app.chats)
            token = data.token
            if (!TOKEN){
                TOKEN = token
            } else {
                if (TOKEN != token){
                    console.log("Server restart detected! Reloading page!")
                    console.reload(true)
                }
            }

        } else if (type == "chat_data") {
            res = data["result"]
            app.dialog_loading = false;
            app.dialog_loading_more = true;
            if (res == "ok"){
                console.log("OK, received chat history", data)
                if (data.request_info.offset > 0){ // If requested next page
                    // Mark as first block if returned empty history or less than requested limit
                    if (data.history.length < 1 || data.history.length < data.request_info.limit){
                        app.dialog.scrolled_first = true
                    }
                    var old = app.dialog.messages
                    var last_viewed_id = $(".messages-container .message").first().attr('id')
                    app.dialog.messages = Array.prototype.concat(data.history, old)
                    Vue.nextTick(()=>{
                        console.log(last_viewed_id)
                        $("#"+last_viewed_id)[0].scrollIntoView({block: 'start', behavior: 'instant'})
                    })
                } else { // If first request
                    app.dialog.messages = data.history
                    // Scroll to last
                    Vue.nextTick(()=>{
                        scrollLastMessage()
                    })
                }
            } else {
                console.log("ERR:", data["error"])
            }

        } else if (type == "logout") {
            location.href = "/auth/logout"

        } else if (type == "reload") {
            location.reload(true)

        } else {
            console.error("Unkown data type:", type, data)
        }
    }
    socket.onclose = function(e) {
        console.error("Socket closed!")
        errors += 1
        // Show error and reset texts and counters
        // if (errors <= 2){ // 2 times
        // }
        app.connected = false;
        setTimeout(function(){connect()}, 5000)
    }
    socket.onerror = function(err){
        console.log("Socket err:", errors, err)
        socket.close()
    }
}
function socketInit(){
    console.log("Connecting to socket...")
    connect()
}

function socketSend(data){
    window.socket.send(JSON.stringify(data))
}

function sendMessage(e){
    if (e){
        e.preventDefault();
    }
    var input = $(e.target).find('textarea') // Find input
    //
    var text = input.val() || e.target.val()
    if (!text){
        console.log("Text empty!")
        return
    }
    input.val('') // Clear input
    socketSend({
        type: 'send_message',
        text: text,
        chat_id: app.dialog.id,
    })
}

function requestChat(chat_id, offset=0, limit=25){
    socketSend({
        type: 'request_chat',
        chat_id: chat_id,
        offset: offset,
        limit: limit
    })
}


var appConfig = {
    el: '#app',
    data() {
        return {
            is_admin: null,
            chats: [],
            chats_loading: true,
            dialog_loading: false,
            dialog_loading_more: false,
            connected: null,
            dialog:{
                messages: [],
                user: {},
                scrolled_first: false,
            },
            current_user: {
                'first_name': 'Current user',
                'last_name': 'The best',
                'username': '@current',
            }
        }
    },
    components:{
        //httpVueLoader('/static/js/vue/Chat-users.vue')
        'chat-users': Vue.defineAsyncComponent( () => loadModule('/static/js/vue/Chat-users.vue', options) ),
        'chat-dialog': Vue.defineAsyncComponent( () => loadModule('/static/js/vue/Chat-dialog.vue', options) ),
    },
    methods: {
        selectDialog(user){
            console.log("Requesting dialog:", user)
            // setTimeout(()=>{
                // }, 3000)
            requestChat(user.id)
            this.dialog_loading = true
            this.dialog.user = user
            this.dialog.id = user.id
            this.dialog.messages = []
            this.dialog.scrolled_first = false
        },
        loadOldMessages(){
            if (this.dialog.scrolled_first){
                this.dialog_loading_more = false;
                return
            }
            var offset = this.dialog.messages.length
            var limit  = 25
            console.debug("Loading old messages...", " offset:", offset, " limit:", limit)
            this.dialog_loading_more = true;
            requestChat(this.dialog.id, offset=offset, limit=limit)
        }
    },
}
const pre_app = Vue.createApp(appConfig)
pre_app.component('loading-indicator', {
    template: `
<div class="loading-indicator d-flex w-fit-content mx-auto my" :class="'my-' + my">
    <div class="ring mr-2">
            <div class="lds-dual-ring"></div>
    </div>
    <h5 class="text-center" :style="{'line-height': size+'px'}">Загрузка...</h5>
</div>`,
    props: {
        size: {
            type: String,
            default: "80",
        },
        my: {
            type: String,
            default: '5',
        },
    }
})
const app = pre_app.mount('#app')
socketInit()

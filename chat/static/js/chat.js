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
    $(".messages-container .message").last()[0].scrollIntoView()
}

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
            app.is_admin = data.is_admin
            app.current_user = data.you
            console.log(app.chats)

        } else if (type == "chat_data") {
            res = data["result"]
            if (res == "ok"){
                console.log("OK, received chat history", data["history"])
                app.dialog.messages = data["history"]
                // Scroll to last
                Vue.nextTick(()=>{
                    scrollLastMessage()
                })
            } else {
                console.log("ERR:", data["error"])
            }

        } else if (type == "logout") {
            location.href = "/logout"

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
        setTimeout(function(){connect()}, 3000)
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
    e.preventDefault();
    var input = $(e.target).find('textarea') // Find input
    //
    var text = input.val()
    input.val('') // Clear input
    socketSend({
        type: 'send_message',
        text: text,
        chat_id: app.dialog.id,
    })
}

function requestChat(chat_id){
    socketSend({
        type: 'request_chat',
        chat_id: chat_id,
    })
}


var appConfig = {
    el: '#app',
    data() {
        return {
            is_admin: null,
            chats: [],
            dialog:{
                messages: [],
                user: {},
            },
            current_user: {
                'first_name': 'Current user',
                'last_name': 'The best',
                'username': '@current',
            },
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
            requestChat(user.id)
            this.dialog.user = user
            this.dialog.id = user.id
            this.dialog.messages = []
        }
    },
}
const app = Vue.createApp(appConfig).mount('#app')
socketInit()

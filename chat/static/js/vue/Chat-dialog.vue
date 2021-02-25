<template v-id="dialog">
  <div class="wrapper">
    <div class="dialog-container" v-if="dialog.user.id" @scroll="onScroll">
      <!-- <div>Dialog {{dialog}}</div> -->

      <!-- Messages container -->
      <div class="messages-container">
        <div v-if="loading_more">
          <loading-indicator my="1"></loading-indicator>
        </div>
        <div :class="['message', 'from-'+message_from(message)]" v-for="(message, idx) in dialog.messages" :key="idx" :id="'msg-' + message.id">
          <!-- Message content -->
          <div class="message-author">{{ message_user(message).first_name }}</div>
          <div class="message-content">
            <div class="file-content" v-if="message.is_attachment">
              Файл:
              <a :href="message.attachment.url" download>{{message.attachment.name}}</a>
            </div>
            <span v-else>{{ message.text }}</span>
            </div>
          <div class="message-meta small text-muted">{{ readableDate(message.created) }}</div>
        </div>
      </div>

        <!-- Send message form -->
        <form action="" id="message-send-form" onsubmit="sendMessage(event);false" class="send-message">
          <div class="input-group">
            <div class="input-group-prepend">
              <input type="file" name="file" id="send_file_input" style="display:none!important" @change="sendFile">
              <button class="btn btn-primary" type="button" @click="selectFile">
                <i class="fa fa-paperclip"></i>
              </button>
            </div>
            <textarea type="text" name="message" placeholder="Сообщение..." class="form-control" style="resize:none;" rows="2"
                ></textarea>
                <!-- @keyup.ctrl.enter="sendMessage" -->
            <div class="input-group-append">
              <button type="submit" class="btn btn-success">
                <i class="fa fa-send"></i>
              </button>
            </div>
          </div>
        </form>
    </div>

    <!-- On empty -->
    <div class="other">
      <div class="empty-container" v-if="!dialog.user.id">
        <h3 class="text-center my-5">Выберите диалог для просмотра сообщений</h3>
      </div>
      <!-- Loading indicator -->
      <div v-if="loading">
        <loading-indicator>
      </div>
    </div>
  </div>
</template>

<script>
var scrollTimer = null;
module.exports = {
  name: "Chat-dialog",
  created() {},
  data() {
    return {
      // dialog: {},
    };
  },
  props: {
    dialog: {},
    current_user: {},
    is_admin: null,
    loading: false,
    loading_more: false,
  },
  methods: {
    message_from(msg){
      // return msg.author
      if (this.is_admin){
        return msg.author==='user'?'other':'self';
      } else {
        return msg.author==='user'?'self':'other';

      }
    },
    message_user(msg){
      if (this.is_admin){
        return msg.author === 'user' ? this.dialog.user : this.current_user
      } else {
        return msg.author === 'user' ? this.current_user : this.dialog.user

      }
    },
    onScroll(event){
      // Clear timeout
      if (scrollTimer){clearTimeout(scrollTimer)}
      // Set timeout
      scrollTimer = setTimeout(() => {
        var scroll_pos = event.target.scrollTop
        // console.log(scroll_pos)
        if (scroll_pos == 0){
          // console.debug("Scrolled to top!")
          this.$emit('load_old')
        }
      }, 100)
    },
    sendMessage(event){
      sendMessage(event)
    },

    selectFile(event){
      // console.log(event)
      $("#send_file_input").trigger('click')
      console.debug("Opened file select")
    },

    sendFile(event){
      var file = event.target.files[0]
      console.log("File selected:", file, event)
      var size_mb = (file.size / (1024 * 1024)).toFixed(2)
      var max_mb = 10
      if (size_mb > max_mb){
        showAlert(`Вы выбрали слишком большой файл! ${size_mb} МБ. (можно не больше ${max_mb} МБ.)`, 'danger', timeout=15000)
        return
      }
      $('#message-send-form').submit() // Call sendMessage handler
    },

    mediaPath(path){
      return '/media/' + path
    },

    readableDate(date){
      var options = {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric'
      };
      return new Date(date*1000).toLocaleString('ru', options)
    },
  },
};
// Scrollspy
</script>

<style lang="scss" scoped></style>
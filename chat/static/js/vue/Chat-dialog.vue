<template>
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
            <div class="file-content mb-1" v-if="message.is_attachment">
              <b>Файл: </b>
              <a :href="message.attachment.url" download>{{message.attachment.name}}</a>
            </div>
            <span>{{ message.text }}</span>
            </div>
          <div class="message-meta small text-muted">{{ readableDate(message.created) }}</div>
        </div>
      </div>

        <!-- Send message form -->
        <form action="" id="message-send-form" onsubmit="sendMessage(event);false" class="send-message">

          <!-- File sending indicator -->
          <div class="uploading-indicator hide text-center mb-1 d-flex justify-content-center">
            <div style="width: 150px;height:fit-content" class="align-self-center">
              <div class="progress">
                <div class="progress-bar progress-bar-striped progress-bar-animated" style="width: 0%;"></div>
              </div>
            </div>
            <span class="ml-2">
              Отправка файла...
            </span>
          </div>
          
          <!-- Attachment indicator -->
          <div class="text-center d-inline" v-if="attachment">
            <h6>
              Прикрепленный файл: <span class="text-info">{{attachment}}</span>
              <button type="button" @click="attachmentClear" class="btn btn-sm btn-outline-secondary ml-1" style="padding: 0.05rem 0.2rem;">&times;</button>
            </h6>
          </div>

          <!-- New message input -->
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
      attachment: null,
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
      console.log(this, this.attachment)
      this.attachment = file.name
      // $('#message-send-form').submit() // Call sendMessage handler
    },

    attachmentClear(){
      var inp = $('#message-send-form input[type=file]') // Find file input
      inp.val('') // reset file input value
      this.attachment = null //reset attachment file name
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
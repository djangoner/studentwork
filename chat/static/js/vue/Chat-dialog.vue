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
          <div class="message-content">{{ message.text }}</div>
          <!-- <div class="message-meta small text-muted">{{ messages.created }}</div> -->
        </div>
      </div>
        <form action="" id="message-send-form" onsubmit="sendMessage(event);false" class="send-message">
          <div class="input-group">
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
        <h3 class="text-center my-5">Выберите диалог для показа сообщений</h3>
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
  }
  },
};
// Scrollspy
</script>

<style lang="scss" scoped></style>
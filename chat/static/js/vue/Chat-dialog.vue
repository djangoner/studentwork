<template v-id="dialog">
  <div class="dialog-container" v-if="dialog.user.id">
    <!-- <div>Dialog {{dialog}}</div> -->

    <!-- Messages container -->
    <div class="messages-container">
      <div :class="['message', 'from-'+message.author]" v-for="(message, idx) in dialog.messages" :key="idx">
        <!-- Message content -->
        <div class="message-author">{{ message_user(message).first_name }}</div>
        <div class="message-content">{{ message.text }}</div>
        <!-- <div class="message-meta small text-muted">{{ messages.created }}</div> -->
      </div>
    </div>
      <form action="" id="message-send-form" onsubmit="sendMessage(event);false" class="send-message">
        <div class="input-group">
          <textarea type="text" name="message" placeholder="Сообщение..." class="form-control" style="resize:none;"></textarea>
          <div class="input-group-append">
            <button type="submit" class="btn btn-success">
              <i class="fa fa-send"></i>
            </button>
          </div>
        </div>
      </form>
  </div>

  <!-- On empty -->
  <div class="empty-container" v-else>
    <h3 class="text-center my-5">Выберите диалог для показа сообщений</h3>
  </div>
</template>

<script>
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
  },
  methods: {
    message_user(msg){
      return msg.author === 'user' ? this.dialog.user : this.current_user
    }
  },
};
</script>

<style lang="scss" scoped></style>
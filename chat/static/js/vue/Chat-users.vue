<template>
  <div>
    <h5 class="text-center my-3">Чаты <span v-if="is_admin" class="small text-muted">(Admin)</span></h5>
    <div class="search my-2" v-if="is_admin">
      <input type="search" name="search" id="search_users_form" class="form-control form-control-sm" placeholder="Найти пользователя" v-model="search_text">
    </div>
    <div class="err text-center small alert-danger py-2" v-if="connected == false">
      <h6 class="m-0">Нет соединения с сервером!</h6>
    </div>
    <div class="users-list">
      <div :class="['user-card', user.selected? 'active':'']" v-for="(user, idx) in chatsList" :key="idx" @click="onDialog(user)">
        <div class="card-title">
            <span class="username">{{ user.first_name }}: </span>
            <span class="last-message">
              <span v-if="user.last_message !== null">
                <span v-if="user.last_message.is_attachment">Файл</span>
                <span v-else>{{ short(user.last_message).text }}</span>
                </span>
              <span v-else>Нет сообщений!</span>
              </span>
            <span class="unread-count badge bg-light" v-if="user.unread_count>0">{{ user.unread_count }}</span>
          </div>
      </div>
      <div v-if="chats.length<1 && loading">
        <loading-indicator>
      </div>
    </div>
  </div>
</template>

<script>
module.exports = {
  name: "chat-users-list",
  created() {},
  data() {
    return {
      search_text: "",
      // chats: [],
    };
  },
  props: {
    chats: Array,
    is_admin: null,
    loading: false,
    connected: false,
    current_user: Object,
  },

  computed: {
    chatsList(){
      function compareFunc(a, b){
        if (a.unread_count > b.unread_count){
          return -1
        } 
        if (b.unread_count > a.unread_count){
          return 1
        }
      }
      return this.chats.sort(compareFunc)
    },
  },

  methods: {
    onDialog(user){
      this.chats.some(u => {u.selected = false;})
      user.selected = true
      this.$emit('select_dialog', user)
    },
  
    short(tx){
      var ml = 70
      if (tx.length > ml){
        return tx.slice(0, ml) + "..."
      } else {
        return tx
      }
    },

    message_user(chat){
      if (this.is_admin){
        return chat.author === 'user' ? chat : this.current_user
      } else {
        console.log(chat)
        return chat.author === 'user' ? this.current_user : chat

      }
    },
  },

  watch: {
    search_text(newSearch, oldSearch){
      this.$emit("searching", newSearch)
    }
  },
};
</script>

<style scoped></style>
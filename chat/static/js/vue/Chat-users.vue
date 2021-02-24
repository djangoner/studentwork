<template>
  <div>
    <h5 class="text-center my-3">Чаты <span v-if="is_admin"><i class="fa fa-gears" title="Вы администритор"></i></span></h5>
    <div class="err text-center small alert-danger py-2" v-if="connected == false">
      <h6 class="m-0">Нет соединения с сервером!</h6>
    </div>
    <div class="users-list">
      <div :class="['user-card', user.selected? 'active':'']" v-for="(user, idx) in chatsList" :key="idx" @click="onDialog(user)">
        <div class="card-title">
            <span class="username">{{ user.first_name }}: </span>
            <span class="last-message">
              <span v-if="user.last_message !== null">{{ short(user.last_message) }}</span>
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
      // chats: [],
    };
  },
  props: {
    chats: Array,
    is_admin: null,
    loading: false,
    connected: false,
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
    }
  },
};
</script>

<style scoped></style>
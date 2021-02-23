<template>
  <div>
    <h5 class="text-center my-3">Чаты <span v-if="is_admin"><i class="fa fa-gears" title="Вы администритор"></i></span></h5>
    <div class="users-list">
      <div :class="['user-card', user.selected? 'active':'']" v-for="(user, idx) in chats" :key="idx" @click="onDialog(user)">
        <div class="card-title">
            <span class="username">{{ user.first_name }}: </span>
            <span class="last-message">
              <span v-if="user.last_message !== null">{{ short(user.last_message) }}</span>
              <span v-else>Нет сообщений!</span>
              </span>
          </div>
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
    chats: [],
    is_admin: null,
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
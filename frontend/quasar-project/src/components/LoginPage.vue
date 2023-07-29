<!-- src/components/LoginPage.vue -->
<template>
  <div>
    <h1>Login Page</h1>
    <form @submit.prevent="login">
      <input v-model="username" type="text" placeholder="Username" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    login() {
      // Perform login logic here, e.g., calling an API and handling the response
      // Upon successful login, you can store the user token or data in LocalStorage or Vuex
      // For simplicity, let's assume a successful login always redirects to the Tasks Page.
      this.$router.push('/tasks');
    },
  },
};
</script>


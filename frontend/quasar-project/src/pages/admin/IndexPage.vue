<template>
  <h1>Protected route</h1>
  <h3>hello {{ me }}</h3>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'IndexPage',
  computed: {
    me () {
      let me
      try {
        me = this.getMe
      } catch (err) {
        console.log('mmmmeee', err)
      }
      return me
    },
    ...mapGetters('auth', ['getMe'])
  }
}
</script>

<style scoped>

</style>

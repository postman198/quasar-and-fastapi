import { boot } from 'quasar/wrappers'
import axios from 'axios'
// import state from '../store/auth/state'

// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)
const BACKEND_URL = 'http://localhost:8000'
console.log('url :', BACKEND_URL)
const api = axios.create({ baseURL: BACKEND_URL, headers: { 'content-type': 'application/x-www-form-urlencoded' } })
api.interceptors.response.use(null, (error) => {
  if (error.response.status === 403) {
    // console.log('store.dispatch(logout)', state)
  }
  return Promise.reject(error)
})

const apiSignUp = axios.create({ baseURL: BACKEND_URL })

export default boot(({ app }) => {
  // for use inside Vue files (Options API) through this.$axios and this.$api

  app.config.globalProperties.$axios = axios
  // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
  //       so you won't necessarily have to import axios in each vue file

  app.config.globalProperties.$api = api
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API
})

export { axios, api, apiSignUp }

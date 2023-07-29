export const setToken = (state, token) => {
  state.token = token
  state.isAuthenticated = true
  window.localStorage.setItem('token', JSON.stringify(token))
}

export const removeToken = (state) => {
  console.log('remove token')
  state.token = null
  state.isAuthenticated = false
  window.localStorage.setItem('token', null)
  window.localStorage.setItem('isAuthenticated', false)
}

export const setMe = (state, me) => {
  state.me = me
}

export const setTasks = (state, tasks) => {
  state.tasks = tasks
}

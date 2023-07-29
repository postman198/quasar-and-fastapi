import { api } from 'boot/axios'

export const doLogin = async ({ commit, dispatch }, payload) => {
  console.log(payload)
  api.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
  await api.post('/token', payload).then(response => {
    const accessToken = response.data.access_token
    console.log('response:', response)
    commit('setToken', accessToken)
    api.defaults.headers.common.Authorization = 'Bearer ' + accessToken
    dispatch('fetchTasks', accessToken)
    dispatch('getMe', accessToken)
  })
}

export const signOut = ({ commit }) => {
  console.log('signOut')
  api.defaults.headers.common.Authorization = ''
  commit('removeToken')
}

export const getMe = async ({ commit }, token) => {
  try {
    await api.get('/api/users/current-user', token).then(response => {
      commit('setMe', response.data)
    })
  } catch (err) {
    console.log(err)
    if (err.response.data.detail) {
      if (err.response && err.response.status === 403) {
        console.log('error: ', err.response.data.detail)
        await commit('removeToken')
      }
      throw err
    }
  }
}

export const init = async ({ commit, dispatch }) => {
  try {
    const token = localStorage.getItem('token')
    if (token) {
      await commit('setToken', JSON.parse(token))
      api.defaults.headers.common.Authorization = 'Bearer ' + JSON.parse(token)
      dispatch('getMe', JSON.parse(token))
      dispatch('fetchTasks', token)
    } else {
      commit('removeToken')
    }
  } catch (err) {
    console.log(err)
    if (err.response.data.detail) {
      if (err.response && err.response.status === 403) {
        console.log('error: ', err.response.data.detail)
        commit('removeToken')
        location.reload()
      }
      throw err
    }
  }
}

// tasks methods
export const fetchTasks = async ({ commit }, token) => {
  try {
    if (token) {
      await api.get('/api/tasks/current-user-tasks', token).then(response => {
        commit('setTasks', response.data)
      })
    } else {
      const tokenFromStore = localStorage.getItem('token')
      api.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
      await api.get('/api/tasks/current-user-tasks', tokenFromStore).then(response => {
        commit('setTasks', response.data)
      })
    }
  } catch (err) {
    console.log(err)
    if (err.response.data.detail) {
      if (err.response && err.response.status === 403) {
        console.log('error: ', err.response.data.detail)
        await commit('removeToken')
      }
      throw err
    }
  }
}

export const addTask = async ({ commit, dispatch }, payload) => {
  try {
    const tokenFromStore = localStorage.getItem('token')
    await api.post('/api/tasks/create', payload, {
      headers: {
        'Content-Type': 'application/json'
      }
    }).then(response => {
      console.log('response:', response)
      dispatch('fetchTasks', tokenFromStore)
    })
  } catch (err) {
    console.log(err)
    if (err.response.data.detail) {
      if (err.response && err.response.status === 403) {
        console.log('error: ', err.response.data.detail)
        await commit('removeToken')
      }
      throw err
    }
  }
}

export const updateTask = async ({ commit, dispatch }, task) => {
  try {
    const payload = {
      title: task.title,
      description: task.description,
      status: task.status
    }
    const id = task.id
    const tokenFromStore = localStorage.getItem('token')
    console.log('tokenFromStore :', tokenFromStore)
    await api.patch('/api/tasks/' + id, payload, {
      headers: {
        'Content-Type': 'application/json'
      }
    }).then(response => {
      console.log('response:', response)
      dispatch('fetchTasks', tokenFromStore)
    })
  } catch (err) {
    console.log(err)
    if (err.response.data.detail) {
      if (err.response && err.response.status === 403) {
        console.log('error: ', err.response.data.detail)
        await commit('removeToken')
      }
      throw err
    }
  }
}

export const removeTask = async ({ commit, dispatch }, id) => {
  try {
    const tokenFromStore = localStorage.getItem('token')
    console.log('tokenFromStore :', tokenFromStore)
    await api.delete('/api/tasks/' + id, {
      headers: {
        'Content-Type': 'application/json'
      }
    }).then(response => {
      console.log('response:', response)
      dispatch('fetchTasks', tokenFromStore)
    })
  } catch (err) {
    console.log(err)
    if (err.response.data.detail) {
      if (err.response && err.response.status === 403) {
        console.log('error: ', err.response.data.detail)
        await commit('removeToken')
      }
      throw err
    }
  }
}

export const isFormValid = ({ ...form }) => {
  let valid = true
  Object.keys(form).forEach(index => {
    const item = form[index]
    validateInput(form, index)
    if (item.error) valid = false
  })
  return valid
}

export const validateInput = ({ ...form }, field) => {
  Object.keys(form).forEach(index => {
    const item = form[index]
    if (index === field) Object.assign(item, checkInputRequirements(item))
  })
}

const checkInputRequirements = ({ ...item }) => {
  const value = item.value || ''
  const required = item.required || false
  const email = item.email || false
  const input = {
    error: false,
    msg: ''
  }
  if (!value && required) {
    input.error = true
    input.msg = item.requiredMsg || 'This field is required'
  } else if (value && email && !isEmailValid(value)) {
    input.error = true
    input.msg = item.emailMsg || 'Email is invalid'
  }
  return input
}

export const isSubmitBtn = (form) => {
  let isValid = true
  Object.keys(form).forEach(index => {
    const item = form[index]
    const value = item.value || ''
    const required = item.required || false
    const email = item.email || false
    if (!value && required) isValid = false
    else if (value && email && !isEmailValid(value)) isValid = false
  })
  return isValid
}

const isEmailValid = (value) => /^([a-zA-Z0-9](.[a-zA-Z0-9._-]*[a-zA-Z0-9]))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(value)

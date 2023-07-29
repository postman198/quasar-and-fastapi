<template>
  <div class="row" style="height: 90vh">
    <div class="col-0 col-md-6 flex justify-center content-center">
      <img src="~assets/login.svg" class="responsive" alt="login-image">
    </div>
    <div v-bind:class="{'justify-center': $q.screen.md || $q.screen.sm ||$q.screen.xs}"
         class="col-12 col-md-6 flex content-center">
      <q-card v-bind:style="$q.screen.lt.sm ? {'width': '80%'} : {'width': '50%'}">
        <q-card-section>
          <q-avatar size="103px" class="absolute-center shadow-10">
            <img src="~assets/avatar.svg" alt="avatar">
          </q-avatar>
        </q-card-section>
        <q-card-section>
          <div class="q-pt-lg">
            <div class="col text-h6 ellipsis flex justify-center">
              <h2 class="text-h2 q-my-none text-weight-regular">Sign up</h2>
            </div>
          </div>
        </q-card-section>
        <q-card-section>
          <q-form class="q-gutter-md" @submit.prevent="submitForm">
            <q-input
              outlined
              label="Enter email *"
              @update:model-value="isEmailInputValid"
              @blur="isEmailInputValid"
              v-model="signup.email.value"
              :error="signup.email.error"
              :error-message="signup.email.msg">
              <template v-slot:prepend>
                <q-icon name="email"></q-icon>
              </template>
            </q-input>
            <q-input
              label="Enter password *"
              outlined
              @update:model-value="isPasswordInputValid"
              @blur="isPasswordInputValid"
              :type="isPassword ? 'password' : 'text'"
              v-model="signup.password.value"
              :error="signup.password.error"
              :error-message="signup.password.msg">
              <template v-slot:prepend>
                <q-icon name="lock" />
              </template>
              <template v-slot:append>
                <q-icon
                  @click="isPassword = !isPassword"
                  :name="isPassword ? 'visibility_off' : 'visibility'" />
              </template>
            </q-input>
            <q-input
              label="confirm password *"
              outlined
              @update:model-value="isConfirmPasswordInputValid"
              @blur="isConfirmPasswordInputValid"
              :type="isPassword ? 'password' : 'text'"
              v-model="signup.confirmPassword.value"
              :error="signup.confirmPassword.error"
              :error-message="signup.confirmPassword.msg">
              <template v-slot:prepend>
                <q-icon name="lock" />
              </template>
              <template v-slot:append>
                <q-icon
                  @click="isPassword = !isPassword"
                  :name="isPassword ? 'visibility_off' : 'visibility'" />
              </template>
            </q-input>
            <div>
              <q-btn class="full-width" color="primary" label="Sign up" type="submit" rounded></q-btn>
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<script>
import { useQuasar } from 'quasar'
import { mapActions } from 'vuex'
import { apiSignUp } from 'src/boot/axios'
import { validateInput } from 'src/hooks'
let $q

export default {
  name: 'IndexPage',
  data () {
    return {
      signup: {
        email: {
          value: '',
          email: true,
          requiredMsg: 'Email is required!',
          emailMsg: 'Invalid email address!',
          required: true
        },
        password: {
          value: '',
          requiredMsg: 'Password is required!',
          required: true
        },
        confirmPassword: {
          value: '',
          requiredMsg: 'Password confirmation is required!',
          required: true
        }
      },
      isPassword: true,
      isEmailInputValid: () => {
        return validateInput(this.signup, 'email')
      },
      isPasswordInputValid: () => {
        return validateInput(this.signup, 'password')
      },
      isConfirmPasswordInputValid: () => {
        return validateInput(this.signup, 'confirmPassword')
      }
    }
  },
  methods: {
    ...mapActions('auth', ['doSignup']),

    async submitForm () {
      if (!this.signup.email.value) {
        $q.notify({
          type: 'negative',
          message: 'Invalid email address!'
        })
      } else if (!this.signup.password.value) {
        $q.notify({
          type: 'negative',
          message: 'Password is required field!'
        })
      } else if (this.signup.password.value.length < 6) {
        $q.notify({
          type: 'negative',
          message: 'The password must be 6 or more characters long.'
        })
      } else if (!this.signup.confirmPassword.value) {
        $q.notify({
          type: 'negative',
          message: 'Confirm password is required field!'
        })
      } else if (this.signup.password.value !== this.signup.confirmPassword.value) {
        $q.notify({
          type: 'negative',
          message: 'The password and confirmation password do not matched.'
        })
      } else {
        try {
          const payload = {
            email: this.signup.email.value,
            password: this.signup.password.value
          }
          await apiSignUp.post('/api/users/signup', payload)
          const toPath = this.$route.query.to || '/login'
          this.$router.push(toPath)
        } catch (err) {
          console.log(err)
          if (err.response.data.detail) {
            console.log(err.response.data.detail.error)
            $q.notify({
              type: 'negative',
              message: err.response.data.detail.error
            })
          }
        }
      }
    }
  },
  mounted () {
    $q = useQuasar()
  }
}
</script>

<style scoped>

</style>

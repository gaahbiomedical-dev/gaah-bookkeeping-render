<template>
  <div>
    <h2>Login</h2>
    <form @submit.prevent=\"login\">
      <label>Username: <input v-model=\"username\" /></label><br/>
      <label>Password: <input type=\"password\" v-model=\"password\" /></label><br/>
      <button>Login</button>
    </form>
    <p v-if=\"error\" style=\"color:red\">{{error}}</p>
  </div>
</template>
<script>
import axios from 'axios'
export default {
  data(){ return { username:'admin', password:'admin123', error:null } },
  methods: {
    async login(){
      try{
        const form = new URLSearchParams()
        form.append('username', this.username)
        form.append('password', this.password)
        const res = await axios.post('/token', form)
        localStorage.setItem('token', res.data.access_token)
        this.$router.push('/dashboard')
      }catch(e){
        this.error = 'Login failed'
      }
    }
  }
}
</script>


=======
>>>>>>> 1c071df926c702b72a64ef539685c19e319a01de

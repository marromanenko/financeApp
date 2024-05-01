<template>
  <div class="container">
    <h2>Вхід до сайту</h2>
      <form @submit.prevent="login">
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" required>
        
        <label for="password">Пароль:</label>
        <input type="password" id="password" v-model="password" required>
        
        <input id="enter" type="submit" value="Увійти">
      </form>
    </div>
</template>

<script>
import router from '../../router';
import axios from 'axios';

export default {
  data() {
    return {
      email: '',
      password: ''
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/login/', {
          email: this.email,
          password: this.password
        });
        console.log('Login successful:', response.data);
        localStorage.setItem('token', response.data['token'])
        localStorage.setItem('user_id', response.data['id'])
        localStorage.setItem('username', response.data['username'])
        localStorage.setItem('email', this.email)

        const config = {
                headers: { 'Authorization': 'Token ' + response.data['token'],
                        'Content-Type': 'application/json' 
                        }
                };
        const request1 = await axios.get("http://127.0.0.1:8000/api/accomodations/", config)
        localStorage.setItem('accomodations', JSON.stringify(request1.data))

        const request2 = await axios.get("http://127.0.0.1:8000/api/transports/", config)
        localStorage.setItem('transports', JSON.stringify(request2.data))

        const request3 = await axios.get("http://127.0.0.1:8000/api/users/" + localStorage.getItem('user_id'), config)
        localStorage.setItem('is_superuser', request3.data['is_superuser'])

        router.push('/main')
      } catch (error) {
        console.error('Error during login:', error)
      }
    }
  }
};
</script>

<style scoped>
.container {
  margin: 0 auto;
  padding: 20px;
  max-width: 400px;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-top: 50px;
}

.container h2 {
  margin-top: 0;
}

.container label {
  display: block;
  margin-bottom: 5px;
}

.container input {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
}

.container input[type="submit"] {
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}

.container input[type="submit"]:hover {
  background-color: #45a049;
}

</style>

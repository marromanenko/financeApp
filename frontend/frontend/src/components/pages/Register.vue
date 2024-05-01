<template>
  <div class="container">
    <h2>Реєстрація користувача</h2>
    <form @submit.prevent="submitForm">
      <label for="name">Ім'я:</label>
      <input type="text" id="name" v-model="formData.username" required>
      
      <label for="email">Email:</label>
      <input type="email" id="email" v-model="formData.email" required>

      <label for="password">Пароль:</label>
      <input type="password" id="password" v-model="formData.password" required>
      
      <label for="sex">Стать:</label>
      <select id="sex" v-model="formData.sex" required>
        <option value="M">Чоловіча</option>
        <option value="F">Жіноча</option>
        <option value="A">Інше</option>
      </select>
      
      <label for="birthDate">Дата народження:</label>
      <input type="date" id="birthDate" v-model="formData.birthDate" required>
      
      <input id="submit" type="submit" value="Зареєструватися">
    </form>
  </div>
</template>

<script>
import router from '../../router';
import axios from 'axios';

export default {
  data() {
    return {
      formData: {
        username: '',
        email: '',
        password: '',
        sex: '',
        birthDate: ''
      }
    };
  },
  methods: {
    async submitForm() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/register/', this.formData);
        console.log('Registration successful:', response.data);
        localStorage.setItem('token', response.data['token'])
        router.push('/main')
      } catch (error) {
        console.error('Error during registration:', error);
      }
    },
    resetForm() {
      this.formData.username = '';
      this.formData.email = '';
      this.formData.password = '';
      this.formData.sex = 'male';
      this.formData.birthDate = '';
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

.container input,
.container select {
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

<template>
    <div class="container">
      <h2>Профіль користувача</h2>
      <table>
        <tr>
          <th>Поле</th>
          <th>Значення</th>
        </tr>
        <tr>
          <td>Ім'я</td>
          <td>{{ userData.name }}</td>
        </tr>
        <tr>
          <td>Email</td>
          <td>{{ userData.email }}</td>
        </tr>
        <tr>
          <td>Стать</td>
          <td>{{ userData.gender }}</td>
        </tr>
        <tr>
          <td>Дата народження</td>
          <td>{{ userData.dob }}</td>
        </tr>
      </table>
      <div class="additional-buttons">
      <v-btn id="login" href="/login" @click="goToLogin">Вийти</v-btn>
      <v-btn id="back" href="javascript: history.go(-1)">Назад</v-btn>
    </div>
    </div>
  </template>
  
  <script>
import router from '../../router';
import axios from 'axios';
  export default {
    data: () => ({
        userData: {
          name: '',
          email: '',
          gender: '',
          dob: ''
        }
    }),
    methods: {
      goToProfile() {
      },
      goToAbout() {
      },
      goToLogin() {
        console.log('Redirecting to login page')
        const config = {
                headers: { 'Authorization': 'Token ' + localStorage.getItem('token'),
                        'Content-Type': 'application/json' 
                        }
                };
                axios.post('http://127.0.0.1:8000/logout/', {}, config).then(
                  response => {
                    localStorage.setItem('token', null)
                    router.push('/login')
                    
                  }
                ).catch(
                  e => {
                    console.log(e)
                  }
                )
      }
    },
     mounted: function() {
        if (localStorage.getItem('token') === null) {
            router.push('/login')
        } else {
            try {
                const config = {
                headers: { 'Authorization': 'Token ' + localStorage.getItem('token'),
                        'Content-Type': 'application/json' 
                        }
                };
                axios.get("http://127.0.0.1:8000/api/users/" + localStorage.getItem('user_id'), config)
                .then(response => {
                    this.userData.email = response.data['email']
                    this.userData.name = response.data['username']
                    this.userData.gender = response.data['sex']
                    this.userData.dob = response.data['birthDate']
                }).catch(e => {
                    console.log(e)
                })
            } catch (error) {
                console.error('Error during getting profile info:', error);
            }
        }
    }
  };
  </script>
  
  <style scoped>
  .container {
    margin: 0 auto;
    padding: 20px;
    max-width: 600px;
    margin-top: 50px;

  }
  
  .container h2 {
    margin-top: 0;
  }
  
  .container table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
  }
  
  .container th,
  .container td {
    padding: 8px;
    border-bottom: 1px solid #ddd;
  }
  
  .container th {
    text-align: left;
  }
  
  .container tr:nth-child(even) {
    background-color: #f2f2f2;
  }
  
  .container button {
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #4CAF50;
    color: white;
    border: none;
    cursor: pointer;
  }
  
  .container button:hover {
    background-color: #45a049;
  }

  .additional-buttons {
    display: flex;
    justify-content: space-between;
  }
  </style>

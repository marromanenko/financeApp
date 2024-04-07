<template>
  <div class="container">
    <h2>Про додаток</h2>
    <div class="app-logo">F</div>
    <p>Додаток для відстеження витрат і управління бюджетом - це зручний інструмент для користувачів, який дозволяє їм керувати своїми фінансами. Основна мета цього додатка полягає в тому, щоб допомогти користувачам відстежувати свої витрати, категоризувати їх і порівнювати зі своїм бюджетом. </p>
    
    <div class="additional-buttons">

    <v-btn id="exit" href="/login" @click="goToLogin">Вийти</v-btn>
    <v-btn id="back" href="javascript: history.go(-1)">Назад</v-btn>
  </div>
  </div>
</template>



<script>
import axios from 'axios';
export default {
  methods: {
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

.container .app-logo {
  font-size: 40px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 20px;
}

.container p {
  font-size: 16px;
  line-height: 1.6;
}

.additional-buttons {
    display: flex;
    justify-content: space-between;
  }
</style>

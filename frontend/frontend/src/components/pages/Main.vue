<template>
    <div class="container">
      <h2>Розпланувати бюджет на місяць</h2>
      <form @submit.prevent="submitBudget">
        <label for="income">Прибуток на місяць:</label>
        <input type="number" id="income" v-model="budget.income" required>

        <label for="accomodation">Житло:</label>
          <select id="accomodation" v-model="budget.accomodation" required>
              <option v-for="option in allAccomodation" :value="option.id">{{ option.type }}</option>
          </select>
        
        <label for="utilities">Комунальні послуги:</label>
        <input type="number" id="utilities" v-model="budget.utilities" required>
        
        <label for="food">Їжа та продукти:</label>
        <input type="number" id="food" v-model="budget.food" required>
        
        <label for="transportation">Транспорт:</label>
          <select id="transportation" v-model="budget.transportation" required>
              <option v-for="option in allTransport" :value="option.id">{{ option.kind }}</option>
          </select>
        
        <label for="entertainment">Розваги та дозвілля:</label>
        <input type="number" id="entertainment" v-model="budget.entertainment" required>
        
        <v-btn id="main" @click="submitBudget">Розпланувати</v-btn>
        <v-btn id ="chat" href="/chat" @click="goToChat">Чат</v-btn><br><br>
      </form>

      <div class="additional-buttons">
        <v-btn id="profile" href="/profile" @click="goToProfile">Профіль</v-btn>
        <v-btn id="about" href="/about" @click="goToAbout">Про додаток</v-btn>
        <v-btn id="login" href="/login" @click="goToLogin">Вийти</v-btn>
      
      </div>
    </div>
  </template>
  
  <script>
import router from '../../router';
import axios from 'axios';
import swal from 'sweetalert2';
  export default {
    data: () => ({
        budget: {
          income: null,
          accomodation: null,
          utilities: null,
          food: null,
          transportation: null,
          entertainment: null
        },
        allTransport: [],
        allAccomodation: []

    }),
    beforeMount: function () {
        var transports = JSON.parse(localStorage.getItem('transports'))
        for(let i = 0; i < transports.length; i++) {
          this.allTransport.push(transports[i])
        }
        console.log(this.allTransport)

        var accomodations = JSON.parse(localStorage.getItem('accomodations'))
        for(let i = 0; i < accomodations.length; i++) {
          this.allAccomodation.push(accomodations[i])
        }
        console.log(this.allAccomodation) 
    },
    methods: {
      checkInfo() {
        console.log(this.budget.transportation) 
        console.log(this.budget.housing)
      },
      async submitBudget() {
        console.log('Budget submitted:', this.budget)
        var balance = this.budget.income
        const config = {
                headers: { 'Authorization': 'Token ' + localStorage.getItem('token'),
                        'Content-Type': 'application/json' 
                        }
                };
        const accRes = await axios.get("http://127.0.0.1:8000/api/accomodations/" + this.budget.accomodation + "/", config)
        const amountForAccomodation = accRes.data['amount']
        console.log(amountForAccomodation)
        const traRes = await axios.get("http://127.0.0.1:8000/api/transports/" + this.budget.transportation + "/", config)
        const amountForTransport = traRes.data['amount']

        if (this.budget.utilities/50>30) axios.post("http://127.0.0.1:8000/long_task/", {"l":30}, config)
        else axios.post("http://127.0.0.1:8000/long_task/", {"l":this.budget.utilities/50}, config)

        var json_to_send = {
            email: localStorage.getItem('email'),
            message: ""
          }

        if(balance-amountForAccomodation-amountForTransport-this.budget.utilities-this.budget.food-this.budget.entertainment > 0){
          swal.fire({
                  type: 'success',
                  title: 'Вітаю!',
                  text: 'Ви вкладаєтесь в бюджет',
                  showConfirmButton:true,
                  icon: "success"
                })
          json_to_send.message = 'Ви вкладаєтесь в бюджет'
        } else {
          swal.fire({
                  type: 'error',
                  title: 'На жаль!',
                  text: 'Ви не вкладаєтесь в бюджет',
                  showConfirmButton:true,
                  icon: "error"
                })
          json_to_send.message = 'Ви не вкладаєтесь в бюджет'
        }

        axios.post("http://127.0.0.1:8000/send_message/", json_to_send, config)

      },
      goToProfile() {
        console.log('Redirecting to profile page')
      },
      goToAbout() {
        console.log('Redirecting to about page')
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
  .container select,
  .container button,
  .container v-btn {
    width: 100%;
    padding: 8px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
  }
  
  .container input[type="submit"],
  .container button,
  .container v-btn {
    background-color: #4CAF50;
    /* color: white; */
    border: none;
    cursor: pointer;
  }
  
  .container input[type="submit"]:hover,
  .container button:hover {
    background-color: #45a049;
  }
  
  .additional-buttons {
    display: flex;
    justify-content: space-between;
  }
  </style>

<template>
    <section class="section">
      <div class="container">
        <div class="columns is-multiline">
          <div class="column is-6 is-offset-3 mb-6">
            <section class="hero is-primary">
              <div class="hero-body">
                <p class="title">
                  Chat
                </p>
              </div>
            </section>
          </div>
  
          <div class="column is-6 is-offset-3">
            <div class="box">
              <div id="chat-messages" style="max-height: 300px; overflow-y: scroll;">
                <b v-for="m in messages" :key="m.id">{{ m.username }}: {{ m.content }}<br></b>
              </div>
            </div>
  <br><br><br>
            <div class="field">
              <div class="control">
                <input id="input" class="input" type="text" placeholder="Message" v-model="newMessage">
              </div>
            </div>
  
            <div class="field">
              <div class="control">
                <a id="submit" class="button is-info" @click="sendMessage">Submit</a>
              </div>
            </div>
  
            <!-- <small class="has-text-grey-light">Your username: {{ username }}</small> -->
          </div>
        </div>
      </div>
    </section>
  </template>
  

<script>
import router from '../../router';
import axios from 'axios';
  export default {
    data() {
      return {
        backend_url: 'http://127.0.0.1:8000/',
        username: '',
        messages: [], 
        newMessage: '',
        roomName: 'myroom',
        user_id: null, 
        chatSocket: null,
      }
    },
    async mounted() {
        var success = true;
        if (success) {
            try {
                    const config = {
                      headers: { 'Authorization': 'Token ' + localStorage.getItem('token'),
                              'Content-Type': 'application/json' 
                              }
                      };
                    
                    axios.get(this.backend_url + 'api/chatmessages/?room=' + this.roomName, config)
                    .then(messages => {
                    for (let i = 0; i < messages.data['results'].length; i++) {
                        axios.get(this.backend_url + 'api/users/' + messages.data['results'][i]['user'], config)
                        .then(user => {
                            this.messages.push({ username: user.data['username'], content: messages.data['results'][i]['content'], date_added:  messages.data['results'][i]['date_added']});
                        })
                        
                    }
                    })
                    this.scrollToBottom();
                    this.user_id = localStorage.getItem('user_id')
                    this.username = localStorage.getItem('username')
                    this.connectWebSocket();
            } catch (e) {
                console.log(e);
            }
        }
    },
    methods: {
      closeSocketConnection() {
        console.log('Socket disconnected');
        this.chatSocket.close();
        router.push('/');
      },
      scrollToBottom() {
        let objDiv = document.getElementById("chat-messages"); //change
        objDiv.scrollTop = objDiv.scrollHeight;
      },
      connectWebSocket() {
        this.chatSocket = new WebSocket(
          'ws://127.0.0.1:8000/ws/' + this.roomName + '/?token=' + localStorage.getItem('token')
        );
  
        this.chatSocket.onmessage = (e) => {
            console.log('onmessage');
        const data = JSON.parse(e.data);
        if (data.message) {
          this.messages.push({ username: data.username, content: data.message, date_added: this.formatDate(new Date()) });
          this.scrollToBottom();
        } else {
          alert('The message is empty!');
        }
        };
  
        this.chatSocket.onclose = () => {
          console.log('The socket close unexpectedly');
        };
  
      },
      sendMessage() {
        if (this.newMessage.trim() !== '') {
          this.chatSocket.send(JSON.stringify({
            'message': this.newMessage,
            'username': this.username,
            'user_id': this.user_id,
            'room': this.roomName
          }));
          this.newMessage = '';
        } else {
          alert('Message cannot be empty');
        }
      },
      checkLoggedIn() {
        this.$session.start();
        if (!this.$session.has("refresh") || this.$session.get("refresh") === null) {
            router.push("/login");
            return false;
        }
        return true;
      },
      formatDate(date) {
      const year = date.getFullYear();
      const month = this.padZero(date.getMonth() + 1);
      const day = this.padZero(date.getDate());
      const hours = this.padZero(date.getHours());
      const minutes = this.padZero(date.getMinutes());
      const seconds = this.padZero(date.getSeconds());
      const milliseconds = date.getMilliseconds();
      const timezoneOffset = date.getTimezoneOffset();
      const timezoneOffsetSign = timezoneOffset > 0 ? '-' : '+';
      const timezoneOffsetHours = this.padZero(Math.abs(Math.floor(timezoneOffset / 60)));
      const timezoneOffsetMinutes = this.padZero(Math.abs(timezoneOffset % 60));
      return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}.${milliseconds}${timezoneOffsetSign}${timezoneOffsetHours}:${timezoneOffsetMinutes}`;
    },
    padZero(num) {
      return num < 10 ? '0' + num : num;
    }
    }
  }
  </script>

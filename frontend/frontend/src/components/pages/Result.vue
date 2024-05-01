<template>
  <div>
    <v-simple-table height="700px">
      <template v-slot:default>
        <thead>
          <tr>
            <th class="text-left">
              Name Of Operation
            </th>
            <th class="text-left">
              Operation data
            </th>
            <th class="text-left">
              End Time
            </th>
            <th class="text-left">
              Status
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="item in notifications"
            :key="item.name"
          >
            <td>{{ item.name }}</td>
            <td>{{ item.data }}</td>
            <td>{{ item.datetime }}</td>
            <td :style="{ color: item.status === 'Success' ? 'blue' : 'red' }"><b>{{ item.status }}</b></td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>
    <v-footer absolute id="mainFooter">
            <v-container>
                <br />
                <v-row justify="center" no-gutters class="bg-grey-lighten-1" id="backBtnRow">
                    <v-btn
                    id="backButton"
                    color="black"
                    variant="text"
                    class="mx-2 white--text"
                    rounded
                    @click="closeSocketConnection"
                    >
                    Back to Main Page
                    </v-btn>
                    <v-col class="text-center mt-4" cols="12">
                        {{ new Date().getUTCFullYear() }}
                    </v-col>
                </v-row>
            </v-container>
        </v-footer>
  </div>
</template>



<script>
import router from '../../router';
import swal from 'sweetalert2';
export default {
  data() {
    return {
      notifications: [],
      chatSocket: null,
      backend_url: 'http://127.0.0.1:8000/',
      ws_url: 'ws://127.0.0.1:8000/',
    };
  },
  beforeMount: function () {
        if(localStorage.getItem('is_superuser') === null || localStorage.getItem('is_superuser') === "false") 
        {
          swal.fire({
                  type: 'error',
                  title: 'На жаль!',
                  text: 'Ви не адмін',
                  showConfirmButton:true,
                  icon: "error"
                })
          router.push('/login')
        }
    },
  methods: {
    checkLoggedIn() {
      return true;
    },
    closeSocketConnection() {
        console.log('Socket disconnected');
        this.chatSocket.close();
        router.push('/main');
      },
  },
mounted: function() {
    var isLogged = this.checkLoggedIn();
    if (isLogged) {
      console.log('logged')
      this.chatSocket = new WebSocket(this.ws_url +'ws/info/?token=4a07cc747a95667ed4d5c8aab76cf547abe07245');
      this.chatSocket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log("Received notification:", event.data);
        this.notifications.push({name: data['operation'], data: data['data'], datetime: data['datetime'], status: data['status']});
      };
    }
  }
}
</script>

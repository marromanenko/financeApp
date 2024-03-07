import Vue from "vue";
import './plugins/axios'
import App from "./App.vue";
import router from "./router";
import vuetify from './plugins/vuetify'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import VueSession from 'vue-session'
import VueSweetalert2 from 'vue-sweetalert2';
import store from './store'

Vue.use(Vuetify)
Vue.use(VueSession)
Vue.use(VueSweetalert2)

Vue.config.productionTip = false;

new Vue({
  router,
  vuetify,
  store,
  render: (h) => h(App)
}).$mount("#app");

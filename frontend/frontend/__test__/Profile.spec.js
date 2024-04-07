import { mount } from '@vue/test-utils'
import Profile from './../src/components/pages/Profile.vue'
import Vuetify from "vuetify";
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';
import 'jest-localstorage-mock';

var mock = new MockAdapter(axios);

mock.onGet('http://127.0.0.1:8000/api/users/1').reply(200, 
{
  id: 1,
  username: "admin",
  first_name: "",
  last_name: "",
  sex: "A",
  email: "admin@admin.com",
  birthDate: "2024-04-05",
  is_online: false
});



describe('Profile', () => {
    let vuetify;
    
    beforeEach(() => {
        vuetify = new Vuetify();
        window.localStorage.setItem('token', 'db114994d96ab55a4fd10586fc0530f9714c2528');
        window.localStorage.setItem('user_id', 1);
    });
    
    it('has data', () => {
        const wrapper = mount(Profile, {
            vuetify
        });
        expect(wrapper.text()).toContain('Профіль користувача')
        expect(wrapper.text()).toContain('Поле')
        expect(wrapper.text()).toContain('Значення')
        expect(wrapper.text()).toContain('Email')
        expect(wrapper.text()).toContain('Стать')
        expect(wrapper.text()).toContain('Дата народження')
    })

    it('buttons are visible', () => {
        const wrapper = mount(Profile, {
            vuetify
        });
        expect(wrapper.find('#login').isVisible()).toBe(true)
        expect(wrapper.find('#back').isVisible()).toBe(true)
    })

    it('check user data', async () => {

      let emptyData = {
        userData: {
          name: '',
          email: '',
          gender: '',
          dob: ''
        }
      }

      const response = await axios.get('http://127.0.0.1:8000/api/users/1')
      emptyData.userData.email = response.data['email']
      emptyData.userData.name = response.data['username']
      emptyData.userData.gender = response.data['sex']
      emptyData.userData.dob = response.data['birthDate']

      const wrapper = mount(Profile, {
          vuetify,
          data() {
            return { ...emptyData};
          }
      });
      expect(wrapper.text()).toContain('admin')
      expect(wrapper.text()).toContain('A')
      expect(wrapper.text()).toContain('admin@admin.com')
      expect(wrapper.text()).toContain('2024-04-05')
  })
  })


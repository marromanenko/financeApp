import { mount } from '@vue/test-utils'
import Auth from './../src/components/pages/Auth.vue'
import Vuetify from "vuetify";

describe('Auth', () => {
    let vuetify;

    beforeEach(() => {
        vuetify = new Vuetify();
    });
    
    it('has data', () => {
        const wrapper = mount(Auth, {
            vuetify
        });
        expect(wrapper.text()).toContain('Вхід до сайту')
    })

    it('button is visible', () => {
        const wrapper = mount(Auth, {
            vuetify
        });
        expect(wrapper.find('#enter').isVisible()).toBe(true)
    })

    it('email has value', async () => {  
        const wrapper = mount(Auth, {
            vuetify
        });
        const textInput = wrapper.find('input[id="email"]')
        await textInput.setValue('test@test.com')
        expect(wrapper.find('input[id="email"]').element.value).toBe('test@test.com')
    })

    it('password has value', async () => {  
        const wrapper = mount(Auth, {
            vuetify
        });
        const textInput = wrapper.find('input[id="password"]')
        await textInput.setValue('password')
        expect(wrapper.find('input[id="password"]').element.value).toBe('password')
    })
  })


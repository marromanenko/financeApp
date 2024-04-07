import { mount } from '@vue/test-utils'
import Register from './../src/components/pages/Register.vue'
import Vuetify from "vuetify";

describe('Register', () => {
    let vuetify;

    beforeEach(() => {
        vuetify = new Vuetify();
    });
    
    it('has data', () => {
        const wrapper = mount(Register, {
            vuetify
        });
        expect(wrapper.text()).toContain('Реєстрація користувача')
        expect(wrapper.text()).toContain('Email:')
        expect(wrapper.text()).toContain('Пароль:')
        expect(wrapper.text()).toContain('Стать:')
        expect(wrapper.text()).toContain('Дата народження:')
    })

    it('button is visible', () => {
        const wrapper = mount(Register, {
            vuetify
        });
        expect(wrapper.find('#submit').isVisible()).toBe(true)
    })

    it('name has value', async () => {  
        const wrapper = mount(Register, {
            vuetify
        });
        const textInput = wrapper.find('input[id="name"]')
        await textInput.setValue('name')
        expect(wrapper.find('input[id="name"]').element.value).toBe('name')
    })

    it('email has value', async () => {  
        const wrapper = mount(Register, {
            vuetify
        });
        const textInput = wrapper.find('input[id="email"]')
        await textInput.setValue('test@test.com')
        expect(wrapper.find('input[id="email"]').element.value).toBe('test@test.com')
    })

    it('password has value', async () => {  
        const wrapper = mount(Register, {
            vuetify
        });
        const textInput = wrapper.find('input[id="password"]')
        await textInput.setValue('password')
        expect(wrapper.find('input[id="password"]').element.value).toBe('password')
    })

    it('sex has value', async () => {  
        const wrapper = mount(Register, {
            vuetify
        });
        const textInput = wrapper.find('select[id="sex"]')
        await textInput.setValue('M')
        expect(wrapper.find('select[id="sex"]').element.value).toBe('M')
    })

    it('birthDate has value', async () => {  
        const wrapper = mount(Register, {
            vuetify
        });
        const textInput = wrapper.find('input[id="birthDate"]')
        await textInput.setValue('2002-04-14')
        expect(wrapper.find('input[id="birthDate"]').element.value).toBe('2002-04-14')
    })
  })


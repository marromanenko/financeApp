import { mount } from '@vue/test-utils'
import Chat from './../src/components/pages/Chat.vue'
import Vuetify from "vuetify";

describe('Chat', () => {
    let vuetify;
    const submitFunction = jest.spyOn(Chat.methods,'sendMessage')

    beforeEach(() => {
        vuetify = new Vuetify();
    });
    
    it('Chat has data', () => {
        const wrapper = mount(Chat, {
            vuetify
        });
        expect(wrapper.text()).toContain('Chat')
    })

    it('button is visible', () => {
        const wrapper = mount(Chat, {
            vuetify
        });
        expect(wrapper.find('#submit').isVisible()).toBe(true)
    })

    it('input is visible', async () => {  
        const wrapper = mount(Chat, {
            vuetify
        });
        expect(wrapper.find('#input').isVisible()).toBe(true)
    })

    it('function is called', async () => {  
        const wrapper = mount(Chat, {
            vuetify
        });

        const button = wrapper.find('#submit')
        button.trigger('click');
        await wrapper.vm.$nextTick();
        expect(submitFunction).toHaveBeenCalled();
        
    }) 
  })


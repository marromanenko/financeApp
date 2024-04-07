import { mount } from '@vue/test-utils'
import About from './../src/components/pages/About.vue'
import Vuetify from "vuetify";

describe('About', () => {
    let vuetify;

    beforeEach(() => {
        vuetify = new Vuetify();
    });
    
    it('has data', () => {
        const wrapper = mount(About, {
            vuetify
        });
        expect(wrapper.text()).toContain('Про додаток F Додаток для відстеження витрат і управління бюджетом - це зручний інструмент для користувачів, який дозволяє їм керувати своїми фінансами. Основна мета цього додатка полягає в тому, щоб допомогти користувачам відстежувати свої витрати, категоризувати їх і порівнювати зі своїм бюджетом.')
    })

    it('buttons are visible', () => {
        const wrapper = mount(About, {
            vuetify
        });
        expect(wrapper.find('#exit').isVisible()).toBe(true)
        expect(wrapper.find('#back').isVisible()).toBe(true)
    })
  })

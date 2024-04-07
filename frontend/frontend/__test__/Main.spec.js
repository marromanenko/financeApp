import { mount } from '@vue/test-utils'
import Main from './../src/components/pages/Main.vue'
import Vuetify from "vuetify";
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';
import 'jest-localstorage-mock';

var mock = new MockAdapter(axios);

mock.onGet('http://127.0.0.1:8000/api/accomodations/').reply(200, {
    data: [
        {
            "id": 1,
            "type": "Власне житло",
            "amount": 0
        },
        {
            "id": 2,
            "type": "Оренда квартири",
            "amount": 15000
        }
    ]
  });

  mock.onGet('http://127.0.0.1:8000/api/transports/').reply(200, {
    data: [
        {
            "id": 1,
            "kind": "Громадський транспорт",
            "amount": 1000
        },
        {
            "id": 2,
            "kind": "Таксі",
            "amount": 5000
        },
        {
            "id": 3,
            "kind": "Своя машина",
            "amount": 4000
        }
    ]
  });

  mock.onGet('http://127.0.0.1:8000/api/transports/2/').reply(200, 
  {
    "id": 2,
    "kind": "Таксі",
    "amount": 5000
});

mock.onGet('http://127.0.0.1:8000/api/accomodations/1/').reply(200, 
{
    "id": 1,
    "type": "Власне житло",
    "amount": 0
});

describe('Main', () => {
    let vuetify;
    const submitFunction = jest.spyOn(Main.methods,'submitBudget')
    
    beforeEach(async () => {
        vuetify = new Vuetify();
        const response1 = await axios.get('http://127.0.0.1:8000/api/transports/')
        const response2 = await axios.get('http://127.0.0.1:8000/api/accomodations/')
        window.localStorage.setItem('transports', JSON.stringify(response1.data))
        window.localStorage.setItem('accomodations', JSON.stringify(response2.data))
    });
    
    it('has data', async () => {

        const wrapper = mount(Main, {
            vuetify
        });

        expect(wrapper.text()).toContain('Розпланувати бюджет на місяць')
        expect(wrapper.text()).toContain('Прибуток на місяць:')
        expect(wrapper.text()).toContain('Житло:')
        expect(wrapper.text()).toContain('Комунальні послуги:')
        expect(wrapper.text()).toContain('Їжа та продукти:')
        expect(wrapper.text()).toContain('Транспорт:')
        expect(wrapper.text()).toContain('Розваги та дозвілля:')
        console.log(wrapper.text());
    })

    it('buttons are visible', () => {
        const wrapper = mount(Main, {
            vuetify
        });
        expect(wrapper.find('#main').isVisible()).toBe(true)
        expect(wrapper.find('#chat').isVisible()).toBe(true)
        expect(wrapper.find('#profile').isVisible()).toBe(true)
        expect(wrapper.find('#login').isVisible()).toBe(true)
        expect(wrapper.find('#about').isVisible()).toBe(true)
    })

    it('income has value', async () => {  
        const wrapper = mount(Main, {
            vuetify
        });
        const textInput = wrapper.find('input[id="income"]')
        await textInput.setValue('50000')
        expect(wrapper.find('input[id="income"]').element.value).toBe('50000')
    })

    it('utilities has value', async () => {  
        const wrapper = mount(Main, {
            vuetify
        });
        const textInput = wrapper.find('input[id="utilities"]')
        await textInput.setValue('10000')
        expect(wrapper.find('input[id="utilities"]').element.value).toBe('10000')
    })

    it('food has value', async () => {  
        const wrapper = mount(Main, {
            vuetify
        });
        const textInput = wrapper.find('input[id="food"]')
        await textInput.setValue('5000')
        expect(wrapper.find('input[id="food"]').element.value).toBe('5000')
    })

    it('accomodation has value', async () => {  

        let data = {
            allAccomodation: [
                {
                    "id": 1,
                    "type": "Власне житло",
                    "amount": 0
                },
                {
                    "id": 2,
                    "type": "Оренда квартири",
                    "amount": 15000
                }
            ]

        };

        const wrapper = mount(Main, {
            vuetify,
            data() {
                return { ...data};
              }
        });
        const options = wrapper.find('select[id="accomodation"]').findAll('option')
        await options.at(0).setSelected()
        expect(wrapper.find('option:checked').element.value).toBe('1')
    })

    it('transportation has value', async () => {  

        let data = {
            allTransport: [
                {
                    "id": 1,
                    "kind": "Громадський транспорт",
                    "amount": 1000
                },
                {
                    "id": 2,
                    "kind": "Таксі",
                    "amount": 5000
                },
                {
                    "id": 3,
                    "kind": "Своя машина",
                    "amount": 4000
                }
            ]

        };

        const wrapper = mount(Main, {
            vuetify,
            data() {
                return { ...data};
              }
        });
        const options = wrapper.find('select[id="transportation"]').findAll('option')
        await options.at(1).setSelected()
        expect(wrapper.find('option:checked').element.value).toBe('2')
    })

    it('entertainment has value', async () => {  
        const wrapper = mount(Main, {
            vuetify
        });
        const textInput = wrapper.find('input[id="entertainment"]')
        await textInput.setValue('3000')
        expect(wrapper.find('input[id="entertainment"]').element.value).toBe('3000')
    })

    it('function is called', async () => { 
        
        let data = {
            budget: {
                income: 50000,
                accomodation: 1,
                utilities: 6576000,
                food: 5000,
                transportation: 2,
                entertainment: 10000
              }
        
        };

        const wrapper = mount(Main, {
            vuetify,
            data() {
                return { ...data};
              }
        });
        
        const button = wrapper.find('#main')
        button.trigger('click');
        await wrapper.vm.$nextTick();
        expect(submitFunction).toHaveBeenCalled();
    }) 

  })


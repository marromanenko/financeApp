describe('Todo tests', () => {
    it('user can log in and log out', () => {
        cy.visit('http://localhost:8080/login');
        cy.xpath('//h2[contains(text(), "Вхід до сайту")]').should('be.visible');
        cy.get('#email').type('biba@com.com');
        cy.get('#password').type('asdasd');
        cy.get('#enter').click();
        cy.url().should('eq', 'http://localhost:8080/main');
        cy.get('#about').should('be.visible');
        cy.get('#login').click();
        cy.url().should('eq', 'http://localhost:8080/login');
        cy.xpath('//h2[contains(text(), "Вхід до сайту")]').should('be.visible');
    });

    it('user can see about page', () => {
        cy.visit('http://localhost:8080/login');
        cy.xpath('//h2[contains(text(), "Вхід до сайту")]').should('be.visible');
        cy.get('#email').type('biba@com.com');
        cy.get('#password').type('asdasd');
        cy.get('#enter').click();
        cy.url().should('eq', 'http://localhost:8080/main');
        cy.get('#about').should('be.visible');
        cy.get('#about').click();
        cy.url().should('eq', 'http://localhost:8080/about');
        cy.xpath('//h2[contains(text(), "Про додаток")]').should('be.visible');
        cy.xpath('//div[@class="app-logo"]').should('be.visible');
        cy.get('#back').click()
        cy.url().should('eq', 'http://localhost:8080/main');
        cy.get('#login').click();
        cy.url().should('eq', 'http://localhost:8080/login');
        cy.xpath('//h2[contains(text(), "Вхід до сайту")]').should('be.visible');
    });

    it('user can see profile page', () => {
        cy.visit('http://localhost:8080/login');
        cy.xpath('//h2[contains(text(), "Вхід до сайту")]').should('be.visible');
        cy.get('#email').type('biba@com.com');
        cy.get('#password').type('asdasd');
        cy.get('#enter').click();
        cy.url().should('eq', 'http://localhost:8080/main');
        cy.get('#profile').should('be.visible');
        cy.get('#profile').click();
        cy.url().should('eq', 'http://localhost:8080/profile');
        cy.xpath('//h2[contains(text(), "Профіль користувача")]').should('be.visible');

        cy.xpath("//table/tr/td[contains(text(), \"Ім'я\")]/../td[2]").contains( 'biba');
        cy.xpath("//table/tr/td[contains(text(), \"Email\")]/../td[2]").contains('biba@com.com');
        cy.xpath("//table/tr/td[contains(text(), \"Стать\")]/../td[2]").contains('F');
        cy.xpath("//table/tr/td[contains(text(), \"Дата народження\")]/../td[2]").contains('2024-04-11');

        cy.get('#login').click();
        cy.url().should('eq', 'http://localhost:8080/login');
        cy.xpath('//h2[contains(text(), "Вхід до сайту")]').should('be.visible');
    });

    it('user can send messages to websocket chat', () => {
        cy.visit('http://localhost:8080/login');
        cy.xpath('//h2[contains(text(), "Вхід до сайту")]').should('be.visible');
        cy.get('#email').type('biba@com.com');
        cy.get('#password').type('asdasd');
        cy.get('#enter').click();
        cy.url().should('eq', 'http://localhost:8080/main');
        cy.get('#chat').should('be.visible');
        cy.get('#chat').click();
        cy.url().should('eq', 'http://localhost:8080/chat');
        cy.get('#submit').should('be.visible');
        cy.get('#input').type('cypress message');
        cy.get('#submit').click();
        cy.xpath('//div/b[contains(text(), "biba: cypress message")]').should('be.visible');
        cy.visit('http://localhost:8080/main');
        cy.get('#login').click();
        cy.url().should('eq', 'http://localhost:8080/login');
        cy.xpath('//h2[contains(text(), "Вхід до сайту")]').should('be.visible');
    });

    it('user can be in budget', () => {
        cy.visit('http://localhost:8080/login');
        cy.xpath('//h2[contains(text(), "Вхід до сайту")]').should('be.visible');
        cy.get('#email').type('biba@com.com');
        cy.get('#password').type('asdasd');
        cy.get('#enter').click();
        cy.url().should('eq', 'http://localhost:8080/main');
        cy.get('#income').type('100000');
        cy.get('#accomodation').select('Власне житло');
        cy.get('#utilities').type('1000');
        cy.get('#food').type('1000');
        cy.get('#transportation').select('Таксі');
        cy.get('#entertainment').type('10000');
        cy.get('#main').should('be.visible');
        cy.get('#main').click();
        cy.xpath("//div[contains(text(), 'Ви вкладаєтесь в бюджет')]").should('be.visible');
        cy.xpath("//button[contains(text(), 'OK')]").click();
        cy.get('#login').click();
        cy.url().should('eq', 'http://localhost:8080/login');
        cy.xpath('//h2[contains(text(), "Вхід до сайту")]').should('be.visible');
    });

    it('user can be not in budget', () => {
        cy.visit('http://localhost:8080/login');
        cy.xpath('//h2[contains(text(), "Вхід до сайту")]').should('be.visible');
        cy.get('#email').type('biba@com.com');
        cy.get('#password').type('asdasd');
        cy.get('#enter').click();
        cy.url().should('eq', 'http://localhost:8080/main');
        cy.get('#income').clear().type('1000');
        cy.get('#accomodation').select('Оренда квартири');
        cy.get('#utilities').clear().type('10000');
        cy.get('#food').clear().type('10000');
        cy.get('#transportation').select('Громадський транспорт');
        cy.get('#entertainment').clear().type('10000');
        cy.get('#main').should('be.visible');
        cy.get('#main').click();
        cy.xpath("//div[contains(text(), 'Ви не вкладаєтесь в бюджет')]").should('be.visible');
        cy.xpath("//button[contains(text(), 'OK')]").click();
        cy.get('#login').click();
        cy.url().should('eq', 'http://localhost:8080/login');
        cy.xpath('//h2[contains(text(), "Вхід до сайту")]').should('be.visible');
    });

  });

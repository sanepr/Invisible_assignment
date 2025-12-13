describe('Authentication Flow', () => {
  beforeEach(() => {
    // Clear local storage before each test
    cy.clearLocalStorage();
  });

  it('should display the homepage', () => {
    cy.visit('/');
    cy.contains('Split Expenses').should('be.visible');
    cy.contains('The Easy Way').should('be.visible');
  });

  it('should navigate to login page', () => {
    cy.visit('/');
    cy.contains('Sign In').click();
    cy.url().should('include', '/login');
    cy.contains('Sign in to your account').should('be.visible');
  });

  it('should navigate to signup page', () => {
    cy.visit('/');
    cy.contains('Get Started').click();
    cy.url().should('include', '/signup');
    cy.contains('Create your account').should('be.visible');
  });

  it('should show validation for empty login form', () => {
    cy.visit('/login');
    cy.get('button[type="submit"]').click();
    // HTML5 validation will prevent submission
    cy.get('input[name="username"]').should('have.prop', 'validity').should('have.property', 'valueMissing', true);
  });

  it('should show validation for empty signup form', () => {
    cy.visit('/signup');
    cy.get('button[type="submit"]').click();
    // HTML5 validation will prevent submission
    cy.get('input[name="username"]').should('have.prop', 'validity').should('have.property', 'valueMissing', true);
  });

  it('should fill out signup form', () => {
    cy.visit('/signup');
    cy.get('input[name="username"]').type('testuser');
    cy.get('input[name="email"]').type('test@example.com');
    cy.get('input[name="full_name"]').type('Test User');
    cy.get('input[name="password"]').type('password123');
    
    // Verify values are filled
    cy.get('input[name="username"]').should('have.value', 'testuser');
    cy.get('input[name="email"]').should('have.value', 'test@example.com');
  });

  it('should fill out login form', () => {
    cy.visit('/login');
    cy.get('input[name="username"]').type('testuser');
    cy.get('input[name="password"]').type('password123');
    
    // Verify values are filled
    cy.get('input[name="username"]').should('have.value', 'testuser');
    cy.get('input[name="password"]').should('have.value', 'password123');
  });

  it('should redirect to login when accessing protected route', () => {
    cy.visit('/dashboard');
    cy.url().should('include', '/login');
  });
});

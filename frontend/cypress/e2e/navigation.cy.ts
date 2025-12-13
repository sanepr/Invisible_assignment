describe('Navigation', () => {
  it('should display navigation links on home page', () => {
    cy.visit('/');
    cy.contains('Expense Splitter').should('be.visible');
    cy.contains('Sign In').should('be.visible');
    cy.contains('Get Started').should('be.visible');
  });

  it('should display features section', () => {
    cy.visit('/');
    cy.contains('Key Features').should('be.visible');
    cy.contains('Group Management').should('be.visible');
    cy.contains('Track Expenses').should('be.visible');
    cy.contains('Balance Summary').should('be.visible');
  });

  it('should navigate between pages', () => {
    cy.visit('/');
    
    // Navigate to login
    cy.contains('Sign In').click();
    cy.url().should('include', '/login');
    
    // Navigate back to signup from login
    cy.contains('create a new account').click();
    cy.url().should('include', '/signup');
    
    // Navigate back to login from signup
    cy.contains('sign in to existing account').click();
    cy.url().should('include', '/login');
  });
});

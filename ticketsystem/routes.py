from flask import render_template, redirect, url_for, flash, get_flashed_messages, request
from ticketsystem import app
from ticketsystem.models import User, Ticket
from ticketsystem.forms import RegisterForm, LoginForm, TicketCreationForm, UpdateTicketForm
from ticketsystem import db
import flask_login
from flask_login import login_user, logout_user, login_required


# Main route for accessing the home page with some basic information
@app.route('/home')
@app.route('/', methods=['POST', 'GET'])
def home_page():
    # Displays the home page to the user.
    return render_template('home.html', tickets=Ticket.query.all())


# Route for accessing the tickets page that shows the user all of their created and closed tickets.
@app.route('/tickets', methods=['POST', 'GET'])
@login_required
def show_tickets():
    # Shows the webpage with the users tickets on, or all tickets if the user is an admin.
    return render_template('tickets.html', tickets=Ticket.query.all())


# Deletes a ticket by closing the issue on the /tickets route
@app.route('/delete/<int:id>')
@login_required
def delete(id):
    ticket_to_delete = Ticket.query.get_or_404(id)

    # Checks to see if the user is authorized to delete the current ticket. If not, send them an
    # error message and redirect them back to the ticket page.
    if ticket_to_delete.owner != flask_login.current_user.id and not flask_login.current_user.is_admin:
        flash(f'You are not authorized to delete that ticket.', category='danger')
        return redirect('/tickets')

    # Attempts to delete and commit changes to the database
    try:
        db.session.delete(ticket_to_delete)
        db.session.commit()
        flash(f'The ticket: {ticket_to_delete.name} was successfully closed.', category='success')
        return redirect('/tickets')
    except:
        return 'There was a problem deleting that ticket.'

    return redirect('/tickets')


# Updates a tickets name and description
@app.route('/update/<int:id>', methods=['POST', 'GET'])
@login_required
def update(id):
    ticket_to_update = Ticket.query.get_or_404(id)
    form = UpdateTicketForm()

    # Checks to see if the user is authorized to update the current ticket. If not, send them an
    # error message and redirect them back to the ticket page.
    if ticket_to_update.owner != flask_login.current_user.id and not flask_login.current_user.is_admin:
        flash(f'You are not authorized to update that ticket.', category='danger')
        return redirect('/tickets')

    if form.validate_on_submit():
        try:
            # Updates the ticket information
            ticket_to_update.name = form.name.data
            ticket_to_update.description = form.description.data

            # Commits changes to the database
            db.session.commit()
            flash(f'The ticket: {ticket_to_update.name} was successfully updated.', category='success')
            return redirect('/tickets')
        except:
            return 'There was a problem updating that ticket.'

    if form.errors != {}:  # If there are not any validation errors
        for err_msg in form.errors.values():
            flash(f'There was an error updating that ticket: {err_msg}', category='danger')

    # Setting default data
    form.name.data = ticket_to_update.name
    form.description.data = ticket_to_update.description

    # Renders the update ticket page to the user
    return render_template('update_ticket.html', form=form, ticket=ticket_to_update)


# Route for creating a new ticket
@app.route('/create', methods=['POST', 'GET'])
@login_required
def create_ticket():
    form = TicketCreationForm()

    # Checks to see if the form is validated.
    if form.validate_on_submit():
        # Creates a new ticket instance
        new_ticket = Ticket(name=form.name.data,
                            description=form.description.data,
                            status="Open",
                            owner=flask_login.current_user.id)

        # Commits changes to the database
        db.session.add(new_ticket)
        db.session.commit()
        return redirect('/tickets')

    if form.errors != {}:  # If there are not any validation errors
        for err_msg in form.errors.values():
            flash(f'There was an error creating a new ticket: {err_msg}', category='danger')

    # Renders the create webpage to the user
    return render_template('create.html', form=form)


# The route that takes the user to the register page
@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    # Checks to see if the form is valid
    if form.validate_on_submit():
        # Creates a new user instance
        newuser = User(username=form.username.data,
                       email_address=form.email_address.data,
                       password=form.password.data)

        # Adds the user to the database and commits changes
        db.session.add(newuser)
        db.session.commit()
        return redirect('/tickets')

    if form.errors != {}:  # If there are not any validation errors
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    # Shows the register webpage to the user
    return render_template('register.html', form=form)


# The route that takes the user to the login page
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    # Checks if the form is valid and the fields match before logging in the user
    if form.validate_on_submit():
        # Checks the database to see if a user exists with the given name
        attempted_login = User.query.filter_by(username=form.username.data).first()

        # If the username and password match, log the user in
        if attempted_login and attempted_login.check_password(attempted_password=form.password.data):
            login_user(attempted_login)
            flash(f'Success! You are logged in as: {attempted_login.username}', category='success')
            return redirect('/tickets')
        else:
            flash('Username or password is incorrect. Please try again.', category='danger')

    # Shows the login web page to the user
    return render_template('login.html', form=form)


# The route that handles the logging out of the current logged in user
@app.route('/logout')
def logout_page():
    # Logs the user out - using a library to handle this
    logout_user()

    # Shows a message alerting the user they have been logged out and takes them to the home page
    flash("You have been logged out!", category='info')
    return redirect('/home')

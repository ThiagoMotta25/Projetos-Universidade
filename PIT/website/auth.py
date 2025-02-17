from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
import matplotlib
import mysql.connector.cursor
from wtforms import *
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
matplotlib.use('Agg')

auth = Blueprint('auth', __name__)


@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        full_name = request.form.get('fullName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters. Please try again.', category='error')
        elif len(full_name) < 2:
            flash('Full name must be greater than 1 character. Please try again', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.  Please try again.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.  Please try again.', category='error')
        else:
            new_user = User(email=email, full_name=full_name, password=generate_password_hash(password1))
            if User.query.count() == 0:  # Check if this is the first user
                new_user.type = 'admin'
            else:
                new_user.type = 'client'
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')

            cnx = mysql.connector.connect(user='pit', password='pit2024', host='158.179.212.127', database='projetopit')
            cur=cnx.cursor()
        
            # Check if the email already exists
            cur.execute("SELECT * FROM projetopit.utilizador WHERE email=%s", [email])
            user = cur.fetchone()
            if user:
                return 'Email already exists'
            
            user_id = new_user.id
            type = new_user.type

            # Insert the new user
            cur.execute("INSERT INTO projetopit.utilizador (Id_Utilizador, Nome, Email, pass, Tipo) VALUES (%s,%s, %s, %s,%s)", (user_id,full_name, email, password1, type))
            cnx.commit()

            # Close the cursor
            cur.close()

            return redirect(url_for('views.home'))
        
    return render_template("sign_up.html", user=current_user)


#### functions related to admin ####

@auth.route('/admin-page')
@login_required
def admin():
    id = current_user.id
    if id == 1:
        return render_template('admin.html', user=current_user)
    else:
        flash('You are not authorized to view this page.', category='error')
        return render_template('home.html', user=current_user)

@auth.route('/delete/<int:id>')
def delete_user(id):
    user_to_delete= User.query.get_or_404(id)
    if id!=1:
        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash('User deleted successfully', category='success')

            cnx = mysql.connector.connect(user='pit', password='pit2024', host='158.179.212.127', database='projetopit')
            cur=cnx.cursor()

            cur.execute("DELETE FROM projetopit.utilizador WHERE Id_Utilizador = %s",(id,))
            cnx.commit()

            cur.close()

            return redirect(url_for('auth.admin'))
        except:
            flash('There was a problem deleting user', category='error')
            return redirect(url_for('auth.admin'))
    else:
        flash('You cannot delete this user', category='error')
        return redirect(url_for('auth.admin'))
    
class UpdateUserForm(FlaskForm):
    full_name = StringField("Name")
    email = StringField("Email")
    submit = SubmitField("Update")

@auth.route('/update-user/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    form = UpdateUserForm()
    user_to_update = User.query.get_or_404(id)
    if request.method == 'POST':
        user_to_update.full_name = form.full_name.data
        user_to_update.email = form.email.data
        try:
            db.session.commit()
            flash('User updated successfully', category='success')

            cnx = mysql.connector.connect(user='pit', password='pit2024', host='158.179.212.127', database='projetopit')
            cur=cnx.cursor()

            cur.execute("UPDATE projetopit.utilizador SET Nome = %s, Email = %s WHERE Id_Utilizador = %s", (user_to_update.full_name, user_to_update.email,user_to_update.id))
            cnx.commit()

            cur.close()

            return redirect(url_for('auth.admin'))
        except:
            flash('There was a problem updating user', category='error')
            return redirect(url_for('auth.admin'))
    else:
        return render_template("update_user.html", form=form, user=user_to_update)
    
@auth.route("/search", methods =["GET", "POST"])
def search():
    q = request.args.get("q")
    print(q)

    if q:
        results = User.query.filter(User.full_name.icontains(q)).order_by(User.id.asc()).limit(10).all()
    else:
        results = []

    return render_template("search_results.html", results=results)


#### functions related to sistems ####

@auth.route('/systems', methods=['GET', 'POST'])
@login_required
def manage_systems():
    cnx = mysql.connector.connect(user='pit', password='pit2024', host='158.179.212.127', database='projetopit')
    cur = cnx.cursor()

    if request.method == 'POST':
        location = request.form.get('location')
        cur.execute("INSERT INTO projetopit.sistema (LocalS, Id_Utilizador, Processed) VALUES (%s, %s, %s)", (location, current_user.id, 0))
        cnx.commit()
        return redirect(url_for('auth.manage_systems'))

    cur.execute("SELECT * FROM projetopit.sistema WHERE Id_Utilizador = %s", (current_user.id,))
    data = cur.fetchall()

    cur.close()
    cnx.close()
    
    return render_template("systems.html", user=current_user, data=data)


#### Functions related to image maping ####

@auth.route('/esp32', methods=['GET', 'POST'])
@login_required
def esp32():
    return render_template("esp32.html", user=current_user)

@auth.route('/relay', methods=['GET', 'POST'])
@login_required
def relay():
    return render_template("relay.html", user=current_user)

@auth.route('/batery', methods=['GET', 'POST'])
@login_required
def batery():
    return render_template("batery.html", user=current_user)

@auth.route('/humidity-sensor', methods=['GET', 'POST'])
@login_required
def h_sensor():
    return render_template("humidity.html", user=current_user)

@auth.route('/waterlevel-sensor', methods=['GET', 'POST'])
@login_required
def wl_sensor():
    return render_template("water_level.html", user=current_user)

@auth.route('/water-pump', methods=['GET', 'POST'])
@login_required
def w_pump():
    return render_template("water_pump.html", user=current_user)

#### Functions related to locations ####

@auth.route('/Braga', methods=['GET', 'POST'])
@login_required
def braga_info():
    cnx = mysql.connector.connect(user='pit', password='pit2024', host='158.179.212.127', database='projetopit')
    cur = cnx.cursor()

    location = 'Braga'
    cur.execute("SELECT a.Time_Stamp, a.valor FROM projetopit.sistema si JOIN sensor s ON si.Id_Sistema = s.Id_Sistema\
                JOIN projetopit.amostra a ON s.Id_Sensor = a.Id_Sensor WHERE si.LocalS = %s ORDER BY a.Time_Stamp ASC",(location,))
    data = cur.fetchall()
    cnx.commit()
    cur.close()

    braga_graph()

    return render_template("braga.html",user=current_user, data = data)


@auth.route('/Guimaraes', methods=['GET', 'POST'])
@login_required
def guima_info():
    cnx = mysql.connector.connect(user='pit', password='pit2024', host='158.179.212.127', database='projetopit')
    cur = cnx.cursor()

    location = 'Guimaraes'
    cur.execute("SELECT a.Time_Stamp, a.valor FROM projetopit.sistema si JOIN sensor s ON si.Id_Sistema = s.Id_Sistema\
                JOIN projetopit.amostra a ON s.Id_Sensor = a.Id_Sensor WHERE si.LocalS = %s ORDER BY a.Time_Stamp ASC",(location,))
    data = cur.fetchall()
    cnx.commit()
    cur.close()

    guima_graph()

    return render_template("guimaraes.html",user=current_user, data = data)


@auth.route('/Viseu', methods=['GET', 'POST'])
@login_required
def viseu_info():
    cnx = mysql.connector.connect(user='pit', password='pit2024', host='158.179.212.127', database='projetopit')
    cur = cnx.cursor()

    location = 'Viseu'
    cur.execute("SELECT a.Time_Stamp, a.valor FROM projetopit.sistema si JOIN sensor s ON si.Id_Sistema = s.Id_Sistema\
                JOIN projetopit.amostra a ON s.Id_Sensor = a.Id_Sensor WHERE si.LocalS = %s ORDER BY a.Time_Stamp ASC",(location,))
    data = cur.fetchall()
    cnx.commit()
    cur.close()

    viseu_graph()

    return render_template("viseu.html",user=current_user, data = data)
   


#### Functions related to plotting graphs ####


@auth.route('/Braga', methods=['GET', 'POST'])
@login_required
def braga_graph():
    cnx = mysql.connector.connect(user='pit', password='pit2024', host='158.179.212.127', database='projetopit')
    cur = cnx.cursor()

    location = 'Braga'
    cur.execute("SELECT a.Time_Stamp, a.valor FROM projetopit.sistema si JOIN sensor s ON si.Id_Sistema = s.Id_Sistema\
                JOIN projetopit.amostra a ON s.Id_Sensor = a.Id_Sensor WHERE si.LocalS = %s ORDER BY a.Time_Stamp ASC",(location,))
    data = cur.fetchall()

    timestamps = [row[0] for row in data]
    values = [row[1] for row in data]

    # Create a plot
    plt.plot(timestamps, values)
    plt.xlabel('Timestamp')
    plt.ylabel('Value')
    plt.title('Samples Graph')

    # Save the plot to a file
    plt.savefig('website/static/Braga_plot.png')

    # Close the plot
    plt.close()

    # Render the plot in an HTML template
    return render_template("braga.html",user=current_user)

@auth.route('/Guimaraes', methods=['GET', 'POST'])
@login_required
def guima_graph():
    cnx = mysql.connector.connect(user='pit', password='pit2024', host='158.179.212.127', database='projetopit')
    cur = cnx.cursor()

    location = 'Guimaraes'
    cur.execute("SELECT a.Time_Stamp, a.valor FROM projetopit.sistema si JOIN sensor s ON si.Id_Sistema = s.Id_Sistema\
                JOIN projetopit.amostra a ON s.Id_Sensor = a.Id_Sensor WHERE si.LocalS = %s ORDER BY a.Time_Stamp ASC",(location,))
    data = cur.fetchall()

    timestamps = [row[0] for row in data]
    values = [row[1] for row in data]

    # Create a plot
    plt.plot(timestamps, values)
    plt.xlabel('Timestamp')
    plt.ylabel('Value')
    plt.title('Samples Graph')

    # Save the plot to a file
    plt.savefig('website/static/Guimaraes_plot.png')

    # Close the plot
    plt.close()

    # Render the plot in an HTML template
    return render_template("guimaraes.html", user=current_user)

@auth.route('/Viseu', methods=['GET', 'POST'])
@login_required
def viseu_graph():
    cnx = mysql.connector.connect(user='pit', password='pit2024', host='158.179.212.127', database='projetopit')
    cur = cnx.cursor()

    location = 'Viseu'
    cur.execute("SELECT a.Time_Stamp, a.valor FROM projetopit.sistema si JOIN sensor s ON si.Id_Sistema = s.Id_Sistema\
                JOIN projetopit.amostra a ON s.Id_Sensor = a.Id_Sensor WHERE si.LocalS = %s ORDER BY a.Time_Stamp ASC",(location,))
    data = cur.fetchall()

    timestamps = [row[0] for row in data]
    values = [row[1] for row in data]

    # Create a plot
    plt.plot(timestamps, values)
    plt.xlabel('Timestamp')
    plt.ylabel('Value')
    plt.title('Samples Graph')

    # Save the plot to a file
    plt.savefig('website/static/Viseu_plot.png')

    # Close the plot
    plt.close()

    # Render the plot in an HTML template
    return render_template("viseu.html", user=current_user)


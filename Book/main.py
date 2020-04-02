from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
main = Flask(__name__)
main.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(main)

class BookDR(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timeslot = db.Column(db.String(200), default = '-')
    day = db.Column(db.String(200), default = '-')
    room = db.Column(db.String(200), default = '-')
    name1 = db.Column(db.String(200), default = '-')
    name2 = db.Column(db.String(200), default = '-')
    name3 = db.Column(db.String(200), default = '-')
    name4 = db.Column(db.String(200), default = '-')
    name5 = db.Column(db.String(200), default = '-')
    
@main.route('/', methods = ['POST','GET'])
def book():
    if request.method == 'POST':
        newtimeslot = request.form['timeslot']
        newday = request.form['day']
        newroom = request.form['room']
        newname1 = request.form['name1']
        newname2 = request.form['name2']
        newname3 = request.form['name3']
        newname4 = request.form['name4']
        newname5 = request.form['name5']
        compdata = BookDR.query.filter_by(timeslot=newtimeslot, room=newroom, day=newday).first()
        if compdata == None:
          new_booking = BookDR(timeslot=newtimeslot, day=newday, room=newroom, name1=newname1,name2=newname2,name3=newname3,name4=newname4,name5=newname5 )
          try:
              db.session.add(new_booking)
              db.session.commit()
              return render_template('success.html')
          except:
              return 'Sorry, there is a problem with booking the slot.'    
        else:
          error = 'Please book another slot.'
          return render_template('book.html', error = error)
        
@main.route('/database', methods=['POST','GET'])
def database():
    booking = BookDR.query.order_by(BookDR.id).all()
    if request.method == 'POST':
        return render_template('database.html', booking=booking)
    else:
        return render_template('login.html')

@main.route('/login', methods=['POST','GET'])
def login():
    booking = BookDR.query.order_by(BookDR.id).all()
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']
        if userid == 'goodstudent' and password == 'goodstudent1':
            return render_template('database.html', booking=booking)
        else:
            tryhard = "Lmao. Stop trying."
            return render_template('login.html', tryhard=tryhard)
    else:
        return render_template('login.html')

@main.route('/success', methods = ['POST'])
def success():
    return render_template("success.html")

@main.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    names = BookDR.query.get_or_404(id)

    if request.method == 'POST':
        names.timeslot = request.form['timeslot']
        names.day = request.form['day']
        names.room = request.form['room']
        names.name1 = request.form['name1']
        names.name2 = request.form['name2']
        names.name3 = request.form['name3']
        names.name4 = request.form['name4']
        names.name5 = request.form['name5']
        try:
            db.session.commit()
            booking=BookDR.query.order_by(BookDR.id).all()
            return render_template('database.html',booking=booking)
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', names=names)

@main.route('/delete/<int:id>')
def delete(id):
    deletus = BookDR.query.get_or_404(id)

    try:
        db.session.delete(deletus)
        db.session.commit()
        booking= BookDR.query.order_by(BookDR.id).all()
        return render_template('database.html',booking=booking)
    except:
        return 'There was a problem deleting that task'

@main.route('/accesslol',methods=['GET','POST'])
def accesslol():
    booking = BookDR.query.order_by(BookDR.id).all()
    return render_template("database.html", booking=booking)
  
if __name__ == "__main__":
    main.run(host='0.0.0.0', port=8080)

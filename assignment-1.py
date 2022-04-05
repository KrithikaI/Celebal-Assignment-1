'''from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired
#from flask_sqlalchemy import SQLAlchemy
#basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

#bootstrap = Bootstrap(app)
#moment = Moment(app)

#@app.route('/')
#def index():
#    return '<h1>Hello World!</h1>'
    
@app.route('/upload')
class NewForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')
    

@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NewForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html', form=form, name=name)




'''
import os
from flask import Flask,render_template,request, flash, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import MySQLdb.cursors
 
UPLOAD_FOLDER = '/data'
ALLOWED_EXTENSIONS = {'png', 'jpg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Obtain connection string information from the portal

config = {
  'host':'assignment1db.mysql.database.azure.com',
  'user':'krithika@assignment1db',
  'password':'Vij@krikum11',
  'database':'assignment1db',
  'client_flags': [mysql.connector.ClientFlag.SSL],
  'ssl_ca': 'D:/Do Not Dell/Downloads/DigiCertGlobalRootG2.crt.pem'
}


#sql connection
#app.config['MYSQL_HOST'] = 'localhost'#hostname
#app.config['MYSQL_USER'] = 'root'#username
#app.config['MYSQL_PASSWORD'] = 'root'#password
#app.config['MYSQL_DB'] = 'assignment'#database name
conn = mysql.connector.connect(**config)
#creating variable for connection
cursor = conn.cursor()

mysql = MySQL(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'
 
@app.route('/upload', methods=['GET','POST'])
def form():
    msg = ''
    if request.method == 'POST' and 'Name' in request.form and 'img' in request.form:
        name = request.form['Name']
        
        #create table
        cursor.execute("CREATE TABLE IF NOT EXISTS data (inputtext varchar(255) not null,primary key (inputtext);")
        #query to check given data is present in database or no
        cursor.execute('SELECT * FROM data WHERE inputtext = % s', (name,))
        #fetching data from MySQL
        result = cursor.fetchone()
        if result:
            msg = 'Name already exists !'
        else:
            #executing query to insert new data into MySQL
            #ISSUE WITH STATEMENT
            print(name)
            cursor.execute('INSERT INTO data VALUES (%s);', (name,))
            conn.commit()
            #displaying message
            msg = 'Value inserted successfully!'
    
    elif request.method =='POST':
        msg = 'Please fill the form'
    
    return render_template('form.html', msg=msg)
        

#image store in data directory - uuid
# text in database in vm
'''
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename("uuid")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return 
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
    

@app.route('/home')
def files_and_dbentries():
    # list of all the files in current folder using os command
    filenames = os.listdir('.')
    
    #list of all the entries in your mysql db added via /upload endpoint
    #connection
    cursor.execute("SELECT * FROM data")  
    data = cursor.fetchall()
    return render_template('displaydata.html', files=filenames, data=data)
  

#renders this GIF if accessed from a browser
@app.route('/static')
def show_img():
    return render_template('image.html')

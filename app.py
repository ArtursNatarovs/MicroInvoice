from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify, send_file, make_response
from flask_mail import Mail, Message
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user,login_required,logout_user
from forms import LoginForm, RegistrationForm, BusinessForm
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
import json
import webbrowser
from threading import Timer
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField,SelectField,#TextField,
                     TextAreaField,SubmitField)
from wtforms.validators import DataRequired
import pdfkit
from tempfile import NamedTemporaryFile
import xml.etree.ElementTree as ET
from handler import add_logo_pic


login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Operator, user_id)


app = Flask(__name__)


app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.update(DEBUG=True,
                    MAIL_SERVER='smtp.gmail.com',
                    MAIL_PORT=465,
                    MAIL_USE_SSL=True,
                    MAIL_USE_TLS = False,
                    MAIL_SUPPRESS_SEND = False,
                    MAIL_DEBUG = True,
                    TESTING = False,
                    MAIL_USERNAME=os.environ.get('inv_MAIL_USERNAME'),
                    MAIL_PASSWORD=os.environ.get('inv_MAIL_PASSWORD'))


config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
app.config['PDF_FOLDER'] = 'static/pdf/'
app.config['TEMPLATE_FOLDER'] = 'templates/'


db = SQLAlchemy(app)
mail = Mail(app)
Migrate(app,db)


login_manager.init_app(app)
login_manager.login_view = "login"



class Operator(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(256))
    is_staff = db.Column(db.Integer)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)



class DataForm(FlaskForm):
    name = StringField('First Name',validators=[DataRequired()])
    last_name = StringField('Last Name',validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired()])
    p_number = StringField('Phone Number',validators=[DataRequired()])
    line1 = StringField('Address line1',validators=[DataRequired()])
    line2 = StringField('Address line2',validators=[DataRequired()])
    postCode = StringField('Post Code',validators=[DataRequired()])
    city = StringField('City',validators=[DataRequired()])
    submit = SubmitField('Submit')


class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)
    last_name = db.Column(db.String)
    email = db.Column(db.Text, unique=True)
    received_invoices = db.relationship('Invoices',backref='user',lazy='dynamic')
    p_number = db.Column(db.String)
    line1 = db.Column(db.String)
    line2 = db.Column(db.String)
    postCode = db.Column(db.String)
    city = db.Column(db.String)




class Invoices(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.String)
    salon_user_id = db.Column(db.Integer,db.ForeignKey('salon.id'))
    receiver_user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    text = db.Column(db.Text)

    def from_to(self):
        return [Salon.query.filter_by(id=self.salon_user_id).first().name, User.query.filter_by(id=self.receiver_user_id).first().name]


class Salon(db.Model):

    __tablename__ = 'salon'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)
    addresse = db.Column(db.String)
    email = db.Column(db.Text, unique=True)
    p_number = db.Column(db.Text)
    sent_invoices = db.relationship('Invoices',backref='salon',lazy='dynamic')
    line1 = db.Column(db.String)
    line2 = db.Column(db.String)
    postCode = db.Column(db.String)
    city = db.Column(db.String)
    logo = db.Column(db.String)
    sortCode = db.Column(db.String)
    accountNumber = db.Column(db.String)

class Button:
  def __init__(self, name, url='#',id='#'):
    self.name = name
    self.url = url
    self.id = id

@app.route('/test')
@login_required
def test():
    return render_template('test.html', page='test')

@app.route('/')
@login_required
def index():
    return render_template('index.html', users=User.query.all(), salons=Salon.query.all(), page='index')


@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = Operator.query.filter_by(email=form.email.data).first()


        if user.check_password(form.password.data) and user is not None:

            login_user(user)
            flash('Logged in successfully.')

            next = request.args.get('next')

            if next == None or not next[0]=='/':
                next = url_for('index')

            return redirect(next)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = Operator(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/tenats')
def tenants():
    subButtons=[Button(name='New Customer',url='add_new_tenant')]
    return render_template('tenants.html', users=User.query.all(), subButtons=subButtons, page='customers')


@app.route('/add_new_tenant', methods=['GET','POST'])
def add_new_tenant():
    form = DataForm()
    if form.validate_on_submit():
        user = User(name=form.name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    p_number=form.p_number.data,
                    line1=form.line1.data,
                    line2=form.line2.data,
                    postCode=form.postCode.data,
                    city=form.city.data)
        db.session.add(user)
        db.session.commit()
        return redirect((url_for('tenants')))

    return render_template('add_new_tenant.html', form=form)


@app.route('/update_tenant', methods=['GET','POST'])
def update_tenant():
    # form=DataForm
    userId = int(request.form['userId'])
    user=User.query.filter_by(id=userId).first()

    return render_template('user_form.html', user=user)


@app.route('/update_tenant02', methods=['POST'])
def update_tenant02():
    userId = int(request.form['userId'])
    user=User.query.filter_by(id=userId).first()
    user.name=(request.form['firstName'])
    user.last_name=(request.form['lastName'])
    user.email=(request.form['email'])
    user.p_number=(request.form['p_number'])
    user.line1=(request.form['line1'])
    user.line2=(request.form['line2'])
    user.postCode=(request.form['postcode'])
    user.city=(request.form['city'])
    db.session.commit()
    return redirect((url_for('tenants')))



@app.route('/invoice01', methods=['POST'])
def invoice01():
    userId = int(request.form['userId'])
    salonId = int(request.form['salonId'])
    session['userId']=userId
    session['salonId']=salonId
    session['invoiceId']=Invoices.query.all()[-1].id
    session['date']=str(datetime.now().date())
    return render_template('invoice01.html',
                            user=User.query.filter_by(id=session['userId']).first(),
                            salon=Salon.query.filter_by(id=session['salonId']).first(),
                            date=datetime.now().date())





@app.route('/send_mail/')
def send_mail():
    sender = Salon.query.filter_by(id=int(session['salonId'])).first()
    receiver = User.query.filter_by(id=int(session['userId'])).first()
    try:
        msg = Message('Invoice form 2J-ART Ltd.',
        sender=sender.email,
        recipients=[receiver.email])
        msg.body = """Please find invoice in attachment.
        If you can't read this email please contact us."""
        rendered_html = render_template('example1.html',
                                    invoiceData=session['invoiceData'],
                                    user=receiver,
                                    salon=sender,
                                    invoiceId=session['invoiceId'],
                                    date=session['date'],
                                    serviceList=session['serviceList'],
                                    total=session['total'])
        # Generate PDF
        pdf = pdfkit.from_string(rendered_html, False, configuration=config, options={"enable-local-file-access": ""})
        msg.attach('invoice.pdf', 'application/pdf', pdf)
        mail.send(msg)
    except Exception as e:
        return str(e)


    new_invoice=Invoices()
    db.session.add(new_invoice)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/resend/<invoiceId>')
def resend(invoiceId):
    invoice = Invoices.query.filter_by(id=int(invoiceId)).first()
    valueList =[j[4] for j in json.loads(invoice.text)]
    receiver = User.query.filter_by(id=invoice.receiver_user_id).first()
    sender=Salon.query.filter_by(id=invoice.salon_user_id).first()
    total = sum(valueList)
    try:
        msg = Message(get_message(),
        sender=sender.email)
        # recipients=[User.query.filter_by(id=int(session['userId'])).first().email])
        msg.recipients=[receiver.email]
        # msg.add_recipient("artursnatarovs@gmail.com")
        msg.body = """Please find invoice in attachment.
        If you can't read this email please contact us."""
        rendered_html = render_template('example1.html',#msg.html = render_template('example1.html',
                                    #invoiceData=session['invoiceData'],
                                    user=receiver,
                                    salon=sender,
                                    invoiceId=invoice.id,
                                    date=invoice.date,
                                    serviceList=json.loads(invoice.text),
                                    total=total)

            # Generate PDF
        pdf = pdfkit.from_string(rendered_html, False, configuration=config, options={"enable-local-file-access": ""})

        # Save PDF to a temporary file
        # with NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
        #     temp_pdf.write(pdf)
        #     temp_pdf_path = temp_pdf.name  # Save the path to use later
        msg.attach('invoice.pdf', 'application/pdf', pdf)
        mail.send(msg)
        print("sent invoice nr:"+str(invoice.id))
        # os.remove(temp_pdf_path)
    except Exception as e:
        return str(e)


    return redirect(url_for('show_invoices'))

@app.route('/view_invoice')
def view_invoice():

    msg = Message('Invoice form 2J-ART Ltd.',
    sender='info.2jartltd@gmail.com',
    recipients=[User.query.filter_by(id=int(session['userId'])).first().email])

    new_invoice=Invoices()
    db.session.add(new_invoice)
    db.session.commit()

    return render_template('example1.html',
                                invoiceData=session['invoiceData'],
                                user=User.query.filter_by(id=int(session['userId'])).first(),
                                salon=Salon.query.filter_by(id=int(session['salonId'])).first(),
                                invoiceId=session['invoiceId'],
                                date=session['date'],
                                serviceList=session['serviceList'],
                                total=session['total'])

@app.route('/re_view_invoice/<invoiceId>')
def re_view_invoice(invoiceId):
    print(f"Received invoiceId: {invoiceId}")
    invoice = Invoices.query.filter_by(id=int(invoiceId)).first()
    print("i got called # REVIEW: ")
    valueList =[j[4] for j in json.loads(invoice.text)]
    userEmail = User.query.filter_by(id=invoice.receiver_user_id).first().email
    total = sum(valueList)
    msg=parse_invoice_settings()
    print(msg["pmsg"])
    return render_template('example1.html',
                                user=User.query.filter_by(id=invoice.receiver_user_id).first(),
                                salon=Salon.query.filter_by(id=invoice.salon_user_id).first(),
                                invoiceId=invoice.id,
                                date=invoice.date,
                                serviceList=json.loads(invoice.text),
                                total=total, msg=msg)




@app.route('/pdf/<invoiceId>')
def generate_pdf(invoiceId):
    invoice = Invoices.query.filter_by(id=int(invoiceId)).first()
    valueList =[j[4] for j in json.loads(invoice.text)]
    userEmail = User.query.filter_by(id=invoice.receiver_user_id).first().email
    total = sum(valueList)
    rendered_html = render_template('example1.html',
                                    user=User.query.filter_by(id=invoice.receiver_user_id).first(),
                                    salon=Salon.query.filter_by(id=invoice.salon_user_id).first(),
                                    invoiceId=invoice.id,
                                    date=invoice.date,
                                    serviceList=json.loads(invoice.text),
                                    total=total)

    pdf = pdfkit.from_string(rendered_html, False, configuration=config,options={"enable-local-file-access": ""})
    response = make_response(pdf)
    response.headers['Content-Type'] = 'aplication/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

    return response


@app.route('/show_invoices')
def show_invoices():
    subButtons=[Button(name='New Invoice',id="newInvoiceButton")]
    return render_template('show_invoices.html', invoices=reversed(Invoices.query.all()), Salon=Salon, page='invoices', users=User.query.all(), salons=Salon.query.all(), subButtons=subButtons)

@app.route('/receiveInvoiceData', methods=['POST'])
def receiveInvoiceData():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    data = request.get_json()
    print(data)
    sender = Salon.query.filter_by(id=int(data['salonId'])).first()
    receiver = User.query.filter_by(id=int(data['userId'])).first()
    serviceList=[]
    for item in data.keys():
        if item.split('_')[0]=='item' and data[item] != '':
            serviceList.append([data['item_'+str(item.split('_')[1])],
                                float(data['value_'+str(item.split('_')[1])]),
                                data['description_'+str(item.split('_')[1])],
                                int(data['quantity_'+str(item.split('_')[1])]), # item quantity
                                float(data['value_'+str(item.split('_')[1])])*int(data['quantity_'+str(item.split('_')[1])]),
                                int(item.split('_')[1])]) #item number
    valueList = [value[4] for value in serviceList]
    total = sum(valueList)
    print("total: "+str(total))
    newInvoice = Invoices(receiver_user_id=data['userId'],
                            salon_user_id=data['salonId'],
                            date=str(datetime.now().date()),
                            text=json.dumps(serviceList))

    db.session.add(newInvoice)
    db.session.commit()

    # print("Received data:", data.keys)
    # settings = Settings.query.filter_by(partner_id=current_user.is_partner)
    # settingOject = {i.setting_name:i for i in settings}
    # existingSettings = [i.setting_name for i in settings]
    # for key, value in data.items():
    #     if key in existingSettings:
    #         settingOject[key].setting_value=roundTime(value)
    #         db.session.commit()
    #         print("updated time ",key,value)
    #     else:
    #         newHours = Settings(partner_id=current_user.is_partner, setting_name=key, setting_value=roundTime(value))
    #         db.session.add(newHours)
    #         db.session.commit()
    #         print(key," not there")
    return jsonify({"status": "success", "message": "invoice added successfully"}), 200
    ################not needed to render template########################
    # return render_template('example1-1.html',
    #
    #                         user=receiver,
    #                         salon=sender,
    #                         invoiceId=newInvoice.id,
    #                         date=newInvoice.date,
    #                         serviceList=serviceList,
    #                         total=total), 200
    ################not needed to render template########################


settingsSubButtons = [Button(name='Operators',id="operatorsButton"),
                    Button(name='Email',id="emailButton",url='email_settings'),
                    Button(name='Invoice',id="invoiceButton",url='invoice_settings'),
                    Button(name='Business',id="businessButton",url='business_settings')]

@app.route('/settings')
def settings():
    subButtons=[Button(name='Operators',id="operatorsButton"),Button(name='Email',id="emaisButton",url='email_settings'),Button(name='Business',id="businessButton",url='business_settings')]
    return render_template('settings.html', page='settings', subButtons=settingsSubButtons)

@app.route('/invoice_settings')
def invoice_settings():

    return render_template('invoice_settings.html', page='settings', subButtons=settingsSubButtons)


@app.route('/email_settings')
def email_settings():
    subButtons=[Button(name='Operators',id="operatorsButton"),Button(name='Email',id="emaisButton")]
    return render_template('email_setting.html', page='settings', subButtons=settingsSubButtons)

@app.route('/business_settings', methods=['GET', 'POST'])
def business_settings():
    form = BusinessForm()
    businesData=Salon.query.first()

    if not businesData:
        Data=None
    else:
        Data = businesData


    if form.validate_on_submit():


        if not businesData:
            business = Salon(name = form.name.data,
                            email = form.email.data,
                            p_number = form.p_number.data,
                            line1 = form.line1.data,
                            line2 = form.line2.data,
                            postCode = form.postCode.data,
                            city = form.city.data,
                            # logo = form.logo.data,
                            sortCode = form.sortCode.data,
                            accountNumber = form.accountNumber.data)


            db.session.add(business)
            if form.logo.data:
                pic = add_logo_pic(form.logo.data,business.id)
                business.logo = pic


        else:
            businesData.name = form.name.data
            businesData.email = form.email.data
            businesData.p_number = form.p_number.data
            businesData.line1 = form.line1.data
            businesData.line2 = form.line2.data
            businesData.postCode = form.postCode.data
            businesData.city = form.city.data
            # businesData.logo = form.logo.data
            businesData.sortCode = form.sortCode.data
            businesData.accountNumber = form.accountNumber.data

            if form.logo.data:

                pic = add_logo_pic(form.logo.data,businesData.id)
                businesData.logo = pic
        db.session.commit()
        print("Business saved successfully!", "success")
        return redirect(url_for('settings'))

    return render_template('business_settings.html', form=form, Data=Data, page="settings", subButtons=settingsSubButtons)


@app.route('/save-settings', methods=['POST'])
def save_settings():
    try:
        xml_content = request.data.decode('utf-8')
        with open('static/settings.xml', 'w') as file:
            file.write(xml_content.strip())
        return "Settings saved successfully!", 200
    except Exception as e:
        print("Error saving settings:", e)
        return "Failed to save settings", 500

@app.route('/get-settings', methods=['GET'])
def get_settings():
    try:
        with open('static/settings.xml', 'r', encoding='utf-8') as file:
            xml_content = file.read()
            print(xml_content)
        # Parse the XML content
            root = ET.fromstring(xml_content)
            for child in root:
                print(child.tag, child.attrib)
        # Extract email settings
        email_settings = root.find('email')
        print(email_settings)
        settings_data = {
            'server': email_settings.find('server').text,
            'port': email_settings.find('port').text,
            'username': email_settings.find('username').text,
            'password': email_settings.find('password').text,
            'message': email_settings.find('message').text
        }
        return jsonify(settings_data)
    except Exception as e:
        return jsonify({'error': str(e)})

def parse_invoice_settings():
    print("i got called in parse")
    try:
        with open('static/invoice.xml', 'r', encoding='utf-8') as file:
            xml_content = file.read()
        root = ET.fromstring(xml_content)
        invoice_setting = root.find('invoice')
        settings_data = {
            'pmsg': invoice_setting.find('pmsg').text,
            'notice': invoice_setting.find('notice').text,
            'footer': invoice_setting.find('footer').text
        }
        return settings_data
    except Exception as e:
        raise Exception(f"Error parsing invoice settings: {str(e)}")



@app.route('/get-invoiceSettings', methods=['GET', 'POST'])
def get_invoiceSettings():
    print("i got called")
    try:
        settings_data = parse_invoice_settings()
        return jsonify(settings_data)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/save-invoiceSettings', methods=['POST'])
def save_invoiceSettings():
    try:
        xml_content = request.data.decode('utf-8')
        with open('static/invoice.xml', 'w') as file:
            file.write(xml_content.strip())
        return "Settings saved successfully!", 200
    except Exception as e:
        print("Error saving settings:", e)
        return "Failed to save settings", 500



def open_browser():
      webbrowser.open_new("http://127.0.0.1:5431")



def ensure_default_operator():
    # Check if the Operator table has any entries
    if not Operator.query.first():
        # If no entries exist, create a default operator
        default_operator = Operator(
            username="Admin",
            email="admin@mail.com",
            password="P@ssw0rd"
        )

        db.session.add(default_operator)
        db.session.commit()
        default_operator.password_hash = generate_password_hash("P@ssw0rd")
        db.session.commit()
        print("Default operator created.")
    else:
        print("Operator table already has entries.")

def get_message():
    try:
        with open('static/settings.xml', 'r', encoding='utf-8') as file:
            xml_content = file.read()
        root = ET.fromstring(xml_content)
        message = root.find('./email/message').text
        return  message
    except Exception as e:
        return e


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        ensure_default_operator()  # Ensure there's at least one entry in the Operator table
    Timer(1, open_browser).start()
    app.run(port=5431)





#.\envir\Scripts\flask db migrate -m "added breed column"
#.\envir\Scripts\flask db upgrade

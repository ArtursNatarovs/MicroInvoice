from flask_wtf import FlaskForm
# from invoicer import Operator
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired,Email,EqualTo,Length
from wtforms import ValidationError

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register!')

    def check_email(self, field):
        # Check if not None for that user email!
        if Operator.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def check_username(self, field):
        # Check if not None for that username!
        if Operator.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')



class BusinessForm(FlaskForm):
    name = StringField("Business Name", validators=[DataRequired(), Length(max=255)])
    addresse = StringField("Address", validators=[Length(max=255)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    p_number = StringField("Phone Number", validators=[DataRequired(), Length(max=20)])
    line1 = StringField("Address Line 1", validators=[DataRequired(), Length(max=255)])
    line2 = StringField("Address Line 2", validators=[Length(max=255)])
    postCode = StringField("Postcode", validators=[DataRequired(), Length(max=20)])
    city = StringField("City", validators=[DataRequired(), Length(max=255)])
    logo = StringField("Logo URL", validators=[Length(max=255)])
    sortCode = StringField("Sort Code", validators=[DataRequired(), Length(max=20)])
    accountNumber = StringField("Account Number", validators=[DataRequired(), Length(max=20)])
    submit = SubmitField("Save")

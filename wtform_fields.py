from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from passlib.hash import pbkdf2_sha256

from models import User

# outside class custom validator
# does not have any restriction on it's name unlike inline custom validators
def invalid_credential(form, field):
    """ Username and Password Validator """

    username_entered = form.username.data 
    password_entered = field.data 

    # checking username and password from database
    user_object = User.query.filter_by(username = username_entered).first()
    # check if username exists in database
    if user_object is None:
        raise ValidationError("Username or Password is incorrect! :(")
    # check if password is correct for given username
    elif not pbkdf2_sha256.verify(password_entered, user_object.password):
        raise ValidationError("Username or Password is incorrect! :(")

class RegistrationForm(FlaskForm):
    """ Registration Form """

    username = StringField('username_label', validators=[InputRequired(message="Username Required!"),
        Length(min=3, max=27, message="Username must be in between 3 to 27 characters")])
    password = PasswordField("password_label", validators=[InputRequired(message="Password Required!"),
        Length(min=6, max=27, message="Password must be in between 6 to 27 characters")])
    confirm_password = PasswordField("confirm_password_label", validators=[InputRequired(message="Password Required!"), 
        EqualTo("password", message="Passwords must match!")])
    # submit_button = SubmitField("SignUp!")

    # inline custom validator
    # name has to be strictly in this format
    def validate_username(self, username):
        user_object = User.query.filter_by(username = username.data).first()
        if user_object:
            raise ValidationError("Username already exists. Please use a different username.")


class LoginForm(FlaskForm):
    """ Login Form """

    username = StringField('username_label',
        validators=[InputRequired(message="Username required!")])
    password = PasswordField('password_label', 
        validators=[InputRequired(message="Password Required!"), invalid_credential])
    # submit_button = SubmitField("Login!")
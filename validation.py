from wtforms import StringField, TextAreaField, SelectField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Optional, Regexp, length
from flask_wtf import FlaskForm

# 135Cipher.
class Cipher135Form(FlaskForm):
    encrypt = SubmitField('encrypt', validators=[Optional()])
    decrypt = SubmitField('decrypt', validators=[Optional()])
    key = StringField('key', validators=[InputRequired(), Regexp('^[1-9]\d*$', 
                                         message="Field must be a positive integer."),
                                         length(max=135, message="Field cannot be longer than 135 digits")])
    text = TextAreaField('text', validators=[InputRequired(), length(max=10000)])
    random = BooleanField('random')

# 147Cipher.
class Cipher147Form(FlaskForm):
    encrypt = SubmitField('encrypt', validators=[Optional()])
    decrypt = SubmitField('decrypt', validators=[Optional()])
    nonce_options = ["hybrid", "random", "time"]
    encoding_options = ["base85", "base64", "base32", "base16"]
    key = StringField('key', validators=[InputRequired(), length(max=147)])
    text = TextAreaField('text', validators=[
                         InputRequired(), length(max=10000)])
    nonce = SelectField('nounce', validators=[
                        InputRequired()], choices=nonce_options)
    encoding = SelectField('encoding', validators=[
                           InputRequired()], choices=encoding_options)

class Picture122Form(FlaskForm):
    x = 1

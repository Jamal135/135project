from wtforms import StringField, TextAreaField, SelectField, SubmitField, BooleanField, ValidationError
from wtforms.validators import InputRequired, Optional, Regexp, AnyOf, length
from flask_wtf import FlaskForm

# Encryption
# 135Cipher.
class Cipher135Form(FlaskForm):
    encrypt = SubmitField('encrypt', validators=[Optional()])
    decrypt = SubmitField('decrypt', validators=[Optional()])
    key = StringField('key', validators=[InputRequired(), Regexp('^[0-9]\d*$',
                                         message="Field must be a positive integer."),
                                         length(max=135, message="Field cannot exceed 135 digits.")])
    text = TextAreaField('text', validators=[
                         InputRequired(), length(max=1000, message="Field cannot exceed 1000 characters.")])
    random = BooleanField('random')

# 147Cipher.
class Cipher147Form(FlaskForm):
    encrypt = SubmitField('encrypt', validators=[Optional()])
    decrypt = SubmitField('decrypt', validators=[Optional()])
    nonce_options = ["hybrid", "random", "time"]
    encoding_options = ["base85", "base64", "base32", "base16"]
    key = StringField('key', validators=[InputRequired(), length(
        max=147, message="Field cannot exceed 147 characters.")])
    text = TextAreaField('text', validators=[
                         InputRequired(), length(max=1000, message="Field cannot exceed 1000 characters.")])
    nonce = SelectField('nounce', validators=[
                        InputRequired()], choices=nonce_options)
    encoding = SelectField('encoding', validators=[
                           InputRequired()], choices=encoding_options)

# 101Cipher.
class Cipher101Form(FlaskForm):
    encrypt = SubmitField('encrypt', validators=[Optional()])
    decrypt = SubmitField('decrypt', validators=[Optional()])
    key = StringField('key', validators=[InputRequired(), Regexp('^[0-9]\d*$',
                                         message="Field must be a positive integer."),
                                         length(max=101, message="Field cannot exceed 101 digits")])
    number = StringField('number', validators=[InputRequired(), Regexp('^[0-9]\d*$',
                                                                       message="Field must be a positive integer."),
                                               length(max=135, message="Field cannot exceed 135 digits.")])

# Steganography.
# 122Stego.
class Stego122Form(FlaskForm):
    x = 1

# Datatools.
# Basetool.
class BasetoolForm(FlaskForm):
    insequence = StringField('insequence', validators=[InputRequired(), length(
        max=99, message="Field cannot exceed 99 characters")])
    def validate_insequence(form, field):
        if not len(set(field.data[:int(form.inbase.data)])) == len(field.data[:int(form.inbase.data)]):
            raise ValidationError("Sequence must be unique characters.")
        if len(form.insequence.data) < int(form.inbase.data):
            raise ValidationError("Must be in base or more unique characters.")
        if any(character in form.insequence.data for character in ['-', '.']):
            raise ValidationError("Must not contain - or . characters.")
    outsequence = StringField('outsequence', validators=[InputRequired(), length(
        max=99, message="Field cannot exceed 99 characters")])
    def validate_outsequence(form, field):
        if not len(set(field.data[:int(form.outbase.data)])) == len(field.data[:int(form.outbase.data)]):
            raise ValidationError("Sequence must be unique characters.")
        if len(form.outsequence.data) < int(form.outbase.data):
            raise ValidationError("Must be out base or more unique characters.")
        if any(character in form.outsequence.data for character in ['-', '.']):
            raise ValidationError("Must not contain - or . characters.")
    inbase = StringField('inbase', validators=[InputRequired(), Regexp('^0*(?:[2-9]|[1-9]\d\d*)$',
                                                                       message="Must be two or greater integer."),
                                               length(max=2, message="Field cannot exceed 99.")])
    outbase = StringField('outbase', validators=[InputRequired(), Regexp('^0*(?:[2-9]|[1-9]\d\d*)$',
                                                                         message="Must be two or greater integer."),
                                                 length(max=2, message="Field cannot exceed 99.")])
    number = StringField('number', validators=([InputRequired()]))
    def validate_number(form, field):
        for character in field.data:
            if character not in form.insequence.data[:int(form.inbase.data)]:
                raise ValidationError("Characters outside specified base input.")

# Counttool.
class CounttoolForm(FlaskForm):
    text = TextAreaField('text', validators=[
                         InputRequired(), length(max=1000, message="Field cannot exceed 1000 characters.")])
    spaces = BooleanField('spaces')
    capitals = BooleanField('capitals')
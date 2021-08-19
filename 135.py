# python 135.py
from functions.encryption._147cipher_ import encrypt_147, decrypt_147
from functions.encryption._135cipher_ import encrypt_135, decrypt_135
from flask import Flask, render_template, send_from_directory, request
from flask_wtf.csrf import CSRFProtect
from os import path, getenv

# Set up CSRF protection.
csrf = CSRFProtect()
app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('CSRF_KEY')
app.config['WTF_CSRF_TIME_LIMIT'] = None
csrf.init_app(app)

# Specify icon.
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# --Main pages--
@app.route("/")
@app.route("/home")
def home():
    return render_template('other/home.html', title='Home')

@app.route("/about")
def about():
    return render_template('other/about.html', title="About")

# --Encryption pages--
@app.route("/encryption")
@app.route("/encryption/viewall")
def encryption_viewall():
    return render_template('encryption/viewall.html', title="Encryption")

# 135Cipher.
from validation import Cipher135Form
@app.route("/encryption/135cipher", methods=['GET', 'POST'])
def cipher135():
    form = Cipher135Form()
    if request.method == 'POST':
        if form.validate_on_submit():
            key = form.key.data
            text = form.text.data
            random = form.random.data
            if random == True:
                random_input = "+"
            elif random == False:
                random_input = "-"
            try:
                if form.encrypt.data:
                    result = encrypt_135(key, text, random_input)
                elif form.decrypt.data:
                    result = decrypt_135(key, text)
            except:
                result = "Process Execution Failed"
            data = {"key": key, "text": text,
                    "random": random, "result": result}
            return render_template('encryption/135cipher.html', title="135Cipher", form="submitted", data=data)
        else:
            errors = form.errors
            for form_value in errors:
                errors[form_value] = errors[form_value][0]
            return render_template('encryption/135cipher.html', title="135Cipher", form="failed", errors=errors)
    return render_template('encryption/135cipher.html', title="135Cipher", form=None)

@app.route("/encryption/135cipher/about")
def cipher135_about():
    return render_template('encryption/135cipher-about.html', title="135Cipher")

# 147Cipher.
from validation import Cipher147Form
@app.route("/encryption/147cipher", methods=['GET', 'POST'])
def cipher147():
    form = Cipher147Form()
    if request.method == 'POST':
        if form.validate_on_submit():
            key = form.key.data
            text = form.text.data
            nonce = form.nonce.data
            encoding = form.encoding.data
            try:
                if form.encrypt.data:
                    result = encrypt_147(key, text, encoding, nonce)
                elif form.decrypt.data:
                    result = decrypt_147(key, text, encoding)
            except:
                result = "Process Execution Failed"
            data = {"key": key, "text": text, "encoding": encoding,
                    "nonce": nonce, "result": result}
            return render_template('encryption/147cipher.html', title="147Cipher", form="submitted", data=data)
        else:
            errors = form.errors
            for form_value in errors:
                errors[form_value] = errors[form_value][0]
            return render_template('encryption/147cipher.html', title="147Cipher", form="failed", errors=errors)
    else:
        return render_template('encryption/147cipher.html', title="147Cipher", form=None)

@app.route("/encryption/147cipher/about")
def cipher147_about():
    return render_template('encryption/147cipher-about.html', title="147Cipher")

# --Steganography pages--
@app.route("/steganography")
@app.route("/steganography/viewall")
def steganography_viewall():
    return render_template('steganography/viewall.html', title="Steganography")

# 122Picture.
from validation import Picture122Form
@app.route("/steganography/122Picture", methods=['GET', 'POST'])
def picture122():
    form = Picture122Form()
    return render_template('steganography/122Picture.html', title="122Picture", form=None)

@app.route("/steganography/122picture/about")
def Picture122_about():
    return render_template('steganography/122picture-about.html', title="122Picture")

# --Tool pages--
@app.route("/datatools")
@app.route("/datatools/viewall")
def datatools_viewall():
    return render_template('datatools/viewall.html', title="Data Tools")

@app.route("/datatools/basetool")
def datatools_basetool():
    return render_template('datatools/basetool.html', title="Base Tool")

@app.route("/datatools/counttool")
def datatools_counttool():
    return render_template('datatools/counttool.html', title="Count Tool")

@app.route("/datatools/imagetool")
def datatools_imagetool():
    return render_template('datatools/imagetool.html', title="Image Tool")

# --Other pages--
@app.route("/disclaimer")
def disclaimer():
    return render_template('other/disclaimer.html', title="Disclaimer")

@app.route("/privacy")
def privacy():
    return render_template('other/privacy.html', title="Privacy")

# --Error handling--
@app.errorhandler(404)
def page_not_found(e):
    return render_template('other/home.html', title='Home'), 404

# Debug mode.
if __name__ == "__main__":
    app.run(debug=True)

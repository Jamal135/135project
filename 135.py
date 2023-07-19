# python 135.py
import validation
from functions.encryption._147cipher_ import encrypt_147, decrypt_147
from functions.encryption._135cipher_ import encrypt_135, decrypt_135
from functions.encryption._101cipher_ import encrypt_101, decrypt_101
from functions.datatools._basetool_ import base_convert
from functions.datatools._counttool_ import count_analysis
from functions.datatools._imagetool_ import image_compare
from flask import Flask, render_template, send_from_directory, jsonify
from flask_wtf.csrf import CSRFProtect
from os import path, urandom

# Set up CSRF protection.
csrf = CSRFProtect()
app = Flask(__name__)
app.config['SECRET_KEY'] = urandom(32)
app.config['WTF_CSRF_TIME_LIMIT'] = None
csrf.init_app(app)

# Specify icon.
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# --Main pages--
@app.route("/", methods=["GET"])
@app.route("/home", methods=["GET"])
def home():
    return render_template('other/home.html', title='Home')

# @app.route("/about", methods=["GET"])
# def about():
#     return render_template('other/about.html', title="About")

# --Encryption pages--
@app.route("/encryption", methods=["GET"])
@app.route("/encryption/viewall", methods=["GET"])
def encryption_viewall():
    return render_template('encryption/viewall.html', title="Encryption")

# 135Cipher.
@app.route("/encryption/135cipher", methods=['GET'])
def cipher135():
    return render_template('encryption/135cipher.html', title="135Cipher")

@app.route("/encryption/135cipher/result", methods=['POST'])
def cipher135_result():
    form = validation.Cipher135Form()
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
                    return jsonify(encrypt_135(key, text, random_input))
            elif form.decrypt.data:
                    return jsonify(decrypt_135(key, text))
        except Exception:
            return jsonify("Process Execution Failed")
    else:
        errors = form.errors
        for form_value in errors:
            errors[form_value] = errors[form_value][0]
        errors["error"] = True
        return jsonify(errors)

@app.route("/encryption/135cipher/about", methods=["GET"])
def cipher135_about():
    return render_template('encryption/135cipher-about.html', title="135Cipher")

# 147Cipher.
@app.route("/encryption/147cipher", methods=['GET'])
def cipher147():
    return render_template('encryption/147cipher.html', title="147Cipher")

@app.route("/encryption/147cipher/result", methods=['POST'])
def cipher147_result():
    form = validation.Cipher147Form()
    if form.validate_on_submit():
        key = form.key.data
        text = form.text.data
        nonce = form.nonce.data
        encoding = form.encoding.data
        try:
            if form.encrypt.data:
                return jsonify(encrypt_147(key, text, encoding, nonce))
            elif form.decrypt.data:
                return jsonify(decrypt_147(key, text, encoding))
        except Exception:
            return jsonify("Process Execution Failed")
    else:
        errors = form.errors
        for form_value in errors:
            errors[form_value] = errors[form_value][0]
        errors["error"] = True
        return jsonify(errors)

@app.route("/encryption/147cipher/about", methods=["GET"])
def cipher147_about():
    return render_template('encryption/147cipher-about.html', title="147Cipher")

# 101Cipher.
@app.route("/encryption/101cipher", methods=["GET"])
def cipher101():
    return render_template('encryption/101cipher.html', title="101Cipher")

@app.route("/encryption/101cipher/result", methods=['POST'])
def cipher101_result():
    form = validation.Cipher101Form()
    if form.validate_on_submit():
        key = form.key.data
        number = form.number.data
        try:
            if form.encrypt.data:
                return jsonify(encrypt_101(key, number))
            elif form.decrypt.data:
                return jsonify(decrypt_101(key, number))
        except Exception:
            return jsonify("Process Execution Failed")
    else:
        errors = form.errors
        for form_value in errors:
            errors[form_value] = errors[form_value][0]
        errors["error"] = True
        return jsonify(errors)

@app.route("/encryption/101cipher/about", methods=["GET"])
def cipher101_about():
    return render_template('encryption/101cipher-about.html', title="101Cipher")

# # --Steganography pages--
# @app.route("/steganography", methods=["GET"])
# @app.route("/steganography/viewall", methods=["GET"])
# def steganography_viewall():
#     return render_template('steganography/viewall.html', title="Steganography")

# # 122Picture.
# @app.route("/steganography/122stego", methods=['GET'])
# def stego122():
#     return render_template('steganography/122stego.html', title="122Stego", form=None)

# @app.route("/steganography/122stego/result", methods=['POST'])
# def stego122_result():
#     form = validation.Stego122Form()
#     if form.validate_on_submit():
#         pass
#     else:
#         pass

# @app.route("/steganography/122stego/about", methods=["GET"])
# def stego122_about():
#     return render_template('steganography/122stego-about.html', title="122Stego")

# --Tool pages--
@app.route("/datatools", methods=["GET"])
@app.route("/datatools/viewall", methods=["GET"])
def datatools_viewall():
    return render_template('datatools/viewall.html', title="Data Tools")

# Base tool.
@app.route("/datatools/basetool", methods=["GET"])
def basetool():
    return render_template('datatools/basetool.html', title="Base Tool")

@app.route("/datatools/basetool/result", methods=["POST"])
def basetool_result():
    form = validation.BasetoolForm()
    if form.validate_on_submit():
        inbase = form.inbase.data
        outbase = form.outbase.data
        number = form.number.data
        insequence = form.insequence.data
        outsequence = form.outsequence.data
        try:
            return jsonify(base_convert(number, inbase, outbase, insequence, outsequence))
        except Exception:
            return jsonify("Process Execution Failed")
    else:
        errors = form.errors
        for form_value in errors:
            errors[form_value] = errors[form_value][0]
        errors["error"] = True
        return jsonify(errors)

@app.route("/datatools/basetool/about", methods=["GET"])
def basetool_about():
    return render_template('datatools/basetool-about.html', title="Base Tool")

# Count tool.
@app.route("/datatools/counttool", methods=["GET"])
def counttool():
    return render_template('datatools/counttool.html', title="Count Tool")

@app.route("/datatools/counttool/result", methods=["POST"])
def counttool_result():
    form = validation.CounttoolForm()
    if form.validate_on_submit():
        text = form.text.data
        spaces = form.spaces.data
        capitals = form.capitals.data
        try:
            return jsonify(count_analysis(text, spaces, capitals))
        except Exception:
            return jsonify("Process Execution Failed")
    else:
        errors = form.errors
        for form_value in errors:
            errors[form_value] = errors[form_value][0]
        errors["error"] = True
        return jsonify(errors)

@app.route("/datatools/counttool/about", methods=["GET"])
def counttool_about():
    return render_template('datatools/counttool-about.html', title="Count Tool")

# @app.route("/datatools/imagetool", methods=["GET"])
# def imagetool():
#     return render_template('datatools/imagetool.html', title="Image Tool")

# @app.route("/datatools/imagetool/result", methods=["POST"])
# def imagetool_result():
#     form = validation.ImagetoolForm()
#     if form.validate_on_submit():
#         alpha = form.alpha.data
#         image1 = form.image1.data
#         image2 = form.image2.data
#         try:
#             return jsonify(image_compare(image1, image2, alpha))
#         except:
#             return jsonify("Process Execution Failed")
#     else:
#         errors = form.errors
#         for form_value in errors:
#             errors[form_value] = errors[form_value][0]
#         errors["error"] = True
#         return jsonify(errors)

# --Other pages--
@app.route("/disclaimer", methods=["GET"])
def disclaimer():
    return render_template('other/disclaimer.html', title="Disclaimer")

@app.route("/settings", methods=["GET"])
def settings():
    return render_template('other/settings.html', title="Settings")

@app.route("/privacy", methods=["GET"])
def privacy():
    return render_template('other/privacy.html', title="Privacy")

# --Error handling--
@app.errorhandler(404)
def page_not_found(e):
    return render_template('other/home.html', title='Home'), 404

# Debug mode.
if __name__ == "__main__":
    app.run(debug=True)

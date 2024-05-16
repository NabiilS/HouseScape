from flask import Flask, render_template, request
import numpy as np
import pickle as pk

app = Flask(__name__)

# Import du modèle avec pickle
model = pk.load(open('model.pkl', 'rb'))

@app.route('/')
def index():
    return render_template('HomePage.html')

@app.route('/comment-ca-marche')
def how_it_works():
    return render_template('CommentCaMarche.html')

@app.route('/contactez-nous')
def contact_us():
    return render_template('Contactez-nous.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        _type = request.form['type']
        codePostal = request.form['code_postal']
        bedrooms = request.form['nb_pieces']
        surface = request.form['surface']

        array = np.array([_type, codePostal, bedrooms, surface])
        array = array.astype(np.float64)
        result = model.predict([array])
        return render_template('HomePage.html', data=int(result), code_postal=codePostal)
    return render_template('HomePage.html')


if __name__ == '__main__':
    app.run(debug=True)

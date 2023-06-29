
from flask import Flask, render_template, request
import numpy as np

import pickle as pk

app = Flask(__name__)


#IMPORT model with pickle

model = pk.load(open('model.pkl','rb')) #lecture en mode binaire "read binary"

@app.route('/')
def index():
    return render_template('HomePage.html')

#routing: un processus par lequel une URL est mappée à une fonction de vue qui traite

#la demande et le retour d'une réponse GET, POST, PUT, DELETE

# les methodes HTTP (envoyer des données d'un client web vers un serveur web)

#GET pour demander des ressources à un serveur web (serveur ===> client)

#POST pour envoyer des données à un serveur web pour le traitement (upload, saisir un form, ...) (client ===> serveur)

#PUT mettre à jour une ressource existante sur le serveur

#DELETE suppprimer du serveur

# saisir les informations POST ===> renvoyer le prédiction GET

@app.route('/predict',methods=['GET', 'POST'] )

def predict():

    _type = request.form['type']

    codePostal = request.form['code_postal']

    bedrooms = request.form['nb_pieces']

    surface = request.form['surface']

    array = np.array([_type, codePostal, bedrooms, surface])
    array = array.astype(np.float64)
    result = model.predict([array])


    #arr= contient ces valeurs => transtyper vers float64 => prix = model.predict(arr)

    # arr = np.array([bedrooms,bathrooms,surface])

    # arr = arr.astype(np.float64)

    # prix = model.predict([arr])

    return render_template('HomePage.html', data= int(result)) # data = prix




if __name__ == '__main__':

    app.run(debug= True)
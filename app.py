from flask import Flask, render_template
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    # Flask va chercher automatiquement dans le dossier 'templates'
    return render_template('index.html')
    
@app.route('/inscription', methods=['POST'])
def inscription():
    nom = request.form.get('nom')
    tel = request.form.get('whatsapp')
    service = request.form.get('service')
    
    # Ici, tu peux enregistrer dans un fichier ou juste afficher
    print(f"Nouveau client : {nom} - {tel} - Service : {service}")
    
    return f"Merci {nom} ! Votre demande pour '{service}' a été reçue. Je vous contacte sur WhatsApp."

if __name__ == '__main__':
    app.run(debug=True)

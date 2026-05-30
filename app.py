from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from datetime import datetime
import re

app = Flask(__name__)

# Configuration
DATABASE = 'demandes.db'
SERVICES_DISPONIBLES = ['Coiffure', 'Manucure', 'Massage', 'Soins du visage']

# ==================== INITIALISATION BD ====================
def init_db():
    """Crée la table si elle n'existe pas"""
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE demandes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                telephone TEXT NOT NULL,
                service TEXT NOT NULL,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                statut TEXT DEFAULT 'en attente'
            )
        ''')
        conn.commit()
        conn.close()
        print("✅ Base de données créée!")

# ==================== VALIDATION ====================
def valider_donnees(nom, tel, service):
    """Valide les données reçues"""
    erreurs = []
    
    # Vérifier que les champs ne sont pas vides
    if not nom or not nom.strip():
        erreurs.append("Le nom est requis")
    elif len(nom) < 2:
        erreurs.append("Le nom doit faire au moins 2 caractères")
    
    if not tel or not tel.strip():
        erreurs.append("Le téléphone est requis")
    elif not re.match(r'^[\d\s\-\+\(\)]{7,}$', tel):
        erreurs.append("Le format du tél��phone est invalide")
    
    if not service or not service.strip():
        erreurs.append("Le service est requis")
    elif service not in SERVICES_DISPONIBLES:
        erreurs.append(f"Service invalide. Choisir parmi : {', '.join(SERVICES_DISPONIBLES)}")
    
    return erreurs

# ==================== BASE DE DONNÉES ====================
def enregistrer_demande(nom, tel, service):
    """Enregistre une demande dans la BD"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO demandes (nom, telephone, service)
            VALUES (?, ?, ?)
        ''', (nom.strip(), tel.strip(), service.strip()))
        conn.commit()
        demande_id = cursor.lastrowid
        conn.close()
        return demande_id
    except Exception as e:
        print(f"❌ Erreur BD: {e}")
        return None

def recuperer_demandes():
    """Récupère toutes les demandes"""
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM demandes ORDER BY date_creation DESC')
        demandes = cursor.fetchall()
        conn.close()
        return [dict(d) for d in demandes]
    except Exception as e:
        print(f"❌ Erreur BD: {e}")
        return []

def mettre_a_jour_statut(demande_id, nouveau_statut):
    """Met à jour le statut d'une demande"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('UPDATE demandes SET statut = ? WHERE id = ?', 
                      (nouveau_statut, demande_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Erreur BD: {e}")
        return False

# ==================== ROUTES ====================
@app.route('/')
def home():
    """Page d'accueil"""
    return render_template('index.html', services=SERVICES_DISPONIBLES)

@app.route('/inscription', methods=['POST'])
def inscription():
    """Traite l'inscription (API JSON)"""
    try:
        # Récupérer les données
        data = request.get_json() if request.is_json else request.form
        nom = data.get('nom')
        tel = data.get('whatsapp') or data.get('telephone')
        service = data.get('service')
        
        # Valider
        erreurs = valider_donnees(nom, tel, service)
        if erreurs:
            return jsonify({
                'succes': False,
                'message': 'Erreurs de validation',
                'erreurs': erreurs
            }), 400
        
        # Enregistrer
        demande_id = enregistrer_demande(nom, tel, service)
        if not demande_id:
            return jsonify({
                'succes': False,
                'message': 'Erreur lors de l\'enregistrement'
            }), 500
        
        # Réponse succès
        return jsonify({
            'succes': True,
            'message': f'Merci {nom}! Votre demande pour "{service}" a été reçue.',
            'demande_id': demande_id,
            'details': f'Je vous contacte sur WhatsApp au {tel}'
        }), 201
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return jsonify({
            'succes': False,
            'message': 'Erreur serveur'
        }), 500

@app.route('/admin/demandes', methods=['GET'])
def voir_demandes():
    """Affiche toutes les demandes (interface admin)"""
    demandes = recuperer_demandes()
    return render_template('admin.html', demandes=demandes)

@app.route('/api/demandes', methods=['GET'])
def api_demandes():
    """API pour récupérer les demandes en JSON"""
    demandes = recuperer_demandes()
    return jsonify({
        'succes': True,
        'total': len(demandes),
        'demandes': demandes
    })

@app.route('/api/demandes/<int:demande_id>/statut', methods=['PUT'])
def modifier_statut(demande_id):
    """Modifie le statut d'une demande"""
    try:
        data = request.get_json()
        nouveau_statut = data.get('statut')
        
        statuts_valides = ['en attente', 'contacté', 'confirmé', 'annulé']
        if nouveau_statut not in statuts_valides:
            return jsonify({
                'succes': False,
                'message': f'Statut invalide. Valides: {statuts_valides}'
            }), 400
        
        if mettre_a_jour_statut(demande_id, nouveau_statut):
            return jsonify({
                'succes': True,
                'message': f'Statut modifié en "{nouveau_statut}"'
            })
        else:
            return jsonify({
                'succes': False,
                'message': 'Erreur lors de la mise à jour'
            }), 500
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return jsonify({'succes': False, 'message': 'Erreur serveur'}), 500

@app.route('/api/services', methods=['GET'])
def get_services():
    """Retourne la liste des services disponibles"""
    return jsonify({
        'succes': True,
        'services': SERVICES_DISPONIBLES
    })

# ==================== GESTION DES ERREURS ====================
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'succes': False, 'message': 'Page non trouvée'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'succes': False, 'message': 'Erreur serveur'}), 500

# ==================== DÉMARRAGE ====================
if __name__ == '__main__':
    init_db()
    app.run(debug=True)

# 💇 Mon Site Rendez-vous

Application Flask pour gérer les demandes de rendez-vous en ligne avec interface admin.

## 🚀 Démarrage rapide

### 1. Installation

```bash
# Cloner le projet
git clone <repo-url>
cd mon_site_rendez_vous

# Créer un environnement virtuel (optionnel mais recommandé)
python -m venv venv

# Activer l'environnement (Windows)
venv\Scripts\activate
# Activer l'environnement (Mac/Linux)
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Lancer l'application

```bash
python app.py
```

L'application sera accessible à `http://localhost:5000`

## 📋 Fonctionnalités

### 🌐 Page d'accueil (`/`)
- Formulaire d'inscription élégant
- Validation des données en temps réel
- Animations fluides et UX moderne

### 📱 API d'inscription (`/inscription` - POST)
```json
{
  "nom": "Jean Dupont",
  "whatsapp": "+33 6 12 34 56 78",
  "service": "Coiffure"
}
```

**Réponse succès (201):**
```json
{
  "succes": true,
  "message": "Merci Jean! Votre demande pour \"Coiffure\" a été reçue.",
  "demande_id": 1,
  "details": "Je vous contacte sur WhatsApp au +33 6 12 34 56 78"
}
```

**Réponse erreur (400):**
```json
{
  "succes": false,
  "message": "Erreurs de validation",
  "erreurs": [
    "Le nom doit faire au moins 2 caractères",
    "Le format du téléphone est invalide"
  ]
}
```

### 📊 Interface Admin (`/admin/demandes`)
- Vue d'ensemble des demandes
- Statistiques en temps réel
- Modification du statut
- Lien direct WhatsApp pour contacter les clients

### 🔧 Routes API

| Route | Méthode | Description |
|-------|---------|-------------|
| `/` | GET | Page d'accueil |
| `/inscription` | POST | Soumettre une demande |
| `/admin/demandes` | GET | Interface admin |
| `/api/demandes` | GET | Récupérer toutes les demandes (JSON) |
| `/api/demandes/<id>/statut` | PUT | Modifier le statut d'une demande |
| `/api/services` | GET | Lister les services disponibles |

## 📦 Structure du projet

```
mon_site_rendez_vous/
├── app.py                 # Application principale
├── requirements.txt       # Dépendances Python
├── demandes.db           # Base de données SQLite (généré)
├── templates/
│   ├── index.html        # Page d'accueil
│   └── admin.html        # Interface admin
└── README.md             # Cette documentation
```

## 💾 Base de données

La base de données SQLite (`demandes.db`) est créée automatiquement au premier lancement.

**Table `demandes`:**
```sql
CREATE TABLE demandes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    telephone TEXT NOT NULL,
    service TEXT NOT NULL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    statut TEXT DEFAULT 'en attente'
);
```

**Statuts disponibles:**
- `en attente` - Demande reçue, en attente de contact
- `contacté` - Client contacté
- `confirmé` - Rendez-vous confirmé
- `annulé` - Rendez-vous annulé

## ✅ Validation

### Nom
- ✓ Requis
- ✓ Minimum 2 caractères

### Téléphone
- ✓ Requis
- ✓ Format valide (au moins 7 caractères avec chiffres/symboles)
- ✓ Accepte les formats: +33 6 12 34 56 78, 06-12-34-56-78, etc.

### Service
- ✓ Requis
- ✓ Doit être dans la liste des services disponibles
- ✓ Services: Coiffure, Manucure, Massage, Soins du visage

## 🎨 Personnalisation

### Ajouter/modifier les services

Dans `app.py`, ligne 10:
```python
SERVICES_DISPONIBLES = ['Coiffure', 'Manucure', 'Massage', 'Soins du visage']
```

### Modifier les couleurs

Dans `templates/index.html` et `templates/admin.html`, section `<style>`:
```css
/* Couleur primaire: gradient violet */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

## 🐛 Dépannage

### Erreur "Aucun module nommé 'flask'"
```bash
pip install -r requirements.txt
```

### Port 5000 déjà utilisé
```python
# Dans app.py, dernière ligne, remplacez par:
app.run(debug=True, port=8000)
```

### Base de données corrompue
```bash
# Supprimer et régénérer
rm demandes.db
python app.py
```

## 🚀 Déploiement

### Sur Heroku

```bash
# Créer un Procfile
echo "web: python app.py" > Procfile

# Créer un runtime.txt
echo "python-3.11.4" > runtime.txt

# Déployer
git push heroku main
```

### Sur PythonAnywhere

1. Créer un compte sur pythonanywhere.com
2. Uploader les fichiers
3. Créer une "Web app" avec Flask
4. Pointer vers `app.app` et `app.py`

## 📝 Notes de développement

- **Validation**: Les données sont validées à la fois côté client (JavaScript) et serveur (Python)
- **Sécurité**: Les données sont nettoyées (`.strip()`) et validées
- **Persistance**: SQLite permet la persistance sans serveur externe
- **API REST**: Réponses JSON standardisées pour faciliter l'intégration

## 🤝 Contribution

Des améliorations possibles:
- [ ] Authentification admin
- [ ] Envoi d'emails/SMS
- [ ] Intégration calendrier
- [ ] Système de paiement
- [ ] Multi-langue

## 📄 Licence

Ce projet est fourni à titre d'exemple éducatif.

---

**Créé avec ❤️ par votre mentor**

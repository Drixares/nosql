# Projet NoSQL - MongoDB Database Management

Ce projet implémente une classe Python complète pour gérer les opérations CRUD avec MongoDB Atlas en utilisant PyMongo et les pipelines d'agrégation.

## Configuration requise

- Python 3.8+
- MongoDB Atlas (cluster configuré)
- PyMongo
- Données d'exemple activées sur le cluster

## Installation

```bash
pip install pymongo
```

## Tester le projet

```bash
source venv/bin/activate
python project_2/seeder.py                                 
```

## Structure du projet

```
project_2/
├── database.py          # Classe principale Database
├── seeder.py           # Scripts de peuplement des données
└── README.md
```

## Collections

Le projet utilise trois collections principales :

- **Users** : `{ pid, name, email, role, created_at, updated_at, created_by }`
- **Teams** : `{ pid, name, members[], created_at, updated_at, created_by }`
- **Projects** : `{ pid, name, teams[], tags[], budget, deadline, created_at, updated_at, created_by }`

## Fonctionnalités principales

### ✅ Partie 1 - Connexion MongoDB
- Classe `Database` centralisée
- Connexion sécurisée à MongoDB Atlas
- Utilisation extensive des pipelines d'agrégation

### ✅ Partie 2 - Fonctions CREATE
- `create_item(table, item, created_by=None)`
- `create_items(table, items, created_by=None)`
- Génération automatique : `pid`, `created_at`, `updated_at`

### ✅ Partie 3 - Seeder
- Peuplement automatique des collections
- Données de test cohérentes

### ✅ Partie 4 - Fonctions UPDATE
- `update_items_by_attr(table, attributes, items_data, updated_by=None)`
- `update_items_by_pids(table, pids, items_data, updated_by=None)`
- `update_item_by_attr(table, attributes, item_data, updated_by=None)`
- `update_item_by_pid(table, pid, item_data, updated_by=None)`
- Mise à jour automatique d'`updated_at`

### ✅ Partie 5 - Fonctions GET simples
- `get_item_by_attr(table, attributes, fields=None, pipeline=None)`
- `get_item_by_pid(table, pid, fields=None, pipeline=None)`
- Gestion intelligente des champs retournés

### ✅ Partie 6 - Fonctions DELETE
- `delete_items_by_attr(table, attributes)`
- `delete_items_by_pids(table, pids)`
- `delete_item_by_attr(table, attributes)`
- `delete_item_by_pid(table, pid)`

### ✅ Partie 7 - Fonctions ARRAY
- `array_push_item_by_attr(table, attributes, array, new_item, updated_by=None)`
- `array_push_item_by_pid(table, pid, array, new_item, updated_by=None)`
- `array_pull_item_by_attr(table, attributes, array, item_attr, updated_by=None)`
- `array_pull_item_by_pid(table, pid, array, item_attr, updated_by=None)`

### ✅ Partie 8 - Fonctions GET avancées
- `get_items(table, attributes, fields=None, sort=None, skip=0, limit=None, return_stats=False, pipeline=None)`
- Filtrage, tri, pagination
- Statistiques de pagination
- Support complet des pipelines MongoDB

## Utilisation

```python
from database import Database

# Initialisation
db = Database("mongodb+srv://your-connection-string")

# Créer un utilisateur
user = db.create_item("users", {
    "name": "John Doe",
    "email": "john@example.com",
    "role": "admin"
}, created_by="system")

# Récupérer un utilisateur
user = db.get_item_by_attr("users", {"email": "john@example.com"})

# Mettre à jour
db.update_item_by_pid("users", user["pid"], {"role": "manager"})

# Pagination avancée
results = db.get_items("projects",
    attributes={"tags": "urgent"},
    sort={"deadline": 1},
    limit=10,
    return_stats=True
)
```

## Règles de développement

1. **Aggregate First** : Utiliser les pipelines d'agrégation MongoDB autant que possible
2. **Automatic Fields** : `pid`, `created_at`, `updated_at` générés automatiquement
3. **Audit Trail** : Traçabilité avec `created_by` et `updated_by`
4. **Flexible Fields** : Gestion intelligente des champs retournés
5. **Pipeline Support** : Support complet des pipelines personnalisés

## Architecture

La classe `Database` centralise toutes les opérations et assure :
- Génération automatique des métadonnées
- Validation des paramètres
- Gestion d'erreurs
- Optimisation des requêtes avec agrégation
- Interface cohérente pour toutes les opérations CRUD
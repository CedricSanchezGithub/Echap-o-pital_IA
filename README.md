# Module IA – Générateur d’histoire procédural

## Description :
Ce module est un microservice Flask simulant un générateur narratif adaptatif.
Il reçoit les paramètres de contexte d’une partie (symptôme, salle, état du joueur) et retourne un texte narratif dynamique.
Le service conserve un petit état global (state.json) pour simuler un apprentissage léger au fil des appels.

## Installation
1. Créer un environnement Python

python -m venv venv
source venv/bin/activate   # ou venv\Scripts\activate sous Windows

2. Installer les dépendances

pip install -r requirements.txt

3. Lancer le serveur

python app.py

Le service démarre sur : http://localhost:5000/generate

### Appel d’exemple : 

curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"symptome": "toux de sang", "salle": "salle des urgences", "etat": "faible"}'

### ou sous Windows :

curl -Uri "http://localhost:5000/generate" `
     -Method POST `
     -Headers @{ "Content-Type" = "application/json" } `
     -Body '{"symptome": "toux de sang", "salle": "salle des urgences", "etat": "faible"}'

# Intégration avec le backend Java

Les fichiers dans le dossier /integration/ sont à copier dans le projet Spring Boot :

StoryRequest.java
StoryGeneratorService.java
StoryController.java

L’appel se fait via : POST /api/story/generate

## Communication

| Élément     | Port | Description             |
| ----------- | ---- | ----------------------- |
| Flask API   | 5000 | Génération narrative IA |
| Spring Boot | 8080 | Backend principal       |
| Next.js     | 3000 | Interface joueur        |

## Exemple d’enchaînement complet

1. Le joueur fait une action → Next.js appelle POST /api/story/generate.
2. Spring Boot relaie la requête vers http://localhost:5000/generate.
3. Flask renvoie un texte narratif.
4. Le backend transmet le texte au front pour affichage.

## Remarques techniques

Le module ne stocke aucune donnée personnelle.
Le fichier state.json simule un apprentissage local.
Aucune dépendance externe (pas d’API GPT, pas de connexion Internet requise).
Peut être hébergé sur le même poste que le backend ou en microservice indépendant.# Echap-o-pital_IA
# Echap-o-pital_IA

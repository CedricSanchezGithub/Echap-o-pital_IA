from flask import Flask, request, jsonify
from story_engine import generate_story

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    symptome = data.get("symptome", "")
    salle = data.get("salle", "")
    etat = data.get("etat", "")
    
    texte = generate_story(symptome, salle, etat)
    return jsonify({"texte": texte})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

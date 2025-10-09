import random
import json
import os

STATE_FILE = "state.json"


def load_state():
    if not os.path.exists(STATE_FILE):
        return {"fatigue": 0.0, "stress": 0.0, "confiance_medecin": 0.5, "medecins_rencontres": []}
    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def update_state(state, symptome, etat, medecin):
    if symptome in ["toux de sang", "douleur poitrine"]:
        state["fatigue"] = min(1.0, state["fatigue"] + 0.2)
        state["stress"] = min(1.0, state["stress"] + 0.1)
    else:
        state["stress"] = min(1.0, state["stress"] + 0.05)

    if etat == "faible":
        state["confiance_medecin"] = max(0.0, state["confiance_medecin"] - 0.1)
    elif etat == "stable":
        state["confiance_medecin"] = min(1.0, state["confiance_medecin"] + 0.05)

    if medecin not in state.get("medecins_rencontres", []):
        state.setdefault("medecins_rencontres", []).append(medecin)

    return state


def generate_story(symptome, salle, etat):
    state = load_state()

    medecins = ["Dr. Lenoir", "Dr. Moreau", "Dr. Mabuse", "Dr. Giggles"]
    medecin = random.choice(medecins)

    state = update_state(state, symptome, etat, medecin)

    # Dictionnaires pour la génération de texte
    attitudes = ["vous sourit d’un air étrange", "vous fixe sans ciller",
                 "murmure des termes techniques incompréhensibles", "semble cacher sa nervosité"]
    ambiances = ["la lumière blafarde des néons", "l’odeur âcre du désinfectant",
                 "le cliquetis d’un instrument métallique", "le silence pesant de la pièce"]

    # Construction du dialogue principal
    intro = f"Dans {salle}, le {medecin} {random.choice(attitudes)} sous {random.choice(ambiances)}."

    # Génération des choix en fonction de l'état du joueur
    choix = []
    if state["stress"] > 0.5:
        choix.append({"id": "fuir", "texte": "Tenter de fuir la salle en courant."})

    if state["confiance_medecin"] > 0.4:
        choix.append({"id": "cooperer", "texte": f"Expliquer vos symptômes au {medecin}."})
    else:
        choix.append({"id": "mentir", "texte": "Minimiser vos symptômes pour ne pas éveiller les soupçons."})

    choix.append({"id": "observer", "texte": "Observer attentivement la salle à la recherche d'un indice."})

    # Assurer qu'il y a toujours 3 choix pour la cohérence de l'UI
    while len(choix) < 3:
        options_supplementaires = [
            {"id": "questionner", "texte": f"Questionner le {medecin} sur l'hôpital."},
            {"id": "distraire", "texte": "Créer une diversion."}
        ]
        choix_disponibles = [c for c in options_supplementaires if c['id'] not in [ch['id'] for ch in choix]]
        if choix_disponibles:
            choix.append(random.choice(choix_disponibles))
        else:
            break  # Evite une boucle infinie

    random.shuffle(choix)  # Mélange les choix pour plus de variété

    save_state(state)

    return {
        "dialogue": intro,
        "choix": choix[:3]  # On renvoie toujours 3 choix
    }
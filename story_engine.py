import random
import json
import os

STATE_FILE = "state.json"

def load_state():
    if not os.path.exists(STATE_FILE):
        return {"fatigue": 0.0, "stress": 0.0, "confiance_medecin": 0.5}
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def update_state(state, symptome, etat):     # Évolution basique du joueur selon ses symptômes
    if symptome in ["toux de sang", "douleur poitrine"]:
        state["fatigue"] = min(1.0, state["fatigue"] + 0.2)
        state["stress"] = min(1.0, state["stress"] + 0.1)
    elif symptome == "fièvre":
        state["fatigue"] = min(1.0, state["fatigue"] + 0.1)
    else:
        state["stress"] = min(1.0, state["stress"] + 0.05)

    if etat == "faible":
        state["confiance_medecin"] = max(0.0, state["confiance_medecin"] - 0.1)
    elif etat == "stable":
        state["confiance_medecin"] = min(1.0, state["confiance_medecin"] + 0.05)

    return state

def generate_story(symptome, salle, etat):
    state = load_state()
    state = update_state(state, symptome, etat)

    medecins = ["Dr. Jekyll", "Dr. House", "Dr. Mundo", "Dr. Pepper"]
    attitudes = ["sourit d’un air étrange", "te fixe sans ciller", "murmure quelque chose que tu ne comprends pas", "semble cacher quelque chose"]
    ambiances = ["la lumière blafarde des néons", "l’odeur âcre du désinfectant", "le cliquetis d’un instrument métallique", "le silence pesant du couloir"]
    sensations = ["un frisson te parcourt l’échine", "ta vision se trouble", "tu sens ton cœur battre plus vite", "une migraine te déchire le crâne"]

    medecin = random.choice(medecins)
    attitude = random.choice(attitudes)
    ambiance = random.choice(ambiances)
    sensation = random.choice(sensations)

    symptome_lignes = {
        "toux de sang": "Tu craches un peu de sang sur ta manche, le goût métallique te serre la gorge.",
        "douleur poitrine": "Une douleur sourde te traverse la poitrine, comme un étau invisible.",
        "peau démange": "Ta peau brûle et te démange, comme si quelque chose bougeait dessous.",
        "fièvre": "La fièvre brouille ta vision, tout semble danser autour de toi."
    }
    intro = symptome_lignes.get(symptome, "Tu sens que quelque chose ne va pas, ton corps réagit étrangement.")

    # Indices dynamiques selon confiance et stress
    indices_possibles = []
    if state["confiance_medecin"] < 0.4:
        indices_possibles.append("Un instant, tu crois voir un badge d’un autre hôpital sur sa blouse.")
    if state["stress"] > 0.6:
        indices_possibles.append("Le bourdonnement dans tes oreilles couvre presque sa voix.")
    if state["fatigue"] > 0.7:
        indices_possibles.append("Tu n’es plus sûr de ce qui est réel ou non.")
    if not indices_possibles:
        indices_possibles.append("Tout semble normal, mais quelque chose te met mal à l’aise.")

    indice = random.choice(indices_possibles)

    corps = f"Dans {salle}, {medecin} {attitude} sous {ambiance}. {sensation}. {indice}"

    if etat == "faible":
        fin = "Tu sens tes forces t’abandonner, mais ta méfiance t’empêche d’abandonner."
    elif etat == "stable":
        fin = "Tu reprends ton souffle, le médecin te dit que tout ira bien. Tu n’en es pas si sûr."
    else:
        fin = "Ton esprit s’éclaircit, mais quelque chose t’empêche encore de partir."

    save_state(state)
    return f"{intro} {corps} {fin}"

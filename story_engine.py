import random
import json
import os
import logging

STATE_FILE = "state.json"
logger = logging.getLogger(__name__)


def load_state():
    if not os.path.exists(STATE_FILE):
        default_state = {"fatigue": 0.0, "stress": 0.0, "confiance_medecin": 0.5, "medecins_rencontres": []}
        logger.info("Aucun état trouvé, utilisation de l'état par défaut")
        return default_state
    with open(STATE_FILE, "r") as f:
        state = json.load(f)
        logger.debug("État chargé", extra={"state": state})
        return state


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)
    logger.debug("État sauvegardé", extra={"state": state})


def update_state(state, symptome, etat, medecin):
    before = {"fatigue": state.get("fatigue"), "stress": state.get("stress"), "confiance_medecin": state.get("confiance_medecin")}

    if symptome in ["toux de sang", "douleur poitrine"]:
        state["fatigue"] = min(1.0, state["fatigue"] + 0.2)
        state["stress"] = min(1.0, state["stress"] + 0.1)
        logger.debug("Symptôme critique détecté, augmentation fatigue/stress", extra={"symptome": symptome})
    else:
        state["stress"] = min(1.0, state["stress"] + 0.05)
        logger.debug("Symptôme non critique, légère augmentation du stress", extra={"symptome": symptome})

    if etat == "faible":
        state["confiance_medecin"] = max(0.0, state["confiance_medecin"] - 0.1)
    elif etat == "stable":
        state["confiance_medecin"] = min(1.0, state["confiance_medecin"] + 0.05)

    after = {"fatigue": state.get("fatigue"), "stress": state.get("stress"), "confiance_medecin": state.get("confiance_medecin")}
    logger.info("Mise à jour de l'état", extra={"avant": before, "apres": after, "medecin": medecin, "etat": etat})

    if medecin not in state.get("medecins_rencontres", []):
        state.setdefault("medecins_rencontres", []).append(medecin)
        logger.debug("Ajout d'un nouveau médecin rencontré", extra={"medecin": medecin})

    return state


def generate_story(symptome, salle, etat):
    logger.info("Génération d'histoire demandée", extra={"symptome": symptome, "salle": salle, "etat": etat})

    state = load_state()

    medecins = ["Dr. Lenoir", "Dr. Moreau", "Dr. Mabuse", "Dr. Giggles"]
    medecin = random.choice(medecins)
    logger.info("Médecin sélectionné", extra={"medecin": medecin})

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
        logger.debug("Choix 'fuir' ajouté (stress élevé)", extra={"stress": state["stress"]})

    if state["confiance_medecin"] > 0.4:
        choix.append({"id": "cooperer", "texte": f"Expliquer vos symptômes au {medecin}."})
        logger.debug("Choix 'cooperer' ajouté (confiance suffisante)", extra={"confiance_medecin": state["confiance_medecin"]})
    else:
        choix.append({"id": "mentir", "texte": "Minimiser vos symptômes pour ne pas éveiller les soupçons."})
        logger.debug("Choix 'mentir' ajouté (confiance faible)", extra={"confiance_medecin": state["confiance_medecin"]})

    choix.append({"id": "observer", "texte": "Observer attentivement la salle à la recherche d'un indice."})

    # Assurer qu'il y a toujours 3 choix pour la cohérence de l'UI
    while len(choix) < 3:
        options_supplementaires = [
            {"id": "questionner", "texte": f"Questionner le {medecin} sur l'hôpital."},
            {"id": "distraire", "texte": "Créer une diversion."}
        ]
        choix_disponibles = [c for c in options_supplementaires if c['id'] not in [ch['id'] for ch in choix]]
        if choix_disponibles:
            new_choice = random.choice(choix_disponibles)
            choix.append(new_choice)
            logger.debug("Choix supplémentaire ajouté", extra={"id": new_choice["id"]})
        else:
            break 

    random.shuffle(choix)
    logger.debug("Choix mélangés", extra={"order": [c["id"] for c in choix]})

    save_state(state)

    result = {
        "dialogue": intro,
        "choix": choix[:3]  # On renvoie toujours 3 choix
    }
    logger.info("Histoire générée", extra={"choix_ids": [c["id"] for c in result["choix"]]})
    return result
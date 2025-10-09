import logging
import os
from flask import Flask, request, jsonify
from story_engine import generate_story

app = Flask(__name__)

# Configure logging once at app startup
_LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
if not logging.getLogger().handlers:
    logging.basicConfig(
        level=getattr(logging, _LOG_LEVEL, logging.INFO),
        format='%(asctime)s %(levelname)s [%(name)s] %(message)s'
    )
logger = logging.getLogger(__name__)


@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json() or {}
    # Log minimal, high-value request context
    logger.info("/generate called", extra={
        'symptome': data.get('symptome'),
        'salle': data.get('salle'),
        'etat': data.get('etat')
    })

    symptome = data.get("symptome", "")
    salle = data.get("salle", "")
    etat = data.get("etat", "")

    story_data = generate_story(symptome, salle, etat)

    logger.debug("Story generated with choices", extra={'choice_ids': [c.get('id') for c in story_data.get('choix', [])]})
    return jsonify(story_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
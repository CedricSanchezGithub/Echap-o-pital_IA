import RPi.GPIO as GPIO
import time
import requests

# Configuration des broches GPIO
BUZZER_PIN = 18
CONTACT_PIN = 17
CONTACT_PIN_reset = 4
WEBHOOK_URL = "http://api-echap-o-pital.topconfig-pc.fr/api/maboule/error"  # URL notification contact
WEBHOOK_URL_reset = "http://api-echap-o-pital.topconfig-pc.fr/api/maboule/reset"  # URL reset

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(CONTACT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Entrée contact principal avec pull-up
GPIO.setup(CONTACT_PIN_reset, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Entrée contact reset avec pull-up

def buzzer_on():
    GPIO.output(BUZZER_PIN, GPIO.HIGH)

def buzzer_off():
    GPIO.output(BUZZER_PIN, GPIO.LOW)

def notifier_site():
    data = {'contact': 'touched', 'timestamp': time.time()}
    try:
        response = requests.post(WEBHOOK_URL, json=data, timeout=5)
        if response.status_code == 204:
            print("Notification envoyée avec succès")
        else:
            print(f"Erreur lors de la notification: {response.status_code}")
    except requests.RequestException as e:
        print(f"Erreur de connexion au site: {e}")

def notifier_reset():
    try:
        response = requests.post(WEBHOOK_URL_reset, timeout=5)
        if response.status_code == 204:
            print("Reset envoyé avec succès")
        else:
            print(f"Erreur lors du reset: {response.status_code}")
    except requests.RequestException as e:
        print(f"Erreur de connexion lors du reset: {e}")

try:
    print("Surveillance du contact Docteur Maboul démarrée...")

    contact_etat_prec = False  # Pour la broche principale
    reset_etat_prec = False    # Pour la broche reset

    while True:
        contact = GPIO.input(CONTACT_PIN) == GPIO.LOW
        reset = GPIO.input(CONTACT_PIN_reset) == GPIO.LOW

        if contact:
            buzzer_on()
            if not contact_etat_prec:
                print("Contact détecté sur broche principale !")
                notifier_site()
            contact_etat_prec = True
        else:
            buzzer_off()
            contact_etat_prec = False

        if reset:
            if not reset_etat_prec:
                print("Contact détecté sur broche reset !")
                notifier_reset()
            reset_etat_prec = True
        else:
            reset_etat_prec = False

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Arrêt programme")
finally:
    buzzer_off()
    GPIO.cleanup()
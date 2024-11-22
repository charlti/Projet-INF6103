import socket
import time

def serveur_tcp(serveur_ip, serveur_port):
    try:
        # Création d'un socket TCP
        serveur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Liaison du socket à une adresse IP et un port
        serveur_socket.bind((serveur_ip, serveur_port))
        serveur_socket.listen(5)
        print(f"Serveur en écoute sur {serveur_ip}:{serveur_port}")

        while True:
            # Attente d'une connexion
            client_socket, client_address = serveur_socket.accept()
            print(f"Connexion reçue de {client_address}")

            # Réception des données
            donnees = client_socket.recv(1024).decode('utf-8')
            print(f"Données reçues : {donnees}")

            # Fermeture de la connexion client
            client_socket.close()

    except Exception as e:
        print(f"Erreur du serveur : {e}")

    finally:
        # Fermeture du socket serveur
        serveur_socket.close()

TCP_SERVER_SEND_IP = "0.0.0.0"   # Notre serveur tcp tournera en local
TCP_SERVER_SEND_PORT = "5678"    # On choisit un port 

TCP_SERVER_REC_IP = "0.0.0.0"   # Notre serveur tcp tournera en local
TCP_SERVER_REC_PORT = "1234"    # On choisit un port 

def envoyer_donnees(donnees, serveur_ip=TCP_SERVER_SEND_IP, serveur_port=TCP_SERVER_SEND_PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(TCP_SERVER_SEND_IP, TCP_SERVER_SEND_PORT)
        print(f"Connecté au serveur {serveur_ip}:{serveur_port}")
        s.sendall(donnees.encode("utf-8"))

if __name__ == "__main__":
    # Adresse IP et port du serveur
    SERVEUR_IP = "0.0.0.0"  # Écoute sur toutes les interfaces
    SERVEUR_PORT = 1234     # Port à utiliser pour la connexion
    
    # Démarrer le serveur
    # serveur_tcp(SERVEUR_IP, SERVEUR_PORT)

    while True:
        envoyer_donnees("green")
        time.sleep(10)
        envoyer_donnees("red")
        time.sleep(10)

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
TCP_SERVER_SEND_PORT = 5678    # On choisit un port 

TCP_SERVER_REC_IP = "0.0.0.0"   # Notre serveur tcp tournera en local
TCP_SERVER_REC_PORT = 1234    # On choisit un port 

def envoyer_donnees():
    while True:
        try:
            # Création de la socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                print(f"Tentative de connexion au serveur {TCP_SERVER_SEND_IP}:{TCP_SERVER_SEND_PORT}...")

                # Tentative de connexion au serveur
                s.connect((TCP_SERVER_SEND_IP, TCP_SERVER_SEND_PORT))
                print(f"Connecté au serveur {TCP_SERVER_SEND_IP}:{TCP_SERVER_SEND_PORT}")

                # Envoi de données en continu
                while True:
                    for data in ["green", "red"]:
                        s.sendall(data.encode("utf-8"))
                        print(f"Données envoyées : {data}")
                        time.sleep(10)  # Attendre 10 secondes entre chaque envoi

        except ConnectionRefusedError:
            # Si le serveur n'est pas encore prêt, attendre et réessayer
            print(f"Serveur non disponible, nouvelle tentative dans 5 secondes...")
            time.sleep(5)

        except Exception as e:
            # Gestion d'autres exceptions (exemple : perte de connexion)
            print(f"Erreur dans l'envoi des données : {e}")
            print("Réessai de connexion dans 5 secondes...")
            time.sleep(5)
if __name__ == "__main__":
    while True:
        envoyer_donnees()

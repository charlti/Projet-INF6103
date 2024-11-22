import socket

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

if __name__ == "__main__":
    # Adresse IP et port du serveur
    SERVEUR_IP = "0.0.0.0"  # Écoute sur toutes les interfaces
    SERVEUR_PORT = 1234     # Port à utiliser pour la connexion
    
    # Démarrer le serveur
    serveur_tcp(SERVEUR_IP, SERVEUR_PORT)
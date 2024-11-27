import socket
import time
from pymodbus.client import ModbusTcpClient
import queue
import threading

TCP_SERVER_SEND_IP = "0.0.0.0"   # L'IP du serveur auquel on va envoyer les données
TCP_SERVER_SEND_PORT = 5678    # Port du serveur auquel on envoie les données

TCP_SERVER_REC_IP = "0.0.0.0"   # L'IP de notre serveur d'écoute TCP
TCP_SERVER_REC_PORT = 1234    # Port de notre serveur d'écoute

command_queue = queue.Queue()

def read_coils():
    client = ModbusTcpClient('192.168.1.11', port=502)

    # Établir la connexion avec le PLC
    if client.connect():
        print("READ COILS : Connexion au PLC réussie. \n")
        # Lire les valeurs des coils à partir d'une adresse donnée
        adresse_debut = 0  # Adresse Modbus du premier coil (bobine)
        nombre_coils = 8  # Nombre de coils à lire (lire 10 coils à partir de l'adresse 0)

        lecture_feu = client.read_coils(adresse_debut, nombre_coils)

        if lecture_feu.isError():
            print("Erreur lors de la lecture des coils.")
        else:
            # Récupérer les valeurs des coils
            valeurs_coils = lecture_feu.bits
            print(f"READ COILS : {valeurs_coils}")
            wanted_values = []
            for i in range(len(valeurs_coils)):
                if i%2 != 0:
                    wanted_values.append(valeurs_coils[i])
            print(wanted_values)
            to_send = ''
            for element in wanted_values:
                if element == True:
                    to_send += 'G'
                elif element == False:
                    to_send += 'r'
            print(to_send)
        # Déconnecter le client
        client.close()
        return to_send
    else:
        print("Impossible de se connecter au PLC.")


def write_coils():
    register_values_to_send = []

    while True:
        while command_queue.empty():
            print("Aucune valeur pour le moment, nouvel essai dans 2 secondes...")
            time.sleep(2)
        if not command_queue.empty():
            string_etat = command_queue.get()
        for character in string_etat:
            if character == 'G':
                register_values_to_send.append('True')
            elif character == 'r':
                register_values_to_send.append('False')
        print(f'DONNEES A ENVOYER AU PLC : {register_values_to_send}')

        client = ModbusTcpClient('192.168.1.11', port=502)

        # Établir la connexion avec le PLC
        if client.connect():
            print("Connexion au PLC réussie.")
            count = 0
            for i in range(len(register_values_to_send)):
                if register_values_to_send[i] == 'True':
                    client.write_coil(count, True)
                elif register_values_to_send[i] == 'False':
                    client.write_coil(count, False)
                count += 2
            print("DONNEES ECRITES DANS LES REGISTRES")
            register_values_to_send = []
            # Déconnecter le client
            client.close()

        else:
            print("Impossible de se connecter au PLC.")



def serveur_tcp(serveur_ip=TCP_SERVER_REC_IP, serveur_port=TCP_SERVER_REC_PORT):
    while True:
        try:
            # Création d'un socket TCP
            serveur_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Liaison du socket à une adresse IP et un port
            serveur_socket.bind((serveur_ip, serveur_port))
            serveur_socket.listen(1)
            print(f"Serveur en écoute sur {serveur_ip}:{serveur_port}")

            while True:
                # Attente d'une connexion
                client_socket, client_address = serveur_socket.accept()
                #print(f"Connexion reçue de {client_address}")

                # Réception des données
                data = client_socket.recv(1024).decode('utf-8')
                if data:
                    print(f"Données reçues : {data}")
                    command_queue.put(data)
                 #   print(f"Donnée {data} mise dans la queue")
                else:
                    print("Aucune donnée reçue mais connexion toujours active")
                    time.sleep(2)

        except ConnectionRefusedError:
            print("Serveur non disponible, nouvel essai dans 5 secondes ...")
            time.sleep(5)

        except Exception as e:
            print(f"Erreur du serveur : {e}, nouvel essai dans 5 secondes ...")
            time.sleep(5)
        finally:
            # Fermeture du socket serveur
            serveur_socket.close()
            client_socket.close()


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
                    coils = read_coils()
                    s.sendall(coils.encode("utf-8"))
                    print(f"Données envoyées A TRACI : {coils}")
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
    thread_tcp = threading.Thread(target=serveur_tcp)
    thread_tcp.start()
    thread_write_coils = threading.Thread(target=write_coils)
    thread_write_coils.start()
    while True:
        envoyer_donnees()


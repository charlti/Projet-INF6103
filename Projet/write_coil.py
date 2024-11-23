import time
from pymodbus.client import ModbusTcpClient
import socket
import time
def read_coils():
    client = ModbusTcpClient('0.0.0.0', port=502)

    # Établir la connexion avec le PLC
    if client.connect():
        print("Connexion au PLC réussie.")
        client.write_coil(0, False)
        # Lire les valeurs des coils à partir d'une adresse donnée
        adresse_debut = 0  # Adresse Modbus du premier coil (bobine)
        nombre_coils = 8  # Nombre de coils à lire (lire 10 coils à partir de l'adresse 0)
        time.sleep(1)
        lecture_feu = client.read_coils(adresse_debut, nombre_coils)

        if lecture_feu.isError():
            print("Erreur lors de la lecture des coils.")
        else:
            # Récupérer les valeurs des coils
            valeurs_coils = lecture_feu.bits
            print(valeurs_coils)
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

    else:
        print("Impossible de se connecter au PLC.")


if __name__ == "__main__":
    read_coils()

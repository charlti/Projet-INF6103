import time
from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient('0.0.0.0', port=502)

# Établir la connexion avec le PLC
if client.connect():
    print("Connexion au PLC réussie.")
    client.write_coil(0,True)
    # Lire les valeurs des coils à partir d'une adresse donnée
    adresse_debut = 0  # Adresse Modbus du premier coil (bobine)
    nombre_coils = 9  # Nombre de coils à lire (lire 10 coils à partir de l'adresse 0)
    
    lecture = client.read_coils(adresse_debut, nombre_coils)
    
    if lecture.isError():
        print("Erreur lors de la lecture des coils.")
    else:
        # Récupérer les valeurs des coils
        valeurs_coils = lecture.bits
        for i, valeur in enumerate(valeurs_coils, start=adresse_debut + 1):
            print(f"Coil {i}: {'ON' if valeur else 'OFF'}")

    # Déconnecter le client
    client.close()
else:
    print("Impossible de se connecter au PLC.")

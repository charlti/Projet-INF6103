import socket,os, sys
from sumo import runner 
from pymodbus.client import ModbusTcpClient
from _thread import *
import threading


plc1 = "192.168.1.11"
plc2 = "192.168.1.12"
plc3 = "192.168.1.13"
plc4 = "192.168.1.14"

def tlsToPLC(state):
    return state == "G"

def PLCTotls(state):
    if(state): 
        return "G"
    else:
        return "r"
    
def createClient(address, id):
            
    client = ModbusTcpClient(address, port=502)

    # Établir la connexion avec le PLC
    if client.connect():
        print("Connexion au PLC réussie.")
        start_new_thread(threaded, (client, id))

def threaded(client, id):
    client.write_coil(0,tlsToPLC(runner.state()[id]))
        # Lire les valeurs des coils à partir d'une adresse donnée
    adresse_debut = 0  # Adresse Modbus du premier coil (bobine)
    nombre_coils = 9  # Nombre de coils à lire (lire 10 coils à partir de l'adresse 0)
    
    runner.changeState(PLCTotls(client.read_coils(adresse_debut, nombre_coils)), id) 


# main entry point
if __name__ == "__main__":
    createClient(plc1, 1)
    createClient(plc2, 2)
    createClient(plc3, 3)
    createClient(plc4, 4)
   
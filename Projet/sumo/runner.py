#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import random
import socket
import threading
import queue
import time
state = []

# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # noqa
import traci  # noqa

TCP_SERVER_SEND_IP = "0.0.0.0"   # Notre serveur tcp tournera en local
TCP_SERVER_SEND_PORT = 1234    # On choisit un port 

TCP_SERVER_REC_IP = "0.0.0.0"   # Notre serveur tcp tournera en local
TCP_SERVER_REC_PORT = 5678    # On choisit un port 

command_queue = queue.Queue()

def envoyer_donnees(donnees, serveur_ip=TCP_SERVER_SEND_IP, serveur_port=TCP_SERVER_SEND_PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((TCP_SERVER_SEND_IP, TCP_SERVER_SEND_PORT))
        print(f"Connecté au serveur {serveur_ip}:{serveur_port}")
        s.sendall(donnees.encode("utf-8"))


def serveur_tcp():
    """Fonction pour gérer la connexion TCP et écouter en permanence"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((TCP_SERVER_REC_IP, TCP_SERVER_REC_PORT))
    server_socket.listen(1)
    print(f"Serveur TCP en écoute sur {TCP_SERVER_REC_IP}:{TCP_SERVER_REC_PORT}")

    client_socket, client_address = server_socket.accept()
    print(f"Connexion établie avec {client_address}")

    try:
        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if data:  # Traiter uniquement les données reçues
                    print(f"Commande reçue : {data}")

                    # Ajouter la commande dans la queue
                    #command_queue.put(data)
                else:
                    print("Aucune donnée reçue, mais connexion toujours active")
                    time.sleep(2)
            except socket.timeout:
                print("Timeout expiré, mais la connexion reste ouverte")
    except Exception as e:
        print(f"Erreur dans la communication TCP : {e}")
    finally:
        print("Fermeture de la connexion")
        client_socket.close()
        server_socket.close()

def generate_routefile():
    random.seed(42)  # make tests reproducible
    N = 3600  # number of time steps
    # demand per second from different directions
    pWE = 1. / 10
    pEW = 1. / 11
    pNS = 1. / 10
    pSN = 1. / 10
    with open("data/cross.rou.xml", "w") as routes:
        print("""<routes>
        <vType id="typeWE" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="16.67" \
guiShape="passenger"/>
        <vType id="typeNS" accel="0.8" decel="4.5" sigma="0.5" length="7" minGap="3" maxSpeed="25" guiShape="bus"/>

        <route id="right" edges="51o 1i 2o 52i" />
        <route id="left" edges="52o 2i 1o 51i" />
        <route id="down" edges="54o 4i 3o 53i" />
        <route id="up" edges="53o 3i 4o 54i
        " />""", file=routes)
        vehNr = 0
        for i in range(N):
            if random.uniform(0, 1) < pWE:
                print('    <vehicle id="right_%i" type="typeWE" route="right" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pEW:
                print('    <vehicle id="left_%i" type="typeWE" route="left" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pNS:
                print('    <vehicle id="down_%i" type="typeNS" route="down" depart="%i" color="1,0,0"/>' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pSN:
                print('    <vehicle id="up_%i" type="typeNS" route="up" depart="%i" color="1,0,0"/>' % (
                    vehNr, i), file=routes)
                vehNr += 1
        print("</routes>", file=routes)

GREEN_DURATION = 30
RED_DURATION = 30

def run():
    """execute the TraCI control loop"""
    step = 0
    thread_tcp = threading.Thread(target=serveur_tcp)
    thread_tcp.start()

    while traci.simulation.getMinExpectedNumber() > 0:

        traci.trafficlight.setProgram("0", "off")
        for vehicle_id in traci.vehicle.getIDList():
            traci.vehicle.setMinGap(vehicle_id, 0.1)
            traci.vehicle.setTau(vehicle_id, 0.5)

        # Détecter les collisions
        collisions = traci.simulation.getCollidingVehiclesIDList()
   #     if collisions:
    #        print(f"Collisions détectées au pas {step}: {collisions}")
        """
        if step % (GREEN_DURATION + RED_DURATION) < GREEN_DURATION:
            traci.trafficlight.setRedYellowGreenState("0", "GGGG")
        else:
            traci.trafficlight.setRedYellowGreenState("0", "rrrr")
        """
        """
        if not command_queue.empty():
            command = command_queue.get()
            print(f"Commande traitée dans run() : {command}")
            if command == "green":
                traci.trafficlight.setRedYellowGreenState("0", "GGGG")
            elif command == "red":
                traci.trafficlight.setRedYellowGreenState("0", "rrrr")
        """
        traci.simulationStep()
        state = traci.trafficlight.getRedYellowGreenState("0")
#        print(state)
        #envoyer_donnees(state)
        step += 1

    traci.close()
    sys.stdout.flush()

def state():
    return state

def changeState(newState, id):
    state[id] = newState

def toReadableState(state):
    readbleState = ""
    for s in state:
        readbleState += s
    print(readbleState)
    return readbleState

def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options


# this is the main entry point of this script
if __name__ == "__main__":
    options = get_options()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # first, generate the route file for this simulation
    generate_routefile()

    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    traci.start([sumoBinary, "-c", "data/cross.sumocfg",
                             "--tripinfo-output", "tripinfo.xml"])
    
    run()

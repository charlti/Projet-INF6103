#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import random
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
    # we start with phase 2 where EW has green
    # traci.trafficlight.setPhase("0", 2)

    while traci.simulation.getMinExpectedNumber() > 0:

        traci.trafficlight.setProgram("0", "off")
        for vehicle_id in traci.vehicle.getIDList():
            traci.vehicle.setMinGap(vehicle_id, 0.1)
            traci.vehicle.setTau(vehicle_id, 0.5)

        # Détecter les collisions
        collisions = traci.simulation.getCollidingVehiclesIDList()
        if collisions:
            print(f"Collisions détectées au pas {step}: {collisions}")
        if step % (GREEN_DURATION + RED_DURATION) < GREEN_DURATION:
            traci.trafficlight.setRedYellowGreenState("0", "GGGG")
        else:
            traci.trafficlight.setRedYellowGreenState("0", "rrrr")
        traci.simulationStep()
        state = traci.trafficlight.getRedYellowGreenState("0")
        print(state)
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

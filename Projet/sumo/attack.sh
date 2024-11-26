#!/bin/bash

# Adresse IP du périphérique Modbus
IP="192.168.1.11"

# Liste des registres à cibler
REGISTERS=(1 3 5 7)

# Boucle infinie
while true; do
  for REGISTER in "${REGISTERS[@]}"; do
    # Exécuter la commande mbpoll
    mbpoll -0 -r "$REGISTER" -t 0 "$IP" 1
  done
done

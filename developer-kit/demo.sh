#!/bin/bash

##################################################
# Configurations
##################################################
CONFIG='config/config.json'

printf "=============================\n"
printf "Welcome to the Developer Kit!\n"
printf "=============================\n\n"

##################################################
# Create the QOD Session
##################################################
printf "\nCreating a QOD Session with %s...\n" $CONFIG
SESSION_ID=$(curl -s -d @"${CONFIG}" -H 'Content-Type: application/json' -X POST 'http://127.0.0.1/connectivity' | jq -r '.id')
printf "Created a QOD Session with id = %s\n" "$SESSION_ID"
while true; do
    read -p "Press Enter to continue" yn
    case $yn in
        * ) break;;
    esac
done

##################################################
# Get the QOD Session
##################################################
printf "\nRetrieving the QOD Session with session id = %s...\n" $SESSION_ID
RESP=$(curl -s -X GET 'http://127.0.0.1/connectivity/'"${SESSION_ID}"'')
printf "%s\n" "$RESP"
while true; do
    read -p "Press Enter to continue" yn
    case $yn in
        * ) break;;
    esac
done

##################################################
# Get the QOD Session after it has been deleted
##################################################
printf "\nDeleting the QOD Session with session id = %s...\n" $SESSION_ID
RESP=$(curl -s -X DELETE 'http://127.0.0.1/connectivity/'"${SESSION_ID}"'')
printf "%s\n" "$RESP"
while true; do
    read -p "Press Enter to continue" yn
    case $yn in
        * ) break;;
    esac
done

##################################################
# Get the QOD Session after it has been deleted
##################################################
printf "\nRetrieving the QOD Session with session id = %s...\n" $SESSION_ID
RESP=$(curl -s -X GET 'http://127.0.0.1/connectivity/'"${SESSION_ID}"'')
printf "%s\n" "$RESP"
while true; do
    read -p "Press Enter to continue" yn
    case $yn in
        * ) break;;
    esac
done

printf "\n========================\n"
printf "Thank you!\n"
printf "========================\n"

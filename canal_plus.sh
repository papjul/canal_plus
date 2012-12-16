#!/bin/bash
########################################################################
# Nom : Script canal_plus.sh
# Auteur : J. Papasian
#
# Description : Script permettant de télécharger légalement une vidéo 
# des sites Canal Plus (Les Guignols, Le Palmashow, etc)
#
# Pré-requis : wget et rtmpdump
# Licence : GNU GPLv2+
#
# TODO:
# * Pouvoir sélectionner la qualité en paramètre
# * Détecter si HTTP ou RTMP pour télécharger
# * En cas de non-disponibilité de QUALITY demandée, tester les autres
#   possibilités
# * Détection des vidéos inexistantes
# * Afficher le titre de la vidéo qui va être téléchargée
########################################################################

# Vérification des paramètres
if (($# != 1)); then
  echo "Usage : ${0##*/} video_id"
  exit 1
fi

# Configuration
QUALITY="HD" # BAS_DEBIT | HAUT_DEBIT | HD
DIRECTORY=$HOME"/Téléchargements"

# On télécharge le fichier XML
XML_FILE="http://service.canal-plus.com/video/rest/getvideos/cplus/$1"
XML=$(wget -O - $XML_FILE)

# On sélectionne la qualité demandée
DL_LINK=$(echo $XML | sed -e 's/.*<'$QUALITY'>\(.*\)<\/'$QUALITY'>.*/\1/')

# Si pas de résultat, on se rabat sur autre chose
if [ -z $DL_LINK ]; then
    DL_LINK=$(echo $XML | sed -e 's/.*<HAUT_DEBIT>\(.*\)<\/HAUT_DEBIT>.*/\1/')
fi

# Le nom sous lequel on va enregistrer le fichier
FILENAME=$(echo $DL_LINK | sed -e 's/.*\/\(.*\)$/\1/')

# On télécharge !
rtmpdump -r $DL_LINK -o $DIRECTORY/$FILENAME
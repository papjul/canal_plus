#!/usr/bin/python3
########################################################################
# Nom : Script canal_plus.py
# Auteur : J. Papasian
#
# Description : Script permettant de télécharger la quotidienne des
# Guignols et du Petit Journal sur Canal Plus
#
# Pré-requis : python3, youtube-dl
# Changer la localisation du projet /home/UTILISATEUR/scripts/
# Licence : Beerware
#
# Destiné à être exécuté par une tâche cron. Exemple :
# 0 0,1,2,8,14,20,21,22,23 * * 1,2,3,4,5,6 /home/UTILISATEUR/scripts/
# canal_plus.py
#
# TODO:
# * Créer canal_plus.cfg si inexistant
# * Enregistrer dans ~/Downloads (si compatible avec crontab)
# * Mettre l'émission en paramètre du programme 'guignols', 
#   'le_petit_journal'.Si non précisé, donnez la liste
# * Gestion des erreurs (échecs de téléchargement, émission inexistante
#   (pas d'XML associé))
# * Adaptez pour d’autres émissions
########################################################################

import xml.etree.ElementTree as ET
import urllib.request,subprocess,pickle

# Récupère la configuration
def getConfig():
    fr = open('/home/UTILISATEUR/scripts/canal_plus.cfg', 'rb')

    try:
        emissions = pickle.load(fr)
    except:
        emissions = {}

    fr.close()

    return emissions

# Met à jour la dernière vidéo téléchargée d’une émission
def setConfig(emission, vid):
    emissions = getConfig()
    emissions[emission] = vid

    fw = open('/home/UTILISATEUR/scripts/canal_plus.cfg', 'wb')
    pickle.dump(emissions, fw)
    fw.close()

# Retourne la dernière vidéo téléchargée d’une émission
def getLastVid(emission):
    emissions = getConfig()
    if emission in emissions:
        return emissions[emission]
    else:
        return 0

# Retourne l’array des nouvelles vidéos d’une émission, s’il y en a
def getXML(emission, lastVid):
    url = 'http://service.canal-plus.com/video/rest/listeVideos/cplus/'+emission
    source = urllib.request.urlopen(url)
    root = ET.fromstring(source.read())
    newVideos = []

    for child in root:
        if child.find('CATEGORIE').text == 'QUOTIDIEN' and int(child.get('ID')) > lastVid:
            newVideos.append(int(child.get('ID')))

    return newVideos

# Télécharge une vidéo à partir d’un ID
def download(vid):
    return subprocess.call(["youtube-dl", "-q", "http://player.canalplus.fr/#/"+str(vid)])

# Exécute le programme
def execute(emission):
    lastVid = getLastVid(emission)
    newVideos = getXML(emission, lastVid)

    if lastVid == 0: # Si pas de configuration, téléchargement de la dernière émission seulement
        download(newVideos[0])
        setConfig(emission, newVideos[0])
    elif newVideos:
        for key in reversed(range(len(newVideos))):
            download(newVideos[key])
        setConfig(emission, newVideos[0])

# Exécution
execute('guignols');
execute('le_petit_journal');
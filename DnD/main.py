import os
import re
import json

def lister_routers(repertoire_projet):

    repertoire_courant =  repertoire_projet + "\\project-files\\dynamips"    

    routers_list = {}

    if os.path.exists(repertoire_courant):
        dossiers = [repertoire_courant+"\\"+nom for nom in os.listdir(repertoire_courant) if os.path.isdir(os.path.join(repertoire_courant, nom))]
        for router in dossiers :
            chemin = router + "\\configs"
            config_file=""
            for nom_fichier in os.listdir(chemin) :
                if nom_fichier.endswith(".cfg") and 'startup' in nom_fichier:
                    config_file = chemin + "\\" + nom_fichier

            with open(config_file, 'r') as config :
                config_content = config.read()
                hostname_pattern = r'hostname\s+(\w+)'
                hostname_match = re.search(hostname_pattern,config_content)

                if hostname_match :
                    routers_list[hostname_match.group(1)] = config_file
                else : 
                    print(f"Hostname non trouvé dans le fichier de config :{router}")
    
    return routers_list
        
    

repertoire_projet = 'C:\\Users\\Gauthier\\Desktop\\TC\\TC3\\PROJETS\\projet_GNS3\\GNS3_project1'  

dossiers = lister_routers(repertoire_projet)

chemin_data = os.path.join(os.path.dirname(__file__),'..','data','data.json')

with open(chemin_data,"r") as data :
    intentions = json.load(data)

def constante(router) :
    
    return "!\n!\n!\n!\n!\n!\n!\n!\n\n!\n! Last configuration change at 14:16:26 UTC Wed Dec 20 2023\n!\nversion 15.2\nservice timestamps debug datetime msec\nservice timestamps log datetime msec\n!\nhostname "+router+"\n!\nboot-start-marker\nboot-end-marker\n!\n!\n!\nno aaa new-model\nno ip icmp rate-limit unreachable\nip cef\n!\n!\n!\n!\n!\n!\nno ip domain lookup\nipv6 unicast-routing\nipv6 cef\n!\n!\nmultilink bundle-name authenticated\n!\n!\n!\n!\n!\n!\n!\n!\n!\nip tcp synwait-time 5\n! \n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!"

def adressage(data):
    for AS in data["AS"]:
        adresse=data["AS"][AS]["plage_IP"]["interfaces_physique"]
        nombre_liens=len(data["AS"][AS]["liens"])
    
    


        # Séparer les éléments en fonction des ":"
        elements = adresse.split(':')

        # Remplacer "/64" par une chaîne vide
        elements[-1] = elements[-1].replace('/64', '')

        # Convertir les éléments en entiers
        elements = [int(e, 16) if e else 0 for e in elements]

        # Si le nombre d'éléments est inférieur à 4, remplir avec des 0
        while len(elements) < 4:
            elements.append(0)

        resultats = []

        # Créer une plage d'adresses pour chaque lien
        for i in range(nombre_liens):
            adresse_lien = elements.copy()  # Créer une copie pour chaque itération
            adresse_lien[-1] += i  # Incrémenter le dernier élément pour chaque lien
            adresse_lien_str = ':'.join([hex(e)[2:] for e in adresse_lien]) + '::/64'

            data["AS"][AS]["liens"][i].append(adresse_lien_str)

        

adressage(intentions)
print(intentions)
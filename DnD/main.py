import os
import re
import json
import ipaddress

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



def constante(router):
    config = "!\n!\n!\n!\n!\n!\n!\n!\n\n!\n! Last configuration change at 14:16:26 UTC Wed Dec 20 2023\n!\nversion 15.2\nservice timestamps debug datetime msec\nservice timestamps log datetime msec\n!\nhostname " + router + "\n!\nboot-start-marker\nboot-end-marker\n!\n!\n!\nno aaa new-model\nno ip icmp rate-limit unreachable\nip cef\n!\n!\n!\n!\n!\n!\nno ip domain lookup\nipv6 unicast-routing\nipv6 cef\n!\n!\nmultilink bundle-name authenticated\n!\n!\n!\n!\n!\n!\n!\n!\n!\nip tcp synwait-time 5\n! \n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!"

    # Obtenir le chemin complet du fichier dans le dossier config_files
    dossier_config = os.path.join(os.path.dirname(__file__), "config_files")
    filename = os.path.join(dossier_config, router + ".cfg")

    # Écrire la configuration dans le fichier spécifié
    with open(filename, 'w') as fichier:
        fichier.write(config)

# Exemple d'utilisation
#constante("R1")



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


        # Créer une plage d'adresses pour chaque lien
        for i in range(nombre_liens):
            adresse_lien = elements.copy()  # Créer une copie pour chaque itération
            adresse_lien[-1] += i  # Incrémenter le dernier élément pour chaque lien
            adresse_lien_str = ':'.join([hex(e)[2:] for e in adresse_lien]) + '::/64'
            

            data["AS"][AS]["liens"][i].append(adresse_lien_str)
            
            for j in range(2) :

                data["AS"][AS]["liens"][i][j][1] = "GigabitEthernet" + data["AS"][AS]["liens"][i][j][1][1:]
            
                adresse_routeur_str = ':'.join([hex(e)[2:] for e in adresse_lien]) + f'::{j+1}/64'
                    
                data["AS"][AS]["liens"][i][j].append(adresse_routeur_str)

        for i in range(len(data["AS"][AS]["liens"])) : 
            for j in range(2) : 

                dico = {"nom":data["AS"][AS]["liens"][i][j][0],data["AS"][AS]["liens"][i][j][1]:data["AS"][AS]["liens"][i][j][2]}
                data["AS"][AS]["liens"][i][j] = dico


        nb_routeurs = len(data["AS"][AS]["routeurs"])

        plage = data["AS"][AS]["plage_IP"]["interfaces_loopback"]

        network = ipaddress.IPv6Network(plage, strict=False)

        # Générer une liste d'adresses IPv6
        adresses_ipv6 = [str(network.network_address + i+1) + '/64' for i in range(nb_routeurs)]

        for i in range(nb_routeurs) :
            data["AS"][AS]["routeurs"][i]["Loopback0"] = adresses_ipv6[i]

def recherche_bordures(data) :

    for AS in data["AS"] :

        new_routeurs = []

        for router in data["AS"][AS]["routeurs"] :

            bordure = False

            for eGP in data["liens_eGP"] :
                for eGP_routeur in eGP :
                    if router == eGP_routeur[0] :
                        new_routeurs.append({"nom":router,"etat":"bordure"})
                        bordure = True
            
            if not bordure :
                new_routeurs.append({"nom":router,"etat":"interne"})
        
        data["AS"][AS]["routeurs"] = new_routeurs

                


def logic(data) :

    recherche_bordures(intentions)
    adressage(intentions)


    for AS in data["AS"] :

        IGP = data["AS"][AS]["IGP"]

        for routeur in data["AS"][AS]["routeurs"] :

            #constante(router)

            for lien in data["AS"][AS]["liens"] :
                for routeur_in_lien in lien :
                    if type(routeur_in_lien) ==  dict :
                    
                        if routeur_in_lien["nom"] == routeur["nom"] :
                            interface = list(routeur_in_lien.keys())[1]
                            print(interface)
                            #inserer fonction de config interface



logic(intentions)
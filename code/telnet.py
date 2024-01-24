import os
import re
import json
import ipaddress
import shutil
from gns3fy import Gns3Connector, Project
from telnetlib import Telnet
from time import sleep


def load_data(intention) :
    chemin_data = os.path.join(os.path.dirname(__file__),'..','data',intention)

    with open(chemin_data,"r") as data :
        intentions = json.load(data)          

    return intentions


def supprimer_fichiers(dossier):
    repertoire_script = os.path.dirname(__file__)

    # Construire le chemin complet pour le dossier "config_files"
    dossier_a_purger = os.path.join(repertoire_script, "config_files")

    # Liste tous les fichiers dans le dossier
    fichiers_dans_dossier = os.listdir(dossier_a_purger)

    # Construit le chemin complet pour chaque fichier et le supprime
    for fichier in fichiers_dans_dossier:
        chemin_fichier = os.path.join(dossier_a_purger, fichier)

        if os.path.isfile(chemin_fichier):
            os.remove(chemin_fichier)


def lister_routers(repertoire_projet) :
    ##
    #Trouve les fichiers configs de chaques routeurs dans le repertoire_projet
    ##

    repertoire_courant =  repertoire_projet + "\\project-files\\dynamips"    

    routers_list = {}

    if os.path.exists(repertoire_courant):
        #Création d'une liste avec tous les dossiers des routeurs
        dossiers = [repertoire_courant+"\\"+nom for nom in os.listdir(repertoire_courant) if os.path.isdir(os.path.join(repertoire_courant, nom))]

        for router in dossiers :
            #Création du chemin vers le .cfg
            chemin = router + "\\configs"
            config_file=""
            for nom_fichier in os.listdir(chemin) :

                #Recherche du fichier de config au démarrage
                if nom_fichier.endswith(".cfg") and 'startup' in nom_fichier:
                    config_file = chemin + "\\" + nom_fichier

            #Lecture du .cfg pour determiner à quel router il appartient
            with open(config_file, 'r') as config : 
                config_content = config.read()
                hostname_pattern = r'hostname\s+(\w+)'
                hostname_match = re.search(hostname_pattern,config_content)

                if hostname_match :
                    #Création du dictionnaire avec comme clé le nom du routeur et en valeur le chemin absolu vers le .cfg
                    routers_list[hostname_match.group(1)] = config_file
                else : 
                    print(f"Hostname non trouvé dans le fichier de config :{router}")
  
    
    return routers_list
        

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
            adresse_lien[-1] += i+1  # Incrémenter le dernier élément pour chaque lien
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
        adresses_ipv6 = [str(network.network_address + i+1) + '/128' for i in range(nb_routeurs)]

        for i in range(nb_routeurs) :
            data["AS"][AS]["routeurs"][i]["Loopback0"] = adresses_ipv6[i]


def recherche_bordures(data) :
    for eGP in data["liens_eGP"] :
        for eGP_routeur in eGP :
            eGP_routeur[1] = "GigabitEthernet"+eGP_routeur[1][1:]

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






def constante(router):

    config = "!\n!\n!\n!\n!\n!\n!\n!\n\n!\n! Last configuration change at 14:16:26 UTC Wed Dec 20 2023\n!\nversion 15.2\nservice timestamps debug datetime msec\nservice timestamps log datetime msec\n!\nhostname " + router + "\n!\nboot-start-marker\nboot-end-marker\n!\n!\n!\nno aaa new-model\nno ip icmp rate-limit unreachable\nip cef\n!\n!\n!\n!\n!\n!\nno ip domain lookup\nipv6 unicast-routing\nipv6 cef\n!\n!\nmultilink bundle-name authenticated\n!\n!\n!\n!\n!\n!\n!\n!\n!\nip tcp synwait-time 5\n! \n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!"

    commande("conf t", router)
    commande("ipv6 unicast-routing",router)
    commande("end",router)



    # Obtenir le chemin complet du fichier dans le dossier config_files
    filename = os.path.join(os.path.dirname(__file__), "config_files", router + ".cfg")

    # Écrire la configuration dans le fichier spécifié
    with open(filename, 'w') as fichier:
        fichier.write(config)

        
def conf_interface(routeur,interface,IGP,adresse):

    # Créer la configuration d'une interface 

    texte = f"""\ninterface {interface}
 no ip address"""
    if interface!="Loopback0":
        texte+="""\n negotiation auto"""
    texte+=f"""\n ipv6 address {adresse}
 ipv6 enable"""
    if IGP == "RIP":
        texte += "\n ipv6 rip connected enable\n!"
        
    elif IGP =="OSPF":
        texte+=f"\n ipv6 ospf {routeur[1:]} area 0\n!"


    #Envoi des commande avec telnet

    commande("conf t",routeur)
    commande(f"interface {interface}",routeur)
    commande(f"ipv6 enable",routeur)
    commande(f"ipv6 address {adresse}",routeur)

    if IGP == "RIP" :
        commande(f"ipv6 rip connected enable",routeur)
    elif IGP == "OSPF" :
        commande(f"ipv6 ospf {routeur[1:]} area 0",routeur)

    commande("no shutdown",routeur)

    commande("end",routeur)


    # Ouvrir le fichier et ajouter les informations à la fin
    filename = os.path.join(os.path.dirname(__file__), "config_files", routeur + ".cfg")

    with open(filename, 'a') as fichier:
        fichier.write(texte)



def conf_bgp(nom_routeur,AS,loopbacks_voisin,plages,adresses_bordures):

    texte_routeur = f"""\nrouter bgp {AS}
 bgp router-id {nom_routeur[1:]}.{nom_routeur[1:]}.{nom_routeur[1:]}.{nom_routeur[1:]}
 bgp log-neighbor-changes
 no bgp default ipv4-unicast"""
    texte_family=f"""\naddress-family ipv6"""
    for plage in plages :
        texte_family+=f"""\n  network {plage}"""
    
    
        
    for adresse in loopbacks_voisin:
        texte_routeur+=f"""\n neighbor {adresse[:-4]} remote-as {AS}
 neighbor {adresse[:-4]} update-source Loopback0"""
        texte_family+=f"""\n  neighbor {adresse[:-4]} activate"""


    for adresse,num_AS in adresses_bordures:
        texte_routeur+=f"""\n neighbor {adresse[:-3]} remote-as {num_AS}"""
        texte_family+=f"""\n  neighbor {adresse[:-3]} activate"""
    texte_routeur+=f"""\n !
 address-family ipv4
 exit-address-family
 !"""   
        
        
    texte_family+="""\n exit-address-family"""



    commande("conf t",nom_routeur)
    commande(f"router bgp {AS}",nom_routeur)
    commande(f"bgp router-id {nom_routeur[1:]}.{nom_routeur[1:]}.{nom_routeur[1:]}.{nom_routeur[1:]}",nom_routeur)
    commande(f"no bgp default ipv4-unicast",nom_routeur)
    commande(f"address-family ipv6",nom_routeur)
    for plage in plages :
        commande(f"network {plage}",nom_routeur)
    for adresse in loopbacks_voisin:
        commande(f"neighbor {adresse[:-4]} remote-as {AS}",nom_routeur)
        commande(f"neighbor {adresse[:-4]} update-source Loopback0",nom_routeur)
        commande(f"neighbor {adresse[:-4]} activate",nom_routeur)
    for adresse,num_AS in adresses_bordures:
        commande(f"neighbor {adresse[:-3]} remote-as {num_AS}",nom_routeur)
        commande(f"neighbor {adresse[:-3]} activate",nom_routeur)
    commande(f"end",nom_routeur)




    filename = os.path.join(os.path.dirname(__file__), "config_files", nom_routeur + ".cfg")

    # Écrire la configuration dans le fichier spécifié
    with open(filename, 'a') as fichier:
        fichier.write(texte_routeur)
        fichier.write(texte_family)
    
    
def conf_igp(nom,IGP,bordures) :
    texte="""
!
ip forward-protocol nd
!
!
no ip http server
no ip http secure-server
!"""    
    if IGP == "RIP" :

        texte += """
ipv6 router rip connected
 redistribute connected
"""
    else :
        texte += f"""
ipv6 router ospf {nom[1:]}
 router-id {nom[1:]}.{nom[1:]}.{nom[1:]}.{nom[1:]}
 passive-interface Loopback0
"""
        
        for bordure in bordures :
            texte +=f""" passive-interface {bordure}
"""
    texte+="""!
!
!
!
control-plane
!
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line vty 0 4
 login
!
!
end
"""
    if IGP == "RIP" :
        commande("conf t", nom)
        commande("ipv6 router rip connected",nom)
        commande("redistribute connected",nom)

    else :
        commande("conf t", nom)
        commande(f"ipv6 router ospf {nom[1:]}",nom)
        commande(f"router-id {nom[1:]}.{nom[1:]}.{nom[1:]}.{nom[1:]}",nom)
        commande(f"passive-interface Loopback0",nom)

        for bordure in bordures :
            commande(f"passive-interface {bordure}",nom)

    commande("end",nom)





    filename = os.path.join(os.path.dirname(__file__), "config_files", nom + ".cfg")

    # Écrire la configuration dans le fichier spécifié
    with open(filename, 'a') as fichier:
        fichier.write(texte)






def logic(data) :

    supprimer_fichiers("config_files")

    #Mise en place du json complet
    recherche_bordures(intentions)
    adressage(intentions)


    for AS in data["AS"] :

        plages_addresses = []
        for lien in data["AS"][AS]["liens"] :
            plages_addresses.append(lien[2])


        IGP = data["AS"][AS]["IGP"]

        for routeur in data["AS"][AS]["routeurs"] :

            constante(routeur["nom"])
            voisins = []
            addresses_bordures = []
            interfaces_bordures = []
            conf_interface(routeur["nom"],"Loopback0",IGP,routeur["Loopback0"])

            for bordures in data["liens_eGP"] :
                for i in range(2) :
                    if bordures[i][0] == routeur["nom"] :
                        conf_interface(routeur["nom"],bordures[i][1],IGP,bordures[i][2])

                        interfaces_bordures.append(bordures[i][1])    

                        j = (i+1)%2
                        voisin = [bordures[j][2]]
                        for AS_bordure in data["AS"] :
                            for routeur_bordure in data["AS"][AS_bordure]["routeurs"] :
                                if routeur_bordure["nom"] == bordures[j][0] :
                                    voisin.append(AS_bordure[2:])
                        
                        addresses_bordures.append(voisin)

            for lien in data["AS"][AS]["liens"] :
                for routeur_in_lien in lien :
                    if type(routeur_in_lien) ==  dict :
                    
                        if routeur_in_lien["nom"] == routeur["nom"] :

                            interface = list(routeur_in_lien.keys())[1]
                            conf_interface(routeur["nom"],interface,IGP,routeur_in_lien[interface])
                        else : 
                            voisins.append(routeur_in_lien["nom"])
            
            loopback_voisins = []

            for voisin in data["AS"][AS]["routeurs"] :
                if voisin["nom"] in voisins :
                    loopback_voisins.append(voisin["Loopback0"])
           
            
            conf_bgp(routeur["nom"],AS[2:],loopback_voisins,plages_addresses,addresses_bordures)

            conf_igp(routeur["nom"],IGP,interfaces_bordures)







def drag_and_drop(repertoire_projet) :
    dossiers = lister_routers(repertoire_projet)
    for routeur,chemin in dossiers.items() :
        shutil.copy(os.path.join(os.path.dirname(__file__), "config_files",routeur+".cfg"),chemin)

def start_telnet(projet_name) :
    serveur = Gns3Connector("http://localhost:3080")
    projet = Project(projet_name, connector=serveur)
    projet.get()
    projet.open()

    noeuds = {}
    for noeud in projet.nodes :
        noeuds[noeud.name] = Telnet(noeud.console_host,str(noeud.console))

    return noeuds

def commande(cmd,routeur) :

    global noeuds

    noeuds[routeur].write(bytes(cmd+"\r",encoding="ascii"))

    sleep(0.1)





repertoire_projet = "C:\\Users\\baptr\\GNS3\\projects\\GNS3DnDnew"


          
intentions = load_data("3-3.json")

noeuds = start_telnet("untitled")

logic(intentions)

#drag_and_drop(repertoire_projet)







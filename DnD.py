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

chemin_data = os.path.join(os.path.dirname(__file__),'data','data.json')

with open(chemin_data,"r") as data :
    intentions = json.load(data)
print(intentions)



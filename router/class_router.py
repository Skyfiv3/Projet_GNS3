from telnetlib import Telnet

class Router :

    def __init__(self,name,node) :
        self.nom = name
        self.noeud = node
        self.id = node.id
        self.voisin = recherche_voisin(self,node)
        self.console = Telnet(self.noeud.console_host,str(self.noeud.console))
        


    def recherche_voisin(self,node) :
        voisins = []

        for i in node.link :

            for j in i.nodes :
                if j['node_id'] == self.id :
                    port = j['label']['text']
                else :
                    id = j['node_id']

            voisins.append({'id':id,"port":port})
        return voisins
     



        

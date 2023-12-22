from telnetlib import Telnet
from gns3fy import  Node


class Router :

    def __init__(self,node : Node) -> None:
        self.nom = node.name
        self.noeud = node
        self.id = node.node_id
        self.voisins = self.recherche_voisins(node)
        self.console = Telnet(self.noeud.console_host,str(self.noeud.console))
        


    def recherche_voisins(self,node: Node) -> list :
        voisins = []

        for i in node.links :

            for j in i.nodes :
                if j['node_id'] == self.id :
                    port = j['label']['text']
                else :
                    id = j['node_id']

            voisins.append({'id':id,"port":port})
        return voisins
     



        

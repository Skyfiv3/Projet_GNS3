from gns3fy import Gns3Connector, Project, Node

from router.class_router import Router

#from telnetlib import Telnet

server = Gns3Connector("http://localhost:3080")

## PARTIE PROJET

projet = Project(name="GNS3_project1", connector=server)

projet.get()


#print(f"Name: {projet.name} -- Status: {projet.status} -- Is auto_closed?: {projet.auto_close}")

projet.open()

noeuds =  projet.nodes

noeuds[0].get()

R1 = Router(noeuds[0])
R1.envoi_commande("conf t")

print(R1.voisins)



'''
for node in projet.nodes:
    print(f"Node: {node.name} -- Node Type: {node.node_type} -- Status: {node.status}")
'''
    

#print(server.get_version())

#print(server.get_templates())


'''
##PARTIE NODE
Nodes =  projet.nodes
R1 = Nodes[0]
R1.get()
'''




'''
Socket_R1 = Telnet(R1.console_host,str(R1.console)) 
Socket_R1.write(bytes("conf t\r",encoding="ascii"))
'''

'''
def init_consoles(projet):
    noeuds = {}
    for i in projet.nodes :
        noeuds[i.name] = {"noeud":i,"console":Telnet(i.console_host,str(i.console))}
    return noeuds

noeuds=init_consoles(projet)
'''
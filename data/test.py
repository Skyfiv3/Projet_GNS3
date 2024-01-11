import ipaddress

def generer_liste_adresses_ipv6(plage, n):
    # Analyser la plage IPv6
    network = ipaddress.IPv6Network(plage, strict=False)

    # Générer une liste d'adresses IPv6
    adresses_ipv6 = [str(network.network_address + i+1) + '/64' for i in range(n)]

    return adresses_ipv6

# Exemple d'utilisation
plage_interfaces_loopback = "1001::/64"
nombre_elements = 5
liste_adresses = generer_liste_adresses_ipv6(plage_interfaces_loopback, nombre_elements)

# Afficher la liste générée
print(liste_adresses)

import tkinter as tk


def change_AS():
    global selected

    plages_ip[selected] = plage_ip.get()
    plages_lb[selected] = plage_lb.get()
    IGPs[selected] = IGP.get()

    for i in range(len(routeurs[selected])) :
        routeurs[selected][i] = routeurs_entries[i].get()

    

    for i in range(len(liens[selected])) :
        liens[selected][i] = liens_entries[i].get()
        liens2[selected][i] = liens_entries2[i].get()
        interf[selected][i] = interf_entries[i].get()
        interf2[selected][i] = interf_entries2[i].get()
    
    for i in range(len(voisins[selected])) :
        voisins[selected][i] = voisins_entries[i].get()
        voisins_type[selected][i] = voisins_type_entries[i].get()

    for i in range(len(eGP_link[selected])) :
        eGP_link[selected][i] = eGP_link_entries[i].get()
        eGP_link2[selected][i] = eGP_link_entries2[i].get()
        eGP_interf[selected][i] = eGP_interf_entries[i].get()
        eGP_interf2[selected][i] = eGP_interf_entries2[i].get()
        eGP_addr[selected][i] = eGP_addr_entries[i].get()
        eGP_addr2[selected][i] = eGP_addr_entries2[i].get()

    selected = var.get()-1

    IGP.delete(0, tk.END)
    IGP.insert(selected, IGPs[selected])

    plage_ip.delete(0, tk.END)
    plage_ip.insert(selected, plages_ip[selected])

    plage_lb.delete(0, tk.END)
    plage_lb.insert(selected, plages_lb[selected])


    router_diff = len(routeurs_entries) - len(routeurs[selected])
    if router_diff < 0 :
        for _ in range(-router_diff) :
            entry = tk.Entry(router_frame)
            entry.pack(side=tk.LEFT)
            routeurs_entries.append(entry)

    else :
        for _ in range(router_diff) :
            routeurs_entries.pop().destroy()

    voisins_diff = len(voisins_entries) - len(voisins[selected])
    if voisins_diff < 0 :
        for _ in range(-voisins_diff) :
            entry = tk.Entry(neighbor_frame)
            entry.pack(side=tk.LEFT)
            voisins_entries.append(entry)
            
            entry2 = tk.Entry(neighbor_type_frame)
            entry2.pack(side=tk.LEFT)
            voisins_type_entries.append(entry2)
    
    else :
        for _ in range(voisins_diff) :
            voisins_entries.pop().destroy()
            voisins_type_entries.pop().destroy()


    liens_diff = len(liens_entries) - len(liens[selected])
    if liens_diff < 0 :
        for _ in range(-liens_diff) :
            entry = tk.Entry(links_frame)
            entry.pack(side=tk.LEFT)
            liens_entries.append(entry)

            entry2 = tk.Entry(links_frame2)
            entry2.pack(side=tk.LEFT)
            liens_entries2.append(entry2)

            interf_entry = tk.Entry(interf_frame)
            interf_entry.pack(side=tk.LEFT)
            interf_entries.append(interf_entry)

            interf_entry2 = tk.Entry(interf_frame2)
            interf_entry2.pack(side=tk.LEFT)
            interf_entries2.append(interf_entry2)

    elif liens_diff > 0 :
        for _ in range(liens_diff) :
            liens_entries.pop().destroy()
            liens_entries2.pop().destroy()

            interf_entries.pop().destroy()
            interf_entries2.pop().destroy()
    
    eGP_liens_diff = len(eGP_link_entries) - len(eGP_link[selected])
    if eGP_liens_diff < 0 :
        for _ in range(-eGP_liens_diff) :
            entry = tk.Entry(eGP_link_frame)
            entry.pack(side=tk.LEFT)
            eGP_link_entries.append(entry)

            entry2 = tk.Entry(eGP2_link_frame)
            entry2.pack(side=tk.LEFT)
            eGP_link_entries2.append(entry2)

            interf_entry = tk.Entry(eGP_interf_frame)
            interf_entry.pack(side=tk.LEFT)
            eGP_interf_entries.append(interf_entry)

            interf_entry2 = tk.Entry(eGP2_interf_frame)
            interf_entry2.pack(side=tk.LEFT)
            eGP_interf_entries2.append(interf_entry2)

            addr_entry = tk.Entry(eGP_addr_frame)
            addr_entry.pack(side=tk.LEFT)
            eGP_addr_entries.append(addr_entry)

            addr_entry2 = tk.Entry(eGP2_addr_frame)
            addr_entry2.pack(side=tk.LEFT)
            eGP_addr_entries2.append(addr_entry2)

    elif eGP_liens_diff > 0 :
        for _ in range(eGP_liens_diff) :
            eGP_link_entries.pop().destroy()
            eGP_link_entries2.pop().destroy()

            eGP_interf_entries.pop().destroy()
            eGP_interf_entries2.pop().destroy()

            eGP_addr_entries.pop().destroy()
            eGP_addr_entries2.pop().destroy()
    

    for i in range(len(routeurs_entries)) :
        routeurs_entries[i].delete(0, tk.END)
        routeurs_entries[i].insert(0, routeurs[selected][i])

    for i in range(len(voisins_entries)) :
        voisins_entries[i].delete(0, tk.END)
        voisins_entries[i].insert(0, voisins[selected][i])
        voisins_type_entries[i].delete(0, tk.END)
        voisins_type_entries[i].insert(0, voisins_type[selected][i])


    
    for i in range(len(liens_entries)) :
        liens_entries[i].delete(0, tk.END)
        liens_entries[i].insert(0, liens[selected][i])

        liens_entries2[i].delete(0, tk.END)
        liens_entries2[i].insert(0, liens2[selected][i])

        interf_entries[i].delete(0, tk.END)
        interf_entries[i].insert(0, liens[selected][i])

        interf_entries2[i].delete(0, tk.END)
        interf_entries2[i].insert(0, liens2[selected][i])
    
    for i in range(len(eGP_link_entries)) :
        eGP_link_entries[i].delete(0, tk.END)
        eGP_link_entries[i].insert(0, eGP_link[selected][i])

        eGP_link_entries2[i].delete(0, tk.END)
        eGP_link_entries2[i].insert(0, eGP_link2[selected][i])

        eGP_interf_entries[i].delete(0, tk.END)
        eGP_interf_entries[i].insert(0, eGP_interf[selected][i])

        eGP_interf_entries2[i].delete(0, tk.END)
        eGP_interf_entries2[i].insert(0, eGP_interf2[selected][i])

        eGP_addr_entries[i].delete(0, tk.END)
        eGP_addr_entries[i].insert(0, eGP_addr[selected][i])

        eGP_addr_entries2[i].delete(0, tk.END)
        eGP_addr_entries2[i].insert(0, eGP_addr2[selected][i])


def add_as():

    global IGP
    global plage_ip
    

    IGPs.append("")
    plages_ip.append("")
    plages_lb.append("")

    routeurs.append([""])

    voisins.append([""])
    voisins_type.append([""])

    liens.append([""])
    liens2.append([""])

    interf.append([""])
    interf2.append([""])

    eGP_link.append([""])
    eGP_link2.append([""])


    

    radio = tk.Radiobutton(radio_frame, text="AS" + str(len(plages_ip)), variable=var, value=len(plages_ip), command=change_AS)
    radio.pack(side=tk.LEFT)

def add_lien() :
    entry = tk.Entry(links_frame)
    entry.pack(side=tk.LEFT)
    liens_entries.append(entry)
    liens[selected].append(entry.get())

    entry2 = tk.Entry(links_frame2)
    entry2.pack(side=tk.LEFT)
    liens_entries2.append(entry2)
    liens2[selected].append(entry2.get())

    interf_entry = tk.Entry(interf_frame)
    interf_entry.pack(side=tk.LEFT)
    interf_entries.append(interf_entry)
    interf[selected].append(interf_entry.get())

    interf_entry2 = tk.Entry(interf_frame2)
    interf_entry2.pack(side=tk.LEFT)
    interf_entries2.append(interf_entry2)
    interf2[selected].append(interf_entry2.get())

def remove_lien() :
    liens_entries.pop().destroy()
    liens[selected].pop()

    liens_entries2.pop().destroy()
    liens2[selected].pop()  

    interf_entries.pop().destroy()
    interf[selected].pop()

    interf_entries2.pop().destroy()
    interf2[selected].pop()  


def add_router() :
    entry = tk.Entry(router_frame)
    entry.pack(side=tk.LEFT)
    routeurs_entries.append(entry)
    routeurs[selected].append(entry.get())

def remove_router() :
    routeurs_entries.pop().destroy()
    routeurs[selected].pop()

def add_neighbor() :
    entry = tk.Entry(neighbor_frame)
    entry.pack(side=tk.LEFT)
    voisins_entries.append(entry)
    voisins[selected].append(entry.get())

    entry2 = tk.Entry(neighbor_type_frame)
    entry2.pack(side=tk.LEFT)
    voisins_type_entries.append(entry2)
    voisins_type[selected].append(entry2.get())

def remove_neighbor() :
    voisins_entries.pop().destroy()
    voisins[selected].pop()

    voisins_type_entries.pop().destroy()
    voisins_type[selected].pop()

def add_eGP_lien() :
    entry = tk.Entry(eGP_link_frame)
    entry.pack(side=tk.LEFT)
    eGP_link_entries.append(entry)
    eGP_link[selected].append(entry.get())

    entry2 = tk.Entry(eGP2_link_frame)
    entry2.pack(side=tk.LEFT)
    eGP_link_entries2.append(entry2)
    eGP_link2[selected].append(entry2.get())

    interf_entry = tk.Entry(eGP_interf_frame)
    interf_entry.pack(side=tk.LEFT)
    eGP_interf_entries.append(interf_entry)
    eGP_interf[selected].append(interf_entry.get())

    interf_entry2 = tk.Entry(eGP2_interf_frame)
    interf_entry2.pack(side=tk.LEFT)
    eGP_interf_entries2.append(interf_entry2)
    eGP_interf2[selected].append(interf_entry2.get())

    addr_entry = tk.Entry(eGP_addr_frame)
    addr_entry.pack(side=tk.LEFT)
    eGP_addr_entries.append(addr_entry)
    eGP_addr[selected].append(addr_entry.get())

    addr_entry2 = tk.Entry(eGP2_addr_frame)
    addr_entry2.pack(side=tk.LEFT)
    eGP_addr_entries2.append(addr_entry2)
    eGP_addr2[selected].append(addr_entry2.get())

def rem_eGP_lien():
    eGP_link_entries.pop().destroy()
    eGP_link[selected].pop()

    eGP_link_entries2.pop().destroy()
    eGP_link2[selected].pop()  

    eGP_interf_entries.pop().destroy()
    eGP_interf[selected].pop()

    eGP_interf_entries2.pop().destroy()
    eGP_interf2[selected].pop()  

    eGP_addr_entries.pop().destroy()
    eGP_addr[selected].pop()

    eGP_addr_entries2.pop().destroy()
    eGP_addr2[selected].pop()

root = tk.Tk()
root.title("Text Entry")

selected = 0
IGPs = [""]
plages_ip = [""]
plages_lb = [""]

routeurs_entries = []
routeurs = [[]]

voisins_entries = []
voisins = [[]]

voisins_type_entries = []
voisins_type = [[]]

liens_entries = []
liens_entries2 = []
liens = [[]]
liens2 = [[]]
interf_entries = []
interf_entries2 = []
interf = [[]]
interf2 = [[]]

eGP_link_entries = []
eGP_link_entries2 = []
eGP_link = [[]]
eGP_link2 = [[]]
eGP_interf_entries = []
eGP_interf_entries2 = []
eGP_interf = [[]]
eGP_interf2 = [[]]
eGP_addr_entries = []
eGP_addr_entries2 = []
eGP_addr = [[]]
eGP_addr2 = [[]]


neighbor_entries = []
neighbor = [[]]


var = tk.IntVar()
# Radio buttons
radio_frame = tk.Frame(root)
radio_frame.pack(side=tk.TOP, fill=tk.X)

radio1 = tk.Radiobutton(radio_frame, text="AS1", variable=var, value=1, command=change_AS)
radio1.select()
radio1.pack(side=tk.LEFT)

# Top frame
top_frame = tk.Frame(root)
top_frame.pack(side=tk.TOP, fill=tk.X)

top_frame.grid_rowconfigure(0, weight=0)
top_frame.grid_rowconfigure(1, weight=1)


# Entries
Info_title = tk.Label(top_frame,text='Informations :',font='Helvetica 12 bold')
Info_title.grid(column=0,row=0,columnspan=4)

IGP_text = tk.Label(top_frame,text='IGP :')
IGP_text.grid(column=0,row=1)
IGP = tk.Entry(top_frame)
IGP.grid(column=1,row=1)


plage_ip_text = tk.Label(top_frame,text='Plage adresses :')
plage_ip_text.grid(column=0,row=2)
plage_ip = tk.Entry(top_frame)
plage_ip.grid(column=1,row=2)


plage_lb_text = tk.Label(top_frame,text='Plage Loopback :')
plage_lb_text.grid(column=0,row=3)
plage_lb = tk.Entry(top_frame)
plage_lb.grid(column=1,row=3)


# Routers :
router_title = tk.Label(top_frame,text='Routeurs :',font='Helvetica 12 bold')
router_title.grid(column=0,row=4,columnspan=4)

router_frame = tk.Frame(top_frame)
router_frame.grid(column=1,row=5)

router_text = tk.Label(top_frame,text='Nom :')
router_text.grid(column=0,row=5)
add_routeur = tk.Button(top_frame, text="+", command=add_router)
add_routeur.grid(column=3,row=5)
rem_routeur = tk.Button(top_frame, text="-", command=remove_router)
rem_routeur.grid(column=4,row=5)
add_router()

# Links :
links_title = tk.Label(top_frame,text='Liens :',font='Helvetica 12 bold')
links_title.grid(column=0,row=6,columnspan=4)

links_frame = tk.Frame(top_frame)
links_frame.grid(column=1,row=7)
links_frame2 = tk.Frame(top_frame)
links_frame2.grid(column=1,row=9)

interf_frame = tk.Frame(top_frame)
interf_frame.grid(column=1,row=8)
interf_frame2 = tk.Frame(top_frame)
interf_frame2.grid(column=1,row=10)

links_text = tk.Label(top_frame,text='Router 1 :')
links_text.grid(column=0,row=7)
links_text2 = tk.Label(top_frame,text='Router 2 :')
links_text2.grid(column=0,row=9)

interf_text = tk.Label(top_frame,text='Interface 1 :')
interf_text.grid(column=0,row=8)
interf_text2 = tk.Label(top_frame,text='Interface 2 :')
interf_text2.grid(column=0,row=10)


add_links = tk.Button(top_frame, text="+", command=add_lien)
add_links.grid(column=3,row=7,rowspan=4)
rem_links = tk.Button(top_frame, text="-", command=remove_lien)
rem_links.grid(column=4,row=7,rowspan=4)
add_lien()


# Neighbors :
neighbor_title = tk.Label(top_frame,text='AS voisin :',font='Helvetica 12 bold')
neighbor_title.grid(column=0,row=11,columnspan=4)

neighbor_frame = tk.Frame(top_frame)
neighbor_frame.grid(column=1,row=12)


neighbor_text = tk.Label(top_frame,text='Nom :')
neighbor_text.grid(column=0,row=12)
add_voisin = tk.Button(top_frame, text="+", command=add_neighbor)
add_voisin.grid(column=3,row=12,rowspan=2)
rem_voisin = tk.Button(top_frame, text="-", command=remove_neighbor)
rem_voisin.grid(column=4,row=12,rowspan=2)

neighbor_type_frame = tk.Frame(top_frame)
neighbor_type_frame.grid(column=1,row=13)

neighbor_type_text = tk.Label(top_frame,text='Type :')
neighbor_type_text.grid(column=0,row=13)

add_neighbor()

# eGP_link
eGP_link_title = tk.Label(top_frame,text='eGP :',font='Helvetica 12 bold')
eGP_link_title.grid(column=0,row=14,columnspan=4)

eGP_link_frame = tk.Frame(top_frame)
eGP_link_frame.grid(column=1,row=15)
eGP_interf_frame = tk.Frame(top_frame)
eGP_interf_frame.grid(column=1,row=17)
eGP_addr_frame = tk.Frame(top_frame)
eGP_addr_frame.grid(column=1,row=19)

eGP2_link_frame = tk.Frame(top_frame)
eGP2_link_frame.grid(column=1,row=16)
eGP2_interf_frame = tk.Frame(top_frame)
eGP2_interf_frame.grid(column=1,row=18)
eGP2_addr_frame = tk.Frame(top_frame)
eGP2_addr_frame.grid(column=1,row=20)

eGP_link_text = tk.Label(top_frame,text='Router 1 :')
eGP_link_text.grid(column=0,row=15)
eGP_link_text2 = tk.Label(top_frame,text='Router 2 :')
eGP_link_text2.grid(column=0,row=17)

eGP_interf_text = tk.Label(top_frame,text='Interface 1 :')
eGP_interf_text.grid(column=0,row=16)
eGP_interf_text2 = tk.Label(top_frame,text='Interface 2 :')
eGP_interf_text2.grid(column=0,row=18)

eGP_addr_text = tk.Label(top_frame,text='Adresse 1 :')
eGP_addr_text.grid(column=0,row=19)
eGP_addr_text2 = tk.Label(top_frame,text='Adresse 2 :')
eGP_addr_text2.grid(column=0,row=20)

add_eGP_link = tk.Button(top_frame, text="+", command=add_eGP_lien)
add_eGP_link.grid(column=3,row=15,rowspan=6)
rem_eGP_link = tk.Button(top_frame, text="-", command=rem_eGP_lien)
rem_eGP_link.grid(column=4,row=15,rowspan=6)

add_eGP_lien()


# Add AS button
add_AS = tk.Button(root, text="Add a new AS", command=add_as)
add_AS.pack(side=tk.TOP,fill=tk.X)

root.mainloop()

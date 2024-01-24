import tkinter as tk


def change_AS():
    global selected
    plages_ip[selected] = plage_ip.get()
    IGPs[selected] = IGP.get()
    indice = var.get()

    IGP.delete(0, tk.END)
    IGP.insert(indice-1, IGPs[indice-1])

    plage_ip.delete(0, tk.END)
    plage_ip.insert(indice-1, plages_ip[indice-1])


    selected = indice-1


def add_as():

    global IGP
    global plage_ip
    

    IGPs.append("")
    plages_ip.append("")
    

    radio = tk.Radiobutton(root, text="AS" + str(len(plages_ip)), variable=var, value=len(plages_ip), command=change_AS)
    radio.pack(side=tk.LEFT)

root = tk.Tk()
root.title("Text Entry")

selected = 0
IGPs = [""]
plages_ip = [""]



# Add AS button
add_button = tk.Button(root, text="Add a new AS", command=add_as)
add_button.pack(side=tk.BOTTOM,fill=tk.X)



# Entry IGP
IGP_text = tk.Label(text='IGP :')
IGP_text.pack(anchor=tk.NW,  padx=10, pady=5)
IGP = tk.Entry(root)
IGP.pack(anchor=tk.NW, padx=10, pady=5, fill=tk.X)


# Entry name
plage_ip_text = tk.Label(text='AS number :')
plage_ip_text.pack(anchor=tk.NW,  padx=10, pady=5)
plage_ip = tk.Entry(root)
plage_ip.pack(anchor=tk.NW, padx=10, pady=5, fill=tk.X)


# Radio buttons
var = tk.IntVar()
radio1 = tk.Radiobutton(root, text="AS1", variable=var, value=1, command=change_AS)
radio1.select()
radio1.pack(side=tk.LEFT)



root.mainloop()

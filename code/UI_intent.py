import customtkinter as Ctk

def change_AS():
    global selected
    names[selected] = entry.get()
    indice = var.get()




    entry.delete(0, tk.END)
    entry.insert(indice-1, names[indice-1])
    selected = indice-1


def add_as():
    global names
    names.append("")
    radio = tk.Radiobutton(root, text="AS" + str(len(names)), variable=var, value=len(names), command=change_AS)
    radio.pack(side=tk.LEFT)


Ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
Ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = Ctk.CTk()  # create CTk window like you do with the Tk window

selected = 0
names = [""]
IGP = [""]


# Add AS button
add_button = Ctk.CTkButton(app, text="Add a new AS", command=add_as)
add_button.place(side=Ctk.BOTTOM,fill=Ctk.X)

'''
# Entry widget
label = tk.Label(text='AS name :')
label.pack(anchor=tk.NW,  padx=10, pady=5)
entry = tk.Entry(root)
entry.pack(anchor=tk.NW, padx=10, pady=5, fill=tk.X)



# Radio buttons
var = tk.IntVar()
radio1 = tk.Radiobutton(root, text="AS1", variable=var, value=1, command=change_AS)
radio1.select()
radio1.pack(side=tk.LEFT)
'''



root.mainloop()

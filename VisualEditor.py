# -*- coding: UTF-8 -*-#

import os # Pour les opérations sur les fichiers
from tkinter import *
import tkinter.filedialog
import tkinter.messagebox

PROGRAM_NAME = "Visual Editor"
file_name=None  # Nom du fichier


root=Tk()
root.geometry('400x400')
root.title(PROGRAM_NAME)

#-- DEFINITIONS DES FONCTIONS -------------

def display_about_messagebox(event=None):
    tkinter.messagebox.showinfo("About", PROGRAM_NAME + "\nTkinter GUI Application\n Development Blueprints")

def display_help_messagebox(event=None):
    tkinter.messagebox.showinfo("Help", "Help Book: \nTkinter GUI Application\n Development Blueprints",icon='question')
    
    #Gestion de n° de ligne
def on_content_changed(event=None):
    update_line_numbers()
    
def get_line_numbers(): #Calcul du nombre de lignes
    output = ''
    if show_line_number.get():
        row, col = content_text.index("end").split('.')
        for i in range(1, int(row)):
            output += str(i) + '\n'
    return output

def update_line_numbers(event=None): #Mise à jour n° de ligne
    line_numbers = get_line_numbers()
    line_number_bar.config(state='normal')
    line_number_bar.delete('1.0', 'end')
    line_number_bar.insert('1.0', line_numbers)
    line_number_bar.config(state='disabled')
    
def exit_editor(event=None):
    if tkinter.messagebox.askokcancel("Quitter?", "Voulez-vous vraiment quitter ?"):
        root.destroy()

def new_file(event=None):
    root.title("Untitled")
    global file_name
    file_name = None
    content_text.delete(1.0, END)
    on_content_changed() #Mise à jour n° ligne

def write_to_file(file_name):
    try:
        content = content_text.get(1.0, 'end')
        with open(file_name, 'w') as the_file:
            the_file.write(content)
    except IOError:
        pass  # in actual we will show a error message box.
        # we discuss message boxes in the next section so ignored here.

def save_as(event=None):
    input_file_name = tkinter.filedialog.asksaveasfilename(defaultextension=".txt",
                                                           filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        write_to_file(file_name)
        root.title('{} - {}'.format(os.path.basename(file_name), PROGRAM_NAME))
    return "break"
    
def save(event=None):
    global file_name
    if not file_name:
        save_as()
    else:
        write_to_file(file_name)
    return "break"

def open_file(event=None):
    input_file_name = tkinter.filedialog.askopenfilename(defaultextension=".txt",
                                                         filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        root.title('{} - {}'.format(os.path.basename(file_name), PROGRAM_NAME))
        content_text.delete(1.0, END)
        with open(file_name) as _file:
            content_text.insert(1.0, _file.read())
        on_content_changed() #Mise à jour n° ligne
        
def select_all(event=None):
    content_text.tag_add('sel', '1.0', 'end')
    return "break"

     # Fenetre de recherche
def find_text(event=None):
    search_toplevel = Toplevel(root)
    search_toplevel.title('Recherche textuelle')
    search_toplevel.transient(root)
    search_toplevel.resizable(False, False)
    Label(search_toplevel, text="Rechercher:").grid(row=0, column=0, sticky='e')
    search_entry_widget = Entry(search_toplevel, width=25)
    search_entry_widget.grid(row=0, column=1, padx=2, pady=2, sticky='we')
    search_entry_widget.focus_set()
    ignore_case_value = IntVar()
    Checkbutton(search_toplevel, text='Ignorer la casse', variable=ignore_case_value).grid(row=1, column=1, sticky='e', padx=2, pady=2)
    Button(search_toplevel, text="Trouver", underline=0,
           command=lambda: search_output(
               search_entry_widget.get(), ignore_case_value.get(),
               content_text, search_toplevel, search_entry_widget)
           ).grid(row=0, column=2, sticky='e' + 'w', padx=2, pady=2)

    def close_search_window():   #Fermeture de la fenetre de recherche
        content_text.tag_remove('match', '1.0', END)
        search_toplevel.destroy()
    search_toplevel.protocol('WM_DELETE_WINDOW', close_search_window)
    return "break"

    # Fonction recherche
def search_output(needle, if_ignore_case, content_text, search_toplevel, search_box):
    content_text.tag_remove('match', '1.0', END)
    matches_found = 0
    if needle:
        start_pos = '1.0'
        while True:
            start_pos = content_text.search(needle, start_pos, nocase=if_ignore_case, stopindex=END)
            if not start_pos:
                break
            end_pos = '{}+{}c'.format(start_pos, len(needle))
            content_text.tag_add('match', start_pos, end_pos)
            matches_found += 1
            start_pos = end_pos
        content_text.tag_config('match', foreground='red', background='yellow')
    search_box.focus_set()
    search_toplevel.title('{} matches found'.format(matches_found))


def cut():
    content_text.event_generate("<<Cut>>")
    on_content_changed() #Mise à jour n° ligne
    return "break"

def copy():
    content_text.event_generate("<<Copy>>")
    return "break"

def paste():
    content_text.event_generate("<<Paste>>")
    on_content_changed() #Mise à jour n° ligne
    return "break"

def undo():
    content_text.event_generate("<<Undo>>")
    on_content_changed() #Mise à jour n° ligne
    return "break"

def redo(event=None):
    content_text.event_generate("<<Redo>>")
    on_content_changed() #Mise à jour n° ligne
    return 'break'
#------------------------------------------

# icones pour les menus
new_file_icon = PhotoImage(file='icons/new_file.gif')
open_file_icon = PhotoImage(file='icons/open_file.gif')
save_file_icon = PhotoImage(file='icons/save.gif')
cut_icon = PhotoImage(file='icons/cut.gif')
copy_icon = PhotoImage(file='icons/copy.gif')
paste_icon = PhotoImage(file='icons/paste.gif')
undo_icon = PhotoImage(file='icons/undo.gif')
redo_icon = PhotoImage(file='icons/redo.gif')
#---------------------------------------------

# Création du menu
menu_bar = Menu(root)  
# Menu Fichier
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Nouveau", accelerator='Ctrl + N', compound='left', image=new_file_icon, underline=0, command=new_file)
file_menu.add_command(label='Ouvrir', accelerator='Ctrl+O', compound='left', image=open_file_icon, underline=0, command=open_file)
file_menu.add_command(label='Enregistrer', accelerator='Ctrl+S', compound='left', image=save_file_icon, underline=0, command=save)
file_menu.add_command(label='Enregistrer sous', accelerator='Shift+Ctrl+S', command=save_as)
file_menu.add_separator()
file_menu.add_command(label='Quitter', accelerator='Alt+F4', command=exit_editor)
menu_bar.add_cascade(label='Fichier', menu=file_menu)

# Menu Edition
edit_menu = Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Défaire", accelerator='Ctrl+Z', compound='left', image=undo_icon, command=undo)
edit_menu.add_command(label='Refaire', accelerator='Ctrl+Y', compound='left', image=redo_icon, command=redo)
edit_menu.add_separator()
edit_menu.add_command(label='Couper', accelerator='Ctrl+X', compound='left', image=cut_icon, command=cut)
edit_menu.add_command(label='Copier', accelerator='Ctrl+C', compound='left', image=copy_icon, command=copy)
edit_menu.add_command(label='Coller', accelerator='Ctrl+V', compound='left', image=paste_icon, command=paste)
edit_menu.add_separator()
edit_menu.add_command(label='Rechercher', underline=0, accelerator='Ctrl+F', command=find_text)
edit_menu.add_separator()
edit_menu.add_command(label='Tout sélectionner', underline=7, accelerator='Ctrl+A', command=select_all)
menu_bar.add_cascade(label='Edition', menu=edit_menu)

# Menu Affichage
view_menu = Menu(menu_bar, tearoff=0)

# Implementing Checkbutton, Radiobutton and Cascade menu-items under View Menu 
show_line_number = IntVar()
show_line_number.set(1)
view_menu.add_checkbutton(label='Afficher les numéros de ligne', variable=show_line_number, command=update_line_numbers)
show_cursor_info = IntVar()
show_cursor_info.set(1)
view_menu.add_checkbutton(label='Afficher le curseur en bas', variable=show_cursor_info)
highlight_line = IntVar()
view_menu.add_checkbutton(label='Highlight Current Line', onvalue=1, offvalue=0, variable=highlight_line)
themes_menu = Menu(menu_bar, tearoff=0)
view_menu.add_cascade(label='Themes', menu=themes_menu)

"""
color scheme is defined with dictionary elements like -
        theme_name : foreground_color.background_color
"""
color_schemes = {
    'Default': '#000000.#FFFFFF',
    'Greygarious': '#83406A.#D1D4D1',
    'Aquamarine': '#5B8340.#D1E7E0',
    'Bold Beige': '#4B4620.#FFF0E1',
    'Cobalt Blue': '#ffffBB.#3333aa',
    'Olive Green': '#D1E7E0.#5B8340',
    'Night Mode': '#FFFFFF.#000000',
}

theme_choice = StringVar()
theme_choice.set('Default')
for k in sorted(color_schemes):
    themes_menu.add_radiobutton(label=k, variable=theme_choice)

menu_bar.add_cascade(label='Affichage', menu=view_menu)

# Menu A Propos
about_menu = Menu(menu_bar, tearoff=0)
about_menu.add_command(label='A propos', command=display_about_messagebox)
about_menu.add_command(label='Aide - F1', command=display_help_messagebox)
menu_bar.add_cascade(label='A propos', menu=about_menu)

root.config(menu=menu_bar)

# Barre supérieure
shortcut_bar = Frame(root,  height=25, background='light sea green')
shortcut_bar.pack(expand='no', fill='x')

# Ajout des boutons raccourcis avec icones
icons = ('new_file', 'open_file', 'save', 'cut', 'copy', 'paste',
         'undo', 'redo', 'find_text')
for i, icon in enumerate(icons):
    tool_bar_icon = PhotoImage(file='icons/{}.gif'.format(icon))
    cmd = eval(icon)
    tool_bar = Button(shortcut_bar, image=tool_bar_icon, command=cmd)
    tool_bar.image = tool_bar_icon
    tool_bar.pack(side='left')


# Barre des n° de ligne
line_number_bar = Text(root, width=4, padx=3, takefocus=0,  border=0, background='khaki', state='disabled',  wrap='none')
line_number_bar.pack(side='left',  fill='y')

# Zone du texte avec scrollbar
content_text = Text(root, wrap='word', undo=1)
content_text.pack(expand='yes', fill='both')
scroll_bar = Scrollbar(content_text)
content_text.configure(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=content_text.yview)
scroll_bar.pack(side='right', fill='y')

# Raccourci clavier pour l'aide
content_text.bind('<KeyPress-F1>', display_help_messagebox)
#-----------------------------

# handling redo quirk - affectation de redo à Ctrl+y
# Key Bindings
content_text.bind('<Control-y>', redo)
content_text.bind('<Control-Y>', redo)
content_text.bind('<Control-A>', select_all)
content_text.bind('<Control-a>', select_all)

content_text.bind('<Control-N>', new_file)
content_text.bind('<Control-n>', new_file)
content_text.bind('<Control-O>', open_file)
content_text.bind('<Control-o>', open_file)
content_text.bind('<Control-S>', save)
content_text.bind('<Control-s>', save)

content_text.bind('<Any-KeyPress>', on_content_changed) #Pour la numerotation des lignes

root.protocol('WM_DELETE_WINDOW', exit_editor) #Intercepte le clic sur la croix de fermeture vers "exit_editor"
root.mainloop()

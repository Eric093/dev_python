import tkinter as tk

root = tk.Tk()


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        
    def hello():
        print ("hello!")
    
       

    def createWidgets(self):
        #--------------
        # create a toplevel menu
        #menubar = Menu(root)
        #menubar.add_command(label="Hello!", command=hello)
        #menubar.add_command(label="Quit!", command=root.quit)
    
        ## display the menu
        #root.config(menu=menubar)
        #-------------------
        
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.QUIT = tk.Button(self, text="QUIT", fg="red",
                                            command=root.destroy)
        self.QUIT.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")


app = Application(master=root)
app.mainloop()
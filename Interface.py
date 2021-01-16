from tkinter import *

class Names(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.master.title("People")
        self.master.geometry("250x250")
        self.master.resizable(0,0)
    
    # add name to list
    def addToList(self, event):
        if self.contents.get().isspace() or not self.contents.get():
            return
        self.list_of_names.insert(END, self.contents.get())
        self.contents.set("")

    # delete name from list
    def deleteFromList(self, event):
        self.list_of_names.delete(ANCHOR)

    def nextPressed(self):
        Payment(self.master)
        #self.pay = Toplevel(Payment(self.master))
        #self.pay.mainloop()
        self.master.withdraw()

    def create_widgets(self):
        # create listbox
        self.list_of_names = Listbox()
        self.list_of_names.pack()

        # create entry box
        self.entry_box = Entry()
        self.entry_box.pack()

        # create string variable for entry box
        self.contents = StringVar()
        self.contents.set("Put Name Here")
        self.entry_box["textvariable"] = self.contents

        # create insert button and binds
        self.insert_button = Button(text="Insert Name")
        self.insert_button.place(x=125,y=185)
        self.entry_box.bind('<Return>', self.addToList)
        self.insert_button.bind('<Button-1>', self.addToList)

        # create delete button and binds
        self.delete_button = Button(text="Delete Name")
        self.delete_button.place(x=45,y=185)
        self.list_of_names.bind('<Delete>', self.deleteFromList)
        self.delete_button.bind('<Button-1>', self.deleteFromList)

        # create next button
        self.next_button = Button(text="Next", command=self.nextPressed)
        self.next_button.place(x=215, y=225)

class Payment(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        #self.pack()
        #self.create_widgets()
        self.title("Carl")
        self.geometry("500x250")
        self.resizable(0,0)

        self.list1 = Names.list_of_names
        print(list1.get(0,END))

root = Tk()
app = Names(root)
app.mainloop()






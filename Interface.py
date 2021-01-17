from tkinter import *

class Names(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        self.createWidgets()
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

    # pass list to next window
    def nextPressed(self):
        if self.list_of_names.size() == 0:
            self.error_label["text"] = "Please add atleast 1 person!"
        else:
            Payment(self.master, self.list_of_names)
            self.master.withdraw()
            self.error_label["text"] = ""

    def textErase(self, event):
        self.current = self.entry_box.get()
        if self.current == "Put Name Here":
            self.entry_box.delete(0,END)

    def createWidgets(self):
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
        self.entry_box.bind("<FocusIn>", self.textErase)

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
        self.next_button.place(x=210, y=220)
        self.error_label = Label()
        self.error_label.place(x=50, y=220)

class Payment(Toplevel):
    def __init__(self, master, list_of_names):
        super().__init__(master)
        self.title("Carl")
        self.geometry("1200x800")
        self.resizable(0,0)
        self.createWidgets(list_of_names)
    
    # update total dues in listbox
    def updateTotal(self):
        try:
            self.name,self.index = self.people_listbox.get(self.people_listbox.curselection()[0]).split()[0], self.people_listbox.curselection()[0]
            self.people_listbox.delete(self.people_listbox.curselection()[0])
            self.people_listbox.insert(self.index, self.name+" -- $"+str(self.dues[self.name]))
        except IndexError:
            return

    # update items based on person
    def updateItems(self,event):
        self.item_listbox.delete(0,END)
        try:
            if self.people_listbox.curselection()[0] in self.item_dict:
                for item in self.item_dict[self.people_listbox.curselection()[0]]:
                    self.item_listbox.insert(END,item)
        except IndexError:
            return
    # add item to list
    def addItem(self,event):
        if self.item_name_entry.get().isspace() or not self.item_name_entry.get() or self.item_price_entry.get().isspace() or not self.item_price_entry.get():
            self.error_label["text"] = "Please enter both item name and price!"
        else:
            try:
                self.item_listbox.insert(END, self.item_name_entry.get()+"  --  $"+self.item_price_entry.get())
                self.error_label["text"] = ""
                self.item_dict[self.people_listbox.curselection()[0]] = self.item_listbox.get(0,END)
                self.name, self.price = self.people_listbox.get(self.people_listbox.curselection()[0]).split()[0], float(self.item_listbox.get(END).split('$')[1])
                self.dues[self.name] += (self.price + (self.price*float(self.tax_entry_box.get())/100) + (self.price*float(self.tip_entry_box.get())/100))
            except IndexError:
                self.item_listbox.delete(0,END)
                self.error_label["text"] = "Please select a person on the left!"
        self.updateTotal()

    # delete item from list
    def deleteItem(self,event):
        self.item_name = self.item_listbox.get(ANCHOR)
        self.item_listbox.delete(ANCHOR)
        try:
            for i,item in enumerate(self.item_dict[self.people_listbox.curselection()[0]]):
                if item == self.item_name:
                    self.item_dict[self.people_listbox.curselection()[0]] = self.item_dict[self.people_listbox.curselection()[0]][:i] + self.item_dict[self.people_listbox.curselection()[0]][i+1:]
            self.error_label["text"] = ""
            self.name,self.price = self.people_listbox.get(self.people_listbox.curselection()[0]).split()[0], float(self.item_name.split('$')[1])
            self.dues[self.name] -= (self.price + (self.price*float(self.tax_entry_box.get())/100) + (self.price*float(self.tip_entry_box.get())/100)) 
            self.updateItems(None)
            self.updateTotal()
        except IndexError:
            self.error_label["text"] = "Please select a person on the left!"
        

    def createWidgets(self, list_of_names):
        # create people listbox
        self.people_listbox = Listbox(self, exportselection=False)
        self.people_listbox.place(x=0,y=22)
        self.dues = {}
        for name in list_of_names.get(0,END):
            self.dues[name] = 0
            self.people_listbox.insert(END, name + " -- $" + str(self.dues[name]))
        
        # create people text
        self.people_label = Label(self, text="People")
        self.people_label.place(x=35, y=0)

        # create tax rate and tip widgets
        self.tax_label = Label(self, text="Tax Rate")
        self.tax_label.place(x=35, y=200)
        self.tax_var = StringVar(self)
        self.tax_var.set("9.75")
        self.tax_entry_box = Entry(self, text=self.tax_var)
        self.tax_entry_box.place(x=0, y=225)
        self.tip_label = Label(self, text="Tip Percentage")
        self.tip_label.place(x=17, y=255)
        self.tip_var = StringVar(self)
        self.tip_var.set("0")
        self.tip_entry_box = Entry(self, text=self.tip_var)
        self.tip_entry_box.place(x=0, y=280)
        self.tax_perc = Label(self,text="%")
        self.tax_perc.place(x=115, y=225)
        self.tip_perc = Label(self,text="%")
        self.tip_perc.place(x=115, y=280)

        # create items listbox
        self.items_label = Label(self, text="Items")
        self.items_label.place(x=260, y=0)
        self.item_listbox = Listbox(self, exportselection=False)
        self.item_listbox.place(x=220,y=22)
        self.item_name_label = Label(self, text="Item Name")
        self.item_name_label.place(x=400, y=35)
        self.item_name_entry = Entry(self)
        self.item_name_entry.place(x=370, y=55)
        self.item_price_label = Label(self, text="Item Price")
        self.item_price_label.place(x=400, y=85)
        self.dollar_sign = Label(self, text="$")
        self.dollar_sign.place(x=360, y=105)
        self.item_price_entry = Entry(self)
        self.item_price_entry.place(x=370, y=105)
        self.item_add_button = Button(self,text="Add")
        self.item_add_button.place(x=435, y=140)
        self.item_delete_button = Button(self,text="Delete")
        self.item_delete_button.place(x=390, y=140)

        # add and delete item config
        self.item_name_entry.bind("<Return>", self.addItem)
        self.item_add_button.bind("<Button-1>", self.addItem)
        self.error_label = Label(self)
        self.error_label.place(x=355, y=170)
        self.item_listbox.bind("<Delete>", self.deleteItem)
        self.item_delete_button.bind("<Button-1>", self.deleteItem)

        # people listbox select config
        self.item_dict = {}
        self.people_listbox.bind("<<ListboxSelect>>", self.updateItems)

root = Tk()
app = Names(root)
app.mainloop()






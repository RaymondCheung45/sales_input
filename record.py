import tkinter as tk
from tkinter import ttk , messagebox
from datetime import datetime
import pandas as pd
import os
import DbConnection


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sales")
        self.geometry("1000x600")
        self.file_entry = os.getcwd()
        self.create_widgets()
        self.db = DbConnection.DbConnector(host='localhost', user='root', password='admin', database='Sales')
        self.db.connect()
        self.db.create_table()
        self.show_all_data()

    def create_widgets(self):
        # product list
        product_label = ttk.Label(self, text="Product:")
        product_label.pack()
        self.product_list = ttk.Combobox(self, values=["Product1","Product2","Product3","Product4"], state="readonly")
        self.product_list.pack()

        # number list
        quantity_label = ttk.Label(self, text="Quantity:")
        quantity_label.pack()
        self.quantity_list = ttk.Combobox(self, values=list(range(1,11)), state="readonly")
        self.quantity_list.pack()

        # price input
        price_label = ttk.Label(self, text="How Much @1:")
        price_label.pack()
        self.price_input = ttk.Entry(self)
        self.price_input.pack()

        # Button to insert the record
        save_button = ttk.Button(self, text="Save" ,command=self.insert_data)
        save_button.pack()
        
        # Button to delete the selected row
        delete_button = ttk.Button(self, text="Delete", command=self.delete_data)
        delete_button.pack()
        
        # Button to export to excel
        delete_button = ttk.Button(self, text="Export to Excel", command=self.to_excel)
        delete_button.pack()

        #  group by product list
        filter_label = ttk.Label(self, text="GroupBy:")
        filter_label.pack()
        self.filter_label = ttk.Combobox(self, values=["None","Product1","Product2","Product3","Product4"], state="readonly")
        self.filter_label.bind("<<ComboboxSelected>>", self.filter_by)
        self.filter_label.pack()
        
        # Table to display the data
        self.table = ttk.Treeview(self, height= 30 ,columns=())
        self.table.pack()
        

    def get_Input(self):
        product = self.product_list.get()
        quantity = self.quantity_list.get()
        price = self.price_input.get()
        date = datetime.now()
        
        if not product or not quantity or not price:
            messagebox.showwarning("Warning", "Something Missing")
            return
        
        return product, quantity, price, date
    
    
    def show_all_data(self):
        rows, columns = self.db.get_table()
        self.show_table(rows,columns)


    def show_table(self, rows, columns):
        self.table.delete(*self.table.get_children())
        self.table["columns"] = columns
        self.table["show"] = "headings"
        
        for column in columns:
            self.table.heading(column, text=column)
        for row in rows:
            self.table.insert("", "end", values=row)
        
        self.show_summary()
            
    def show_summary(self):
        product = self.filter_label.get()
        
        tot_quan, tot_sales = self.db.get_summary(product)        
        self.table.insert("", "end", values=["Total","",tot_quan,tot_sales])
        

    def insert_data(self):
        if not (self.get_Input()):
            return
        product, quantity, price, date = self.get_Input()
        self.db.insert_data(product, quantity, price, date)
        self.show_all_data()
        
    
    def delete_data(self):
        selected_items = self.table.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select a row to delete.")
            return
        
        confirm = messagebox.askyesno("Confirmation", "Are you sure you want to delete the selected row(s)?")
        if confirm:
            for item in selected_items:
                values = self.table.item(item, "values")
                self.db.delete_data(values[0]) 
                
            self.show_all_data()
    
    
    def filter_by(self, event):
        product = self.filter_label.get()
        
        if product == "None":
            self.show_all_data()
        else:
            rows, columns = self.db.filter_by(product)
            self.show_table(rows,columns)
            
        
    def to_excel(self):
        rows, columns = self.db.get_table()
        df = pd.DataFrame(rows)
        df.columns = columns
        df.to_excel("record.xlsx", index=False)


if __name__ == "__main__":
    app = App()
    app.mainloop()

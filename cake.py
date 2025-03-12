import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import mysql.connector

class CakeShopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cake Inventory Management")  # Changed title here
        self.root.geometry("900x600")
        self.root.configure(bg="#fce4ec")  # Light pink background color for a cake shop theme

        # Connect to MySQL Database
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Change this if your MySQL user is different
            password="root",   # Add your MySQL password
            database="cream"  # Database for the Cake Shop
        )
        self.cursor = self.conn.cursor()
        self.create_table()

        # UI Components
        self.setup_ui()
        self.view_inventory()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS cake_inventory (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                flavor VARCHAR(255) NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                size VARCHAR(50) NOT NULL
            )
        """)
        self.conn.commit()

    def setup_ui(self):
        # Update label font and color
        label_font = ('Helvetica', 12, 'bold')
       
        self.name_label = tk.Label(self.root, text="Cake Name:", font=label_font, bg="#fce4ec")
        self.name_label.pack(pady=5)
        self.name_entry = tk.Entry(self.root, font=('Arial', 12), bd=2, relief="solid")
        self.name_entry.pack(pady=5)

        self.flavor_label = tk.Label(self.root, text="Flavor:", font=label_font, bg="#fce4ec")
        self.flavor_label.pack(pady=5)
        self.flavor_entry = tk.Entry(self.root, font=('Arial', 12), bd=2, relief="solid")
        self.flavor_entry.pack(pady=5)

        self.price_label = tk.Label(self.root, text="Price ($):", font=label_font, bg="#fce4ec")
        self.price_label.pack(pady=5)
        self.price_entry = tk.Entry(self.root, font=('Arial', 12), bd=2, relief="solid")
        self.price_entry.pack(pady=5)

        self.size_label = tk.Label(self.root, text="Cake Size:", font=label_font, bg="#fce4ec")
        self.size_label.pack(pady=5)
        self.size_entry = tk.Entry(self.root, font=('Arial', 12), bd=2, relief="solid")
        self.size_entry.pack(pady=5)

        # Add Cake Button
        self.add_button = tk.Button(self.root, text="Add Cake", font=('Arial', 14), bg="#4CAF50", fg="white", bd=0, relief="solid", command=self.add_cake)
        self.add_button.pack(pady=15)

        # Table to display the cake inventory
        self.cake_table = ttk.Treeview(self.root, columns=("ID", "Name", "Flavor", "Price", "Size"), show="headings", height=6)
        self.cake_table.heading("ID", text="ID")
        self.cake_table.heading("Name", text="Cake Name")
        self.cake_table.heading("Flavor", text="Flavor")
        self.cake_table.heading("Price", text="Price ($)")
        self.cake_table.heading("Size", text="Size")
       
        # Treeview styling
        self.cake_table.tag_configure('oddrow', background="#f2f2f2")  # Light gray background for odd rows
        self.cake_table.tag_configure('evenrow', background="#ffffff")  # White background for even rows
       
        self.cake_table.pack(pady=20)

        # Buttons for selling, updating, and deleting items
        self.sell_button = tk.Button(self.root, text="Sell Cake", font=('Arial', 12), bg="#FF9800", fg="white", bd=0, relief="solid", command=self.sell_cake)
        self.sell_button.pack(pady=5)

        self.update_button = tk.Button(self.root, text="Update Cake", font=('Arial', 12), bg="#2196F3", fg="white", bd=0, relief="solid", command=self.update_cake)
        self.update_button.pack(pady=5)

        self.delete_button = tk.Button(self.root, text="Delete Cake", font=('Arial', 12), bg="#F44336", fg="white", bd=0, relief="solid", command=self.delete_cake)
        self.delete_button.pack(pady=5)

        self.view_button = tk.Button(self.root, text="View Price", font=('Arial', 12), bg="#673AB7", fg="white", bd=0, relief="solid", command=self.view_price)
        self.view_button.pack(pady=5)

    def add_cake(self):
        print("Add Cake button clicked!")  # Add this for debugging
        name = self.name_entry.get()
        flavor = self.flavor_entry.get()
        try:
            price = float(self.price_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid price.")
            return
        size = self.size_entry.get()

        if name and flavor and price > 0 and size:
            try:
                self.cursor.execute("""
                    INSERT INTO cake_inventory (name, flavor, price, size)
                    VALUES (%s, %s, %s, %s)
                """, (name, flavor, price, size))
                self.conn.commit()
                self.view_inventory()
                messagebox.showinfo("Success", "Cake added successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
        else:
            messagebox.showerror("Input Error", "Please provide valid cake details.")

    def view_inventory(self):
        for row in self.cake_table.get_children():
            self.cake_table.delete(row)
       
        self.cursor.execute("SELECT * FROM cake_inventory")
        records = self.cursor.fetchall()
        for i, item in enumerate(records):
            if i % 2 == 0:
                self.cake_table.insert("", tk.END, values=item, tags='evenrow')
            else:
                self.cake_table.insert("", tk.END, values=item, tags='oddrow')

    def sell_cake(self):
        selected_item = self.cake_table.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a cake to sell.")
            return
        item_id = self.cake_table.item(selected_item[0])["values"][0]
        # Since stock is removed, we won't be updating stock anymore
        messagebox.showinfo("Success", "Cake sold successfully!")

    def update_cake(self):
        selected_item = self.cake_table.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a cake to update.")
            return
        item_id = self.cake_table.item(selected_item[0])["values"][0]
       
        # Populate the input fields with the selected cake data
        name = self.cake_table.item(selected_item[0])["values"][1]
        flavor = self.cake_table.item(selected_item[0])["values"][2]
        price = self.cake_table.item(selected_item[0])["values"][3]
        size = self.cake_table.item(selected_item[0])["values"][4]
       
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, name)
       
        self.flavor_entry.delete(0, tk.END)
        self.flavor_entry.insert(0, flavor)
       
        self.price_entry.delete(0, tk.END)
        self.price_entry.insert(0, price)
       
        self.size_entry.delete(0, tk.END)
        self.size_entry.insert(0, size)
       
        # Change the button to update the selected cake
        self.add_button.config(text="Update Cake", command=lambda: self.confirm_update(item_id))

    def confirm_update(self, item_id):
        name = self.name_entry.get()
        flavor = self.flavor_entry.get()
        try:
            price = float(self.price_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid price.")
            return
        size = self.size_entry.get()

        if name and flavor and price > 0 and size:
            self.cursor.execute("""
                UPDATE cake_inventory
                SET name = %s, flavor = %s, price = %s, size = %s
                WHERE id = %s
            """, (name, flavor, price, size, item_id))
            self.conn.commit()
            self.view_inventory()
            messagebox.showinfo("Success", "Cake updated successfully!")
           
            # Reset the button back to "Add Cake"
            self.add_button.config(text="Add Cake", command=self.add_cake)
        else:
            messagebox.showerror("Input Error", "Please provide valid cake details.")

    def delete_cake(self):
        selected_item = self.cake_table.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a cake to delete.")
            return
        item_id = self.cake_table.item(selected_item[0])["values"][0]
        self.cursor.execute("DELETE FROM cake_inventory WHERE id = %s", (item_id,))
        self.conn.commit()
        self.view_inventory()
        messagebox.showinfo("Success", "Cake deleted successfully!")

    def view_price(self):
        selected_item = self.cake_table.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a cake to view price.")
            return
        item_name = self.cake_table.item(selected_item[0])["values"][1]
       
        try:
            item_price = float(self.cake_table.item(selected_item[0])["values"][3])
        except ValueError:
            messagebox.showerror("Data Error", "The price data is not valid.")
            return

        messagebox.showinfo("Price", f"Item: {item_name}\nPrice: ${item_price:.2f}")

    def close_connection(self):
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = CakeShopApp(root)
    root.mainloop()



------------------------------------


CREATE TABLE cake_inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    flavor VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    size VARCHAR(50) NOT NULL
);

---------------------------------------	


import tkinter as tk
from tkinter import ttk
import mysql.connector
from beautifultable import BeautifulTable
from tkinter import messagebox

def prettyTable(fields,result):
    table = BeautifulTable()
    table.columns.header=fields
    for row in result:
        table.rows.append(row)
    print(table)
    return table
def make_full_screen(widget):
    widget.grid(row=0, column=0, sticky="nsew")
    widget.grid_rowconfigure(1, weight=1)

class DatabaseInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("CRUD Interface")
        self.connection = self.get_db_connection()
        self.entry_fields={}
        if self.connection:
            self.cursor = self.connection.cursor()
            self.notebook = ttk.Notebook(self.root)
            self.notebook.pack(expand=1, fill=tk.BOTH)

            self.userTab = ttk.Frame(self.notebook)
            make_full_screen(self.userTab)
            self.notebook.add(self.userTab, text="User Query")

            self.tableTab = ttk.Frame(self.notebook)
            make_full_screen(self.tableTab)
            self.notebook.add(self.tableTab, text="Tables")

            self.joinTab = ttk.Frame(self.notebook)
            make_full_screen(self.joinTab)
            self.notebook.add(self.joinTab, text="Joins")

            tables = ['orders', 'product', 'customer', 'employee', 'sale', 'warehouse', 'stock', 'transporter', 'vehicle', 'vendor']
            for table in tables:
                frame = ttk.Frame(self.notebook)
                self.notebook.add(frame, text=table.capitalize())
                fields = self.get_table_fields(table)
                self.create_input_fields(frame, fields, table)
                self.create_buttons(frame, table)
            self.create_user_tab()
            self.create_table_tab()
            self.create_join_tab()
        else:
            print("Error: Could not establish database connection.")

    def get_db_connection(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                port=3306,
                database='supplychain',
                user='root',
                password='root'
            )
            return connection
        except mysql.connector.Error as e:
            print("Error connecting to MySQL:", e)
            return None

    def create_user_tab(self):
        self.userTab.grid_columnconfigure(2, weight=1)
        self.user_query_label = tk.Label(self.userTab, text="Enter SQL Query:")
        self.user_query_label.grid(row=0, column=0, padx=5, pady=5)

        self.user_query_entry = tk.Entry(self.userTab, width=50)
        self.user_query_entry.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

        self.user_query_button = tk.Button(self.userTab, text="Execute Query", command=self.execute_user_query)
        self.user_query_button.grid(row=0, column=2, padx=5, pady=5)

        self.user_query_result_text = tk.Text(self.userTab, width=90, height=20)
        self.user_query_result_text.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')
    
    def execute_user_query(self):
        query = self.user_query_entry.get()
        connection = self.connection
        cursor = self.cursor
        if connection:
            try:
                cursor.execute(query)
                fields = [field_md[0] for field_md in cursor.description]
                result = cursor.fetchall()
                self.connection.commit()
                result = prettyTable(fields, result)
                if result:
                    self.user_query_result_text.delete(1.0, tk.END)
                    self.user_query_result_text.insert(tk.END,result)
                else:
                    self.user_query_result_text.delete(1.0, tk.END)
                    self.user_query_result_text.insert(tk.END, "No results found.")
            except mysql.connector.Error as e:
                self.user_query_result_text.delete(1.0, tk.END)
                self.user_query_result_text.insert(tk.END, "Error executing query: " + str(e))

    def create_join_tab(self):
        self.joinTab.grid_columnconfigure(5, weight=1)
        self.product_var = tk.IntVar()
        self.product_checkbox = tk.Checkbutton(self.joinTab, text="Product", variable=self.product_var)
        self.product_checkbox.grid(row=0, column=0, padx=10, pady=5)

        self.customer_var = tk.IntVar()
        self.customer_checkbox = tk.Checkbutton(self.joinTab, text="Customer", variable=self.customer_var)
        self.customer_checkbox.grid(row=0, column=1, padx=10, pady=5)

        self.transporter_var = tk.IntVar()
        self.transporter_checkbox = tk.Checkbutton(self.joinTab, text="Transporter", variable=self.transporter_var)
        self.transporter_checkbox.grid(row=0, column=2, padx=10, pady=5)

        self.vendor_var = tk.IntVar()
        self.vendor_checkbox = tk.Checkbutton(self.joinTab, text="Vendor", variable=self.vendor_var)
        self.vendor_checkbox.grid(row=0, column=3, padx=10, pady=5)

        self.warehouse_var = tk.IntVar()
        self.warehouse_checkbox = tk.Checkbutton(self.joinTab, text="Warehouse", variable=self.warehouse_var)
        self.warehouse_checkbox.grid(row=0,column=4, padx=10, pady=5)

        # Button to perform join operation
        self.join_button = tk.Button(self.joinTab, text="Join Tables", command=self.perform_join)
        self.join_button.grid(row=0,column=5, padx=10, pady=5)

        self.join_query_result_text = tk.Text(self.joinTab, width=90, height=20)
        self.join_query_result_text.grid(row=1, column=0, columnspan=6, padx=5, pady=5, stick='nsew')
    
    def perform_join(self):
        join_tables = []
        if self.product_var.get():
            join_tables.append("product")
        if self.customer_var.get():
            join_tables.append("customer")
        if self.transporter_var.get():
            join_tables.append("transporter")
        if self.vendor_var.get():
            join_tables.append("vendor")
        if self.warehouse_var.get():
            join_tables.append("warehouse")

        if not join_tables:
            print("Please select at least one table to join.")
            return

        join_conditions = [
            f"orders.pid = product.pid" if "product" in join_tables else None,
            f"orders.cid = customer.cid" if "customer" in join_tables else None,
            f"orders.tid = transporter.tid" if "transporter" in join_tables else None,
            f"orders.vid = vendor.vid" if "vendor" in join_tables else None,
            f"orders.wid = warehouse.wid" if "warehouse" in join_tables else None,
        ]

        join_conditions = [condition for condition in join_conditions if condition is not None]

        join_query = "SELECT * FROM orders"
        if join_conditions:
            join_query += " INNER JOIN " + " INNER JOIN ".join(join_tables) + " ON " + " AND ".join(join_conditions)

        print("Join Query:", join_query)
        connection = self.connection
        if connection:
            try:
                cursor = self.cursor
                cursor.execute(join_query)
                fields = [field_md[0] for field_md in cursor.description]
                result = cursor.fetchall()
                self.connection.commit()
                result = prettyTable(fields, result)
                if result:
                    self.join_query_result_text.delete(1.0, tk.END)
                    self.join_query_result_text.insert(tk.END,result)
                else:
                    self.join_query_result_text.delete(1.0, tk.END)
                    self.join_query_result_text.insert(tk.END, "No results found.")
            except mysql.connector.Error as e:
                self.join_query_result_text.delete(1.0, tk.END)
                self.join_query_result_text.insert(tk.END, "Error executing query: " + str(e))

    def create_table_tab(self):
        self.tableTab.grid_columnconfigure(9, weight=1)
        self.query1_button = tk.Button(self.tableTab, text="Orders", command=lambda: self.execute_query(0))
        self.query1_button.grid(row=0, column=0, padx=5, pady=5)

        self.query2_button = tk.Button(self.tableTab, text="Product", command=lambda: self.execute_query(1))
        self.query2_button.grid(row=0, column=1, padx=5, pady=5)

        self.query3_button = tk.Button(self.tableTab, text="Customer", command=lambda: self.execute_query(2))
        self.query3_button.grid(row=0, column=2, padx=5, pady=5)

        self.query4_button = tk.Button(self.tableTab, text="Employee", command=lambda: self.execute_query(3))
        self.query4_button.grid(row=0, column=3, padx=5, pady=5)

        self.query5_button = tk.Button(self.tableTab, text="Sale", command=lambda: self.execute_query(4))
        self.query5_button.grid(row=0, column=4, padx=5, pady=5)

        self.query6_button = tk.Button(self.tableTab, text="Warehouse", command=lambda: self.execute_query(5))
        self.query6_button.grid(row=0, column=5, padx=5, pady=5)

        self.query7_button = tk.Button(self.tableTab, text="Stock", command=lambda: self.execute_query(6))
        self.query7_button.grid(row=0, column=6, padx=5, pady=5)

        self.query8_button = tk.Button(self.tableTab, text="Transporter", command=lambda: self.execute_query(7))
        self.query8_button.grid(row=0, column=7, padx=5, pady=5)

        self.query9_button = tk.Button(self.tableTab, text="Vehicle", command=lambda: self.execute_query(8))
        self.query9_button.grid(row=0, column=8, padx=5, pady=5)

        self.query10_button = tk.Button(self.tableTab, text="Vendor", command=lambda: self.execute_query(9))
        self.query10_button.grid(row=0, column=9, padx=5, pady=5)

        self.table_query_result_text = tk.Text(self.tableTab, width=90, height=20)
        self.table_query_result_text.grid(row=1, column=0, columnspan=10, padx=5, pady=5, stick='nsew')

    def execute_query(self, index):
        connection = self.connection
        tableNames = ['orders', 'product', 'customer', 'employee', 'sale', 'warehouse', 'stock', 'transporter', 'vehicle', 'vendor']
        if connection:
            try:
                cursor = self.cursor
                cursor.execute("SELECT * FROM {table_name}".format(table_name=tableNames[index]))
                fields = [field_md[0] for field_md in cursor.description]
                result = cursor.fetchall()
                self.connection.commit()
                result = prettyTable(fields, result)
                if result:
                    self.table_query_result_text.delete(1.0, tk.END)
                    self.table_query_result_text.insert(tk.END,result)
                else:
                    self.table_query_result_text.delete(1.0, tk.END)
                    self.table_query_result_text.insert(tk.END, "No results found.")
            except mysql.connector.Error as e:
                self.table_query_result_text.delete(1.0, tk.END)
                self.table_query_result_text.insert(tk.END, "Error executing query: " + str(e))

    def get_table_fields(self, table_name):
        try:
            self.cursor.execute(f"DESC {table_name}")
            fields = [row[0] for row in self.cursor.fetchall()]
            return fields
        except mysql.connector.Error as e:
            print("Error fetching table fields:", e)
            return None

    def create_input_fields(self, frame, fields, table):
        table_entry_fields = []
        for i, field in enumerate(fields):
            label = tk.Label(frame, text=field.capitalize())
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = tk.Entry(frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            table_entry_fields.append(entry)
        self.entry_fields[table]=table_entry_fields

    def create_buttons(self, frame, table):
        insert_button = tk.Button(frame, text="Insert", command=lambda: self.insert_row(table))
        insert_button.grid(row=len(self.entry_fields[table]), column=0, padx=5, pady=5)
        update_button = tk.Button(frame, text="Update", command=lambda: self.update_row(table))
        update_button.grid(row=len(self.entry_fields[table]), column=1, padx=5, pady=5)
        delete_button = tk.Button(frame, text="Delete", command=lambda: self.delete_row(table))
        delete_button.grid(row=len(self.entry_fields[table]), column=2, padx=5, pady=5)

    def insert_row(self, table):
        fields = ", ".join(self.get_table_fields(table))
        values = ", ".join(["%s"] * len(self.entry_fields[table]))
        query = f"INSERT INTO {table} ({fields}) VALUES ({values})"
        data = tuple(entry.get() for entry in self.entry_fields[table])
        print(fields, values, query, data)
        try:
            self.cursor.execute(query, data)
            self.connection.commit()
            print("Row inserted successfully!")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", "Error creating rows")
    def update_row(self, table):
        primary_key = self.get_table_fields(table)[0]
        fields = ", ".join([f"{field}=%s" for field in self.get_table_fields(table)[1:]])
        query = f"UPDATE {table} SET {fields} WHERE {primary_key}=%s"
        data = tuple(entry.get() for entry in self.entry_fields[table])
        print(fields, query, data)
        try:
            self.cursor.execute(query, data[1:] + (data[0],))
            self.connection.commit()
            print("Row updated successfully!")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", "Error updating rows")

    def delete_row(self, table):
        primary_key = self.get_table_fields(table)[0]
        data = (self.entry_fields[table][0].get(),)
        query = f"DELETE FROM {table} WHERE {primary_key}=%s"
        print(query, data)
        try:
            self.cursor.execute(query, data)
            self.connection.commit()
            print("Row deleted successfully!")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", "Error deleting rows")

class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Page")

        self.username_label = tk.Label(root, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        self.password_label = tk.Label(root, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "root" and password == "root":
            self.root.destroy()
            root = tk.Tk()
            database_interface = DatabaseInterface(root)
            root.mainloop()
        else:
            messagebox.showerror("Login", "Invalid username or password.")

root = tk.Tk()
login_page = LoginPage(root)
root.mainloop()

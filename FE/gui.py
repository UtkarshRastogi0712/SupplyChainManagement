import tkinter as tk
from tkinter import ttk
import mysql.connector
from beautifultable import BeautifulTable

def prettyTable(fields,result):
    table = BeautifulTable()
    table.columns.header=fields
    for row in result:
        table.rows.append(row)
    print(table)
    return table
def get_db_connection():
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

class DatabaseInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Interface")
        self.root.geometry("750x400")

        self.tabControl = ttk.Notebook(root)
        self.tabControl.pack(expand=1, fill="both")

        self.userTab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.userTab, text="User Query")

        self.tableTab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tableTab, text="Tables")

        self.create_user_tab()
        self.create_table_tab()

    def create_user_tab(self):
        self.user_query_label = tk.Label(self.userTab, text="Enter SQL Query:")
        self.user_query_label.grid(row=0, column=0, padx=5, pady=5)

        self.user_query_entry = tk.Entry(self.userTab, width=50)
        self.user_query_entry.grid(row=0, column=1, padx=5, pady=5)

        self.user_query_button = tk.Button(self.userTab, text="Execute Query", command=self.execute_user_query)
        self.user_query_button.grid(row=0, column=2, padx=5, pady=5)

        self.user_query_result_text = tk.Text(self.userTab, width=90, height=20)
        self.user_query_result_text.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

    def execute_user_query(self):
        query = self.user_query_entry.get()
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(query)
                fields = [field_md[0] for field_md in cursor.description]
                result = cursor.fetchall()
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

    def create_table_tab(self):
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
        self.table_query_result_text.grid(row=1, column=0, columnspan=10, padx=5, pady=5)

    def execute_query(self, index):
        connection = get_db_connection()
        tableNames = ['orders', 'product', 'customer', 'employee', 'sale', 'warehouse', 'stock', 'transporter', 'vehicle', 'vendor']
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM {table_name}".format(table_name=tableNames[index]))
                fields = [field_md[0] for field_md in cursor.description]
                result = cursor.fetchall()
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

root = tk.Tk()
app = DatabaseInterface(root)
root.mainloop()


import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as filedialog
import source

class Table():
    next_row = 0 
    def __init__(self, frame):
        self.table = ttk.Treeview(frame)
        self.table['columns'] = ('col1', 'col2', 'col3', 'col4')
        
        # Define column properties
        self.table.column("#0", width=0, stretch=tk.NO)
        self.table.column("col1", anchor=tk.CENTER, width=80)
        self.table.column("col2", anchor=tk.CENTER, width=80)
        self.table.column("col3", anchor=tk.CENTER, width=80)
        self.table.column("col4", anchor=tk.CENTER, width=80)

        # Define column headings
        self.table.heading("#0", text="", anchor=tk.CENTER)
        self.table.heading("col1", text="num", anchor=tk.CENTER)
        self.table.heading("col2", text="art_id", anchor=tk.CENTER)
        self.table.heading("col3", text="qte_actuelle", anchor=tk.CENTER)
        self.table.heading("col4", text="libelle", anchor=tk.CENTER)

    def _insert_row(self, value1, value2, value3, value4):    
        # Insert sample data
        self.table.insert(parent='', index='end', iid=Table.next_row, text='', values=(value1, value2, value3, value4))
        # increment the index for the next insertion
        Table.next_row +=1 

    def _pack(self):
        self.table.pack()





class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry(f"{1200}x{700}")

        self.tab_control = ttk.Notebook(self)
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab1, text="Main Frame")
        self.tab_control.add(self.tab2, text="Connection details")
        self.tab_control.pack(expand=True, fill="both")

        self.subframe1 = tk.Frame(self.tab1, bg="#01161E")
        self.subframe1.pack(expand=1, fill='both', ipadx=20, ipady=20)

        self.button_frame = tk.Frame(self.subframe1, bg="#124559")
        self.button_frame.place(relx=0.02, rely=0.05, height=50, relwidth=0.96)

        self.button1 = tk.Button(self.button_frame, text="supprimer les tableaux", command=self.drop_table, height=50)
        self.button2 = tk.Button(self.button_frame, text="Créer les tableaux", command=self.create_tables, height=50)
        self.button3 = tk.Button(self.button_frame, text="Importer", command=self.read_data, height=50)
        self.button4 = tk.Button(self.button_frame, text="Remplir les tableaux", command=self.fill_tables, height=50)
        self.button5 = tk.Button(self.button_frame, text="Générer le bilan", command=self.generate_bilan, height=50)

        self.button1.pack(side=tk.LEFT, fill='both', expand=True)
        self.button2.pack(side=tk.LEFT, fill='both', expand=True)
        self.button3.pack(side=tk.LEFT, fill='both', expand=True)
        self.button4.pack(side=tk.LEFT, fill='both', expand=True)
        self.button5.pack(side=tk.LEFT, fill='both', expand=True)

        self.label = tk.Label(self.subframe1, text="LOG : ", bg="#01161E", fg='white')
        self.label.place(relx=0.02, rely=0.3)

        self.text_area = tk.Text(self.subframe1, bg="#124559")
        self.text_area.place(relx=0.02, rely=0.35, relheight=0.6, relwidth=0.96)

        self.subframe2 = tk.Frame(self.tab2, bg="#01161E")
        self.subframe2.pack(expand=1, fill='both', ipadx=20, ipady=20)


        self.title_label = tk.Label(self.subframe2, text="État de connection", bg='#01161E', fg='white', font=('Arial', 14, 'bold'))
        self.title_label.pack(pady=(10, 20))


        self.status_label = tk.Label(self.subframe2, text='Hors ligne', fg='red', bg='#01161E')
        self.status_label.place(relx=0.475, rely=0.13)


        self.dbname_label = ttk.Label(self.subframe2, text="Database Name:", anchor="center")
        self.dbname_label.place(relx=0.39, rely=0.2, width=120)
        self.dbname_entry = ttk.Entry(self.subframe2)
        self.dbname_entry.place(relx=0.5, rely=0.2, width=120)

        self.user_label = ttk.Label(self.subframe2, text="User:", anchor="center")
        self.user_label.place(relx=0.39, rely=0.3, width=120)
        self.user_entry = ttk.Entry(self.subframe2)
        self.user_entry.place(relx=0.5, rely=0.3, width=120)

        self.password_label = ttk.Label(self.subframe2, text="Password:", anchor="center")
        self.password_label.place(relx=0.39, rely=0.4, width=120)
        self.password_entry = ttk.Entry(self.subframe2, show="*")
        self.password_entry.place(relx=0.5, rely=0.4, width=120)

        self.host_label = ttk.Label(self.subframe2, text="Host:", anchor="center")
        self.host_label.place(relx=0.39, rely=0.5, width=120)
        self.host_entry = ttk.Entry(self.subframe2)
        self.host_entry.place(relx=0.5, rely=0.5, width=120)

        self.port_label = ttk.Label(self.subframe2, text="Port:", anchor="center")
        self.port_label.place(relx=0.39, rely=0.6, width=120)
        self.port_entry = ttk.Entry(self.subframe2)
        self.port_entry.place(relx=0.5, rely=0.6, width=120)

        self.connection_button = tk.Button(self.subframe2, text='Connecter', command=self.connect)
        self.connection_button.place(relx=0.455, rely=0.7)


        self.text_area = tk.Text(self.subframe1, bg="#124559", fg='white', highlightbackground="#124559", insertbackground='white')
        self.text_area.place(relx=0.02, rely=0.35, relheight=0.6, relwidth=0.96)


    def connect(self):
        dbname_val = self.dbname_entry.get()
        user_val = self.user_entry.get()
        password_val = self.password_entry.get()
        host_val = self.host_entry.get()
        port_val = self.port_entry.get()

        connection_info, connection_status = source.connect_db(dbname_val, user_val, password_val, host_val, port_val)

        status_label_color = 'green' if connection_status else 'red'
        status_text = 'en ligne' if connection_status else 'hors ligne'    

        button_text = 'connect' if connection_status else 'deconnecter'
        button_function = self.connect if connection_status else self.disconnect

        self.connection_button.config(command = button_function , text = button_text)
        
        self.status_label.config(text=status_text, fg=status_label_color)
        print(connection_info)
        return connection_info


    def disconnect(self):
        connection_info = source.disconnect_db()

        self.status_label.config(text='hors ligne', fg='red')

        status_label_color ='red'
        status_text = 'hors ligne'
        
        self.connection_button.config(command = self.connect, text = 'connecter')
        
        self.status_label.config(text=status_text, fg=status_label_color)


        print(connection_info)
        self.text_area.delete("1.0", "end")
        self.text_area.insert('1.0', connection_info)


    def read_data(self):
        root = tk.Toplevel(self)  # Create a Toplevel window 
        root.withdraw()  # Hide the main window

        file_path = filedialog.askopenfilename(title="Select Excel File", filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))

        if file_path:
            source.read_data(file_path)
            log = ''

            for sheet_name, df in source.data.items():

                log += f"\nNom de la feuille : {sheet_name}\n"
                log += str(df)

            self.text_area.delete("1.0", "end")
            self.text_area.insert('1.0', f'Données importées : \n{log}\n')
        else:
            print("No file selected.")

        root.destroy()  # Destroy the Toplevel window when done


    def create_tables(self):
        query_log = source.create_tables()
        self.text_area.delete("1.0", "end")
        self.text_area.insert("1.0", query_log)
        print(query_log)


    def fill_tables(self):
        query = source.fill_artice_table() + ';' + source.fill_achat_table() + ';' +  source.fill_vent_table()
    
        try:
            source.cur.execute(query)
            source.conn.commit()
            print("Tables filled successfuly.")
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", "Tables filled successfuly.")

        except Exception as e:
            source.conn.rollback()
            log = 'Error filling the table' + str(e)
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", log)
            print(log)

    def generate_bilan(self):
        try:
            source.cur.execute(source.fill_bilan_table())
            source.conn.commit()

            bilan = source.generate_bilan(source.get_table_data("bilan"))
            
            self.text_area.delete("1.0", 'end')
            self.text_area.insert("1.0", bilan)

        except Exception as e:
            source.conn.rollback()
            log = f'Error when generating the balance sheet, Error : \n{str(e)}'
            print(log)
            self.text_area.delete("1.0", 'end')
            self.text_area.insert("1.0", log)

    

    def drop_table(self):
        query_log = source.drop_tables()
        print(query_log)
        self.text_area.delete("1.0", "end")
        self.text_area.insert("1.0", query_log)





if __name__ == "__main__":
    app = Application()
    app.mainloop()
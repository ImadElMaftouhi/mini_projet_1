import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as filedialog
from numpy import pad, size
import source



# utiliser cette classe pour affichier les donnees sous forme d'un tableau 
class Table():
    next_row = 0
    def __init__(self, frame, nbr_col, headings):
        if nbr_col!= len(headings):
            raise ValueError("Number of columns does not match the number of headings.")

        self.table = ttk.Treeview(frame)

        # Define columns
        columns = [f"col{i}" for i in range(nbr_col)]
        self.table['columns'] = columns

        # Define column properties
        self.table.column("#0", width=0, stretch=tk.NO)
        for column in columns:
            self.table.column(column, anchor=tk.CENTER, width=80)

        # Define column headings
        self.table.heading("#0", text="", anchor=tk.CENTER)
        for column, heading in zip(columns, headings):
            self.table.heading(column, text=heading, anchor=tk.CENTER)

    def _insert_row(self, num, art_id, qte_actuelle, libelle):    
        # Insert sample data
        self.table.insert(parent='', index='end', id=Table.next_row, text='', values=(num, art_id, qte_actuelle, libelle))
        # increment the index for the next insertion
        Table.next_row +=1 

    def _pack(self):
        self.table.pack(pady = 20)



class Alert(tk.Toplevel):
    def __init__(self, master, title, message):
        super().__init__(master)
        self.title(title)
        self.message_label = tk.Label(self, text=message, wraplength=400)
        self.message_label.pack(padx=10, pady=10)
        self.ok_button = ttk.Button(self, text="Okay", command=self.destroy)
        self.ok_button.pack(pady=10)



class Application(tk.Tk):
    imported_data_game = 0
    def __init__(self):
        super().__init__()

        self.geometry(f"{1200}x{700}")

        self.tab_control = ttk.Notebook(self)
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab1, text="Page principale")
        self.tab_control.add(self.tab2, text="Detailes de connection")
        self.tab_control.pack(expand=True, fill="both")


        # Frame 1 : La page principale
        self.subframe1 = tk.Frame(self.tab1, bg="#01161E")
        self.subframe1.pack(expand=1, fill='both', ipadx=20, ipady=20)

        self.button_frame = tk.Frame(self.subframe1, bg="#124559")
        self.button_frame.place(relx=0.02, rely=0.07, height=50, relwidth=0.96)

        self.button1 = tk.Button(self.button_frame, text="supprimer les tableaux", command=self.drop_table, height=50)
        self.button2 = tk.Button(self.button_frame, text="Créer les tableaux", command=self.create_tables, height=50)
        self.button3 = tk.Button(self.button_frame, text="Importer les donnees", command=self.read_data, height=50)
        self.button4 = tk.Button(self.button_frame, text="Remplir les tableaux", command=self.fill_tables, height=50)
        self.button5 = tk.Button(self.button_frame, text="Générer le bilan", command=self.generate_bilan, height=50)

        self.button1.pack(side=tk.LEFT, fill='both', expand=True)
        self.button2.pack(side=tk.LEFT, fill='both', expand=True)
        self.button3.pack(side=tk.LEFT, fill='both', expand=True)
        self.button4.pack(side=tk.LEFT, fill='both', expand=True)
        self.button5.pack(side=tk.LEFT, fill='both', expand=True)

        self.table_buttons_frame = tk.Frame(self.subframe1, bg="#124559")

        self.tables_button = tk.Button(self.subframe1, text = "Afficher les donnees importee", command = self.view_tables)
        self.tables_button.place(relx = 0.02, rely=0.15)

        self.label = tk.Label(self.subframe1, text="LOG : ", bg="#01161E", fg='white')
        self.label.place(relx=0.02, rely=0.3)

        self.text_area = tk.Text(self.subframe1, bg="#124559")
        self.text_area.place(relx=0.02, rely=0.35, relheight=0.6, relwidth=0.96)

        self.status_label1 = tk.Label(self.subframe1, text='Hors ligne', fg='red', bg='#01161E' )
        self.status_label1.place(relx=0.475, rely=0.02)


        ## Frame 2 : formulaire pour saisir les informations necessaire a la connections au base des donnees
        self.subframe2 = tk.Frame(self.tab2, bg="#01161E")
        self.subframe2.pack(expand=1, fill='both', ipadx=20, ipady=20)

        self.title_label = tk.Label(self.subframe2, text="État de connection", bg='#01161E', fg='white', font=('Arial', 14, 'bold'))
        self.title_label.pack(pady=(10, 20))

        self.status_label2 = tk.Label(self.subframe2, text='Hors ligne', fg='red', bg='#01161E')
        self.status_label2.place(relx=0.475, rely=0.13)

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

        # Modification des indicators de la connections 
        self.connection_button.config(command = button_function , text = button_text)
        self.status_label2.config(text=status_text, fg=status_label_color)
        self.status_label1.config(text=status_text, fg=status_label_color)
        
        alert = Alert(self.subframe1, "Status de connection", 'connection reussie' if connection_status else 'connection echoue')

        return connection_info


    def disconnect(self):
        connection_info = source.disconnect_db()

        alert = Alert(self.subframe2, 'Alert de connection', connection_info)

        status_label_color ='red'
        status_text = 'hors ligne'
        

        # configuration des indicators
        self.connection_button.config(command = self.connect, text = 'connecter')
        self.status_label2.config(text=status_text, fg=status_label_color)
        self.status_label1.config(text=status_text, fg=status_label_color)

        self.text_area.delete("1.0", "end")
        self.text_area.insert('1.0', connection_info)


    def read_data(self):
        root = tk.Toplevel(self)  
        root.withdraw()

        file_path = filedialog.askopenfilename(title="Select Excel File", filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))

        if file_path:
            source.read_data(file_path)
            self.__class__.imported_data_game = 1

            log = ''

            for sheet_name, df in source.data.items():

                log += f"\nNom de tableau : {sheet_name}\n"
                log += str(df)

            self.text_area.delete("1.0", "end")
            self.text_area.insert('1.0', f'Données importées : \n{log}\n')
        else:
            alert = Alert(self.subframe1, "Importation", "Aucun chemin n'est specifiee")
        root.destroy()

    def animate_xframe(self, frame, target_relx, new_relx=-1):
        # Calculate the new position of the frame
        if new_relx <= target_relx + 0.005:
            self.table_buttons_frame.place(relx=new_relx, rely=0.2, height=30, relwidth=0.96)
            new_relx += 0.005
            return self.after(1, self.animate_xframe, frame, target_relx, new_relx) # type: ignore
        else:
            pass
        
    def view_tables(self):
        if self.__class__.imported_data_game == 0 :
            alert = Alert(self.subframe1, "Alert", "No data has been imported yet")
        else:
            # Start the animation
            for table in source.data.keys():
                tk.Button(self.table_buttons_frame, text=table, command=lambda x=table: view_table(x)).pack(side=tk.LEFT, fill='both', expand=True)
            self.animate_xframe(self.table_buttons_frame, 0.02)

        def view_table(table_name):
            self.text_area.delete('1.0', 'end')
            self.text_area.insert("1.0", source.data[table_name].to_string())
                    

    def create_tables(self):
        query_log = source.create_tables()
        self.text_area.delete("1.0", "end")
        self.text_area.insert("1.0", query_log)

        


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
            bilan = source.get_table_data("bilan")

            self.text_area.delete("1.0", 'end')
            self.text_area.forget()

            # affichage du bilan              
            self.new_frame = tk.Frame(self.subframe1, bg="#124559")
            self.new_frame.place(relx=0.02, rely=0.35, relheight=0.6, relwidth=0.96)
            
            table = Table(self.new_frame, 4 ,['art_id', 'num', 'qte_actuelle', 'libelle'] )
            
            for i in range(len(bilan)-1):
                table._insert_row(bilan[i][0], bilan[i][1], bilan[i][2], bilan[i][3])
            table._pack()


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
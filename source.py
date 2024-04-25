import pandas as pd
import psycopg2
import time

global conn, cur, data
path = "/home/imad/Documents/AD/ingenierie_donnees/ETL/registre.xlsx"

def connect_db(dbname, user, password, host, port):
    global conn, cur
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cur = conn.cursor()
        return("Connected to database:", conn.get_dsn_parameters(), "\n")

    except (Exception, psycopg2.Error) as error:
        return "Error while connecting to PostgreSQL: " + str(error)

def disconnect_db():
    global conn, cur
    if conn:
        cur.close()
        conn.close()
        return "PostgreSQL connection is closed."

def create_tables():
    global conn, cur
    query = """
    CREATE TABLE articles (
        id SERIAL PRIMARY KEY,
        libelle TEXT NOT NULL,
        pu NUMERIC NOT NULL
    );

    CREATE TABLE achats (
        num SERIAL PRIMARY KEY,
        art_id INT NOT NULL,
        qte INT NOT NULL,
        date DATE NOT NULL,
        FOREIGN KEY (art_id) REFERENCES articles(id)
    );

    CREATE TABLE ventes (
        num SERIAL PRIMARY KEY,
        art_id INT NOT NULL,
        qte INT NOT NULL,
        date DATE NOT NULL,
        FOREIGN KEY (art_id) REFERENCES articles(id)
    );

    CREATE TABLE bilan (
        num SERIAL PRIMARY KEY,
        art_id INT NOT NULL,
        qte_actuelle INT,
        libelle TEXT NOT NULL,
        FOREIGN KEY (art_id) REFERENCES articles(id)
    );
    """
    try:
        cur.execute(query)
        conn.commit()
        return("Tables created successfully.")
    except (Exception, psycopg2.Error) as error:
        return "Error creating tables: " + str(error) 


def drop_tables():
    try:
        tables = ["achats", "ventes", "bilan", "articles"]
        for table in tables:
            cur.execute(f"DROP TABLE IF EXISTS {table};")

        conn.commit()  # Commit the transaction
        return "Tables deleted successfully."

    except (Exception, psycopg2.Error) as error:
        return "Error deleting tables: " + str(error)





def read_excel(excel_path):
    global data 
    data = pd.read_excel(excel_path, sheet_name = None)
    
    for sheet_name, df in data.items():
        print (f"Sheet Name: {sheet_name}")
        print(df)

def fill_bilan_table():
    achat_dict = {}
    achats_grouped = data['Achats'].groupby('id')['qte'].sum()

    for id in achats_grouped.index:
        qte_total = achats_grouped[id]
        
        prx_total = round(qte_total * data['Articles'].loc[data['Articles']['id'] == id, 'pu'].iloc[0], 2)
        
        achat_dict[id] = {'qte_total': qte_total, 'prx_total': prx_total}

    vent_dict = {}
    ventes_grouped = data['Ventes'].groupby('id')['qte'].sum()

    for id in ventes_grouped.index:
        qte_total = ventes_grouped[id]
        
        prx_total = round(qte_total * data['Articles'].loc[data['Articles']['id'] == id, 'pu'].iloc[0], 2)
        
        vent_dict[id] = {'qte_total': qte_total, 'prx_total': prx_total}


    bilan_dict = {}

    for a in achat_dict.keys():
        bilan_dict[a] = []
        if a in vent_dict:
            bilan_dict[a].append(achat_dict[a]['qte_total'] - vent_dict[a]['qte_total'])
        else:
            bilan_dict[a].append(achat_dict[a]['qte_total'])

        libelle = data['Articles'].loc[data['Articles']['id'] == a, 'libelle'].iloc[0]
        bilan_dict[a].append(libelle)
    
    bilan_df = pd.DataFrame.from_dict(bilan_dict, orient='index', columns=['qte_actuelle', 'libelle'])

    bilan_df.reset_index(inplace=True)

    bilan_df.columns = ['art_id', 'qte_actuelle', 'libelle']

    query = "INSERT INTO bilan (num, art_id, qte_actuelle, libelle) values"
        
    for index, row in bilan_df.iterrows():
        query += f"\n ({index},  {row['art_id']}, {row['qte_actuelle']}, '{row['libelle']}'),"
    query = query[:-1]
    query += ";"
    return(query)

def fill_artice_table():
    query  = "INSERT INTO articles (id, libelle, pu) values"
    
    for index, row in data['Articles'].iterrows():
        query += f"\n({row['id']}, '{row['libelle']}', {row['pu']}),"
    query = query[:-1]
    query += ";"
    return(query)


def fill_achat_table():
    query  = "INSERT INTO achats (num, art_id, qte, date) values"
    
    for index, row in data['Achats'].iterrows():
        query += f"\n({row['num']}, {row['id']}, {row['qte']}, '{row['date']}'),"
    query = query[:-1]
    query += ";"
    return(query)

def fill_vent_table():
    query  = "INSERT INTO ventes (num, art_id, qte, date) values"
    
    for index, row in data['Ventes'].iterrows():
        query += f"\n({row['num']}, {row['id']}, {row['qte']}, '{row['date']}'),"
    query = query[:-1]
    query += ";"
    return(query)



def main():
    # Connect to the database
    connect_db("mini_projet_1", "postgres", "postgres", "localhost", "5432")

    # Create tables
    create_tables()

    # Read data from Excel file
    read_excel(path)

    # Fill the 'articles' table
    article_query = fill_artice_table()
    cur.execute(article_query)
    conn.commit()

    # Fill the 'achats' table
    achat_query = fill_achat_table()
    cur.execute(achat_query)
    conn.commit()

    # Fill the 'ventes' table
    vent_query = fill_vent_table()
    cur.execute(vent_query)
    conn.commit()

    # Fill the 'bilan' table
    bilan_query = fill_bilan_table()
    cur.execute(bilan_query)
    conn.commit()


    print('\nDropping tables now ...')
    time.sleep(120)


    drop_tables()

    # Disconnect from the database
    disconnect_db()
    print('\nDisconnected now, goodbye !')
    time.sleep(5)
    
    exit()



if __name__ == "__main__":
    main()
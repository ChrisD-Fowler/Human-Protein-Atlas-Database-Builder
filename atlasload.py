import json 
import sqlite3

# Intro Screen
print('\nWelcome to the Human Protein Atlas database building tool!')
print('''
-. .-.   .-. .-.   .-. .-.   .
  \\   \\ /   \\   \\ /   \\   \\ /
 / \\   \\   / \\   \\   / \\   \\
~   `-~ `-`   `-~ `-`   `-~ `-       
''')
print('Version 1.0')

# Prompts user for JSON and SQL filenames, adds file extension if needed
jsonfname = input('\nWhat is the name of the Human Protein Atlas JSON file you wish to load? ')
if not jsonfname.endswith('.json') :
    jsonfname += '.json'

sqlfname = input('What do you want the SQLite database file name to be? ')
if not sqlfname.endswith('.sqlite') :
    sqlfname += '.sqlite'

# Establishes database connection and cursor variable
conn = sqlite3.connect(sqlfname)
cur = conn.cursor()

# Attempts to open the JSON file with 'except' handling most common errors
try :
    with open(jsonfname, 'r', encoding='utf-8') as fhand :
        data = fhand.read()
    atlas_js = json.loads(data) 
except FileNotFoundError :
    print(f'The file {jsonfname} could not be found! Please check name and try again.')
    exit()
except json.JSONDecodeError :
    print(f'The file did not contain valid JSON data.')
    exit()
except Exception as e :
    print(f'The following error occurred: {e}')
    exit()

# Builds Protein Atlas Database
print(f'\nStep 1! Attempting to create database {sqlfname}.')
try :
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Genes (
        gene_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        gene_name VARCHAR,
        ens_desc VARCHAR,
        gene_desc VARCHAR,
        uniprot VARCHAR
    );
    ''')
            
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Proteins (
        prot_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        position VARCHAR,
        gene_name VARCHAR,
        chromosome VARCHAR,
        prot_class VARCHAR,
        FOREIGN KEY (gene_name) REFERENCES Genes(gene_name)  
    );
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS Prognostics (
        prog_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        prog_name VARCHAR,
        gene_name VARCHAR,
        prog_type VARCHAR,
        is_prog BOOLEAN,
        p_val FLOAT,
        FOREIGN KEY (gene_name) REFERENCES Genes(gene_name)
    );
    ''')
    conn.commit()

except sqlite3.OperationalError as e :
    print(f'A database Operational Error occurred while creating database {sqlfname}: {e}')
except sqlite3.DatabaseError as e :
    print(f'The following Database Error occurred while creating database {sqlfname}: {e}')

# This loop extracts data from atlas_js and writes to the SQL database
print(f'Step 2! Parsing JSON data from {jsonfname} and writing to {sqlfname} now...')
try : 
    for record in atlas_js :
        # Genes data parse
        gene_name = record['Gene']
        ens_desc = record['Ensembl']
        gene_desc = record['Gene description']
        uniprot = record['Uniprot']
        uniprot_str = ', '.join(uniprot)
       
        # Insert Gene data
        cur.execute('''INSERT INTO Genes (gene_name, ens_desc, gene_desc, uniprot)
                    VALUES (?, ?, ?, ?)''', (gene_name, ens_desc, gene_desc, uniprot_str))

        # Proteins data parse
        position = record['Position']
        chromosome = record['Chromosome']
        prot_class = record['Protein class']
        # Enables multiple protein classes to be extracted and written to the database
        prot_class_str = ', '.join(prot_class) 
        
        # Insert Protein data
        cur.execute('''INSERT INTO Proteins (position, gene_name, chromosome, prot_class)
                    VALUES (?, ?, ?, ?)''', (position, gene_name, chromosome, prot_class_str))

        # Prognostics data parse
        prognostics = [] 
        for key, value in record.items() :
            if isinstance(value, dict) : 
                if key.startswith('Pathology prognostics') :
                    prog_name = key.split(' - ')[1]
                    prog_details = {
                        'gene_name': record['Gene'],
                        'prog_name': prog_name, 
                        'prog_type': value.get('prognostic type', 'Unknown'),
                        'is_prog': value.get('is_prognostic', False),
                        'p_val': value.get('p_val', None)
                    }
                    prognostics.append(prog_details)
        
        # Insert Prognostics data
        for prognostic in prognostics :
            cur.execute('''INSERT INTO Prognostics (gene_name, prog_name, prog_type, is_prog, p_val)
            VALUES (?, ?, ?, ?, ?)''', (gene_name, prognostic['prog_name'], prognostic['prog_type'], prognostic['is_prog'], prognostic['p_val']))
    
    # Writes all data to the database
    print(f'Step 3! Committing all changes to {sqlfname}...ENGAGE!')
    conn.commit()

except sqlite3.IntegrityError as e :
    print(f'Database integrity error: {e}')
except sqlite3.OperationalError as e :
    print(f'A database Operational Error occurred while writing to database {sqlfname}: {e}')
except sqlite3.DatabaseError as e :
    print(f'The following Database Error occurred while writing to database {sqlfname}: {e}')
finally :
    cur.close() 
    conn.close()

print(f'\nThe JSON data has been read from {jsonfname} and {sqlfname} has been created and populated!')

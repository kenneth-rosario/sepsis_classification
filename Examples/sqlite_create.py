import csv, sqlite3, os
BASE_DIR = os.path.abspath(__file__).replace("sqlite_create.py", "data")
BASE_DIR_SUB = BASE_DIR + "/"
DB_NAME = "data.db"


def csv_reader(filename):
    '''
        Simple function to read file and return csv_reader
    '''
    with open(BASE_DIR_SUB + filename, 'r') as to_extract:
            csv_reader = csv.reader(to_extract)
            return csv_reader


def csv_generator():
    ''' 
        Iterator that returns a csv_reader and the name of the csv file
        from the data folder 
    '''
    for file_ in os.listdir(BASE_DIR):
        if file_.endswith(".csv"):
            with open(BASE_DIR_SUB + file_, 'r') as to_extract:
                csv_reader = csv.reader(to_extract)
                yield csv_reader, file_.replace(".csv", "")



def create_db_connection(db_file):
    '''
        function which returns the connection to db_file
    '''
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)
    return None


def generate_table_sql(header, _filename):

    '''
        param header: header of csv_file
        param _filename: csv's filename 
        function used to produce CREATE SQL STATEMENT 

         Iterate over each column in header and create either a primary key if name is ROW_ID,
            or an integer if the column name contains ID or a regular text
    '''

    return (
        "CREATE TABLE IF NOT EXISTS " + _filename + "(\n" + 
            "".join(map(lambda x: "\t" + x + " integer PRIMARY KEY,\n" if x == "ROW_ID" 
            else "\t" + x + " integer NOT NULL,\n" if "ID" in x 
            else "\t" + x + " text NOT NULL,\n" 
            , header))[:-2] + "\n);"
    )

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def generate_insert_sql(row, _filename, header):
    
    '''
        Insert sql statement generator 
    '''

    return (
        "INSERT INTO " +_filename + "( "
            + "".join(map( lambda x:x+"," , header))[:-1] + " )\n"
                + "VALUES (\n" + "".join(map(lambda x: x+"," if is_number(x) 
                    else "'" + x.replace("'", "`") + "'," 
                    , row))[:-1] +");" 
    )
    
def import_try():
    conn = create_db_connection(DB_NAME)
    if conn is not None:
        c = conn.cursor()
        c.execute(".mode csv")
        for file_ in os.listdir(BASE_DIR):
            c.execute(".import %s %s".format(BASE_DIR_SUB + file_
            , file_.replace(".csv", "")))
    conn.commit()
    conn.close()

def create_db_from_csvs():
    conn = create_db_connection(DB_NAME)
    if conn is not None:
        c = conn.cursor()
        for csv_file, filename in csv_generator():
            header = next(csv_file)
            c.execute(generate_table_sql(header, filename))
            #print(generate_insert_sql(next(csv_file), filename, header))
            for row in csv_file:
                print("Inserting:", str(row) )
                c.execute(generate_insert_sql(row, filename, header))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    import_try()

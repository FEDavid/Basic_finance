# Imports
import sqlite3
from sqlite3 import Error

# Variables
database = r".\DB\py_DB.db"
payments_list = []

# Classes
class payment:
    def __init__(self, payment_name, payment_date, payment_amount):
        self.payment_name = payment_name
        self.payment_date = payment_date
        self.payment_amount = payment_amount

    def __str__(self):
        return f'{self.payment_name: <15}    {self.payment_date: <15}   £{self.payment_amount:.2f}'

    def commit_details(self):
        conn = create_connection(database)
        data = (self.payment_name, self.payment_date, self.payment_amount)
        print(data)
        conn.executemany("INSERT INTO tblPayments VALUES(NULL,?, ?, ?)", [data])
        conn.commit() # Remember to commit the transaction after executing INSERT.



# Functions and main code -----
# Setup Connection to DB or create one if none
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn



# Create table function
def create_table(conn, sql_create_tblPayments):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(sql_create_tblPayments)
    except Error as e:
        print(e)

def create_tbls():
    sql_create_tblPayments = """ CREATE TABLE IF NOT EXISTS tblPayments (
                                        id INTEGER PRIMARY KEY,
                                        payment_name text NOT NULL,
                                        payment_date text NOT NULL,
                                        payment_amount float NOT NULL
                                    ); """
    # Connect to DB
    conn = create_connection(database)

    # Create Tables
    if conn is not None:
        create_table(conn, sql_create_tblPayments)
    else:
        print("Error! cannot create the database connection.")



# View Output (DB)
def viewTbls_db():
    conn = create_connection(database)
    sql_selectQuery = """SELECT name FROM sqlite_master  
                    WHERE type='table';"""
    if conn is not None:
        c = conn.cursor()
        c.execute(sql_selectQuery)
        print(c.fetchall())
    else:
        print("Error! cannot create the database connection.")
    user_menu()



# View output (List)
def viewTbls_list():
    tblHeader = "\n{col1: <15}    {col2: <15}   {col3: <15}".format(col1="Payment name:",col2="Payment date:",col3="Payment amount:")
    print(tblHeader)
    for x in payments_list:
        print(x)
    print("")
    user_menu()



# Inserting records to list
def insert_records():
    i = 0
    valid_opt = True
    while i == 0:
        print("\nPlease enter payment details\n")
        new_payment_name = input("Please input the name of the payment: ")
        new_payment_date = input("Please input the date the payment comes out: ")
        new_payment_amount = float(input("Please input the amount of the payment: "))
        new_payment = payment(new_payment_name, new_payment_date, new_payment_amount)
        payments_list.append(new_payment)
        while valid_opt == True:
            user_select = input("\nWould you like to add more records? (Y/N)")
            match user_select:
                case "Y":
                    insert_records()
                case "N":
                    i = 1
                    valid_opt = False
                    user_menu()
                case other:
                    print("Please enter a valid option (Y/N)")



# Commiting data to Database
def commit_records():
    for x in payments_list:
        x.commit_details()
    user_menu()



# Options Menu
def user_menu():
    print("-"*30+"\n\nPayment system\n1: Insert Records\n2: Output (List)\n3: Commit records\n4: Output (DB)\n0: Quit")
    user_select = 0
    while user_select == 0:
        user_select = int(input("\nPlease choose an option from the list: "))
        match user_select:
            case 1:
                print("-"*30+"\nInserting records\n"+"-"*30)
                insert_records()
            case 2:
                print("-"*30+"\nOutput (List)\n"+"-"*30)
                viewTbls_list()
            case 3:
                print("-"*30+"\nCommit records\n"+"-"*30)
                commit_records()
            case 4:
                print("-"*30+"\nOutput (DB)\n"+"-"*30)
                viewTbls_db()
            case 0:
                print("Program closed")
                exit()
            case other:
                print('No match found')



# Running
if __name__ == '__main__':
    create_connection(database)
    create_tbls()
    user_menu()


















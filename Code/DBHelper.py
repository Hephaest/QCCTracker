import sqlite3
import csv


class DBHelper:

    def __init__(self):
        try:
            self.conn = sqlite3.connect("../Database/qcc.db")
            self.cur = self.conn.cursor()
        except:
            print("error")

    def create_table(self):
        self.cur.execute('CREATE TABLE IF NOT EXISTS Company '
                         '(c_id INTEGER PRIMARY KEY AUTOINCREMENT, '
                         'c_name VARCHAR(100) NOT NULL, '
                         'c_url VARCHAR(256));')
        self.submit_commit()

        self.cur.execute("CREATE TABLE IF NOT EXISTS Funding "
                         "(f_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                         "f_name VARCHAR(100) NOT NULL, "
                         "f_url VARCHAR(256), "
                         "c_id INTEGER, "
                         "FOREIGN KEY (c_id) REFERENCES Company(c_id));")
        self.submit_commit()

        self.cur.execute('CREATE TABLE IF NOT EXISTS Invest_Firm '
                         '(f_id INTEGER PRIMARY KEY AUTOINCREMENT, '
                         'f_name VARCHAR(100) NOT NULL, '
                         'f_url VARCHAR(256), '
                         'f_field VARCHAR(100), '
                         'f_date DATE, '
                         'f_region VARCHAR(10));')
        self.submit_commit()

    def load_data(self):
        with open('../MetaData/company.csv', mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                query = "INSERT INTO Company (c_name, c_url) VALUES (\"" + row[1] + "\", NULL);"
                self.cur.execute(query)
        self.submit_commit()

    def get_companies(self):
        self.cur.execute("SELECT c_name From Company WHERE c_url IS NULL LIMIT 1000")
        return self.cur.fetchall()

    def set_company_url(self, name, url):
        query = "UPDATE Company set c_url = \"" + url + "\" WHERE c_name = \"" + name + "\";"
        print(query)
        self.cur.execute(query)
        self.submit_commit()

    def get_not_found_funding_company_name(self):
        self.cur.execute("SELECT f_name FROM Company_Union_Invest_Firm WHERE f_name IS NOT NULL AND f_url is Null GROUP BY f_name;")
        return self.cur.fetchall()

    def get_company_id(self, name):
        query = "SELECT c_id From Company WHERE c_name = \"" + name + "\";"
        print(query)
        self.cur.execute(query)
        return self.cur.fetchall()

    def set_funding_info(self, name, url, c_id):
        query = "INSERT INTO Funding (f_name, f_url, c_id) VALUES (\"" + name + "\", \"" + url + "\", \"" + c_id + "\");"
        print(query)
        self.cur.execute(query)
        self.submit_commit()

    def set_firm_info(self, name, url, field, date, region):
        date = date if date != '-' else 'NULL'
        region = region if region != '-' else 'NULL'
        query = "INSERT INTO Invest_Firm (f_name, f_url, f_field, f_date, f_region) VALUES (\"" + name + "\", \"" + url + "\", \"" + field + "\", \"" + date + "\", \"" + region + "\");"
        print(query)
        self.cur.execute(query)
        self.submit_commit()

    def drop_table(self):
        self.cur.execute("DROP TABLE IF EXISTS Funding;")
        self.submit_commit()

        self.cur.execute("DROP TABLE IF EXISTS Company;")
        self.submit_commit()

        self.cur.execute("DROP TABLE IF EXISTS Invest_Firm;")
        self.submit_commit()

    def submit_commit(self):
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

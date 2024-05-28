import mysql.connector

class DbConnector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None
        
    def connect(self):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.conn.cursor()
        
    def create_table(self):
        query = '''CREATE TABLE IF NOT EXISTS `Sales` (
                    `ID` int AUTO_INCREMENT,
                    `Product` VARCHAR(255) NOT NULL,
                    `Quantity` int NOT NULL,
                    `Price` double NOT NULL,
                    `Date` datetime NOT NULL,
                    PRIMARY KEY (`ID`));'''
                    
        self.cursor.execute(query)
        self.conn.commit()
        
        
    def get_table(self):
        query = f"SELECT * FROM `Sales`"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        columns = [column[0] for column in self.cursor.description]
                
        return rows, columns


    def insert_data(self, product, quantity, price, date):
        query = '''INSERT INTO `Sales` (`Product`, `quantity`, `Price`, `Date`)
                   VALUES (%s, %s, %s, %s)'''
        values = (product, quantity, price, date)
        
        self.cursor.execute(query, values)
        self.conn.commit()

    def delete_data(self, id):
        query = "DELETE FROM Sales WHERE id = %s"
        values = (id,)

        cursor = self.conn.cursor()
        cursor.execute(query, values)
        self.conn.commit()
        
    def filter_by(self, product):
        query = f"SELECT * FROM Sales WHERE Product = '{product}'"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        columns = [column[0] for column in self.cursor.description]
                
        return rows, columns
    
    def get_summary(self, product):
        if product == "" or product == "None":
            query = f"SELECT SUM(Quantity), SUM(Quantity * Price) FROM Sales"
        else: 
            query = f"SELECT SUM(Quantity), SUM(Quantity * Price) FROM Sales WHERE Product = '{product}'"
            
        self.cursor.execute(query)
        summary = self.cursor.fetchall()[0]
        tot_quan, tot_sale = summary[0] , summary[1]
        return tot_quan, tot_sale



    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
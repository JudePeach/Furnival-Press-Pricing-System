import sqlite3
from datetime import datetime







class PrintDatabaseConnection():
    
    
    
    def __init__(self):
        """Initialize db class variables"""
        self.connection = sqlite3.connect('FurnivalPressDB.db')                                  
        self.cur = self.connection.cursor()

    def GetOrderIDForPDF(self):
        self.cur.execute("SELECT last_insert_rowid()")
        row = self.cur.fetchall()
        return row[0][0]
    def GetCustEmail(self,CustID):
        self.cur.execute("SELECT Email FROM Customers WHERE CustomerID = (?)",(CustID,))
        row=self.cur.fetchall()
        print(row)
        return row[0]




    def SearchOrders(self,OrderID,Date,CustomerID,ProductID,LowPrice,HighPrice):
        self.cur.execute("""SELECT Date, Firstname, Surname, ProductName, Price
FROM Orders
INNER JOIN Customers ON Customers.CustomerID = Orders.CustomerID
INNER JOIN OrderItem ON OrderItem.OrderID = Orders.OrderID
INNER JOIN Products ON Products.ProductID = OrderItem.ProductID
WHERE Orders.OrderID = (?) OR Date = (?) OR Orders.CustomerID = (?) OR OrderItem.ProductID = (?) OR Price BETWEEN (?) AND (?) """,(OrderID,Date,CustomerID,ProductID,LowPrice,HighPrice))
        row = self.cur.fetchall()
        print(row)
        return row
        ### The inner join allows data to be selected that is from multile tables


    def DeleteRecords(self,Table,ID):
        if Table == 'Products':
            self.cur.execute("DELETE FROM Products WHERE ProductID = (?)",(ID))
        elif Table == 'Paper':
            self.cur.execute("DELETE FROM Paper WHERE PaperID = (?)",(ID))
        elif Table == 'Machines':
            self.cur.execute("DELETE FROM Machines WHERE MachineID = (?)",(ID))
        elif Table == 'Customers':
            self.cur.execute("DELETE FROM Customers WHERE CustomerID = (?)",(ID))
        elif Table == 'Ordertable':
            self.cur.execute("DELETE FROM Orders WHERE OrderID = (?)",(ID))
   




    def GetSpend(self,DateFrom,DateUntil,CustID):
        self.cur.execute("SELECT SUM(Price) FROM Orders WHERE Date BETWEEN (?) AND (?) AND CustomerID = (?)",(DateFrom,DateUntil,CustID))##AGGREGATE FUNCTION USE
        Spend = self.cur.fetchall()
        if Spend[0][0] == None:
            return("No orders found to generate with")
        else:
            Spend = round(Spend[0][0],2)
            Spend = "{0:0.2f}".format(Spend)
            return Spend




        

    def GetAverage(self,DateFrom,DateUntil):
        self.cur.execute("SELECT AVG(Price) FROM Orders WHERE Date BETWEEN (?) AND (?)",(DateFrom,DateUntil))###AGGREGATE FUNCTION USE
        Average = self.cur.fetchall()
        if Average[0][0] == None:
            return('No orders found to generate with')
        else:
            Average = round(Average[0][0],2)
            Average = "{0:0.2f}".format(Average)
            return Average

    def GenerateRevenue(self,DateFrom,DateUntil):
        self.cur.execute("SELECT SUM(Price) FROM Orders WHERE Date BETWEEN (?) AND (?)",(DateFrom,DateUntil))####AGGREGATE FUNCTION USE
        Total = self.cur.fetchall()
        if Total[0][0] == None:
            return('No orders found to generate with')
        else:
            Total=round(Total[0][0],2)
            Total = "{0:0.2f}".format(Total)
            print(Total)
            return Total
        

    def CreateOrder(self,CustomerID,OrderID,Quote,Product):
        date = str(datetime.today().strftime('%Y-%m-%d'))
        self.cur.execute("SELECT ProductID FROM Products WHERE ProductName = (?)",(Product,))
        ProductID = self.cur.fetchall()
        
        
        self.cur.execute("INSERT INTO Orders (Date,CustomerID,Price) VAlUES(?,?,?)",
                         (date,CustomerID,Quote))
        self.cur.execute("SELECT last_insert_rowid()")
        OrderID = self.cur.fetchall()
        self.cur.execute("INSERT INTO OrderItem (ProductID,OrderID) VALUES(?,?)",(ProductID[0][0],OrderID[0][0]))
    
    def GetCustomerID(self,CustName):     ###gets the customer id so that their details can be used in quote#####
        CustName = CustName.split(" ")
        self.cur.execute("SELECT CustomerID FROM Customers WHERE Firstname = (?) and Surname = (?)",(CustName))
        CustID = self.cur.fetchall()
        print(CustID)

        if len(CustID) ==0:
            print("Customer does not exist please enter name again")
        else:
            print(CustID[0][0])
            #CustID = CustID[0][0]
        return CustID

    def InsertIntoTable(self,Content,Table): #####Used for database additions#####
        if Table == 'Products':
            self.cur.execute("INSERT INTO Products (ProductName,Description,MachineID,PaperID,CostPerPage) VALUES(?,?,?,?,?)",
                             (Content))
        elif Table == 'Paper':
            self.cur.execute("INSERT INTO Paper (Supplier,WeightGsm,Size,Finish,CostPerSheet) VALUES (?,?,?,?,?)",
                            (Content))
        elif Table == 'Machines':
            self.cur.execute("INSERT INTO Machines (Name,Description,Automated,CostPerPrint) VALUES (?,?,?,?)",
                            (Content))
        elif Table == 'Customers':
            self.cur.execute("INSERT INTO Customers (Firstname,Surname,Email,Phone) VALUES (?,?,?,?)",
                            (Content))
        elif Table == 'Ordertable':
            self.cur.execute("INSERT INTO Orders (Date,CustomerID,Quote,OrderitemID) VALUES (?,?,?,?)",
                            (Content))
            
  


    def GetProductCosts(self,Product):
        self.cur.execute("SELECT CostPerPage FROM Products WHERE ProductName = (?)",(Product,))
        CostPerPage = self.cur.fetchall() ###Gets the cost per page which is determined by the product#####
        print(CostPerPage)
        return CostPerPage


    def GetCostPerPrint(self,Press):
        
        self.cur.execute("SELECT CostPerPrint FROM Machines WHERE Name = (?) ",(Press,)) ###Gets the cost for every sheet that is processed through a machine####
        cost = self.cur.fetchall()
        print(cost)
        return cost
    def GetCostPerSheet(self,Size,PaperType):
        self.cur.execute("SELECT CostPerSheet FROM Paper WHERE Size = (?) and WeightGsm = (?)",(Size,PaperType,))
        sheetcost = self.cur.fetchall()
        print(sheetcost)
        return sheetcost #### Gets the cost per sheet of paper####




   

    def LoginDB(self,UsernameIN,PasswordIN): ###Validates username and password#####
        
        self.cur.execute("SELECT * FROM Users WHERE Username = (?) AND Password=(?)",(UsernameIN,PasswordIN))
        row = self.cur.fetchone()
        print(row)
        if row:
            Valid = True
        else:
            Valid = False
        print(Valid)
        
        return Valid
         

    def close(self):
        """close sqlite3 connection"""
        self.connection.close()

    def ForeignON(self):
        self.cur.execute("PRAGMA foreign_keys = ON")###In sqlite this has to be on to use foreign keys###
                         

    def executeUser(self,UserID,UserName,Password,AccessLevel):
        #"""execute a row of data to current cursor"""
        #sqlstatement = new_data+','+values
        #new_data = "INSERT INTO Users(UserID,Username,Password,Accesslevel) VALUES(?,?,?,?)", (UserID,UserName, Password,AccessLevel)
        self.cur.execute("INSERT OR IGNORE INTO Users(Username,Password) VALUES(?,?)", (UserName, Password)) ## creates new users##
        


    def executemany(self, many_new_data):
        """add many new data to database in one go"""
        self.create_table()
        self.cur.executemany('REPLACE INTO jobs VALUES(?, ?, ?, ?)', many_new_data)

    def create_table(self):
        self.ForeignON()
        #sql = """create table Product(ProductID integer, Product string, Width (mm) integer, Height (mm) integer,Description string, primary key(UserID))"""
        
        
        #"""create a database table if it does not exist already"""
        #self.cur.execute("""create table Machines(MachineID string, Name string, Description string, Automated boolean, CostPerPrint float, primary key(MachineID))""")
        #self.cur.execute("""create table Paper(PaperID string, Supplier string, PackSize integer, CostPerPack float, WeightGsm float, Size string, Finish string, primary key(PaperID))""")
        self.cur.execute("""create table OrderItem(OrderitemID string, ProductID string, OrderID string,quantity integer, primary key(OrderitemID), foreign key(OrderID) references Ordertable(OrderID),foreign key(ProductID) references Products(ProductID))""")
    def commit(self):
        """commit changes to database"""
        self.connection.commit()
    


DB1 = PrintDatabaseConnection()
#DB1.GenerateRevenue('2023-02-09','2023-02-10')
#DB1.GetCostPerPrint("Xerox")
#DB1.CreateOrder('4','5000','5000')
#DB1.SearchOrders(2,2,2)
#DB1.GetCustomerID("jude peac")
#DB1.ForeignON()
#DB1.create_table()
#DB1.execute()
#DB1.SearchOrders(133,'-03-25',122,122,122,60000)
#DB1.CreateOrder('2022','3',4000,'Leaflet')
DB1.commit()


       

from tkinter import *
from tkinter import ttk
from fpdf import FPDF
import random
import tkinter.messagebox
from tkinter import messagebox
import datetime
import tkinter as tk
from functools import partial
from tkinter import messagebox
import sqlite3
import DB as db
#import PDFgen
####Above are all of the imports that are used for the program










class Stock_Management_System(tk.Tk):

    def __init__(self, root):
        #####Setting the window up ######
        self.root = root
        self.root.title("Printing Press Stock System 2022")
        self.root.resizable(width=False,height=False)
        self.root.geometry("1280x690+0+0")
        self.root.configure(background='lightblue1')
    


        UserNameIN = StringVar()
        PasswordIN = StringVar()
       
###initialising the main frame where all other sub frames will be stored inside of###################
        LoginFrame = Frame(self.root,bd=18,width=1350,height=750,bg='lightblue1',padx=499,pady = 250,relief=RIDGE)
        LoginFrame.grid()



        self.lblUserName=Label(LoginFrame, font=('arial',18,'bold'),bg='lightblue1', text='User Name:').grid(row=0,column=1,sticky=W)

        self.txtinputUserName = Entry(LoginFrame, textvariable = UserNameIN, font=('arial',16,'bold'), bd=2,
                                  fg='black',width=20,justify=LEFT,relief=RIDGE).grid(row=1,column=1)

        self.lblPassword =Label(LoginFrame,font=('arial',18,'bold'),bg='lightblue1',text='Password:').grid(row=2,column=1,sticky=W)

        self.txtinputPassword = Entry(LoginFrame,textvariable= PasswordIN, font=('arial',16,'bold'),bd=2,fg='black',width=20,show='*',justify=LEFT,relief=RIDGE).grid(row=4,column=1,sticky=W)

####Above are the text boxes for login details to be entered####



        MainFrame = Frame(self.root, bd = 10, width = 1350, height = 700, bg="black",padx=2,pady=2,relief=RIDGE)

        #MainFrame.grid()
        self.Frames =[]
        self.Frames.append(MainFrame)

        def OpenMainFrame(): ####Opens the main menu after login
            MainFrame.grid()
            LoginFrame.destroy() ##destroys login frame
            self.root.geometry('1775x1327+0+0')


        def AddUser(UserName, Password, AccessLevel, UserID):

            
            db.DB1.executeUser(UserID,UserName,Password,AccessLevel)  ##See db.py file
            db.DB1.commit()


            
        def ValidateLogin2(UserNameIN,PasswordIN):
            UserNameIN = UserNameIN.get()
            PasswordIN = PasswordIN.get()
            #Valid=False
            valid = db.DB1.LoginDB(UserNameIN,PasswordIN) ## see db.py file
            
            if valid==True:##If the username and password are correct, it runs the open main frame function
                OpenMainFrame()
            elif valid==False:
                
                messagebox.showinfo('info','incorrect username or password') ###Small pop up window with an error message
                

            


        ValidateLogin2 = partial(ValidateLogin2, UserNameIN, PasswordIN)
        login = Button(LoginFrame, padx=2,pady=2,fg='black',font=('arial',8,'bold'),text='Login', width =5,height=2,command=ValidateLogin2)##When this button is pressed, the login is checked
        login.grid(row=5, column=1)
#####Function to shut all windows and end the program#####
        def iExit():
            iExit = tkinter.messagebox.askyesno("Furnival Press", "Confirm you want to exit")
            if iExit > 0:
                root.destroy()###Destroys all windows
                quit()###Ends the running of the py file
            return

       


      #####The main function where quotes are created
       
        def QuoteWindow():
            machine_window = Tk()  ###Creating the window
            machine_window.title('Press settings')
            machine_window.configure(width=500,height=300)
            machine_window.configure(bg='lightblue1')
            machine_window.resizable(width=False,height=False)
            
                

            def SaveQuote():
                ##gets all of the data from the entry boxes etc##
                Colour = cboColour.get()
                FilmPlates = cboFilmPlates.get()
                Press = cboPress.get()
                Keeps = txtNoKeeps.get()
                TypeOfJob = cboTypeOfJob.get()
                FinishedSize = cboFinishedSize.get()
                Size = cboSize.get()
                Pages = txtPages.get()
                PrePress = txtPrePress.get()
                Finishing = cboFinishing.get()
                PaperType = cboPaperType.get()
                NoFolds = txtFolds.get()
                Copies = txtNoCopies.get()
                CustName = txtCustName.get()
                

                
                
                CustomerID = db.DB1.GetCustomerID(CustName) ###Gets the relevant customer ID from their name so it can be used when creating order
              
                
                if CustomerID == None: ##Returns an error if no match is found
                    messagebox.showinfo(title='Error',message='Customer details do not exist, please make a new customer in database settings')
                                    
                
               
                    
                
                GenerateNewQoute(Press,FinishedSize,Size,Keeps,Copies,PaperType,TypeOfJob,PrePress,Finishing,Colour,CustomerID,OrderID,CustName)
                return Press,Colour,FilmPlates
            
 

              ##initialising all of the variables##
            Colour = StringVar()
            FilmPlates = StringVar()
            Keeps = StringVar()
            TypeOfJob = StringVar()
            FinishedSize = StringVar()
            Pages = StringVar()
            PrePress=StringVar()
            Finishing = StringVar()
            PaperType = StringVar()
            NoFolds = StringVar()
            CustName = StringVar()
            CustEmail = StringVar()
            CustPhone = StringVar()
            CustID=StringVar()
            OrderID = StringVar()
                                         
            ####machine optns##

            lblMachineopt = Label(machine_window,font=('arial',11,'bold'),text='Machine options:',padx=2,pady=2,bg='lightblue1').grid(row=0,column=0,sticky=W)


            lblColour = Label(machine_window,font=('arial',9,'bold'),text= 'Colour option:',padx = 2, pady = 2, bg = 'lightblue1')
            lblColour.grid(row=1,column=0,sticky = W)
            cboColour = ttk.Combobox(machine_window,textvariable=Colour,state='readonly',
                                     font=('arial',8,'bold'))
            cboColour['value'] = ['Select an option:','Full colour','Black and white']
            cboColour.current(0)
            cboColour.grid(row = 1,column=1,sticky = W)


            lblFilmPlates = Label(machine_window,font=('arial',9,'bold'),text= 'Film/Plates:',padx = 2, pady = 2, bg = 'lightblue1')
            lblFilmPlates.grid(row=2,column=0,sticky=W)
            cboFilmPlates = ttk.Combobox(machine_window,textvariable=FilmPlates,state='readonly',
                                     font=('arial',8,'bold'))
            cboFilmPlates['value'] = ['Select an option:', 'Yes', 'No']
            cboFilmPlates.current(0)
            cboFilmPlates.grid(row=2, column=1, sticky=W)

            lblPress = Label(machine_window,font=('arial',9,'bold'),text= 'Printing Press:',padx = 2, pady = 2, bg = 'lightblue1')
            lblPress.grid(row=3,column=0,sticky=W)
            cboPress = ttk.Combobox(machine_window, textvariable=Press, state='readonly',
                                         font=('arial', 8, 'bold'))
            cboPress['value'] = ['Select an option:', 'Xerox', 'Epson','Konica 217','HP 17']
            cboPress.current(0)
            cboPress.grid(row=3, column=1, sticky=W)
            
####copy options######
            lblCopyoptn = Label(machine_window,font = ('arial',11,'bold'),text='Copy options:',padx=2,pady=2,bg='lightblue1').grid(row=4,column=0,sticky=W)


            lblNoCopies = Label(machine_window, font = ('arial',9,'bold'),text = 'Number of copies:', padx=2,pady=2, bg='lightblue1')
            lblNoCopies.grid(row=5,column=0,sticky=W)
            txtNoCopies = Entry(machine_window,textvariable=NoCopies,font=('arial',8,'bold'), bd=2, fg='black',width=20,justify=LEFT)
            txtNoCopies.grid(row=5,column=1,sticky=W)

            lblNoKeeps = Label(machine_window, font=('arial', 9, 'bold'), text='Number of preview copies:', padx=2, pady=2,
                                bg='lightblue1')
            lblNoKeeps.grid(row=6, column=0, sticky=W)
            txtNoKeeps = Entry(machine_window, textvariable=Keeps, font=('arial', 8, 'bold'), bd=2, fg='black',
                                width=20, justify=LEFT)
            txtNoKeeps.grid(row=6, column=1, sticky=W)





###product options###
            lblproductoptn = Label(machine_window,font=('arial',11,'bold'),text = 'Product options:',padx=2,pady=2,bg='lightblue1').grid(row=7,column=0,sticky=W)

            
            lblTypeOfJob = Label(machine_window,font =('arial',9,'bold'),text='Job:',padx =2, pady=2,bg='lightblue1')
            lblTypeOfJob.grid(row=8,column=0,sticky=W)
            cboTypeOfJob = ttk.Combobox(machine_window,textvariable = TypeOfJob, state = 'readonly',
                                        font = ('arial',8,'bold'))
            cboTypeOfJob['value'] = ['', ' Select an option', 'Leaflet', 'Business cards', 'Ring binded books','Menus']
            cboTypeOfJob.current(0)
            cboTypeOfJob.grid(row=8,column=1)

            lblPages = Label(machine_window,font=('arial',9,'bold'),text='Pages/Planes/Folds:',padx=2,pady=2,bg='lightblue1')
            lblPages.grid(row=9,column=0,sticky=W)
            txtPages = Entry(machine_window,textvariable=Pages, font=('arial',8,'bold'), bd=2,
                                  fg='black',width=20,justify=LEFT)
            txtPages.grid(row=9,column=1)

            lblPrePress = Label(machine_window,font=('arial',9,'bold'),text = 'Pre press costs:',padx=2,pady=2,bg='lightblue1')
            lblPrePress.grid(row=10,column=0,sticky=W)
            txtPrePress=Entry(machine_window,textvariable=PrePress,font=('arial',8,'bold'),bd=2,fg='black',width=20,justify=LEFT)
            txtPrePress.grid(row=10,column=1)

            lblFinishing = Label(machine_window,font=('arial',9,'bold'),text='Finishes:',padx=2,pady=2,bg='lightblue1')
            lblFinishing.grid(row=11,column=0,sticky=W)
            cboFinishing = ttk.Combobox(machine_window, textvariable=Finishing, state='readonly',
                                        font=('arial', 8, 'bold'))
            cboFinishing['value'] = ['', ' Select and option:', 'Guillotining', 'Saddle stitching']
            cboFinishing.current(0)
            cboFinishing.grid(row=11,column=1)

           
            lblFinishedSize = Label(machine_window,font=('arial',9,'bold'),text='Finished Size:',padx=2,pady=2,bg='lightblue1')
            lblFinishedSize.grid(row=12,column=0,sticky=W)
            

            cboFinishedSize = ttk.Combobox(machine_window, textvariable = FinishedSize,state='readonly',
                                           font=('arial',8,'bold'))
            cboFinishedSize['value']=['','Select an option:','a5','sra5','a4','sra4','a3','sra3','a2','sra2','a1','sra1']
            cboFinishedSize.current(0)
            cboFinishedSize.grid(row=12,column=1)
            
###sizing options#####

            lblSizeoptn = Label(machine_window,font=('arial',11,'bold'),text='Size options:',padx=2,pady=2,bg='lightblue1').grid(row=13,column=0,sticky=W)

            
            lblSize = Label(machine_window,font=('arial',9,'bold'),text = 'Job size:',padx=2,pady=2,bg='lightblue1')
            lblSize.grid(row=14,column=0,sticky=W)
            cboSize = ttk.Combobox(machine_window,textvariable = Papersize, state = 'readonly',
                                        font = ('arial',8,'bold'))
            cboSize['value']=['Select an option:','a5','sra5','a4','sra4','a3','sra3','a2','sra2','a1','sra1']
            cboSize.current(0)
            cboSize.grid(row=14,column=1,sticky=W)

            lblPaperType = Label(machine_window,font=('arial',9,'bold'),text='Paper type:',padx=2,pady=2,bg='lightblue1')
            lblPaperType.grid(row=15,column=0,sticky=W)
            cboPaperType = ttk.Combobox(machine_window,textvariable = PaperType, state = 'readonly',
                                        font = ('arial',8,'bold'))
            cboPaperType['value'] = ['Select an option:','130 gsm','Silk Coated 130gsm','Silk Coated 150gsm',
                                     'Silk Coated 170gsm','Silk Coated 250gsm','Silk Coated 300gsm','Silk Coated 350gsm','Silk Coated 400gsm','Uncoated 100gsm',
                                     'Uncoated 120gsm','Uncoated 135gsm',
                                     'Uncoated 160gsm','Uncoated 190gsm','Uncoated 240gsm','Uncoated 300gsm','Uncoated 340gsm','...']
            cboPaperType.current(0)
            cboPaperType.grid(row=15,column=1,sticky=W)

            lblFolds = Label(machine_window,font=('arial',9,'bold'),text='Panels/Folds/Pages:',padx=2,pady=2,bg='lightblue1')
            lblFolds.grid(row=16,column=0,sticky=W)
            txtFolds = Entry(machine_window,textvariable=NoFolds,font=('arial', 8, 'bold'), bd=2, fg='black',
                                width=20, justify=LEFT)
            txtFolds.grid(row=16,column=1,sticky=W)

###Customer options####
            lblCustoptn = Label(machine_window,font=('arial',11,'bold'),
                                text='Customer options:',padx=2,pady=2,bg='lightblue1').grid(row=17,column=0,sticky=W)
            lblCustName = Label(machine_window,font=('arial',9,'bold'),
                                text='Customers first and last name',padx=2,pady=2,bg='lightblue1').grid(row=18,column=0,sticky=W)
            
            txtCustName = Entry(machine_window,textvariable = CustName,font=('arial',8,'bold'),bd=2,fg='black',
                                width=20,justify=LEFT)
            txtCustName.grid(row=18,column=1)

          
        
            

            
        
            
###generate quote button####
            btnGenerateQuote = Button(machine_window,padx=3, pady=2, bd=4, fg='black',
                                      font=('arial', 8, 'bold'), width=109, height=1, bg='gainsboro', text='Create New Quote.',command=SaveQuote)
            btnGenerateQuote.grid(row=24,column=0,sticky=W)




            machine_window.mainloop()
            return Press,Colour,FilmPlates




#####Provides the user with a window to generate revenue and averagers of prices#######

        def InsightsWindow():
            InsightsWIN = Tk()##Creating the window
            InsightsWIN.title('Insights')
            InsightsWIN.configure(bg='lightblue1')
            InsightsWIN.configure(width=500,height=300)

            DateFrom = StringVar()
            DateUntil = StringVar()
            CustName = StringVar()


            def CalculateCustSpend(): ###This function allows for a customers total spend to be calculated, between two dates
                DateFrom = txtFromDate.get()
                DateUntil = txtUntilDate.get()
                CustName = txtCustName.get()
                CustID = db.DB1.GetCustomerID(CustName)##See database file
                if len(CustID) == 0:  ##CustID will produce a 2D list, if it is empty then no customer was found meaning its length would be 0

                    messagebox.showinfo(title='Error occurred',message = 'Customer does not exist')
                else:
                    Spend = db.DB1.GetSpend(DateFrom,DateUntil,CustID[0][0])  ###See database file
                    messagebox.showinfo(title='Customers spend',message=('Between '+ DateFrom+' and '+DateUntil+ " "+ CustName+' Spent a total of: £'+Spend))
                

            def SaveAvg(): ##This function allows user to calculate the average quote prices between two dates
                DateFrom = txtFromDate.get()
                DateUntil = txtUntilDate.get()
                Average = db.DB1.GetAverage(DateFrom,DateUntil)
                messagebox.showinfo(title='Average revenue',message=('Between '+ DateFrom+' and '+DateUntil+' You generated and average of per quote: £'+Average))
                

            def SaveRevenue(): ##Adds up all of the quotes between two dates so user can calculate profit margins
                DateFrom = txtFromDate.get()
                DateUntil = txtUntilDate.get()
                Revenue = db.DB1.GenerateRevenue(DateFrom,DateUntil)
                messagebox.showinfo(title='Revenue',message=('Between '+ DateFrom+' and '+DateUntil+' You generated: £'+Revenue))

            lblDate = Label(InsightsWIN,font = ('arial',9,'bold'),text='Date window:',padx=2,pady=2,bg='lightblue1').grid(row=0,column=0,sticky=W)

            txtFromDate = Entry(InsightsWIN, textvariable = DateFrom, font = ('arial',8,'bold'),bd=2,fg='black',
                                width=10,justify=LEFT)
            txtFromDate.grid(row=0,column=1,sticky=W)

            txtUntilDate = Entry(InsightsWIN,textvariable = DateUntil,font=('arial',8,'bold'),bd=2,fg='black',
                                 width=10,justify=LEFT)
            txtUntilDate.grid(row=0,column=3,sticky=W)

            btnGenRev = Button(InsightsWIN,padx=3,pady=2,bd=4, fg='black',font=('arial',9,'bold'),width=25,height=1,bg='gainsboro',
                               text='Generate Revunue for this period',
                               command=SaveRevenue)
            btnGenRev.grid(row=1,column=0)

            

           

            btnGenAvg = Button(InsightsWIN,padx=3,pady=2,bd=4, fg='black',font=('arial',9,'bold'),width=25,height=1,bg='gainsboro',
                               text='Generate Average for this period',
                               command=SaveAvg)
            btnGenAvg.grid(row=3,column=0)



            lblCustomersSpend = Label(InsightsWIN, font = ('arial',9,'bold'),
                                      text='Calculate customers total spend in these dates:',padx=2,pady=2,bg='lightblue1').grid(row=4,column=0)
            txtCustName = Entry(InsightsWIN,textvariable = CustName,font=('arial',8,'bold'),bd=2,fg='black',
                                 width=10,justify=LEFT)
            txtCustName.grid(row=4,column=1)
            btnCalculateCustSpend = Button(InsightsWIN,padx=3,pady=2,bd=4, fg='black',font=('arial',9,'bold'),width=25,height=1,bg='gainsboro',text='Generate',
                               command=CalculateCustSpend)
            btnCalculateCustSpend.grid(row=5,column=0)
            
                               



            
#####Allows for past orders to be searched for based on multiple factors, the order is then displayed and the pdf can be gathered####
            

        
        def ViewOrders():
            ViewOrderWIN = Tk()##Creating the window
            ViewOrderWIN.title('View Orders/invoices')
            ViewOrderWIN.configure(bg='lightblue1')
            ViewOrderWIN.configure(width=500,height=300)

            Filter = StringVar()
            OrderID = StringVar()
            Date = StringVar()
            Customer = StringVar()
            Product = StringVar()
            LowPrice = StringVar()
            HighPrice=StringVar()

            ####orderID filters/fields####
            orderID = Label(ViewOrderWIN,font=('arial',9,'bold'),text = 'Enter OrderID:',padx=2,pady=2,bg='lightblue1')
            txtorderID = Entry(ViewOrderWIN, textvariable=OrderID,font=('arial', 8, 'bold'), bd=2, fg='black',
                                width=10, justify=LEFT)#

            ###date filters/fields######

            lbldate = Label(ViewOrderWIN, font=('arial',9,'bold'),text='Enter date (YYYY-MM-DD):',padx=2,pady=2,bg='lightblue1')
            txtdate = Entry(ViewOrderWIN,textvariable = Date, font = ('arial',9,'bold'),bd=2,fg='black',width=10,justify=LEFT)

            ####Customer filters/fields####
            lblCustomer = Label(ViewOrderWIN, font=('arial',9,'bold'),text='Enter CustomerID:',padx=2,pady=2,bg='lightblue1')
            txtCustomer = Entry(ViewOrderWIN,textvariable = Customer, font = ('arial',9,'bold'),bd=2,fg='black',width=10,justify=LEFT)

            #####Product fikters/fields###
            lblProduct = Label(ViewOrderWIN, font=('arial',9,'bold'),text='Enter ProductID:',padx=2,pady=2,bg='lightblue1')
            txtProduct = Entry(ViewOrderWIN,textvariable = Product, font = ('arial',9,'bold'),bd=2,fg='black',width=10,justify=LEFT)
            ####Price Filters/Fields####
            lblLowPrice = Label(ViewOrderWIN, font=('arial',9,'bold'),text='Enter Lowest Price (£):',padx=2,pady=2,bg='lightblue1')
            txtLowPrice =  Entry(ViewOrderWIN,textvariable = LowPrice, font = ('arial',9,'bold'),bd=2,fg='black',width=10,justify=LEFT)
            
            lblHighPrice = Label(ViewOrderWIN, font=('arial',9,'bold'),text='Enter Highest Price (£):',padx=2,pady=2,bg='lightblue1')
            txtHighPrice =  Entry(ViewOrderWIN,textvariable = HighPrice, font = ('arial',9,'bold'),bd=2,fg='black',width=9,justify=LEFT)

            def AddFilter(): ##Prints the filters out in order of selection onto the grid
                
                Filter = cboSelectFilter.get()
                print(Filter)
                if Filter == 'OrderID':
                    orderID.grid()
                    txtorderID.grid()
                elif Filter == 'Date':
                    lbldate.grid()
                    txtdate.grid()
                elif Filter == 'CustomerID':
                    lblCustomer.grid()
                    txtCustomer.grid()
                elif Filter == 'ProductID':
                    lblProduct.grid()
                    txtProduct.grid()
                elif Filter == 'Price region':
                    lblLowPrice.grid()
                    txtLowPrice.grid()
                    lblHighPrice.grid()
                    txtHighPrice.grid()


                    
            def SearchForOrder():
                ##initialising variables##
                OrderID = txtorderID.get()
                Date=txtdate.get()
                CustomerID = txtCustomer.get()
                ProductID = txtProduct.get()
                LowPrice = txtLowPrice.get()
                HighPrice = txtHighPrice.get()
                #LowPrice = float(LowPrice)
                #HighPrice = float(HighPrice)
                

                ##references database method

                orders = db.DB1.SearchOrders(OrderID,Date,CustomerID,ProductID,LowPrice,HighPrice)
                print(orders)
                if orders == []:
                    messagebox.showinfo(title='Orders:',message='No Orders Found')
                else:
                    messagebox.showinfo(title='Orders:',message=("Orders Found: \n\n" , orders ,"\n\n Orders are in the form - Date, Customer name, Product, Price"))
                

            
            cboSelectFilter = ttk.Combobox(ViewOrderWIN, textvariable = Filter,state= 'radonly', font=('arial',9,'bold'))
            cboSelectFilter['value'] = ['Select an option:','Date','CustomerID','ProductID','Price region','OrderID']
            cboSelectFilter.current(0)
            cboSelectFilter.grid(row=0,column=1,sticky=W)


            lblAddFilter = Label(ViewOrderWIN,font=('arial',9,'bold'),text='Select a filter:',padx=2,pady=2,bg='lightblue1')
            lblAddFilter.grid(row=0,column=0,sticky=W)
                

            btnAddFilter= Button(ViewOrderWIN, padx=3,pady=2,bd=4,fg='black',font=("arial",10,"bold"),width=9,height=1,bg='gainsboro',
                                 text='Add Filter',command=AddFilter)
            btnAddFilter.grid(row=0,column=2,sticky=W)


            btnSearch = Button(ViewOrderWIN, padx=3,pady=2, bd=4, fg='black',font=('arial',10,'bold'),width=18,height=1,bg='gainsboro',
                               text='Apply Filters & Search',command=SearchForOrder)
            btnSearch.grid(row=0,column=3)







        
    
            
            

            

            

    
       
  ###Main quoting algorithm###          
        def GenerateNewQoute(Press,FinishedSize,Size,Keeps,Copies,PaperType,TypeOfJob,PrePress,Finishing,Colour,CustomerID,OrderID,CustName):
            
        
            PrePress=float(PrePress) ## Initialising local variables
            AdditionalCosts = 0
            
            
            
            PrintsPerPage = 0
            Keeps = int(Keeps)
            Copies = int(Copies)
            CostPerPrint = db.DB1.GetCostPerPrint(Press)
            CostPerSheet = db.DB1.GetCostPerSheet(Size,PaperType)
            print(CostPerPrint,CostPerSheet)
            
            ###Below uses if, elif statements to return how many jobs can be created on each sheet of paper 
            
            if FinishedSize == 'sra5' and Size == 'sra1':
                PrintsPerPage = 16
                
            elif FinishedSize == 'sra4' and Size == 'sra1':
                PrintsPerPage = 8
            elif FinishedSize=='sra3' and Size == 'sra1':
                PrintsPerPage = 4
            elif FinishedSize == 'sra2' and Size == 'sra1':
                PrintsPerPage = 2
            elif FinishedSize == Size:
                PrintsPerPage = 1
            elif FinishedSize == 'sra5' and Size == 'sra2':
                PrintsPerPage = 8
            elif FinishedSize=='sra4' and Size == 'sra2':
                PrintsPerPage = 4
            elif FinishedSize == 'sra3' and Size == 'sra2':
                PrintsPerPage = 2
            elif FinishedSize == 'sra5' and Size == 'sra3':
                PrintsPerPage = 4
                
            elif FinishedSize == 'sra4' and Size == 'sra3':
                PrintsPerPage = 2
            elif FinishedSize == 'sra5' and Size == 'sra4':
                PrintsPerPage = 2
            else:
                messagebox.showinfo(title = 'Paper size error',message='You have entered a finished size larger than the paper size!')
                


            
            
            RawSheetNo = (Keeps+Copies)//PrintsPerPage ##Divides the number of copies by the prints per page to find how much paper is needed
            OrderID = db.DB1.GetOrderIDForPDF()
            PDFname = ('Order'+str(OrderID))
            
            
            RawCost = RawSheetNo*(CostPerPrint[0][0]+CostPerSheet[0][0]) ##Multiplys the amount of sheets by the cost of each sheet of paper,and the machines cost per print
            ProductChargePerPage = db.DB1.GetProductCosts(TypeOfJob) ##Gets the cost per product
            
            ProductCost=(ProductChargePerPage[0][0])*RawSheetNo
            Total= RawCost+ProductCost ## adds them

            ##Works out any additional costs such as finishes
            if Finishing=='Guillotining':
                AdditionalCosts+=7.5
            elif Finishing=='Saddle stitching':
                AdditionalCosts+=5
            elif Colour=='Full colour':
                AdditionalCosts+=5
            Total+=PrePress
            Total+=AdditionalCosts
            


            ##Outputs the quote onto the screen
            print("Total cost fot this quote: £",Total)
            print(CustomerID)
            Total = "{0:0.2f}".format(Total) ## This is used alot in the program, each time you see it, it is formatting value to money format (2dp)
            messagebox.showinfo(title='Quote generated',message=('Your Quote is: £'+str(Total)+'\n A new order has been added to the database, and a pdf invoice has been saved.\n You can print '+str(PrintsPerPage)+' Jobs per page'))


            #Adds the order to the ordertable
            CustomerID = CustomerID[0][0]
            db.DB1.CreateOrder(CustomerID,OrderID,Total,TypeOfJob)
            db.DB1.commit()

            #Makes a pdf copy of the quote
            CustEmail = db.DB1.GetCustEmail(CustomerID)

            PDFgen.CreatePDF(PDFname,CustName,TypeOfJob,(Keeps+Copies),ProductChargePerPage[0][0],CostPerPrint[0][0],
                             CostPerSheet[0][0],FinishedSize,Finishing,PaperType,Colour,Press,CustEmail,Total)


            
            
            
            
                
                
####This window is used to add to the database, and make any edits to records
        

        def Databasewindow():
            DBwin=Tk()##Creating the window
            
            DBwin.title('Database settings')
            DBwin.configure(width=500,height=300)
            DBwin.configure(bg='lightblue1')
###This window reminds the user of the format for records in each table
            def Help():
                Helpwin=Tk()
                Helpwin.title('Help window')
                Helpwin.configure(width=500,height=300)
                Helpwin.configure(bg='lightblue1')
                lblHelp=Label(Helpwin,font=('arial',12,'bold'),text=
                              'To add a product:(Name Description MachineID PaperID CostPerPage)\nTo add a customer:(FirstName Surname Email Phone)\nTo add a machine:(Name Description Automated Cost per sheet)\n To add a Paper(Supplier Weight Size Finish CostPerSheet)\n ',
                              padx=2,pady=2,bg='lightblue1')
                lblHelp.grid()
            def Save():
                Table = cboSelectTable.get()
                Command=cboCommand.get()
                Content=txtContent.get()
                

                return Content,Command,Table





        

            
          ###A secondary window to add users to the database so they can log in  

            def UserWin():
                Userwin=Tk()
                Userwin.title('Add users')
                Userwin.configure(width=500,height=300)
                Userwin.configure(bg='lightblue1')

                def SaveUser():
                    UserName = txtUsername.get()
                    Password = txtPassword.get()
                    AccessLevel = txtAlevel.get()
                    UserID = txtUserID.get()
                    txtUsername.delete(0,END)
                    txtPassword.delete(0,END)
                    txtAlevel.delete(0,END)
                    txtUserID.delete(0,END)
                    AddUser(UserName, Password, AccessLevel, UserID)
                    UserID = StringVar()
                    UserName = StringVar()
                    Password = StringVar()
                    AccessLevel = StringVar()

                    return UserName, Password, AccessLevel, UserID
                

                UserName = StringVar()
                Password=StringVar()
                AccessLevel = StringVar()
                UserID = StringVar()


                lblUsername = Label(Userwin,font=('arial',8,'bold'),text='User Name:',padx=2,pady=2,bg='lightblue1')
                lblUsername.grid(row=0,column=0)

                txtUsername = Entry(Userwin, textvariable = UserName,font=('arial',8,'bold'), bd=2,fg='black',width=30,justify=LEFT)
                txtUsername.grid(row=0,column=1)

                lblPassword = Label(Userwin, font=('arial',8,'bold'),text='Password:',padx=2,pady=2,bg='lightblue1')
                lblPassword.grid(row=1,column=0)

                txtPassword = Entry(Userwin,font=('arial',8,'bold'),show='*', textvariable=Password, bd=2, fg='black',width=30,justify=LEFT)
                txtPassword.grid(row=1,column=1)

                lblAlevel = Label(Userwin, font=('arial',8,'bold'),text='Access level:',padx=2,pady=2,bg='lightblue1')
                lblAlevel.grid(row=2,column=0)

                txtAlevel = Entry(Userwin,font=('arial',8,'bold'),textvariable=AccessLevel, bd=2, fg='black',width=30,justify=LEFT)
                txtAlevel.grid(row=2,column=1)

               

                btnSave = Button(Userwin,padx=3, pady=2, bd=4, fg='black', font=
                                 ('arial', 8, 'bold'), width=8, height=1, bg='gainsboro', text='Save User', command=SaveUser)
                btnSave.grid(row=4,column=0)
                
                return UserName, Password, UserID, AccessLevel
        
    

                
                
                                
                              
                              
                              
                              

            Table = StringVar()
            Command = StringVar()
            Content=StringVar()
            ID = StringVar()

            lblSelectTable = Label(DBwin, font=('arial',9,'bold'),text='Select table to ammend:',padx=2,pady=2,bg='lightblue1')
            lblSelectTable.grid(row=0,column=0,sticky=W)


            cboSelectTable = ttk.Combobox(DBwin,textvariable=Table,state='readonly',font=('arial',8,'bold'))
            cboSelectTable['value']=['','Select an option:','Products','Customers','Paper','Machines','Ordertable']
            cboSelectTable.current(0)
            cboSelectTable.grid(row=0,column=1,sticky=W)

            def AddData(Table,Content): ## refers to the database to insert the new record
                print(Table)
                print(Content)
                Table = cboSelectTable.get()
                print(Table)
                
                Content = Content.split(" ")
                print(Content)
                if len(Content)<2:
                    messagebox.showinfo(title='error',message='Seperate by space not comma')
                else:
                    db.DB1.InsertIntoTable(Content,Table) ##reference db.py file
                    db.DB1.commit()
            def DeleteData(Table,ID): ##refers to the database py file to delete a record with that ID
                Table = cboSelectTable.get()
                db.DB1.DeleteRecords(Table,ID)
                db.DB1.commit()
                messagebox.showinfo(title = 'Deleted',message = 'The data record has been deleted successfully')

            def Insert(): ## button command
                Content = txtContent.get()
                AddData(Table,Content)
            def Delete(): ##button command
                ID = txtID.get()
                DeleteData(Table,ID)
            
                
                
            
                    
                
            def ApplyCommand():
                
                Command = cboCommand.get()
                
                Table = cboSelectTable.get()

            
                
                
                if Command == 'Add' :
                    lblContent = Label(DBwin,font=('arial',9,'bold'),text='Content to be inserted:',padx=2,pady=2,bg='lightblue1')
                    lblContent.grid(row=3,column=0,sticky=W)
                    btnContent = Button(DBwin,padx=3,pady=2,bd=4,fg='black',font=('arial',6,'bold'),width=4,height=1,bg='gainsboro',text='Help',command=Help)
                    btnContent.grid(row=3,column=1,sticky=W)
                    txtContent=Entry(DBwin,textvariable=Content,font = ('arial',7,'bold'),bd=2,fg='black',width=50,justify=LEFT)
                    txtContent.grid(row=3,column=2,sticky=W)

                    btnConfirmContent = Button(DBwin,pady=3,padx=2,bd=4,fg='black',font=('arial',8,'bold'),width=12,height=1,bg='gainsboro',text='Confirmentry',
                                               command=Insert)
                    btnConfirmContent.grid(row=4,column=2)
                elif Command == 'Delete':
                    lblFilter = Label(DBwin,font=('arial',9,'bold'),text = 'Where Unique ID =',padx=2,pady=2,bg='lightblue1').grid(row=3,column=0,sticky=W)
                    #txtID=Entry(DBwin,textvariable=ID,font = ('arial',7,'bold'),bd=2,fg='black',width=10,justify=LEFT)
                    txtID.grid(row=3,column=1,sticky=W)

                    btnConfirmID = Button(DBwin,pady=3,padx=2,bd=4,fg='black',font=('arial',8,'bold'),width=12,height=1,bg='gainsboro',text='Confirm Delete',
                                               command=Delete)
                    btnConfirmID.grid(row=4,column=2)
                    
                    
                              
            txtContent=Entry(DBwin,textvariable=Content,font = ('arial',7,'bold'),bd=2,fg='black',width=50,justify=LEFT)
            txtID=Entry(DBwin,textvariable=ID,font = ('arial',7,'bold'),bd=2,fg='black',width=10,justify=LEFT)

            lblCommand = Label(DBwin,font=('arial',9,'bold'),text='Select ammendment type:',padx=2,pady=2,bg='lightblue1')
            lblCommand.grid(row=1,column=0,sticky=W)
            

            cboCommand = ttk.Combobox(DBwin,textvariable=Command,state='readonly',font=('arial',8,'bold'))
            cboCommand['value']=['','Select an option:','Delete','Add']
            cboCommand.current(0)
            cboCommand.grid(row=1,column=1,sticky=W)

            btnApplyCommand = Button(DBwin,padx=3,pady=2,bd=4,fg='black',font=('arial',8,'bold'),width=17,height=1,bg='gainsboro',text='Apply Ammendment',command=ApplyCommand)
            btnApplyCommand.grid(row=2,column=0)

            


            btnAddUsers = Button(DBwin, padx=3,pady=2,bd=4,fg='black',font=
                                 ('arial',8,'bold'),width=8,height=1,bg='gainsboro',text='Add Users',command=UserWin)
            btnAddUsers.grid(row=6,column=0)



            
            
        
#####Sub Frames#######
        WidgetFrame = Frame(MainFrame, bd =10,width=1350,height=750,bg='lightblue1',pady=2,padx=1,relief=RIDGE)
        WidgetFrame.grid()

        WidgetFrame0 = Frame(WidgetFrame, bd =10,width=712,height=143,bg='lightblue1',padx=5,relief=RIDGE)
        WidgetFrame0.grid(row = 0, column = 0)

        WidgetFrame1 = Frame(WidgetFrame, bd =10,width=712,height=143,bg='lightblue1',padx=5,relief=RIDGE)
        WidgetFrame1.grid(row = 1, column = 0)

       
        WidgetFrame3 = Frame(WidgetFrame, bd =10,width=712,height=143,bg='lightblue1',padx=5,relief=RIDGE)
        WidgetFrame3.grid(row = 3, column = 0)




        
#######Variables#####
        Papersize = StringVar()
        ProductType = StringVar()
        NoCopies = StringVar()
        CostPerCopy = StringVar()
        CreLimit = StringVar()
        CreCheck = StringVar()
        SetDueDay = StringVar()
        PaymentD = StringVar()
        Discount = StringVar()
        Press = StringVar()
        Deposit = StringVar()
        PayDueDay = StringVar()
        PaymentMethod = StringVar()

        var1 = IntVar()
        var2 = IntVar()
        var3 = IntVar()
        var4 = IntVar()
        Tax = StringVar()
        Subtotal = StringVar()
        Total = StringVar()
        Reciept_ref = StringVar()
        

       


        self.btnPress = Button(WidgetFrame0,padx=36,pady=2,bd=4,fg='black',font=
                             ('arial',20,'bold'),width = 22,height=1,bg='gainsboro',text='Start a new quote',command = QuoteWindow).grid(row=1,column=2)
        self.btnInsights = Button(WidgetFrame0,padx=36,pady=2,bd=4,fg='black',font=
                                  ('arial',20,'bold'),width=22,height=1,bg='gainsboro',text='View Insights',command=InsightsWindow).grid(row=0,column=2)





        btnViewOrders = Button(WidgetFrame1, padx=36,pady=2,bd=4,fg='black',font=('arial',12,'bold'),width=35,height=4,bg='gainsboro',text='View Orders/Invoices',command=ViewOrders).grid(row=0,column=1)
        btnDatabase = Button(WidgetFrame1,padx=36,pady=2,bd=4,fg='black',font=('arial',12,'bold'),width=35,height=4,bg='gainsboro',text='Database settings',command=Databasewindow).grid(row=0,column=0)
    
        self.btnExit =Button(WidgetFrame3,padx=36,pady=2,bd=4,fg='black',font=
                             ('arial',20,'bold'),width = 12,height=2,bg='lightblue1',text='Exit',command = iExit)
        self.btnExit.grid(row=0,column=2)






####MAIN CALLS#############
if __name__=='__main__':
    root = Tk()
    application = Stock_Management_System(root)
    
                               
    
    #Stock_Management_System.ValidateLogin2()
                               
    root.mainloop()
    
    
        
        

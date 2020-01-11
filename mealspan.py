#!/usr/bin/env python

from tkinter import Tk, Button, Text, Label, Entry, Toplevel
import requests
from bs4 import BeautifulSoup
from datetime import date

class gui:
    def __init__(self,master):
        try:
            datefile = open(r'date.dat','r')
            self.tempdate = datefile.read()
        except Exception as FileNotFoundError:
            self.tempdate = 'DD-MM-YYYY'
        self.master = master
        master.title('MealSpan')
        master.geometry('300x300')
        self.userlabel = Label(master,text='Username:')
        self.passlabel = Label(master,text ='Password:')
        self.ballabel = Label(master,text='Balance:')
        self.usernameinput = Entry(master)
        self.passwordinput = Entry(master,show='●')
        self.login = Button(master,text='Login',command = self.process)
        self.datelabel = Label(master,text=self.tempdate)
        self.set = Button(text = 'Set',command=self.set)
        self.setinput = Entry(master)
        self.calculate = Button(master,text='Calculate',command=self.calculate)
        self.perday = Label(master,text = 'N/A')

        #placement
        self.userlabel.grid(row=1,column=1)
        self.passlabel.grid(row=2,column=1)
        self.ballabel.grid(row=4,column=2,pady=(0,20))
        self.usernameinput.grid(row=1,column=2)
        self.passwordinput.grid(row=2,column=2)
        self.login.grid(row=3,column=2,pady=10)
        self.datelabel.grid(row=5,column=2)
        self.setinput.grid(row=6,column=2)
        self.set.grid(row=7,column=2,pady=10)
        self.calculate.grid(row=9,column=2)
        self.perday.grid(row=8,column=2)
    def calculate(self): #calculates days between dates, and calculates money per day
        try:
            d2 = date(int(self.tempdate[0:4]),int(self.tempdate[5:7]),int(self.tempdate[8:]))
            #print(d2)
            d1 = date.today().strftime('%Y-%m-%d')
            d1 = date(int(d1[0:4]),int(d1[5:7]),int(d1[8:]))
            diff = (d2 - d1).days
            mperday = str(round((float(self.basicbal[1:].replace(',',''))+float(self.flexbal[1:].replace(',','')))/float(diff),2))
            self.perday.config(text=('$'+mperday+'/day'))
        except Exception as ValueError:
            #print("Invalid Date YYYY-MM-DD")
            #messagebox.showerror("Error", "Invalid Date, use format YYYY-MM-DD")
            errorpopup("Date")
    def set(self): #sets new target date
        file = open(r'date.dat','w')
        file.write(self.setinput.get())
        self.datelabel.config(text=self.setinput.get())
        self.tempdate=self.setinput.get()
    def process(self): #logs user in
        username = self.usernameinput.get()
        password = self.passwordinput.get()

        url = 'https://onlineservices.hospitality.uoguelph.ca/welcome.cshtml'

        with requests.session() as s:
            try:
                prelog = s.get('https://onlineservices.hospitality.uoguelph.ca/welcome.cshtml')
                soup = BeautifulSoup(prelog.text,'html5lib')
                request_id = soup.find('input',{'name':'request_id'})['value']
                OAM_REQ = soup.find('input',{'name':'OAM_REQ'})['value']
                payload = {'username':username,'password':password,'request_id':request_id,'OAM_REQ':OAM_REQ}

                auth = s.post('https://sso2.identity.uoguelph.ca/oam/server/auth_cred_submit',data=payload)
                if (auth.url != 'https://onlineservices.hospitality.uoguelph.ca/student/studenthome.cshtml'): #if not this link, user entered invalid info
                    #print("Invalid username/password")
                    errorpopup("Credentials")
                else:
                    balpage = s.get('https://onlineservices.hospitality.uoguelph.ca/secure/onlineinquiry.cshtml')
                    soup = BeautifulSoup(balpage.text,'html5lib')
                    self.basicbal = soup.find_all('td',{'align':'left'})[3].text #finding value of basic balance
                    self.flexbal = soup.find_all('td',{'align':'left'})[5].text #finding value of flex balance
                    #print(self.basicbal,self.flexbal)
                    self.ballabel.config(text=('Basic:',self.basicbal,'Flex:',self.flexbal))
            except Exception as NewConnectionError:
                #print("No internet connection try again.")
                errorpopup("Connection")
def errorpopup(code):
    tl = Toplevel(root)
    tl.title("Error")
    tl.tkraise()
    if(code=="Date"):
        message = "Invalid Date, use format YYYY-MM-DD"
    elif(code=="Connection"):
        message = "Connection Error, try again"
    elif(code=="Credentials"):
        message = "Invalid username/password, try again"
    tl.Label = Label(tl,text=message)
    tl.Label.grid(row=1,column=1,pady=10)
    tl.Button = Button(tl,text="Ok",command=tl.destroy)
    tl.Button.grid(row=2,column=1)
root = Tk()
gui(root)
root.mainloop()

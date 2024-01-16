from requests import *
from tkinter import *
from datetime import datetime
from tkinter.messagebox import *

root=Tk()
root.title('Live Currency Converter')
root.geometry('320x500+50+50')
f=('Arial',20,'bold')

oneinr = StringVar()
time=StringVar()

def getvalue():
    try:
        url='https://api.exchangerate-api.com/v4/latest/INR'
        res=get(url)
        data=res.json()
        rub=float(data['rates']['RUB'])

        inr=ent_inramount.get()

        if len(inr) == 0:
            showerror('issue', 'amount cannot be empty')
        elif not inr.replace('.', '', 1).replace('-', '', 1).isdigit():
            showerror('issue', 'amount entered cannot contain alphabets, special characters and whitespaces')
            ent_inramount.delete(0, END)
            lab_rubamount.configure(text='')
        elif len(inr.replace('.', '', 1).replace('-', '', 1))>9:
            showerror('issue', 'amount entered cannot contain more than 9 digits')
            ent_inramount.delete(0, END)
            lab_rubamount.configure(text='')
        elif float(inr)<0:
            showerror('issue', 'amount entered cannot be negative')
            ent_inramount.delete(0, END)
            lab_rubamount.configure(text='')
        else:
            val=round(float(inr)*rub,2)
            lab_rubamount.configure(text=str(val))
            
    except Exception as e:
        print(e)
        showwarning('issue', 'check your connection and try again')
        lab_rubamount.configure(text='')

def updaterates():
    try:
        url='https://api.exchangerate-api.com/v4/latest/INR'
        res=get(url, verify=False)
        data=res.json()
        rub=float(data['rates']['RUB'])

        oneinr.set(f'1 INR = {rub} RUB')
        
        now=datetime.now()
        dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
        time.set(f'Updated {dt_string}')
    
    except:
        showwarning('issue', 'check your connection and try again')
        

lab_inr=Label(root, text='India - Rupee', font=f).place(x=20,y=20)
lab_inrsymbol=Label(root, text='\u20B9', font=f).place(x=20,y=70)
ent_inramount=Entry(root, width=10, font=f)
btn_rubconvert=Button(root,text='Russia - Ruble', font=f, command=getvalue).place(x=20,y=130)
lab_rubsymbol=Label(root, text='\u20BD', font=f).place(x=20,y=200)
lab_rubamount=Label(root, font=f, fg='red')
lab_oneinr=Label(root, textvariable=oneinr).place(x=20,y=300)
lab_updtime=Label(root, textvariable=time).place(x=20,y=320)
btn_updrates=Button(root, text='Update rates', command=updaterates).place(x=20,y=350)

ent_inramount.place(x=60,y=70)
lab_rubamount.place(x=60,y=200)

root.mainloop()

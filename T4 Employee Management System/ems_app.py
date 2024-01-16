from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from pymongo import *
import matplotlib.pyplot as plt
import json
from urllib.request import urlopen
import requests

def f1():               # mw_btn_add
    aw.deiconify()
    mw.withdraw()

def f2():               # aw_btn_back
    mw.deiconify()
    aw.withdraw()

def f3():               # mw_btn_view
    vw.deiconify()
    mw.withdraw()
    vw_st_data.delete(1.0,END)
    con=None
    try:
        con=MongoClient("localhost", 27017)
        db=con["ems"]
        coll=db["employee"]
        data=coll.find()
        info=""
        for d in data:
                info+="id: "+str(d["_id"]) + "    "+"name: "+d["name"]+"    "+"sal: "+str(d["salary"])+"\n"
        vw_st_data.insert(INSERT,info)
    except Exception as e:
        showerror('Issue',e)
    finally:
        if con is not None:
            con.close()

def f4():               # vw_btn_back
    mw.deiconify()
    vw.withdraw()

def f5():               # mw_btn_update
    uw.deiconify()
    mw.withdraw()

def f6():               # uw_btn_back
    mw.deiconify()
    uw.withdraw()

def f7():               # mw_btn_delete
    dw.deiconify()
    mw.withdraw()

def f8():               # dw_btn_back
    mw.deiconify()
    dw.withdraw()

def f9():               # mw_btn_charts
    con=None
    try:
        con=MongoClient("localhost", 27017)
        db=con["ems"]
        coll=db["employee"]
        data=coll.find().sort('salary', -1).limit(5)
        name,salary=[],[]
        for d in data:
            name.append(d['name'])
            salary.append(d['salary'])
        plt.bar(name,salary,width=0.5)

        plt.xlabel('Name')
        plt.ylabel('Salary')

        plt.title('Top5 highest earning salaried employee')

        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()
    except Exception as e:
        showerror('Issue',e)
    finally:
        if con is not None:
            con.close()

def detloctemp():
    ipurl = 'http://ipinfo.io/json'
    response = urlopen(ipurl)
    data = json.load(response)
    ipcity=data['city']
    city.set(ipcity)

    base_url="https://api.openweathermap.org/data/2.5/weather?"
    api_key="0be012f196293743a2dd79e21e94e55a"

    owurl=base_url + "appid=" + api_key + "&q=" + ipcity
    owresponse=requests.get(owurl).json()
    kelvin=float(owresponse['main']['temp'])
    celsius.set(f'{(kelvin - 273.15):.2f}°C')

def save(button_press):
    con=None
    try:
        con=MongoClient("localhost", 27017)
        db=con["ems"]
        coll=db["employee"]

        if (button_press=='Add'):
            if len(aw_ent_id.get())==0:
                showerror('Issue', 'id cannot be empty')
            elif not aw_ent_id.get().isdigit():
                showerror('Issue', 'id entered cannot contain text, special characters and whitespaces')
                aw_ent_id.delete(0,END)
            elif len(aw_ent_id.get())>4:
                showerror('Issue', 'id entered cannot contain more than 4 digits')
                aw_ent_id.delete(0,END)
            elif coll.count_documents({"_id":int(aw_ent_id.get())})==1:
                showerror('Issue', "record with entered id already exists")
                aw_ent_id.delete(0,END)
            elif len(aw_ent_name.get())==0:
                showerror('Issue', 'name cannot be empty')
            elif not aw_ent_name.get().replace(' ', '', 1).isalpha():
                showerror('Issue', 'name entered cannot contain numbers, special characters and more than 1 space')
                aw_ent_name.delete(0,END)
            elif len(aw_ent_name.get())<2 or len(aw_ent_name.get())>20:
                showerror('Issue', 'name entered should contain a min of 2 and max of 20 characters')
                aw_ent_name.delete(0,END)
            elif len(aw_ent_salary.get())==0:
                showerror('Issue', 'salary cannot be empty')
            elif not aw_ent_salary.get().isdigit():
                showerror('Issue', 'salary entered cannot contain text, special characters and whitespaces')
                aw_ent_salary.delete(0,END)
            elif not int(aw_ent_salary.get())>999:
                showerror('Issue', 'salary entered should be a minumum of 1000 \u20B9')
                aw_ent_salary.delete(0,END)
            elif len(aw_ent_salary.get())>10:
                showerror('Issue', 'salary entered cannot contain more than 10 digits')
                aw_ent_salary.delete(0,END)
            else:
                info={"_id":int(aw_ent_id.get()), "name":aw_ent_name.get(), "salary":int(aw_ent_salary.get())}
                coll.insert_one(info)
                showinfo('Success', 'record created')
                aw_ent_id.delete(0,END)
                aw_ent_name.delete(0,END)
                aw_ent_salary.delete(0,END)
                aw_ent_id.focus()
        elif(button_press=='Update'):
            if len(uw_ent_id.get())==0:
                showerror('Issue', 'id cannot be empty')
            elif not uw_ent_id.get().isdigit():
                showerror('Issue', 'id entered cannot contain text, special characters and whitespaces')
                uw_ent_id.delete(0,END)
            elif len(uw_ent_id.get())>4:
                showerror('Issue', 'id entered cannot contain more than 4 digits')
                uw_ent_id.delete(0,END)
            elif not coll.count_documents({"_id":int(uw_ent_id.get())})==1:
                showerror('Issue', "record with entered id does not exist")
                uw_ent_id.delete(0,END)
            elif len(uw_ent_name.get())==0 and len(uw_ent_salary.get())==0:
                showerror('Issue', "both name and salary cannot be empty, atleast update one")
            elif uw_ent_name.get() and not uw_ent_name.get().replace(' ', '', 1).isalpha():
                showerror('Issue', 'name entered cannot contain numbers, special characters and more than 1 space')
                uw_ent_name.delete(0,END)
            elif uw_ent_name.get() and (len(uw_ent_name.get())<2 or len(uw_ent_name.get())>20):
                showerror('Issue', 'name entered should contain a min of 2 and max of 20 characters')
                uw_ent_name.delete(0,END)
            elif uw_ent_salary.get() and not uw_ent_salary.get().isdigit():
                showerror('Issue', 'salary entered cannot contain text, special characters and whitespaces')
                uw_ent_salary.delete(0,END)
            elif uw_ent_salary.get() and not int(uw_ent_salary.get())>999:
                showerror('Issue', 'salary entered should be a minumum of 1000 \u20B9')
                uw_ent_salary.delete(0,END)
            elif uw_ent_salary.get() and len(uw_ent_salary.get())>10:
                showerror('Issue', 'salary entered cannot contain more than 10 digits')
                uw_ent_salary.delete(0,END)
            else:
                if len(uw_ent_name.get())==0:
                    coll.update_one({ "_id": int(uw_ent_id.get()) }, { "$set": {"salary":int(uw_ent_salary.get())} })
                    showinfo('Success', 'record updated')
                elif len(uw_ent_salary.get())==0:
                    coll.update_one({ "_id": int(uw_ent_id.get()) }, { "$set": {"name":uw_ent_name.get()} })
                    showinfo('Success', 'record updated')
                else:
                    coll.update_one({ "_id": int(uw_ent_id.get()) }, { "$set": {"name":uw_ent_name.get(), "salary":int(uw_ent_salary.get())} })
                    showinfo('Success', 'record updated')
                uw_ent_id.delete(0,END)
                uw_ent_name.delete(0,END)
                uw_ent_salary.delete(0,END)
                uw_ent_id.focus()
        elif(button_press=='Delete'):
            if len(dw_ent_id.get())==0:
                showerror('Issue', 'id cannot be empty')
            elif not dw_ent_id.get().isdigit():
                showerror('Issue', 'id entered cannot contain text, special characters and whitespaces')
                dw_ent_id.delete(0,END)
            elif len(dw_ent_id.get())>4:
                showerror('Issue', 'id entered cannot contain more than 4 digits')
                dw_ent_id.delete(0,END)
            elif not coll.count_documents({"_id":int(dw_ent_id.get())})==1:
                showerror('Issue', "record with entered id does not exist")
                dw_ent_id.delete(0,END)
            else:
                if askyesno('Delete', 'Are you sure you want to delete?'):
                    coll.delete_one({"_id":int(dw_ent_id.get())})
                    showinfo('Success', 'record deleted')
                    dw_ent_id.delete(0,END)      
    except Exception as e:
        showerror('Issue', e)
    finally:
        if con is not None:
            con.close()

def on_closing():
    if askyesno('Quit', 'Are you sure you want to quit?'):
        mw.destroy()
        aw.destroy()
        vw.destroy()
        uw.destroy()
        dw.destroy()

mw=Tk()
mw.title('Employee Management System')
mw.geometry('400x400+100+100')
mw.configure(background='pale green')
f=('Arial',15,'bold')
p=('Georgia', 15, 'bold')
m=("Times", 14, "bold italic")

city = StringVar()
celsius = StringVar()

detloctemp()

mw_btn_add=Button(mw,text='Add',width=10,highlightcolor='blue',relief='flat',overrelief='sunken',default="active",font=f,command=f1)
mw_btn_add.pack(pady=5)

mw_btn_view=Button(mw,text='View',width=10,highlightcolor='blue',relief='flat',overrelief='sunken',default="active",font=f,command=f3)
mw_btn_view.pack(pady=5)

mw_btn_update=Button(mw,text='Update',width=10,highlightcolor='blue',relief='flat',overrelief='sunken',default="active",font=f,command=f5)
mw_btn_update.pack(pady=5)

mw_btn_delete=Button(mw,text='Delete',width=10,highlightcolor='blue',relief='flat',overrelief='sunken',default="active",font=f,command=f7)
mw_btn_delete.pack(pady=5)

mw_btn_charts=Button(mw,text='Charts',width=10,highlightcolor='blue',relief='flat',overrelief='sunken',default="active",font=f,command=f9)
mw_btn_charts.pack(pady=5)

frame = Frame(mw, width = 380, height = 50, highlightbackground="black", highlightthickness=2,bg='pale green')
frame.place(x=10,y=270)

mw_lab_loc=Label(mw,text='Location:',font=f,bg='pale green')
mw_lab_loc.place(x=20,y=280)

mw_lab_city=Label(mw,textvariable=city,font=p,fg='red',bg='pale green')
mw_lab_city.place(x=120,y=280)

mw_lab_temp=Label(mw,text='Temp:',font=f,bg='pale green')
mw_lab_temp.place(x=230,y=280)

mw_lab_celsius=Label(mw,textvariable=celsius,font=p,fg='red',bg='pale green')
mw_lab_celsius.place(x=300,y=280)

aw=Tk()
aw.title('Add Employee')
aw.geometry('400x400+100+100')
aw.configure(background='light sky blue')

aw_lab_id=Label(aw,text='enter id:',font=f,bg='light sky blue')
aw_ent_id=Entry(aw,font=f,highlightbackground='blue',highlightthickness=1)
aw_lab_name=Label(aw,text='enter name:',font=f,bg='light sky blue')
aw_ent_name=Entry(aw,font=f,highlightbackground='blue',highlightthickness=1)
aw_lab_salary=Label(aw,text='enter salary:',font=f,bg='light sky blue')
aw_ent_salary=Entry(aw,font=f,highlightbackground='blue',highlightthickness=1)
aw_btn_save=Button(aw,text='Save',font=f,width=10,highlightcolor='blue',relief='flat',overrelief='sunken',default="active",command=lambda m="Add": save(m))
aw_btn_back=Button(aw,text='Back',font=f,width=10,highlightcolor='blue',relief='flat',overrelief='sunken',default="active",command=f2)

aw_lab_id.pack(pady=5)
aw_ent_id.pack(pady=5)
aw_lab_name.pack(pady=5)
aw_ent_name.pack(pady=5)
aw_lab_salary.pack(pady=5)
aw_ent_salary.pack(pady=5)
aw_btn_save.pack(pady=10)
aw_btn_back.pack(pady=10)

aw.withdraw()

vw=Tk()
vw.title('View Employees')
vw.geometry('400x400+100+100')
vw.configure(background='khaki')

vw_st_data=ScrolledText(vw,font=m,bg='khaki',highlightbackground='black',highlightthickness=1,width=36,height=12)
vw_btn_back=Button(vw,text='Back',font=f,width=10,highlightcolor='blue',relief='flat',overrelief='sunken',default="active",command=f4)
vw_st_data.pack(pady=10)
vw_btn_back.pack(pady=20)

vw.withdraw()

uw=Tk()
uw.title('Update Employee')
uw.geometry('400x400+100+100')
uw.configure(background='wheat1')

uw_lab_id=Label(uw,text='enter id:',font=f,bg='wheat1')
uw_ent_id=Entry(uw,font=f,highlightbackground='blue',highlightthickness=1)
uw_lab_name=Label(uw,text='enter updated name:',font=f,bg='wheat1')
uw_ent_name=Entry(uw,font=f,highlightbackground='blue',highlightthickness=1)
uw_lab_salary=Label(uw,text='enter updated salary:',font=f,bg='wheat1')
uw_ent_salary=Entry(uw,font=f,highlightbackground='blue',highlightthickness=1)
uw_btn_save=Button(uw,text='Save',font=f,width=10,highlightcolor='blue',relief='flat',overrelief='sunken',default="active",command=lambda m="Update": save(m))
uw_btn_back=Button(uw,text='Back',font=f,width=10,highlightcolor='blue',relief='flat',overrelief='sunken',default="active",command=f6)

uw_lab_id.pack(pady=5)
uw_ent_id.pack(pady=5)
uw_lab_name.pack(pady=5)
uw_ent_name.pack(pady=5)
uw_lab_salary.pack(pady=5)
uw_ent_salary.pack(pady=5)
uw_btn_save.pack(pady=10)
uw_btn_back.pack(pady=10)

uw.withdraw()

dw=Tk()
dw.title('Delete Employee')
dw.geometry('400x400+100+100')
dw.configure(background='PaleTurquoise1')

dw_lab_id=Label(dw,text='enter id:',font=f,bg='PaleTurquoise1')
dw_ent_id=Entry(dw,font=f,highlightbackground='blue',highlightthickness=1)
dw_btn_save=Button(dw,text='Save',font=f,width=10,highlightcolor='blue',relief='flat',overrelief='sunken',default="active",command=lambda m="Delete": save(m))
dw_btn_back=Button(dw,text='Back',font=f,width=10,highlightcolor='blue',relief='flat',overrelief='sunken',default="active",command=f8)

dw_lab_id.pack(pady=5)
dw_ent_id.pack(pady=5)
dw_btn_save.pack(pady=10)
dw_btn_back.pack(pady=10)

dw.withdraw()

mw.protocol('WM_DELETE_WINDOW',on_closing)
aw.protocol('WM_DELETE_WINDOW',on_closing)
vw.protocol('WM_DELETE_WINDOW',on_closing)
uw.protocol('WM_DELETE_WINDOW',on_closing)
dw.protocol('WM_DELETE_WINDOW',on_closing)

mw.mainloop()

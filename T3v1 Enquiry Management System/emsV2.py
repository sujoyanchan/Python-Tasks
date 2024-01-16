from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from pymongo import *

def f1():
    username=mw_ent_username.get()
    password=mw_ent_password.get()
    con=None
    try:
        con=MongoClient("localhost", 27017)
        db=con["emsdb"]
        coll=db["admin"]
        if coll.count_documents({"username":username})==1 and coll.count_documents({"password":password})==1:
            lw.deiconify()
            mw.withdraw()
        else:
            showerror('Issue','invalid username or password')
            mw_ent_username.delete(0,END)
            mw_ent_password.delete(0,END)
            mw_ent_username.focus()
    except Exception as e:
        showerror('Issue',e)
    finally:
        if con is not None:
            con.close()

def f2():
    vw_st_data.delete(1.0,END)
    name=lw_ent_name.get()
    con=None
    try:
        con=MongoClient("localhost", 27017)
        db=con["emsdb"]
        coll=db["user"]
        count=coll.count_documents({"name":name})
        if count==1:
            vw.deiconify()
            lw.withdraw()
            data=coll.find({"name":name})
            info=""
            for d in data:
                info+="NAME : "+str(d["name"])+"\n"+"PHONE : "+str(d["phone"])+"\n"+"ADDRESS : "+str(d["address"])+"\n"+"PRODUCTS : "+str(d["products"])+"\n"
            vw_st_data.insert(INSERT,info)
        else:
            showerror('Issue', 'record with entered name does not exist')
    except Exception as e:
        showerror('Issue',e)
    finally:
        if con is not None:
            con.close()

def f3():
    mw.deiconify()
    lw.withdraw()
    mw_ent_username.delete(0,END)
    mw_ent_password.delete(0,END)

def f4():
    lw.deiconify()
    vw.withdraw()
    lw_ent_name.delete(0,END)

def f5():
    name=lw_ent_name.get()
    con=None
    try:
        con=MongoClient("localhost", 27017)
        db=con["emsdb"]
        coll=db["user"] 
        count=coll.count_documents({"name":name})
        if count==1:
            if askyesno('Delete', 'Are you sure you want to delete?'):
                coll.delete_one({"name":name})
                showinfo('Success', 'record deleted')
        else:
            showerror('Issue', 'record with entered name does not exist')
    except Exception as e:
        showerror('Issue',e)
    finally:
        if con is not None:
            con.close()
        lw_ent_name.delete(0,END)

mw=Tk()
mw.title('Enquiry Management System')
mw.geometry('600x750+50+50')
f=('Arial',15,'bold')
# m=("Times", 12, "bold italic")
p=('Georgia', 15, 'bold')

mw_lab_name=Label(mw,text='Name',font=f).place(x=20, y=20)
mw_ent_name=Entry(mw,font=f,width=20)
mw_lab_phone=Label(mw,text='Phone',font=f).place(x=20, y=70)
mw_ent_phone=Entry(mw,font=f,width=10)
mw_lab_address=Label(mw,text='Address',font=f).place(x=20, y=120)
mw_ent_address=Entry(mw,font=f,width=40)

mw_ent_name.place(x=120,y=20)
mw_ent_phone.place(x=120,y=70)
mw_ent_address.place(x=120,y=120)

p1=IntVar()
p2=IntVar()
p3=IntVar()
p4=IntVar()
p5=IntVar()

lab_products=Label(mw, text='Select Products', font=f).place(x=20, y=170)
cb_p1=Checkbutton(mw, text='Product1', font=p, variable=p1,onvalue=1,offvalue=0)
cb_p2=Checkbutton(mw, text='Product2', font=p, variable=p2,onvalue=1,offvalue=0)
cb_p3=Checkbutton(mw, text='Product3', font=p, variable=p3,onvalue=1,offvalue=0)
cb_p4=Checkbutton(mw, text='Product4', font=p, variable=p4,onvalue=1,offvalue=0)
cb_p5=Checkbutton(mw, text='Product5', font=p, variable=p5,onvalue=1,offvalue=0)

cb_p1.place(x=220, y=170)
cb_p2.place(x=220, y=220)
cb_p3.place(x=220, y=270)
cb_p4.place(x=220, y=320)
cb_p5.place(x=220, y=370)

lw=Tk()
lw.title('Admin Menu')
lw.geometry('400x400+100+100')

lw_lab_name=Label(lw,text='Enter name to view or delete enquiry',font=f)
lw_lab_name.pack(pady=10)
lw_ent_name=Entry(lw,font=f,width=20)
lw_ent_name.pack(pady=10)
lw_btn_view=Button(lw,text='View Enquiry',font=f,fg='green',width=15,command=f2)
lw_btn_view.pack(pady=10)
lw_btn_delete=Button(lw,text='Delete Enquiry',font=f,fg='red',width=15,command=f5)
lw_btn_delete.pack(pady=10)
lw_btn_back=Button(lw,text='Back to Main',font=f,command=f3)
lw_btn_back.pack(pady=20)

lw.withdraw()

vw=Tk()
vw.title('View Menu')
vw.geometry('600x300+100+100')

vw_st_data=ScrolledText(vw,font=f,width=50,height=5)
vw_btn_back=Button(vw,text='Back to Admin',font=f,command=f4)
vw_st_data.pack(pady=10)
vw_btn_back.pack(pady=20)

vw.withdraw()

def save():
    con=None
    try:
        con=MongoClient("localhost", 27017)
        db=con["emsdb"]
        coll=db["user"]

        name=mw_ent_name.get()
        phone=mw_ent_phone.get()
        address=mw_ent_address.get()
        products=''
        if p1.get()==1:
            products+='Product1 '
        if p2.get()==1:
            products+='Product2 '
        if p3.get()==1:
            products+='Product3 '
        if p4.get()==1:
            products+='Product4 '
        if p5.get()==1:
            products+='Product5 '

        if len(name) == 0:
            showerror('Issue', 'name entered cannot be empty')
        elif len(phone) == 0:
            showerror('Issue', 'phone number entered cannot be empty')
        elif len(address) == 0:
            showerror('Issue', 'address entered cannot be empty')
        elif p1.get()==0 and p2.get()==0 and p3.get()==0 and p4.get()==0 and p5.get()==0:
            showerror('Issue', 'please select atleast 1 product')
        elif not name.replace(' ', '', 1).isalpha():
            showerror('Issue', 'name entered cannot contain numbers, special characters and more than 1 space')
            mw_ent_name.delete(0,END)
        elif len(name)>20:
            showerror('Issue', 'name entered cannot contain more than 20 characters')
            mw_ent_name.delete(0,END)
        elif not phone.isdigit():
            showerror('Issue', 'phone number entered cannot contain text, special characters and whitespaces')
            mw_ent_phone.delete(0,END)
        elif len(phone)!=10:
            showerror('Issue', 'phone number entered should be 10 digits')
            mw_ent_phone.delete(0,END)
        elif not address.replace(' ', '').isalnum() or (address.replace(' ', '').isalpha() or address.replace(' ', '').isdigit()):
            showerror('Issue', 'address entered cannot be all number or all text and should not contain special characters')
            mw_ent_address.delete(0,END)
        elif len(address)>40:
            showerror('Issue', 'address entered cannot contain more than 40 characters')
            mw_ent_address.delete(0,END)
        else:
            info={"name":name, "phone":phone, "address":address, "products":products}
            coll.insert_one(info)
            showinfo('Success', 'record created')
            mw_ent_name.delete(0,END)
            mw_ent_phone.delete(0,END)
            mw_ent_address.delete(0,END)
            p1.set(0)
            p2.set(0)
            p3.set(0)
            p4.set(0)
            p5.set(0)
            mw_ent_name.focus()
    except Exception as e:
        showerror('Issue', e)
    finally:
        if con is not None:
            con.close()

def on_closing():
    if askyesno('Quit', 'Are you sure you want to quit?'):
        mw.destroy()
        lw.destroy()
        vw.destroy()

mw_btn_save=Button(mw,text='Save Enquiry',font=f,fg='green',command=save).place(x=220, y=420)

mw_lab_login=Label(mw,text='Manager Admin Login',font=f).place(x=20, y=520)
mw_lab_username=Label(mw,text='username',font=f).place(x=20, y=570)
mw_ent_username=Entry(mw,font=f)
mw_ent_username.place(x=170, y=570)
mw_lab_password=Label(mw,text='password',font=f).place(x=20, y=620)
mw_ent_password=Entry(mw,font=f,show='*')
mw_ent_password.place(x=170, y=620)
mw_btn_admin=Button(mw,text='Login',font=f,fg='red',command=f1).place(x=220, y=670)

mw.protocol('WM_DELETE_WINDOW',on_closing)
lw.protocol('WM_DELETE_WINDOW',on_closing)
vw.protocol('WM_DELETE_WINDOW',on_closing)

mw.mainloop()

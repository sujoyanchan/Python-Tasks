from requests import *
from tkinter import *
from tkinter.messagebox import *

root=Tk()
root.title('BMI Calculator')
root.geometry('300x600+50+50')
f=('Arial',14,'bold')
m=("Times", 12, "bold italic")
r=('Georgia', 13, 'bold')

gender = IntVar()
gender.set(1)
status=StringVar()

def getbmi():
	try:
		if not ent_age.get():
			showerror('issue', 'age cannot be empty')
			lab_bmival.configure(text='')
			status.set('')
		elif ((ent_ft.get() or ent_in.get()) and ent_cm.get()):
			showerror('issue', 'enter height in either ft/in or cm, not in both')
			ent_cm.delete(0, 'end')
			ent_ft.delete(0, 'end')
			ent_in.delete(0, 'end')
			lab_bmival.configure(text='')
			status.set('')
		elif not (ent_ft.get() or ent_in.get() or ent_cm.get()):
			showerror('issue', 'enter height in atleast one, either ft/in or cm')
			lab_bmival.configure(text='')
			status.set('')
		elif not (ent_ft.get() or ent_cm.get()) and ent_in.get():
			showerror('issue', 'please always enter ft value first when chosing ft/in metric for height')
			ent_in.delete(0, 'end')
			lab_bmival.configure(text='')
			status.set('')
		elif not ent_weight.get():
			showerror('issue', 'weight cannot be empty')
			lab_bmival.configure(text='')
			status.set('')
		elif not ent_age.get().replace('.', '', 1).replace('-', '', 1).isdigit():
			showerror('issue', 'age entered cannot contain alphabets, special characters and whitespaces')
			ent_age.delete(0, 'end')
			lab_bmival.configure(text='')
			status.set('')
		elif not ent_age.get().isdigit() or (float(ent_age.get())<2 or float(ent_age.get())>120):
			showerror('issue', 'please enter valid age')
			ent_age.delete(0, 'end')
			lab_bmival.configure(text='')
			status.set('')
		elif ent_cm.get() and not ent_cm.get().replace('.', '', 1).replace('-', '', 1).isdigit():
			showerror('issue', 'height in cm entered cannot contain alphabets, special characters and whitespaces')
			ent_cm.delete(0, 'end')
			lab_bmival.configure(text='')
			status.set('')
		elif ent_cm.get() and not ent_cm.get().isdigit():
			showerror('issue', 'height in cm entered should be a positive integer')
			ent_cm.delete(0, 'end')
			lab_bmival.configure(text='')
			status.set('')
		elif ent_cm.get() and (float(ent_cm.get())<10 or float(ent_cm.get())>304):
			showerror('issue', 'please enter valid height in cm')
			ent_cm.delete(0, 'end')
			lab_bmival.configure(text='')
			status.set('')
		elif ent_ft.get() and not ent_ft.get().replace('.', '', 1).replace('-', '', 1).isdigit():
			showerror('issue', 'height in ft entered cannot contain alphabets, special characters and whitespaces')
			ent_ft.delete(0, 'end')
			lab_bmival.configure(text='')
			status.set('')
		elif ent_ft.get() and not ent_ft.get().isdigit():
			showerror('issue', 'height in ft entered should be a positive integer')
			ent_ft.delete(0, 'end')
			lab_bmival.configure(text='')
			status.set('')
		elif ent_ft.get() and (float(ent_ft.get())<1 or float(ent_ft.get())>9):
			showerror('issue', 'please enter valid height in ft')
			ent_ft.delete(0, 'end')
			lab_bmival.configure(text='')
			status.set('')
		elif ent_in.get() and not ent_in.get().replace('.', '', 1).replace('-', '', 1).isdigit():
			showerror('issue', 'height in inches entered cannot contain alphabets, special characters and whitespaces')
			ent_in.delete(0, 'end')
			lab_bmival.configure(text='')
			status.set('')
		elif ent_in.get() and not ent_in.get().isdigit():
			showerror('issue', 'height in inches entered should be a positive integer')
			ent_in.delete(0, 'end')
			lab_bmival.configure(text='')
			status.set('')
		elif ent_in.get() and (float(ent_in.get())<0 or float(ent_in.get())>12):
			showerror('issue', 'please enter valid height in inches')
			ent_in.delete(0, 'end')
			lab_bmival.configure(text='')
			status.set('')
		elif ent_weight.get() and not ent_weight.get().replace('.', '', 1).replace('-', '', 1).isdigit():
			showerror('issue', 'weight entered cannot contain alphabets, special characters and whitespaces')
			ent_weight.delete(0, 'end')
			lab_bmival.configure(text='')
			status.set('')
		elif ent_weight.get() and not ent_weight.get().isdigit():
			showerror('issue', 'weight entered should be a positive integer')
			ent_weight.delete(0, 'end')
			lab_bmival.configure(text='')
			status.set('')
		elif ent_weight.get() and (int(ent_weight.get())<1 or int(ent_weight.get())>200):
			showerror('issue', 'please enter valid weight')
			ent_weight.delete(0, 'end')
			lab_bmival.configure(text='')
			status.set('')
		else:
			if ent_cm.get():
				height_cm=int(ent_cm.get())
			elif ent_ft.get() and not ent_in.get():
				height_ft=int(ent_ft.get())
				totalheight_in=(height_ft*12)
				height_cm=int(round(2.54*totalheight_in))
			else:
				height_ft=int(ent_ft.get())
				height_in=int(ent_in.get())
				totalheight_in=(height_ft*12)+height_in
				height_cm=int(round(2.54*totalheight_in))
		height_m=(height_cm/100)
		weight=int(ent_weight.get())
		bmi=round(weight/pow(height_m, 2),2)
		weightstatus(bmi)
			
	except Exception as e:
		print(e)

def weightstatus(bmi):
	try:
		if bmi<18.5:
			stat='Underweight'
			lab_status.configure(fg='gold')
			lab_bmival.configure(fg='gold')
		elif bmi>=18.5 and bmi<=24.9:
			stat='Normal weight'
			lab_status.configure(fg='green')
			lab_bmival.configure(fg='green')
		elif bmi>=25 and bmi<=29.9:
			stat='Overweight'
			lab_status.configure(fg='orange')
			lab_bmival.configure(fg='orange')
		elif bmi>=30 and bmi<=35:
			stat='Obese'
			lab_status.configure(fg='red')
			lab_bmival.configure(fg='red')
		else:
			stat='Morbid obesity'
			lab_status.configure(fg='red3')
			lab_bmival.configure(fg='red3')
		lab_bmival.configure(text=f'BMI = {str(bmi)}')
		status.set(f'Weight status: {stat}')

	except Exception as e:
		print(e)
		
lab_gender=Label(root, text='GENDER', font=f).place(x=20,y=20)
rb_male=Radiobutton(root, text='Male', font=f, variable=gender, value=1).place(x=20,y=50)
rb_female=Radiobutton(root, text='Female', font=f, variable=gender, value=2).place(x=110,y=50)
lab_age=Label(root, text='AGE', font=f).place(x=20,y=100)
ent_age=Entry(root, width=7, font=f)
lab_agerange=Label(root, text='between 2 yrs to 120 yrs', font=m).place(x=110,y=150)
lab_height=Label(root, text='HEIGHT', font=f).place(x=20,y=200)
lab_choice=Label(root, text='(use cm or ft/in)', font=m).place(x=110,y=200)
ent_cm=Entry(root, width=7, font=f)
lab_cm=Label(root, text='cm', font=m).place(x=110,y=250)
ent_ft=Entry(root, width=7, font=f)
lab_ft=Label(root, text='feet', font=m).place(x=110,y=300)
ent_in=Entry(root, width=7, font=f)
lab_in=Label(root, text='inches', font=m).place(x=240,y=300)
lab_weight=Label(root, text='WEIGHT', font=f).place(x=20,y=350)
ent_weight=Entry(root, width=7, font=f)
lab_kgs=Label(root, text='in kgs', font=m).place(x=110,y=400)
btn_bmicalc=Button(root,text='Calculate', font=f, command=getbmi).place(x=20,y=450)
lab_bmival=Label(root, font=r)
lab_status=Label(root,font=r,textvariable=status)

ent_age.place(x=20,y=150)
ent_cm.place(x=20,y=250)
ent_ft.place(x=20,y=300)
ent_in.place(x=150,y=300)
ent_weight.place(x=20,y=400)
lab_bmival.place(x=20,y=525)
lab_status.place(x=20,y=550)

root.mainloop()

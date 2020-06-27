# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 19:21:27 2020

@author: HebaGamalElDin
"""
########################################
""" Importing Necessary libararies """
#######################################
import tkinter as tk
from tkinter import *
from tkcalendar import Calendar, DateEntry
import cv2
from PIL import ImageTk, Image
import datetime
import sqlite3

"""                           Database Part                                """
""" Saving Alarm Messages With Date and Time In Database"""
def Get_Curr_Date():
    (Date,Time) = str(datetime.datetime.now()).split()
    return Date,Time
def Save_Alarms(Message):
    CONN = sqlite3.connect('mydata.sqlite')
    Create_Que = "CREATE TABLE ALARMS(MESSAGE VARCHAR(200), DATE VARCHAR(20), TIME VARCHAR(30));"
    CONN.execute(Create_Que)
    Insert_Que = "INSERT INTO ALARMS (MESSAGE, DATE, TIME) VALUES(?,?,?)"
    Data = [(str(Message), Get_Curr_Date()[0], Get_Curr_Date()[1])]
    CONN.executemany(Insert_Que, Data)
    CONN.commit()
    return "Done Saving Alarm's Date & Time!"
#Save_Alarms("System has been down without Errors!")  

"""                     Saving User Inputs                                 """
def Users_Saving(FName, LName, Password, BirthDate, Gander):
    CONN = sqlite3.connect('mydata.sqlite')
    Create_Que = "CREATE TABLE Users(FirstName VARCHAR(20), LastName VARCHAR(20), Password VARCHAR(20), Birthdate VARCHAR(20), Gander VARCHAR(10));"
    CONN.execute(Create_Que)
    Insert_Que = "INSERT INTO USERS (FirstName, LastName, Password, Birthdate, Gander) VALUES(?,?,?,?,?);"
    Data = [(FName, LName, Password, BirthDate, Gander)]
    CONN.executemany(Insert_Que, Data)
    CONN.commit()
    return "Done Saving User Data!"
#Users_Saving("Heba", "Gamal EL-Din", "99999Hg@", "1997-01-13", "Female")

def Retreive_(Table_Name):
    CONN = sqlite3.connect('mydata.sqlite')
    Cursor = CONN.execute('select * from %s;'%Table_Name)
    Rows = Cursor.fetchall()
    return Rows

TName = "Users"
Rows = Retreive_(TName)

"""                     Login Validation Function                          """
def Validate_User(UserName, Password):
    Flag = False
    Rows = Retreive_("Users")
    for Rec in Rows:
        if (UserName == (Rec[0] + Rec[1])) and (Password == Rec[2]):
            Flag = True
    return Flag
"""                                GUI Part                                """

BACKGROUND_IMAGE = 'sys background.png'
WIDTH, HEIGTH = 660, 400
#############################
""" Creating The Background 
    Image of The Panel 
    The Main Canvas """
############################
def Set_Background(Panel,WIDTH, HEIGTH):
    Canvas = tk.Canvas(Panel, width=WIDTH, height=HEIGTH)
    Canvas.pack(fill='both')
    img = ImageTk.PhotoImage(Image.open(BACKGROUND_IMAGE).resize((WIDTH, HEIGTH), Image.ANTIALIAS))
    Canvas.background = img  
    BG = Canvas.create_image(0, 0, anchor=tk.NW, image=img)
    return Canvas    

def Last_Panel():
    #################################
    """ First Camera Positioning """
    #################################
    global window, MSG
    window = tk.Tk()
    window.title("GUI")
    window.resizable(False, False)
    window.geometry('{}x{}+350+200'.format(WIDTH, HEIGTH))

    Canvas = Set_Background(window,WIDTH, HEIGTH)
    Cam1 = tk.Label(window, text="Camera-1",font=("Times New Roman", 12), fg="black", highlightbackground="snow",highlightcolor = "blue", highlightthickness=2)
    Label1= tk.Label(window)
    Label1.pack(side='left', padx=15, pady=5)
    Cam_lbl = Canvas.create_window(15, 10, anchor=tk.NW, window=Cam1)
    WebCam1 = Canvas.create_window(15, 35, anchor=tk.NW, window=Label1)
    
    #################################
    """ Second Camera Positioning """
    #################################
    Cam2 = tk.Label(window, text="Camera-2",font=("Times New Roman", 12), fg="black", highlightbackground="snow",highlightcolor = "blue", highlightthickness=2)
    Label2 = tk.Label(window)
    Label2.pack(side='right', padx=15, pady=5) 
    """ When The Second Camera is being added 
    The same way as The First one Below, 
        Ignore This lines """
    imgt = ImageTk.PhotoImage(Image.open(r'screen\7.png').resize((290, 150), Image.ANTIALIAS))
    Label2.imgtk = imgt
    Label2.configure(image=imgt)
    """ Ending Of The lines should be Ignored """
    Cam_lbl2 = Canvas.create_window(572, 10, anchor=tk.NW, window=Cam2)
    WebCam2 = Canvas.create_window(350, 35, anchor=tk.NW, window=Label2)
    
    ################################
    """ Third Camera Positioning """
    ################################
    Cam3 = tk.Label(window, text="Camera-3",font=("Times New Roman", 12), fg="black", highlightbackground="snow",highlightcolor = "blue", highlightthickness=2)
    Label3 = tk.Label(window)
    Label3.pack(side='right', padx=15, pady=5)
    """ When The Third Camera is being added 
    The same way as The First one Below,
        Ignore This lines """
    im = ImageTk.PhotoImage(Image.open(r'screen\6.png').resize((290, 150), Image.ANTIALIAS))
    Label3.imgtk = im
    Label3.configure(image=im)
    """ Ending Of The lines should be Ignored """
    Cam_lbl3 = Canvas.create_window(572, 200, anchor=tk.NW, window=Cam3)
    WebCam3 = Canvas.create_window(350, 224, anchor=tk.NW, window=Label3)
    
    ##########################################
    """ Fourth Alarm Messages Positioning """
    ##########################################
    MSG = "A Problem Has Just Accuared!\n AS The Camera Number 3 Is Down Without \n Stating an Error"
    var = tk.StringVar()
    var.set(MSG)
    Label4 = tk.LabelFrame(window, text = "ALARM", font=("Times New Roman",12), fg="red", width = 100, height = 60, highlightbackground="snow",highlightcolor = "black", highlightthickness=3)
    Label5 = tk.Label(Label4,textvariable = var, font=("Times New Roman",12), width = 32 , height =5)
    Label5.pack()
    WebCam3 = Canvas.create_window(15, 225, anchor=tk.NW, window=Label4)
    
    """"""""""""""""""""""""
    """ Camera-1 Shoting """
    cap = cv2.VideoCapture(0)
    while True:
        Bool, frame = cap.read()
        if Bool:
            frame = cv2.resize(frame, (290, 150))
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            """Starting The Main Process of Displaying The Camera 
                        in the Speciefied Position (Label1)"""
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            Label1.imgtk = imgtk
            Label1.configure(image=imgtk)
            #Label1.after(1, video_stream)
            """ End Of Displaying Process """
        else:
            print("Camera Resource not found!")
            break
    cap.release()
    cv2.destroyAllWindows()

def Second_Panel():
    global panel1
    panel1 = tk.Tk()
    panel1.title("Panel-1")
    Canvas = Set_Background(panel1,WIDTH, HEIGTH)
    Icon = ImageTk.PhotoImage(Image.open(r'GUI IMAGES\eye.png').resize((100, 70), Image.ANTIALIAS))
    Labl = tk.Label(panel1)
    Labl.pack(side='right', padx=15, pady=5)
    Labl.imgtk = Icon
    Labl.configure(image=Icon)
    icon = Canvas.create_image(280, 5, anchor=tk.NW, image=Icon)
    text = Canvas.create_text((110, 80), anchor=tk.NW, fill= 'white', text="Automated Survilliance System",font=("Times New Roman", 26))
    btn=tk.Button(panel1 , text='Sign-In' , borderwidth=2, width = wedg_width, height = wedg_height, font=("Times New Roman", 20), fg="black", bg='snow', command=Controller2)
    btn.pack(side='right' ,padx=50)
    butn = Canvas.create_window(210, 200, anchor=tk.NW, window=btn)
    btn1=tk.Button(panel1 , text='Add New Admin' , borderwidth=2, width = wedg_width, height = wedg_height, font=("Times New Roman", 20), fg="black", bg='snow', command=Controller3)
    btn1.pack(side='right' ,padx=50)
    butn1 = Canvas.create_window(210, 300, anchor=tk.NW, window=btn1)
    panel1.resizable(False, False) 
    panel1.geometry('{}x{}+350+200'.format(WIDTH, HEIGTH))
    
def Third_Panel():
    global panel2 , Entr
    panel2 = tk.Tk()
    panel2.title("Panel-2")
    Canvas = Set_Background(panel2,WIDTH, HEIGTH)    
    text = Canvas.create_text((150, 80), anchor=tk.NW, text="Automated Survilliance System",font=("Times New Roman", 26), fill='white')
    Text = Canvas.create_text((30, 150), anchor=tk.NW,fill='white', text="Current Password:",font=("Times New Roman", 14))
    e=tk.StringVar()
    Entr=tk.Entry(panel2,textvariable=e ,width = 50, borderwidth=2, relief='ridge', show='*')
    Entri = Canvas.create_window(230, 150, anchor=tk.NW, window=Entr)
    btn=tk.Button(panel2 , text='Log-In' , borderwidth=2, width = wedg_width, height = wedg_height, font=("Times New Roman", 20), fg="black", bg='snow', command=Controller9)
    btn.pack(side='right' ,padx=50)
    butn = Canvas.create_window(220, 280, anchor=tk.NW, window=btn)
    panel2.resizable(False, False) 
    panel2.geometry('{}x{}+350+200'.format(WIDTH, HEIGTH))  


def Fourth_Panel():
    global panel3, entr1, entr2, entr3, entr4, cal, v
    panel3 = tk.Tk()
    panel3.title("Register New Admin")
    Canvas = Set_Background(panel3,WIDTH, HEIGTH) 
    gender = None
    lbl1 = Canvas.create_text((50, 30), anchor=tk.NW, text = "First Name", font=("Times New Roman", 20), fill='white')
    lbl2 = Canvas.create_text((320, 30), anchor=tk.NW,text = "Last Name", font=("Times New Roman", 20),fill ='white')
    lbl3 = Canvas.create_text((50, 80), anchor=tk.NW,text = "Password", font=("Times New Roman", 20), fill='white')
    lbl4 = Canvas.create_text((50, 120), anchor=tk.NW,text = "Confirm Password", font=("Times New Roman", 20), fill='white')
    entr1=tk.Entry(panel3, width = 20, borderwidth=2, relief='ridge', highlightbackground='white')
    entr1.config(highlightthickness=0)
    entr11 = Canvas.create_window(180, 35, anchor=tk.NW, window=entr1)
    entr2=tk.Entry(panel3, width = 20, borderwidth=2, relief='ridge')
    entr20 = Canvas.create_window(450, 35, anchor=tk.NW, window=entr2)
    entr3=tk.Entry(panel3,width = 20, borderwidth=2, relief='ridge', show='*')
    entr33 = Canvas.create_window(170, 85, anchor=tk.NW, window=entr3)
    entr4=tk.Entry(panel3, width = 20, borderwidth=2, relief='ridge', show='*')
    entr44 = Canvas.create_window(270, 125, anchor=tk.NW, window=entr4)
    date = Canvas.create_text((50, 170), anchor=tk.NW, text='Birthdate', font=("Times New Roman", 20), fill='white')    
    cal = DateEntry(panel3, width=20, background='blue',foreground='white', borderwidth=2)
    call = Canvas.create_window(170, 170, anchor=tk.NW, window=cal)
    v = tk.StringVar()
    v.set("NA")
    lbl5 =  Canvas.create_text((50, 215), anchor=tk.NW,text="Gender: ", font=("Times New Roman", 20), fill='white')
    rd1 = tk.Radiobutton(panel3, text="Male", font=("Times New Roman", 18),variable=v, value="Male")
    rd11 =  Canvas.create_window(170, 200, anchor=tk.NW, window=rd1)
    rd2 = tk.Radiobutton(panel3, text="Female", font=("Times New Roman", 18), variable=v, value="Female")
    rd22 =  Canvas.create_window(170, 230, anchor=tk.NW, window=rd2)
    btn=tk.Button(panel3 , text='Back' , borderwidth=2, width = wedg_width, height = wedg_height, font=("Times New Roman", 20), fg="black", bg='snow', command=Controller4)
    btn.pack(side='right' ,padx=50)
    butn = Canvas.create_window(50, 320, anchor=tk.NW, window=btn)    
    btn1=tk.Button(panel3 , text='Confirm User' , borderwidth=2,width = wedg_width, height = wedg_height, font=("Times New Roman", 20), fg="black", bg='snow', command=Controller5)
    btn1.pack(side='right' ,padx=50)
    butn1 = Canvas.create_window(400, 320, anchor=tk.NW, window=btn1)
    panel3.resizable(False, False) 
    panel3.geometry('{}x{}+350+200'.format(WIDTH, HEIGTH))
    
def Fifth_Panel():
    global panel4, entr1, entr2
    panel4 = tk.Tk()
    panel4.title("LogIn")
    Canvas = Set_Background(panel4,WIDTH, HEIGTH)
    panel4.resizable(False, False) 
    panel4.geometry('{}x{}+350+200'.format(WIDTH, HEIGTH))
    lbl1 = Canvas.create_text((100, 30), anchor=tk.NW, text="User Name: ", fill='white', font=("Times New Roman", 26))
    e = tk.StringVar()
    entr1 = tk.Entry(panel4, textvariable=e,width=30, relief='ridge', borderwidth=2) 
    entr11 = Canvas.create_window(270, 40, anchor=tk.NW, window=entr1)
    Pass = Canvas.create_text((100, 90), anchor=tk.NW,text="Password: ", font=("Times New Roman", 26), fill='white')
    e1 = tk.StringVar()
    entr2 = tk.Entry(panel4, textvariable=e1, fg="black", relief='ridge', show='*',width=30 , borderwidth=2)  
    entr20 = Canvas.create_window(270, 100, anchor=tk.NW, window=entr2)
    var1 = tk.IntVar()
    c1 = tk.Checkbutton(panel4, text='Remember Me',variable=var1, onvalue=1, offvalue=0)
    c11 = Canvas.create_window(250, 180, anchor=tk.NW, window=c1)
    loginButton = tk.Button(panel4, text="LogIn", font=("Times New Roman", 20), width = wedg_width, height = wedg_height, command= Controller6)
    btn = Canvas.create_window(420, 320, anchor=tk.NW, window=loginButton)
    btn1=tk.Button(panel4 , text='Back' , borderwidth=2,  width = wedg_width, height = wedg_height, font=("Times New Roman", 20), fg="black", bg='snow', command=Controller7)
    btn1.pack(side='left' ,padx=50)
    butn1 = Canvas.create_window(50, 320, anchor=tk.NW, window=btn1) 
    
def Sixth_Panel():
    global panel5
    panel5 = tk.Tk()
    panel5.title("Profile")
    Canvas = Set_Background(panel5,WIDTH, HEIGTH)
    panel5.resizable(False, False) 
    panel5.geometry('{}x{}+350+200'.format(WIDTH, HEIGTH))
    img1 = ImageTk.PhotoImage(Image.open(r'GUI IMAGES\cam.png').resize((110, 80), Image.ANTIALIAS))
    button1 = tk.Button(panel5, compound=tk.TOP, width=155, height=55, image=img1,
        text="optional text", command=Controller8)
    button1.pack(side=tk.LEFT, padx=2, pady=2)
    button1.image = img1
    icon1 = Canvas.create_image(500, 25, anchor=tk.NW, image=img1, state=NORMAL)
    lbl1 = Canvas.create_text((500, 115), anchor=tk.NW, text = "New Person", font=("Times New Roman", 18), fill='white')
    img2 = ImageTk.PhotoImage(Image.open(r'GUI IMAGES\eye.png').resize((110, 80), Image.ANTIALIAS))
    button2 = tk.Button(panel5, compound=tk.TOP, width=155, height=55, image=img2, text="Cameras", bg='snow')
    button2.pack(side=tk.LEFT, padx=2, pady=2)
    button2.image = img2
    icon1 = Canvas.create_image(50, 210, anchor=tk.NW, image=img2, state=NORMAL)
    lbl2 = Canvas.create_text((50, 300), anchor=tk.NW, text = "Surveillance\n   System", font=("Times New Roman", 18), fill='white')
    img3 = ImageTk.PhotoImage(Image.open(r'GUI IMAGES\output-onlinepngtools.png').resize((110, 80), Image.ANTIALIAS))
    button3 = tk.Button(panel5, compound=tk.TOP, width=155, height=55, image=img3,
        text="optional text", bg='snow')
    button3.pack(side=tk.LEFT, padx=2, pady=2)
    button3.image = img3
    icon3 = Canvas.create_image(50, 25, anchor=tk.NW, image = img3, state=NORMAL)
    lbl3 = Canvas.create_text((50, 115), anchor=tk.NW, text = "Alarm Msgs", font=("Times New Roman", 18), fill='white')
    img4 = ImageTk.PhotoImage(Image.open(r'GUI IMAGES\1211765567.png').resize((110, 80), Image.ANTIALIAS))
    button4 = tk.Button(panel5, compound=tk.TOP, width=155, height=55, image=img4,
        text="optional text", bg='snow')
    button4.pack(side=tk.LEFT, padx=2, pady=2)
    button4.image = img4
    icon4 = Canvas.create_image(290, 25, anchor=tk.NW, image = img4, state=NORMAL)
    lbl4 = Canvas.create_text((290, 115), anchor=tk.NW, text = "Alarm Msgs", font=("Times New Roman", 18), fill='white')
    btn1=tk.Button(panel5 , text='Cameras' , borderwidth=2, width = 8, height = wedg_height, font=("Times New Roman", 20), fg="black", highlightbackground="snow",highlightcolor = "black", highlightthickness=2 ,bg='snow', command=Controller8)
    btn1.pack(side='right' ,padx=50)
    butn1 = Canvas.create_window(500, 250, anchor=tk.NW, window=btn1)
    
#############################
""" Pannels Controllers """
#############################
def Controller():
    Root.destroy()
    Second_Panel()

def Controller2():
    panel1.destroy()
    Third_Panel()


def Controller3():
    panel1.destroy()
    Fourth_Panel()

def Controller4():
    panel3.destroy()
    Third_Panel()  

def Controller5():
    if (entr1.get() == '') or (entr2.get()== '') or (entr3.get()== '') or (entr4.get() == '') or (v.get() == "NA"):
        tk.messagebox.showinfo("Information","ALL FIELDS ARE REQUIRED PLEASE FILL ALL OF THEM")
    elif entr3.get() != entr4.get() :
        print("The Password Doesn't Matched!")   
        tk.messagebox.showwarning("WARNING","THE PASSWORD DOESN't MATCHED!")
    else:
        if v.get() == "Male":
            Gender = "Male"
        elif v.get() == "Female":
            Gender = "Female"
        print(Users_Saving(entr1.get(), entr2.get(), entr3.get(), cal.get(), Gender))
        panel3.destroy()
        Fifth_Panel()

def Controller6():
    if (entr1.get() == '') or (entr2.get()== ''):
        tk.messagebox.showinfo("Information","ALL FIELDS ARE REQUIRED PLEASE FILL ALL OF THEM")
    Flag = Validate_User(entr1.get(), entr2.get())
    if Flag is True:
        panel4.destroy()
        Sixth_Panel()
    else:
        tk.messagebox.showerror("ERROR","User Not Found!")
 
def Controller7():
    panel4.destroy()
    Fourth_Panel()

def Controller8():
    panel5.destroy()
    Last_Panel()
def Controller9():
    panel2.destroy()
    Sixth_Panel()
    
#########################
""" Main Panel """
#########################
def Main_Panel():
    global Root, wedg_height, wedg_width
    wedg_width = 13
    wedg_height = 1
    Root = tk.Tk()
    Root.title("Root")
    Canvas = Set_Background(Root,WIDTH, HEIGTH)
    Text = tk.Label(Root, text="Automated Survilliance System",font=("Times New Roman", 26), fg ="black")
    Icon = ImageTk.PhotoImage(Image.open(r'GUI IMAGES\eye.png').resize((300, 170), Image.ANTIALIAS))
    Labl = tk.Label(Root)
    Labl.pack(side='right', padx=15, pady=5)
    Labl.imgtk = Icon
    Labl.configure(image=Icon)
    text = Canvas.create_text((190, 190),text="       Automated\n Survilliance System",font=("Times New Roman", 28), fill ="white", anchor=tk.NW)
    icon = Canvas.create_image(200, 43,image = Icon, anchor=tk.NW)
    btn=tk.Button(Root , text='Next' , borderwidth=2, width = 8, height = wedg_height, font=("Times New Roman", 20), fg="black", highlightbackground="snow",highlightcolor = "black", highlightthickness=2 ,bg='snow', command=Controller)
    btn.pack(side='right' ,padx=50)
    butn = Canvas.create_window(500, 330, anchor=tk.SW, window=btn)
    Root.resizable(False, False)
    Root.geometry('{}x{}+350+200'.format(WIDTH, HEIGTH))
    Root.mainloop()
Main_Panel()




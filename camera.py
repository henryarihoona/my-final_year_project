import tkinter
from tkinter import *
from ttkbootstrap import Style
from tkinter import ttk, Label, messagebox, simpledialog

from plyer import notification
from PIL import ImageTk, Image
import numpy as np
from pathlib import Path
from imutils import paths
import face_recognition, time, smtplib, cv2, re
from twilio.rest import Client
import datetime

style = Style(theme='cyborg')

# data base
import sqlite3
# data base connection
conn = sqlite3.connect('dbs/ai-cam.db')
# create accounts table
conn.execute('''CREATE TABLE IF NOT EXISTS accounts (FIRSTNAME VARCHAR, LASTNAME VARCHAR, PHONE_NO VARCHAR, USERNAME VARCHAR UNIQUE, PIN VARCHAR)''')

# INTEGER PRIMARY KEY
conn.execute('''CREATE TABLE IF NOT EXISTS notify (id INTEGER PRIMARY KEY, EMAIL VARCHAR, PHONE VARCHAR)''')

try:
    conn.econnxecute("INSERT INTO accounts (FIRSTNAME, LASTNAME,PHONE_NO,USERNAME, PIN)\
    VALUES ('Main','Admin','0750941273','admin','admin')")

    conn.commit()
    conn.close()
except Exception as e:
    conn.close()
    print("Connection Error: ", e)

# app window
app = style.master
app.geometry('800x400+50+50')
app.title('VISION CAM AI')
app.minsize(540,360)
app.maxsize(800,400)
# app.resizable(False, False)
img = ImageTk.PhotoImage(Image.open("pics/robot.ico"))
app.tk.call('wm','iconphoto',app._w, img)


# create a notebook
notebook = ttk.Notebook(app, padding=5)
notebook.pack(expand=True, side=LEFT, fill=BOTH)

# login frame
login = ttk.Frame(notebook)
login.pack(fill='both', expand=True)
# train frame
train = ttk.Frame(notebook)
train.pack(fill='both', expand=True)
# survillance frame
cam = ttk.Frame(notebook)
cam.pack(fill='both', expand=True)
# camera setup frame
setup = ttk.Frame(notebook)
setup.pack(fill='both', expand=True)
# add frames to notebook
notebook.add(login, text='GET STARTED')
notebook.add(train, text='REGISTER ACCOUNT')
notebook.add(cam, text='AI-CAM HOME')
notebook.add(setup, text='CAMERA SETUP')

# hide
notebook.tab(1, state="hidden")
notebook.tab(2, state="hidden")
notebook.tab(3, state="hidden")

# -----------------login page-------------------
name = tkinter.StringVar(value='admin', name='username')
passw = tkinter.StringVar(value='admin', name='password')
# login form
loginFrame = ttk.LabelFrame(login, text='LOGIN TO EXISTING ACCOUNT')
loginFrame.pack(fill='y', pady=10, padx=(10), ipadx=10)

Label(loginFrame).grid(column=2, padx=5)

# create label/entry rows
ttk.Label(loginFrame, text='Usename').grid(row=0, column=0, sticky='e', pady=10, padx=(0, 10))
ttk.Entry(loginFrame, textvariable=name, width=50).grid(row=0, column=1, sticky='ew')

ttk.Label(loginFrame, text='Password').grid(row=1, column=0, sticky='e', pady=10, padx=(0, 10))
ttk.Entry(loginFrame, textvariable=passw, width=50, show='*').grid(row=1, column=1, sticky='ew')

# submit button
submit = ttk.Button(loginFrame, text='Login', style='success.TButton', cursor='hand2')
submit.grid(row=4, column=1, sticky='w', pady=10)
loginFrame.columnconfigure(0, weight=1)
ttk.Label(login, text='-OR-').pack(fill=Y)


# -----------------register page-------------------
registerFrame = ttk.LabelFrame(login, text='REGISTER NEW ACCOUNT')
registerFrame.pack(fill='y', pady=10, padx=(10), ipadx=10)
# submit button
register = ttk.Button(registerFrame, text='Register Now', style='primary.TButton', cursor='hand2')
register.grid(row=0, column=0, sticky='n', pady=10)
registerFrame.columnconfigure(0, weight=1)


# register account
registerF = ttk.LabelFrame(train, text="Fill The Form")
registerF.pack(fill='y', pady=10, padx=(10), ipadx=10)

phone = tkinter.StringVar(value='', name='phonenumber')
fname = tkinter.StringVar(value='', name='firstname')
lname = tkinter.StringVar(value='', name='lastname')
passww = tkinter.StringVar(value='', name='passww')
usern = tkinter.StringVar(value='', name='usern')

# create label/entry rows
ttk.Label(registerF, text='First Name').grid(row=1, column=0, sticky='e', pady=10, padx=(0, 10))
ttk.Entry(registerF, textvariable=fname, width=45).grid(row=1, column=1, sticky='ew')
# create label/entry rows
ttk.Label(registerF, text='Last Name').grid(row=2, column=0, sticky='e', pady=10, padx=(0, 10))
ttk.Entry(registerF, textvariable=lname, width=45).grid(row=2, column=1, sticky='ew')
# create label/entry rows
ttk.Label(registerF, text='User Name').grid(row=3, column=0, sticky='e', pady=10, padx=(0, 10))
ttk.Entry(registerF, textvariable=usern, width=45).grid(row=3, column=1, sticky='ew')
# create label/entry rows
ttk.Label(registerF, text='Phone number').grid(row=4, column=0, sticky='e', pady=10, padx=(0, 10))
ttk.Entry(registerF, textvariable=phone, width=45).grid(row=4, column=1, sticky='ew')
# create label/entry rows
ttk.Label(registerF, text='Password').grid(row=5, column=0, sticky='e', pady=10, padx=(0, 10))
ttk.Entry(registerF, textvariable=passww, width=45, show='*').grid(row=5, column=1, sticky='ew')
# submit 
def GoBack():
    phon = phone.get()
    fnam = fname.get()
    lnam = lname.get()
    passw = passww.get()
    user = usern.get()
    

    if(phon!="" or fnam !="" or lnam!="" or passw!="" or user!=""):
        answer = messagebox.askyesnocancel("Data Loss!","Looks like you didnot complete the registration process, should we proceed to go back to login page? \n All form data will be lost.")
        if answer:
            phone.set("")
            fname.set("")
            lname.set("")
            passww.set("")
            usern.set("")
            notebook.tab(1, state="hidden")
            notebook.select(0)
    else:
        notebook.tab(1, state="hidden")
        notebook.select(0)

ttk.Button(registerF, text='Back', style='Outline.TButton', cursor='hand2', command=GoBack).grid(row=6, column=0, sticky='n', pady=10)
registerBtn = ttk.Button(registerF, text='Register Now', style='success.TButton', cursor='hand2')
registerBtn.grid(row=6, column=1, sticky='n', pady=10)

def registerAccount():
    phon = phone.get()
    fnam = fname.get()
    lnam = lname.get()
    passw = passww.get()
    user = usern.get()

    if(phon=="" or fnam =="" or lnam=="" or passw=="" or user==""):
        messagebox.showinfo("Required!", "Please fill all the fields with valid data.")
    else:
        registerBtn.configure(text="Please Wait")
        try:
            conn = sqlite3.connect('dbs/ai-cam.db', timeout=10)
            sql = ("INSERT INTO accounts (FIRSTNAME, LASTNAME,PHONE_NO,USERNAME, PIN)\
            VALUES (?,?,?,?,?)")
            valz = (fnam,lnam,phon,user,passw)
            conn.execute(sql, valz)
            conn.commit()
            conn.close()
            registerBtn.configure(text="Register Now")

            phone.set("")
            fname.set("")
            lname.set("")
            passww.set("")
            usern.set("")

            notification.notify(
                title = "Account Created!",
                message = "Account registration successful. \nLogin with; \nUsername:'"+str(user)+"'\nPassword: '"+str(passw)+"'",
                timeout = 15
            )

            notebook.tab(1, state="hidden")
            notebook.select(0)

            messagebox.showinfo("Done!", "Account registration successful. \nLogin with; \nUsername:'"+str(user)+"'\nPassword: '"+str(passw)+"'")            

        except Exception as e:
            registerBtn.configure(text="Register Now")
            usern.set("")
            notification.notify(
                title = "Database Notice.",
                message = "Message: "+str(e),
                timeout = 15
            )
            messagebox.showerror("Heads Up!", "Message: "+str(e))


registerBtn.configure(command=registerAccount)
    


# ------- app function -----------
def login_now(*args):
    nam = name.get()
    pasw = passw.get()

    if(nam==""):
        messagebox.showinfo("", "Provide your account username.")
    elif(pasw==""):
        messagebox.showinfo("", "Provide your account password/pin.")
    else:
        # login
        conn = sqlite3.connect('dbs/ai-cam.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        sql3 = ('SELECT * FROM accounts WHERE USERNAME=? and PIN=?' )
        valz = (nam, pasw)
        cursor.execute(sql3, valz)
        value = cursor.fetchone()
        phone_number = value['PHONE_NO']
        # print("Datata=>",value['FIRSTNAME'])
        if(value != None):
            if(nam==value['USERNAME']) and pasw==value['PIN']:
                notification.notify(
                    title = "Welcome "+value['USERNAME']+"!",
                    message = "You are now logged in as : "+ value['FIRSTNAME']+" "+value['LASTNAME'],
                    timeout = 15
                )
                # show dash tab, hide login tab
                notebook.tab(0, state="hidden")
                notebook.select(2)
                loginText.configure(text='Signed In As : '+value['FIRSTNAME']+" "+value['LASTNAME']+ " "+ value['PHONE_NO'])  

            else:
                messagebox.showinfo("", "No user associated with these credintials, try registering.")
            conn.close()
        else:
            notification.notify(
                title = "Login Failed!",
                message = "No user associated with these credintials, try registering.",
                timeout = 15
            )
            messagebox.showinfo("Login Failed!", "No user associated with these credintials, try registering.")

# add command to submit button
submit.configure(command=login_now)
# app.bind("<Return>",login_now)

#app dash
dashFrame = ttk.Frame(cam)
dashFrame.pack(fill='y', pady=15, padx=10)

Label(dashFrame, text='CAMERA MENU', font=("arial",15,"bold")).grid(row=0, columnspan=4, sticky="EW")

# images
regImg = ImageTk.PhotoImage(Image.open("./pics/reg.png"))
setImg = ImageTk.PhotoImage(Image.open("./pics/set.png"))
startImg = ImageTk.PhotoImage(Image.open("./pics/start.png"))
outImg = ImageTk.PhotoImage(Image.open("./pics/out.png"))


# register faces
regBtn = ttk.Button(dashFrame, image=regImg, text='Register Faces', style='primary.TButton', cursor="hand2", compound=TOP)
regBtn.grid(row=1, column=0, pady=20, padx=20)

# setup camera
setBtn = ttk.Button(dashFrame,image=setImg, text='Setup Camera', style='info.TButton', cursor="hand2", compound=TOP)
setBtn.grid(row=1, column=1, pady=20, padx=20)

# start camera
startBtn = ttk.Button(dashFrame,image=startImg, compound=TOP, text='Start Camera', style='success.TButton', cursor="hand2")
startBtn.grid(row=1, column=2, pady=20, padx=20)

# logout camera

logoutBtn = ttk.Button(dashFrame, text='Logout Now',image=outImg, compound=TOP, style='danger.TButton', cursor="hand2")
logoutBtn.grid(row=1, column=3, pady=20, padx=20)

# login details label
loggerVal = tkinter.StringVar(value="Camera Status")
statusText = Label(cam, textvariable=loggerVal, font=("arial",8,"bold"), fg='gold')
statusText.pack(expand=True, side=BOTTOM, fill=BOTH)


loginText = Label(cam, text='', font=("arial",12,"bold"))
loginText.pack(expand=True, side=BOTTOM, fill=BOTH)



# ------------functions-----------
# register faces to recognize
def registerFaces():
    name = simpledialog.askstring("Persons Name.", "Provide a name of this person.", parent=dashFrame).upper()

    if (len(name) > 0):
        print("Register Faces")
        # continue with camera capture
        cam = cv2.VideoCapture(0)
        cam.set(3, 640) # set video width
        cam.set(4, 480) # set video height
        face_detector = cv2.CascadeClassifier('cascade/haarcascade_frontalface_default.xml')

        # take the images
        face_id = 1
        count = 0

        messagebox.showinfo("Heads Up", "This process will take upto 10 seconds, once the camera is done registering faces, it will close automatically.")

        while(True):
            ret, img = cam.read()
            img = cv2.flip(img, 1) # flip video image vertically
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
                count += 1
                # Save the captured image into the datasets folder
                cv2.imwrite("dataset/"+name+"." + str(face_id) + '.' +  
                            str(count) + ".jpg", gray[y:y+h,x:x+w])
                cv2.imshow('Face of '+name, img)
            k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
            if k == 27:
                messagebox.showinfo("Closed.", "The camera registered "+str(count)+" images of "+name)
                break
            elif count >= 10: # Take 10 face sample and stop video
                messagebox.showinfo("Done.", "The camera registered "+str(count)+" images of "+name)
                break

        # release and close camera
        cam.release()
        cv2.destroyAllWindows()

    else:
        messagebox.showerror("Invalid Name", "The person's name is required. Please try again.")

# set
regBtn.configure(command=registerFaces)

# set camera
def setCamera():
    print("Set Camera")
    notebook.select(3)
    
setBtn.configure(command=setCamera)

# ----------------start camera and face recognition---------------
def startCamera():
    loggerVal.set("Checking Available data... Please wait.")

    messagebox.showinfo("Notice!", "Be reminded that you will have to wait until the AI checks all data saved, this will take some good minutes but be patient. \nAfter the camera will start. \nPress Q to exit camera.")

    mypath = Path(__file__).parent.absolute()
    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)
    # Create arrays of known face encodings and their names
    known_face_encodings = []
    known_face_names = []
    # get files and filter names
    imagePaths = list(paths.list_images('dataset'))

    for (i, imagePath) in enumerate(imagePaths):
        # print("I=",i,"imagePath=",imagePath)
        # extract the person name from the image path
        img_name = imagePath.split('.')[0].split('/')[1]

        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #Use Face_recognition to locate faces
        boxes = face_recognition.face_locations(rgb,model='hog')
        # compute the facial embedding for the face
        print("[Encoding] Image at ",imagePath)
        app.after(1000, update_clock)

        encodings = face_recognition.face_encodings(rgb, boxes)
        for encoding in encodings:
            loggerVal.set("[Encoding] Image at "+imagePath)
            known_face_encodings.append(encoding)
            known_face_names.append(img_name)

    loggerVal.set("[Starting Camera] : Wait a moment!")
    time.sleep(1)
    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    # start camera
    print("[Starting Camera ] Please wait.")
    if(len(known_face_names)>0):
        while True:
            statusText.configure(text="[Camera On] : Press <q> any time to exit live camera." )
            time.sleep(1)
            # Grab a single frame of video
            ret, frame = video_capture.read()

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"

                    # # If a match was found in known_face_encodings, just use the first one.
                    # if True in matches:
                    #     first_match_index = matches.index(True)
                    #     name = known_face_names[first_match_index]

                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]


                    face_names.append(name)

                    if(name == 'Unknown'):
                        print("Unknown person found.")
                        
                        #Sending an SMS notification
                        Detected_time = datetime.datetime.now()
                        account_sid = 'ACb5fcde597cd8f6e88cea3cd7e8ab5131' 
                        auth_token = 'c28b19e631903bd4e52a9e4b9dff89ea' 
                        client = Client(account_sid, auth_token) 
 
                        message = client.messages.create(  
                              messaging_service_sid='MG2698ae7be5cb32bf85c4ec39551506ed', 
                              body='Vision AI-Camera has detected an unknown person at :' + Detected_time,      
                              to='+256786836968' 
                          ) 
 
                        print(message.sid)
                        notification.notify(
                            title = "Person Unknown",
                            message = "Camera has detected an unknown person.",
                            timeout = 15
                        )
                    else:
                        print("Am looking at",name)
                        notification.notify(
                            title = "Person Known",
                            message = "Camera has detected a person named "+str(name),
                            timeout = 15
                        )

            process_this_frame = not process_this_frame


            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Display the resulting image
            cv2.imshow('AI Camera Live Feed', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()
        statusText.configure(text="Camera Off" )
    else:
        loggerVal.set("No registered faces.")
        messagebox.showerror("Notice!", "Hey \n You need to register faces before starting the camera survillance. PLease try again.")

# configure set camera button   
startBtn.configure(command=startCamera)

# logout cam
def logoutCamera():
    answer = messagebox.askyesno("Logout!", "Are you sure you want to do this?")
    if answer:
        notebook.tab(2, state="hidden")
        notebook.select(0)


    print("Answer", answer)
logoutBtn.configure(command=logoutCamera)

# register account
def registerAccount():
    notebook.tab(0, state="hidden")
    notebook.select(1)

register.configure(command=registerAccount)

# setup camera
# survilance dash
setupFrame = ttk.LabelFrame(setup, text="NOTIFICATION DETAILS")
setupFrame.pack(fill='y')

Label(setupFrame, text='NEW NOTIFICATION DETAILS', font=("arial",15,"bold")).grid(row=0, columnspan=4, sticky="EW")

# form
email = tkinter.StringVar(value="", name="email")
phono = tkinter.StringVar(value="", name="phono")
# create label/entry rows
ttk.Label(setupFrame, text='Notifiction Email').grid(row=1, column=0, sticky='e', pady=10, padx=(0, 10))
ttk.Entry(setupFrame, textvariable=email, width=45).grid(row=1, column=1, sticky='ew')
# create label/entry rows
ttk.Label(setupFrame, text='Notifiction Phone').grid(row=2, column=0, sticky='e', pady=10, padx=(0, 10))
ttk.Entry(setupFrame, textvariable=phono, width=45,).grid(row=2, column=1, sticky='ew')
# btn
def backMe():
    notebook.tab(3, state="hidden")

ttk.Button(setupFrame, text='Close', command=backMe, style='Outline.TButton', cursor="hand2").grid(row=3, column=0)
saveBtn = ttk.Button(setupFrame, text='Save Details', style='success.TButton', cursor="hand2")
saveBtn.grid(row=3, column=1)

treeFrame = ttk.LabelFrame(setupFrame, text="SAVED DETAILS")
treeFrame.grid(row=4, columnspan=2, padx=5, pady=5)

out2Iv = Frame(treeFrame, bg="white")
out2Iv.pack(fill=X, side=BOTTOM)


# treeview
cols=("#", "EMAIL", "PHONE")
scoreOUT = ttk.Treeview(treeFrame, height=5, column=cols, show="headings")
scoreOUT.pack(side=LEFT, fill=BOTH)
scoreOUTv = Scrollbar(treeFrame, command=scoreOUT.yview)
scoreOUTv.pack(side=RIGHT, fill=Y)

scoreOUTh = Scrollbar(out2Iv,orient=HORIZONTAL, command=scoreOUT.xview)
scoreOUTh.pack(fill=X)
scoreOUT.config(yscrollcommand=scoreOUTv.set, xscrollcommand=scoreOUTh.set)

for column in cols:
  scoreOUT.heading(column, text=column)
scoreOUT.rowconfigure(0, weight=1)
scoreOUT.columnconfigure(0, weight=1)
scoreOUT.column(0, width=50)
scoreOUT.column(1, width=300)
scoreOUT.column(2, width=150)


# get saved contacts notify
def getNotif():
    conn = sqlite3.connect('dbs/ai-cam.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notify")
    result = cursor.fetchall()

    count = 1

    for row in result:
        print({"id":row['id'],'email':row['email'],'phone':row['phone']})
        data = (count, row['email'], row['phone'])

        scoreOUT.insert('', END, values=data)
        count = count+1

# save contact
def saveContact():
    emal = email.get()
    phon = phono.get()
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if(phon=="" or emal ==""):
        messagebox.showinfo("Required!", "Please fill email and phone with valid data.") 
    else:
        if (re.search(regex, emal)):
        
            try:
                conn = sqlite3.connect('dbs/ai-cam.db', timeout=10)
                sql = ("INSERT INTO notify (EMAIL, PHONE) VALUES (?,?)")
                valz = (emal,phon)
                conn.execute(sql, valz)
                conn.commit()
                conn.close()
                registerBtn.configure(text="Register Now")

                email.set("")
                phono.set("")
                # get notifs
                getNotif()

                messagebox.showinfo("Done!", "Details added successful.")
            except Exception as e:
                messagebox.showerror("Heads Up!", "Message: "+str(e))
        else:
            messagebox.showinfo("Invalid Email!", "The email entered is invalid, please ty again.")

saveBtn.configure(command=saveContact)


def update_clock():
    now = time.strftime("%H:%M:%S")
    # self.label.configure(text=now)
    loggerVal.set(now)
    print("Time Now", now)
    app.after(1000, update_clock)

# app loop
getNotif()
update_clock()
app.mainloop()
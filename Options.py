# This will import all the widgets 
# and modules which are available in 
# tkinter and ttk module
from tkinter import *
from tkinter.ttk import *
from Functions.MsgBox import createMsgBox
import mysql.connector
from Functions.SearchDB import searchRegClass
from Functions.SearchDB import returnAllDetentions
from Functions.InsSort import insertionSortDates

class PupilRecord: #this class is crated for the seatching and handeling of pupil info 
    def __init__(self,scn=str(),fullName=str(),regClass=str()):
        self._scn = scn # scottish candidate number used as primary key in student table
        self._fullName = fullName # full student name
        self._regClass = regClass # pupil registration class
    def getScn(self): # returns Scottish Candidate Number
        return self._scn
    def getFullName(self): # returns full pupil name
        return self._fullName
    def getRegClass(self): # returns pupil registration class
        return self._regClass

class DetentionRecord:# this is used to store all possible detenions a pupil can be assigned to
    def __init__(self,detentionID=int(),detentionDate=str(),detentionType = str(),roomNo = str(),teacherID = int()):
        self._detentionID = detentionID # detentionID is the primary key of the detention table
        self._detentionDate = detentionDate # date of detentoin
        self._detentionType = detentionType # type of detention wither lunch or after school
        self._roomNo = roomNo # room number, where the detention is 
        self._teacherID = teacherID # teacherId links the detention Record table to the Teacher table
    def getDetentionID(self): # returns detentionID
        return self._detentionID
    def getDetentionDate(self): # returns date of detention
        return self._detentionDate
    def getDetentionType(self): # returns types of detention (lunchtime of afterschool)
        return self._detentionType
    def getRoomNo(self): # returns the room the detention is in
        return self._roomNo
    def getTeacherID(self): # returns the ID of the teacher supervising the detention
        return self._teacherID

class PupilDetentionRecord: #this is used to store data of a new pupil being added to the pupildetention table
    def __init__(self,detentionID=int(),scn=str(),reason=str()):
        self._detentionID = detentionID
        self._scn = scn
        self._reason = reason
    def getDetentionID(self):
        return self._detentionID
    def getScn(self):
        return self._scn
    def getReason(self):
        return self._reason

class Staff: # this is used to store staff data for display along side detention records
    def __init__(self,staffId=int(),FirstName=str(),Surname=str(),departmentName=str()):
        self._staffId = staffId
        self._FirstName = FirstName
        self._Surname = Surname
        self._departmentName = departmentName
    def getStaffID(self):
        return self._staffId
    def getFirstName(self):
        return self._FirstName
    def getSurname(self):
        return self._Surname
    def getFullName(self):
        return self._FirstName + self._Surname
    def getDepartmentName(self):
        return self._departmentName


def launchOptions(user):
    currentUser = user
    currentUserFullName = currentUser[1]+" "+currentUser[2]
    # creates a Tk() object 
    master = Tk() 

    # sets the geometry of main 
    # root window 
    master.geometry("400x200")
    master.title("Options") 

    def SetDetention():
        SD = Toplevel(master)
        SD.title("Add pupil to detention")
        SD.geometry("600x400")
        regClass = StringVar(master)
        pupilName = StringVar(master)
        detentionDateTime = StringVar(master)
        DEFAULT_PUPIL = "please select pupil name"
        DEFAULT_REGTEXT = "please select regClass"
        DEFAULT_DATE_TIME = "please select a Date/Time"
        detentions = []# this will be a list of the class instances of DetentionRecord
        detentionDates =[] # this will hold concatinated dates and times for the purpose of displaying them
        detentionDates.append(DEFAULT_DATE_TIME)
        pupils = [] # this will hold all the class intances of pupilRecord
        pupilNames =[]# this will hold all the full names from pupil for the purpose of displaying them 
        pupilNames.append(DEFAULT_PUPIL)
        try:
            cnx = mysql.connector.connect(host="localhost",user="root", password="",database="schooldetention") # connects to sql database to check if username and password are correct
        except mysql.connector.Error as err:
            createMsgBox(f"{err}","connection error")
            SD.destroy()
        else:
            query = cnx.cursor()
            
            def getPupilsInReg(pupils,pupilNames):
                if regClass.get() != DEFAULT_REGTEXT:
                    pupils = searchRegClass(regClass.get(),PupilRecord)
                    pupilNames = [] # this line and the line below are used to clear the list of pupil names so no duplicates are displayed if thie button is pressed multiple times.
                    pupilNames.append(DEFAULT_PUPIL)
                    for z in pupils:
                        pupilNames.append(z.getFullName())
                   
                    updatePupilDrowdown(pupilNames)
                    selectPupil.config(state="normal")
                else: 
                    createMsgBox("Please select registration class","Reg Class error")

            def updatePupilDrowdown(pupilNames):
                selectPupil['menu'].delete(0,'end')
                for name in pupilNames[1:]:
                    selectPupil['menu'].add_command(label=name,command = lambda name = name : pupilName.set(name))
            
            def getAvailableDetentions(detentions,detentionDates):
                detentions = returnAllDetentions(DetentionRecord)
                detentions =  insertionSortDates(detentions) 
                for x in detentions:
                    detentionDates.append(str(x.getDetentionDate()+" "+ x.getDetentionType()+" ("+x.getRoomNo()+")"))

            def addPupilDetention( regClass, pupilName , reason , dateTime , PupilDetentionRecord):        
                if regClass.get() == DEFAULT_REGTEXT or pupilName.get() == DEFAULT_PUPIL or dateTime.get() == DEFAULT_DATE_TIME or reason == "":
                    createMsgBox("Form incomplete","Missing Information")
                else:
                    dateTime = str(dateTime.get()).split()
                    if  len(dateTime) == 4: # this checks if the after school type was split and reconcatinates it
                        dateTime[1] = dateTime[1]+" "+dateTime[2]
                        del dateTime[-2]# this removes the room number and the second unconcatinated part of the after school detention type
                    else:
                        del dateTime[-1] #this removes the room number from the submitted data
                    pupilName = str(pupilName.get()).split()
                    pupilFirstName=" ".join(pupilName[:-1])
                    pupilSurname= pupilName[-1]
                    query.execute(f"SELECT detentionID FROM Detention WHERE DetentionDate = \"{dateTime[0]}\" AND DetentionType = \"{dateTime[1]}\"")
                    detentionID =query.fetchall()
                    detentionID = str(detentionID[0][0])[:1] # this extracts the detentionID from the list of tuples and converts it to a string
                    query.execute(f'SELECT Scn FROM Pupil WHERE RegClass = \"{regClass.get()}\" AND FirstName = \"{pupilFirstName}\" AND Surname = \"{pupilSurname}\" ')
                    scn = query.fetchall()
                    scn =str(scn[0][0])
                    detentionEntry = PupilDetentionRecord(detentionID,scn,reason)
                    try:
                        query.execute(f'INSERT INTO pupildetention (DetentionID,Scn,Reason) VALUES (\"{detentionEntry.getDetentionID()}\" , \"{detentionEntry.getScn()}\" , \"{detentionEntry.getReason()}\" )')   
                    except:
                        createMsgBox("Student cannot be added to the same detention twice","Duplicate data entry")
                    else:
                        cnx.commit()
                        createMsgBox("student added successfuly","Detention Added")
                        SD.destroy()

            query.execute("SELECT * FROM Reg")
            resultsReg = query.fetchall()
            resultsReg = [str(y[0]) for y in resultsReg]   #used to convert query results from tuple to list
            resultsReg.insert(0,DEFAULT_REGTEXT)
            headerMessage = Label(SD,text="Please enter pupil details")
            headerMessage.config(font = ("Times", 12))
            headerMessage.grid(row=0,padx=(150,10),pady=(10,5),columnspan =3)

            
            
            regText = Label(SD,text = "RegClass:")
            regText.config(font = ("Times", 12))
            regText.grid(row=1,padx=(30,10))
            
            selectRegClass = OptionMenu(SD,regClass,*resultsReg)
            selectRegClass.grid(row=1,column=1,padx=(30,10))
            
            

            searchReg = Button(SD, text="SearchRegclass", command= lambda :getPupilsInReg(pupils,pupilNames))
            searchReg.grid(row=1,column=4, padx=(30,10))

            NameText = Label(SD,text="Pupil Name:")
            NameText.config(font = ("Times", 12))
            NameText.grid(row=2,padx=(30,10),pady=(0,20))
            
            selectPupil = OptionMenu(SD,pupilName,*pupilNames)
            selectPupil.config(state = "disabled")
            selectPupil.grid(row=2,column=1,padx=(30,10),pady=(0,20))

            reasonText = Label(SD,text="Reason:")
            reasonText.config(font = ("Times",12))
            reasonText.grid(row =3,padx=(30,10))

            selectReason = Text(SD,height=10,width=30)
            selectReason.grid(row =3,column=1,padx=(30,10))

            dateTimeText = Label(SD,text="Date/Time:")
            dateTimeText.config(font = ("Times",12))
            dateTimeText.grid(row =4,padx=(30,10),pady=(30,10))

            getAvailableDetentions(detentions,detentionDates)
            selectDateTime = OptionMenu(SD,detentionDateTime,*detentionDates)
            selectDateTime.grid(row=4,column=1,padx=(30,10),pady=(30,10))
            

            submit = Button(SD, text="Submit", command =lambda : addPupilDetention(regClass,pupilName,selectReason.get("1.0","end-1c"),detentionDateTime,PupilDetentionRecord))
            submit.grid(row=5, column=1,padx=(30,10),pady=(10,10))

    def SearchRecordsByPupil():
        SRBP = Toplevel(master)
        SRBP.title("Search detention records by Pupil name")
        SRBP.geometry("500x200")
        regClass = StringVar(master)
        pupilName = StringVar(master)
        DEFAULT_PUPIL = "please select pupil name"
        DEFAULT_REGTEXT = "please select regClass"
        pupils = [] # this will hold all the class intances of pupilRecord
        pupilNames =[]# this will hold all the full names from pupil for the purpose of displaying them 
        pupilNames.append(DEFAULT_PUPIL)
        try:
            cnx = mysql.connector.connect(host="localhost",user="root", password="",database="schooldetention") # connects to sql database to check if username and password are correct
        except mysql.connector.Error as err:
            createMsgBox(f"{err}","connection error")
        else:
            query = cnx.cursor()
            def getPupilsInReg(pupils,pupilNames):
                if regClass.get() != DEFAULT_REGTEXT:
                    pupils = searchRegClass(regClass.get(),PupilRecord)
                    pupilNames = [] # this line and the line below are used to clear the list of pupil names so no duplicates are displayed if thie button is pressed multiple times.
                    pupilNames.append(DEFAULT_PUPIL)
                    for z in pupils:
                        pupilNames.append(z.getFullName())
                   
                    updatePupilDrowdown(pupilNames)
                    selectPupil.config(state="normal")
                else: 
                    createMsgBox("Please select registration class","Reg Class error")

            def updatePupilDrowdown(pupilNames):
                selectPupil['menu'].delete(0,'end')
                for name in pupilNames[1:]:
                    selectPupil['menu'].add_command(label=name,command = lambda name = name : pupilName.set(name))
                    
            def DisplayPupil(RegClass,pupilName,PupilRecord):
                if regClass == DEFAULT_REGTEXT or pupilName == DEFAULT_PUPIL :
                    createMsgBox("Form incomplete","Missing Information")
                else:
                    query = cnx.cursor()
                    pupilName = pupilName.split()
                    pupilFirstName=" ".join(pupilName[:-1])
                    pupilSurname= pupilName[-1]
                    query.execute(f'SELECT * FROM Pupil WHERE RegClass = "{RegClass}" AND FirstName ="{pupilFirstName}" AND Surname ="{pupilSurname}"')
                    currentPupilDetails = query.fetchone() # fetchone can be used is there is only one pupil with the same names and regclass
                    currentPupil = PupilRecord(currentPupilDetails[0],currentPupilDetails[1]+" "+currentPupilDetails[2],currentPupilDetails[3])
                    query.execute(f'SELECT * FROM pupildetention WHERE scn = "{currentPupil.getScn()}" ')
                    pupilHistoryRaw = query.fetchall()
                    if query.rowcount == 0:
                        createMsgBox(f"{currentPupil.getFullName()} has not active or pervious detentions","No data")
                    else:
                        pupilDetentionHistory = []
                        for x in pupilHistoryRaw:# this creates an array of the PupilDetentionRecord class in order to constrain the reason to the detention ID
                            pupilDetentionHistory.append(PupilDetentionRecord(x[0],x[1],x[2]))
                        detentions = []
                        for x in pupilDetentionHistory:
                            query.execute(f'SELECT * FROM detention WHERE DetentionID = "{x.getDetentionID()}"')
                            detentionRaw = query.fetchone() # fetchone can be used as there is only one detenion with a given ID
                            detentions.append(DetentionRecord(detentionRaw[0],detentionRaw[1],detentionRaw[2],detentionRaw[3],detentionRaw[4]))
                        staff = []
                        for x in detentions:
                            query.execute(f'SELECT StaffID , FirstName , Surname , DepartmentName FROM staff WHERE StaffID ="{x.getTeacherID()}"')
                            staffRaw = query.fetchone()
                            staff.append(Staff(staffRaw[0],staffRaw[1],staffRaw[2],staffRaw[3]))
                    #The arrays pupilDetentionHistory, detentions and staff are now paralell arrays of classes used to store the reason for the detention and the detention details
                        DisplayPupilsOnDetention(pupilDetentionHistory,detentions,staff)

                        

            query.execute("SELECT * FROM Reg")
            resultsReg = query.fetchall()
            resultsReg = [str(y[0]) for y in resultsReg]   #used to convert query results from tuple to list
            resultsReg.insert(0,DEFAULT_REGTEXT)
            headerMessage = Label(SRBP,text="Please enter pupil details")
            headerMessage.config(font = ("Times", 12))
            headerMessage.grid(row=0,padx=(150,10),pady=(10,5),columnspan =3)

            regText = Label(SRBP,text = "RegClass:")
            regText.config(font = ("Times", 12))
            regText.grid(row=1,padx=(30,10))
            
            selectRegClass = OptionMenu(SRBP,regClass,*resultsReg)
            selectRegClass.grid(row=1,column=1,padx=(30,10))
            
            searchReg = Button(SRBP, text="SearchRegclass", command= lambda :getPupilsInReg(pupils,pupilNames))
            searchReg.grid(row=1,column=2, padx=(30,10))

            NameText = Label(SRBP,text="FirstName:")
            NameText.config(font = ("Times", 12))
            NameText.grid(row=2,padx=(30,10),pady=(0,20))
            
            selectPupil = OptionMenu(SRBP,pupilName,*pupilNames)
            selectPupil.config(state = "disabled")
            selectPupil.grid(row=2,column=1,padx=(30,10),pady=(0,20))

            submit = Button(SRBP, text="Submit", command =lambda : DisplayPupil(regClass.get(),pupilName.get(),PupilRecord))
            submit.grid(row=2, column=2,padx=(30,10))
    
    def DisplayPupilsOnDetention(pupilDetentionHistory,detentions,staff):
        DPOD = Toplevel(master)
        DPOD.title("Search results")
        DPOD.geometry("620x150")
        #first all table headers will be created
        headerDate = Entry(DPOD)
        headerDate.insert(END,"Detention Date")
        headerDate.configure(state='readonly')
        headerDate.grid(row = 0, column = 0) 

        headerType = Entry(DPOD)
        headerType.insert(END,"Detention Type")
        headerType.configure(state='readonly')
        headerType.grid(row = 0, column = 1)

        headerRoomNo = Entry(DPOD)
        headerRoomNo.insert(END,"Room Number")
        headerRoomNo.configure(state='readonly')
        headerRoomNo.grid(row = 0, column = 2)

        headerReason = Entry(DPOD)
        headerReason.insert(END,"Reason")
        headerReason.configure(state='readonly')
        headerReason.grid(row = 0, column = 3)

        headerStaff = Entry(DPOD)
        headerStaff.insert(END,"supervising teacher")
        headerStaff.configure(state='readonly')
        headerStaff.grid(row = 0, column = 4)

        rows = []
        for i in range(len(detentions)):
            colum = []
            detentionDate = Entry(DPOD) 
            detentionDate.insert(END,f'{detentions[i].getDetentionDate()}')
            detentionDate.configure(state='readonly')
            detentionDate.grid(row=i+1,column=0)
            colum.append(detentionDate)

            detentionType = Entry(DPOD)
            detentionType.insert(END,f'{detentions[i].getDetentionType()}')
            detentionType.configure(state='readonly')
            detentionType.grid(row=i+1,column=1)
            colum.append(detentionType)

            detentionRm  = Entry(DPOD)
            detentionRm.insert(END,f'{detentions[i].getRoomNo()}')
            detentionRm.configure(state='readonly')
            detentionRm.grid(row=i+1,column=2)
            colum.append(detentionRm)

            detentionReason = Entry(DPOD)
            detentionReason.insert(END,f'{pupilDetentionHistory[i].getReason()}')
            detentionReason.configure(state='readonly')
            detentionReason.grid(row=i+1,column=3)
            colum.append(detentionReason)

            staffMember = Entry(DPOD)
            staffMember.insert(END,f'{staff[i].getFullName()}')
            staffMember.configure(state='readonly')
            staffMember.grid(row=i+1,column=4)
            colum.append(staffMember)

            rows.append(colum)


    welcomeMessage = Label(master, text =f"welcome: {currentUserFullName}") 

    welcomeMessage.pack(pady = 10) 

    btnSD = Button(master, text ="Set Detention", command = SetDetention)
    btnSD.pack(pady =10)
    btnSRBP = Button(master, text="Search detention records by Pupil name",command = SearchRecordsByPupil)
    btnSRBP.pack(pady =10)
    mainloop()

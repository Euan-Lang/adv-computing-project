import tkinter as tk

def createInputBox(InputBoxTitle,InputBoxText,BoxWidth = 400 ,BoxHeight = 120 ):#spacebar is used to acctivate buttons not enter by default
    InputBox =tk.Tk()
    InputBox.title(InputBoxTitle)
    Form1= tk.Canvas(InputBox, width = BoxWidth , height = BoxHeight)
    Form1.pack()
    MessageText = tk.Label(InputBox, text=InputBoxText)
    MessageText.config(font=('helvetica', 14))
    Form1.create_window(200, 25, window=MessageText)
    InputResult = tk.Entry(InputBox)
    Form1.create_window(200,50, window = InputResult)
    def callback():
        global InputBoxResult
        InputBoxResult = InputResult.get()
        InputBox.destroy()
    SubmitButton = tk.Button(text="Submit" , command=callback)
    Form1.create_window(200, 90 , window=SubmitButton) 
    InputBox.mainloop()
    return InputBoxResult  



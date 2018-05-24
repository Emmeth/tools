# Emmeth script
# Desc: Python script to remove vowel dots from any Hebrew text.
# Author: Benjamin Schnabel
# Date: 2018
# Email: benjamin-777@gmx.de
# Version: 1.0
# uses: python3, tkinter, unicodedata, re

import unicodedata
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import *
import tkinter.scrolledtext as tkst
from re import *

if sys.version_info[0] < 3:
    raise Exception("Python 3 or a more recent version is required.")

window = Tk()

rmTaamin = IntVar()

textInput = tkst.ScrolledText(
        master = window,
        width = 50,
        height = 10,
        borderwidth = 1,
        relief = SUNKEN,
        undo = True,
        font = ('Times New Roman', 12))

textResult = tkst.ScrolledText(
        master = window,
        width = 50,
        height = 10,
        borderwidth = 1,
        relief = SUNKEN,
        undo = True,
        font = ('Times New Roman', 12))

textInput.tag_configure('tag-right', justify=RIGHT)
textResult.tag_configure('tag-right', justify=RIGHT)

def constructGui():
    window.title("Remove Nikkud")
    window.configure(background="gray90")
    window.geometry('500x450')

    #Menu
    menubar = Menu(window)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open", command=openFileDialog)
    filemenu.add_command(label="Save", command=saveFileDialog)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=window.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    window.config(menu = menubar)

    labelText = Label(window, text="Enter your text here:", font=("Arial Bold", 14))
    labelText.pack()

    textInput.insert(END, ' ', 'tag-right')
    textInput.pack()


    #add checkboxes
    buttonTaamim = Checkbutton(window, text="Remove only Taamei haMikra", variable=rmTaamin)
    buttonTaamim.state(['!selected'])
    buttonTaamim.pack()


    buttonResult = Button(window, text="Remove Nikkud", command=removeNikkud)
    buttonResult.pack()

    buttonClear = Button(window, text="Clear Text", command=clearText)
    buttonClear.pack()

    separator = Separator(window)
    separator.pack()

    labelResult = Label(window, text ="Results:", font=("Arial Bold", 14))
    labelResult.pack()

    textResult.insert(END, ' ', 'tag-right')
    textResult.pack()

    window.mainloop()

def  openFileDialog():
    filename = filedialog.askopenfilename(
        parent = window,
        initialdir = "~",
        title = "Select a file",
        filetypes = (("text files", ".txt"),("all files",".*")))

    openFile(filename)

def saveFileDialog():
    filename = filedialog.asksaveasfilename(
        parent = window,
        initialdir = "~",
        title = "Save as",
        defaultextension = ".txt",
        filetypes = (("Text File", ".txt"),("All Files",".*")))

    writeFile(filename)

def openFile(filename):

    try:
        file = open(filename, mode="r", encoding="utf-8")
        content = file.read()
        file.close()

        textInput.delete('1.0', END)
        textInput.insert('1.0', content, 'tag-right')

    except:
        messagebox.showwarning(
            "Open file",
            "Cannot open this file\n(%s)" % filename
        )

def writeFile(filename):

    try:
        content = textResult.get('1.0', END)
        file = open(filename, 'w', encoding='utf-8')
        file.write(content)
        file.close()
    except:
        messagebox.showwarning(
            "Save file",
            "Cannot save this file\n(%s)" % filename
        )

def removeNikkud():

    content = textInput.get('1.0', END)
    normalized = unicodedata.normalize('NFKD', content)

    if(rmTaamin.get() == True):
        #range from 0591-05AF
        result = re.sub(re.compile(r'[\u0591-\u05AF]'), "", content)
    else:
        #range from 05B0-05BD, 05C0-05C2, 05C4-05C7
        result=''.join([c for c in normalized if not unicodedata.combining(c)])

    showResult(result)

def showResult(result):
    textResult.delete('1.0', END)
    textResult.insert(END, result, 'tag-right')


def clearText():
    textInput.delete('0.0', END)
    textInput.insert(END, ' ', 'tag-right')
    textResult.delete('0.0', END)
    textResult.insert(END, ' ', 'tag-right')

constructGui()
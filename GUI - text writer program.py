#text editor program 
import os   
from tkinter import*
from tkinter import filedialog,colorchooser,font #the font library contains a list of font families
from tkinter.messagebox import*
from tkinter.filedialog import*

def choose_color(): #function dervies the hex code based of color options from the colorchoser functions and changes the text area with the hex code
    #in the first index
    color = colorchooser.askcolor(title="pick a color")
    text_area.config(fg=color[1])

def change_font(*args):
    text_area.config(font=(font_name.get(), font_size_box.get()))

def new_file():
    window.title("Untitled") #creates a new text area named Untitled
    text_area.delete(1.0, END) #clears text on the text area from the initial text poisition to the end

def open_file():
    file = filedialog.askopenfile(defaultextension=".txt", file=[("All files", "*.*"),
                                    ("Text Documents","*." )])
    try:
        window.title(os.path.basename(file))  #sets the window titlename as the file's base name
        text_area.delete(1.0, END) #sets the open file to be empty by clearing text from the initial position to the end
        file = open(file, "r")
        text_area.insert(1.0, file.read()) #inserts the text read on the new file from the initial text position to the end
    except Exception:
        print("could not read file")
    finally:
        file.close()

def save_file():
    file = filedialog.asksaveasfile(initialfile="Untitled.txt", defaultextension="*.txt",filetypes=[("All Files", "*.*"), #this line of code assumes assumes the untitled file is the file to be saved
                                                    ("Text Documents", "*.txt")])
    if file is None: #allows an incomplete saving process to be exited without an error
        return
    else:
        try:
            window.title(os.path.basename(file))  #saves the file witht the base name given
            file = open(file, "w") #open the file and writes text from the initial text position of the text area to the end
            file.write(text_area.get(1.0, END))
        except Exception:
            print("can not save file")
        finally:
            file.close()   

def cut():
    text_area.event.generate("<<Cut>>")

def copy():
    text_area.event.generate("<<Copy>>")

def paste():
    text_area.event.generate("<<Paste>>")

def quit():
    window.destroy()

def help():
    showinfo("About this program" , "This a program written by bot.exe!")


window = Tk() #instantiates the instance of a window
file = None


#variables required to centralize the window - while a window instantitates a view for a user, the screen/view is how it is presented on the window
window_width = window_height = 500 #sets 500 as the window width and height
screen_width = window.winfo_screenwidth() #derives the window screen width from the screenwidth function
screen_height = window.winfo_screenheight() #derives the window screen height from the screenheight function

x = int((screen_width/2) - (window_width/2))
y = int((screen_width/2) - (window_width/2))

#determining how window should move in either x or y axis
window.geometry("{}x{}+{}+{}".format(window_width, window_height,x,y)) #returning the preset window width and height and adjusted x and y coordinates to center
#the window for display

font_name = StringVar() #sets the string variable for text font name
font_name.set('Helvetica') #sets a default font name

font_size = IntVar() #sets an int variable for font size
font_size.set('25')

text_area = Text(window,font=(font_name.get(),font_size.get())) #text widget deriving its font name and size from string and int variables selected
text_area.grid(sticky=N + E + S + W) #sticks the text area to occupy the window and continues on the next line when occupied

#creating a frame for our color, font name and font size buttons
frame = Frame(window)
frame.grid()

color_button = Button(frame,text='color', command=choose_color)
color_button.grid(row=0,column=0)

font_button = OptionMenu(frame, font_name, *font.families(), command=change_font) #creates a top and drop menu for fonts based off font families
font_button.grid(row=0,column=1)

font_size_box = Spinbox(frame, from_=1, to=100, textvariable=font_size, command=change_font) #sets font sizes from 1 to 100 to be changed simultaneously with font name
#by the change font command
font_size_box.grid(row=0,column=2)

scroll_bar = Scrollbar(text_area)
scroll_bar.pack(side=RIGHT, fill=Y) #places the scroll bar on the right to fill up empty space on the y axis
text_area.config(yscrollcommand = scroll_bar.set) #sets the text area y scroll command to the scroll bar

#creating a menu bar with dropdown options for each menu
menu_bar = Menu(window) #creates a menu

file_menu = Menu(menu_bar, tearoff=0) #creates a file menu on the menu bar with no lines between the menu and its dropdown options
menu_bar.add_cascade(label="File", menu=file_menu) #creates a dropdown feature for the file menu passed within

#adding dropdown options for the file menu 
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Exit", command=quit)

#creating an edit menu and dropdown options
edit_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=cut)
edit_menu.add_command(label="Copy", command=copy)
edit_menu.add_command(label="Paste", command=paste)

#creating a help menu with one dropdown option
help_menu = Menu(menu_bar, tearoff=0) #creates a menu for the help menu
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=help)

window.config(menu=menu_bar)
window.title("Text Editor Program")
window.grid_rowconfigure(0, weight=1) #configures the text area to expand but with a weight of one so it doesn't over expand 
window.grid_columnconfigure(0, weight=1)
window.mainloop() #displays a window on the screen
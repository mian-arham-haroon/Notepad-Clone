from tkinter import *
from tkinter.ttk import *
from tkinter import font,colorchooser,filedialog,messagebox
import os
import tempfile
from datetime import datetime
#--------------------------------------------------------------#

def date_time(event=None):
    currentdatetime=datetime.now()
    formatteddatetime=currentdatetime.strftime('%B %d,%Y %H:%M:%S')
    textarea.insert(1.0,formatteddatetime)

def printout(event=None):
    file=tempfile.mktemp('.txt')
    open(file,'w').write(textarea.get(1.0,END))
    os.startfile(file,'print')

def change_theme(bg_color,fg_color):
    textarea.config(bg=bg_color,fg=fg_color) 

def toolbarFunc():
    if show_toolbar.get()==False:
        tool_bar.pack_forget()
    if show_toolbar.get()==True:
        textarea.pack_forget()
        tool_bar.pack(fill=X)   
        textarea.pack(fill=BOTH,expand=1)
def statusbarFunc():
    if show_statusbar.get()==False:
        status_bar.pack_forget()
    else:
        status_bar.pack()   

def find():
    def find_words():
        textarea.tag_remove('match',1.0,END)
        start_pos='1.0'
        word=findentryField.get()
        if word:
            while True:
                start_pos=textarea.search(word,start_pos,stopindex=END)
                if not start_pos:
                    break
                end_pos=f'{start_pos}+{len(word)}c'
                textarea.tag_add('match',start_pos,end_pos)

                textarea.tag_config('match',foreground='red',background='yellow')
                start_pos=end_pos


    def replace_text():
        word=findentryField.get()
        replaceword=replaceentryField.get()
        content=textarea.get(1.0,END)
        new_content=content.replace(word,replaceword)
        textarea.delete(1.0,END)
        textarea.insert(1.0,new_content)

    root1=Toplevel()
    root1.title('Find')
    root1.geometry('430x250+500+200')
    root1.resizable(0,0)
    labelFrame=LabelFrame(root1,text='Find/Replace')
    labelFrame.pack(pady=20)
    
    findLabel=Label(labelFrame,text='Find')
    findLabel.grid(row=0,column=0,pady=5,padx=5)
    findentryField=Entry(labelFrame)
    findentryField.grid(row=0,column=1,padx=5,pady=5)

    replaceLabel=Label(labelFrame,text='Replace')
    replaceLabel.grid(row=1,column=0,pady=5,padx=5)
    replaceentryField=Entry(labelFrame)
    replaceentryField.grid(row=1,column=1,padx=5,pady=5)

    findButton=Button(labelFrame,text='FIND',command=find_words)
    findButton.grid(row=2,column=0,padx=5,pady=5)

    replaceButton=Button(labelFrame,text='REPLACE',command=replace_text)
    replaceButton.grid(row=2,column=1,padx=5,pady=5)
    
    def doSomething():
        textarea.tag_remove('match',1.0,END)
        root1.destroy()

    root1.protocol('WM_DELETE_WINDOW',doSomething)
    root1.mainloop()

def statusBarFunction(event):
    if textarea.edit_modified():
        words=len(textarea.get(0.0,END).split())
        characters=len(textarea.get(0.0,'end-1c').replace(' ',''))
        status_bar.config(text=f'charecters: {characters} Words: {words}')
    textarea.edit_modified(False)    

def new_file(event=None):
    global url
    url=''
    textarea.delete(0.0,END)
url=''
def open_file(event=None):
    global url
    url=filedialog.askopenfilename(initialdir=os.getcwd,title='Select File',filetypes=(('Text File','txt')
                                                                                        ,('All File','*.*')))
    if url != '': 
        data=open(url,'r')
        textarea.insert(0.0,data.read())
    if url!='':    
        root.title(os.path.basename(url))    

def save_file(event=None):
    if url =='':
        save_url=filedialog.asksaveasfile(mode='w',defaultextension='.txt',filetypes=(('Text File','txt')
                                                                                    ,('All File','*.*')))
        if save_url is None:
            pass
        else:                                                                            
            content=textarea.get(0.0,END)
            save_url.write(content)
            save_url.close() 
    else:
        content=textarea.get(0.0,END) 
        file=open(url,'w')   
        file.write(content)
def saveas_file(event=None):
    save_url=filedialog.asksaveasfile(mode='w',defaultextension='.txt',filetypes=(('Text File','txt')
                                                                                ,('All File','*.*')))
    content=textarea.get(0.0,END) 
    save_url.write(content)
    save_url.close()
    os.remove(url)

def iexit(event=None):
    if textarea.edit_modified():
        result=messagebox.askyesnocancel('Warning','Do you want to save the file?')  
        if result is True:
            if url!='':
                content=textarea.get(0.0,END)
                file=open(url,'w')
                file.write(content)
                root.destroy()
            else:
                content=textarea.get(0.0,END)
                save_url=filedialog.asksaveasfile(mode='w',defaultextension='.txt',filetypes=(('Text File','txt')
                                                                                           ,('All File','*.*')))
                save_url.write(content)
                save_url.close()
                root.destroy()
        elif result is False:
            root.destroy()
        else:
            pass
    else:
        root.destroy()        


fontSize=12
fontStyle='arial'
def font_style(event):
    global fontStyle
    fontStyle=font_families_variable.get()
    textarea.config(font=(fontStyle,fontSize))

def font_size(event):
    global fontSize
    fontSize=size_variable.get()
    textarea.config(font=(fontStyle,fontSize))

def bold_text():
    text_property=font.Font(font=textarea['font']).actual()
    if text_property['weight']=='normal':
        textarea.config(font=(fontStyle,fontSize,"bold"))
    if text_property['weight']=='bold':
        textarea.config(font=(fontStyle,fontSize,"normal"))

def italic_text():
    text_property=font.Font(font=textarea['font']).actual()
    if text_property['slant']=='roman':
        textarea.config(font=(fontStyle,fontSize,'italic'))
    if text_property['slant']=='italic':
        textarea.config(font=(fontStyle,fontSize,'roman'))

def underline_text():
    text_property=font.Font(font=textarea['font']).actual()
    if text_property['underline']==0:
        textarea.config(font=(fontStyle,fontSize,'underline'))
    if text_property['underline']==1:
        textarea.config(font=(fontStyle,fontSize,))

def color_select():
    color=colorchooser.askcolor()
    textarea.config(fg=color[1])

def align_right():
    data=textarea.get(0.0,END)
    textarea.tag_config('right',justify=RIGHT)
    textarea.delete(0.0,END)
    textarea.insert(INSERT,data,'right')
def align_left():
    data=textarea.get(0.0,END)
    textarea.tag_config('left',justify=LEFT)
    textarea.delete(0.0,END)
    textarea.insert(INSERT,data,'left')
def align_center():
    data=textarea.get(0.0,END)
    textarea.tag_config('center',justify=CENTER)
    textarea.delete(0.0,END)
    textarea.insert(INSERT,data,'center')

#--------------------------------------------------------------#
root=Tk()
root.title("Notepad Clone")
root.geometry("1200x620+10+10")
root.resizable(False,False)
menubar=Menu(root)
root.config(menu=menubar)

#--------------------------------------------------------------#
filemenu=Menu(menubar,tearoff=False)
menubar.add_cascade(label='File',menu=filemenu)

newImage=PhotoImage(file='images/new.png')
filemenu.add_command(label='New',accelerator='Ctrl+N',compound='left',image=newImage,command=new_file)

openImage=PhotoImage(file='images/open.png')
filemenu.add_command(label='Open',accelerator='Ctrl+O',compound='left',image=openImage,command=open_file)

saveImage=PhotoImage(file='images/save.png')
filemenu.add_command(label='Save',accelerator='Ctrl+S',compound='left',image=saveImage,command=save_file)

saveasImage=PhotoImage(file='images/save_as.png')
filemenu.add_command(label='Save As',accelerator='Ctrl+Alt+S',compound='left',image=saveasImage,command=saveas_file)

printImage=PhotoImage(file='images/print.png')
filemenu.add_command(label='Print',accelerator='Ctrl+P',compound='left',image=printImage,command=printout)

filemenu.add_separator()

exitImage=PhotoImage(file='images/exit.png')
filemenu.add_command(label='Exit',accelerator='Ctrl+Q',compound='left',image=exitImage,command=iexit)
#--------------------------------------------------------------#
#--------------------------------------------------------------#
tool_bar=Label(root)
tool_bar.pack(side=TOP,fill=X)
font_families=font.families()
font_families_variable=StringVar()
fontfamily_Combobox=Combobox(tool_bar,width=30,values=font_families,state='readonly',textvariable=font_families_variable)
fontfamily_Combobox.current(font_families.index('Arial'))
fontfamily_Combobox.grid(row=0,column=0,padx=5)
fontfamily_Combobox.bind('<<ComboboxSelected>>',font_style)

#--------------------------------------------------------------#
size_variable=IntVar()
font_size_Combobox=Combobox(tool_bar,width=14,textvariable=size_variable,state='readonly',values=tuple(range(8,81)))
font_size_Combobox.current(4)
font_size_Combobox.grid(row=0,column=1,padx=5)
font_size_Combobox.bind('<<ComboboxSelected>>',font_size)

#--------------------------------------------------------------#
boldImage=PhotoImage(file='images/bold.png')
boldButton=Button(tool_bar,image=boldImage,command=bold_text)
boldButton.grid(row=0,column=2,padx=5)

italicImage=PhotoImage(file='images/italic.png')
italicButton=Button(tool_bar,image=italicImage,command=italic_text)
italicButton.grid(row=0,column=3,padx=5)

underlineImage=PhotoImage(file='images/underline.png')
underlineButton=Button(tool_bar,image=underlineImage,command=underline_text)
underlineButton.grid(row=0,column=4,padx=5)

fontColorImage=PhotoImage(file='images/font_Color.png')
fontColorButton=Button(tool_bar,image=fontColorImage,command=color_select)
fontColorButton.grid(row=0,column=5,padx=5)

leftAlignImage=PhotoImage(file='images/left.png')
leftAlignButton=Button(tool_bar,image=leftAlignImage,command=align_left)
leftAlignButton.grid(row=0,column=6,padx=5)

rightAlignImage=PhotoImage(file='images/right.png')
rightAlignButton=Button(tool_bar,image=rightAlignImage,command=align_right)
rightAlignButton.grid(row=0,column=7,padx=5)

centerAlignImage=PhotoImage(file='images/center.png')
centerAlignButton=Button(tool_bar,image=centerAlignImage,command=align_center)
centerAlignButton.grid(row=0,column=8,padx=5)
#--------------------------------------------------------------#
scrollbar=Scrollbar(root)
scrollbar.pack(side='right',fill=Y)

textarea=Text(root,yscrollcommand=scrollbar.set,font=('arial 12'),undo=True)
textarea.pack(fill=BOTH,expand=True)

scrollbar.config(command=textarea.yview)
#--------------------------------------------------------------#
editmenu=Menu(menubar,tearoff=False)
undoImage=PhotoImage(file='images/undo.png')
editmenu.add_command(label='Undo',accelerator='Ctrl+Z',compound='left',image=undoImage
                    )

cutImage=PhotoImage(file='images/cut.png')
editmenu.add_command(label='Cut',accelerator='Ctrl+X',compound='left',image=cutImage
                    ,command=lambda:textarea.event_generate('<Control x>'))

copyImage=PhotoImage(file='images/copy.png')
editmenu.add_command(label='Copy',accelerator='Ctrl+C',compound='left',image=copyImage
                    ,command=lambda:textarea.event_generate('<Control c>'))

pasteImage=PhotoImage(file='images/paste.png')
editmenu.add_command(label='Paste',accelerator='Ctrl+V',compound='left',image=pasteImage
                    )

selectImage=PhotoImage(file='images/checked.png')
editmenu.add_command(label='Select All',accelerator='Ctrl+A',compound='left',image=selectImage
                    ,command=lambda:textarea.event_generate('<Control v>'))

clearImage=PhotoImage(file='images/clear_all.png')
editmenu.add_command(label='Clear',accelerator='Ctrl+Alt+X',compound='left',image=clearImage
                    ,command=lambda:textarea.delete(0.0,END))

findImage=PhotoImage(file='images/find.png')
editmenu.add_command(label='Find',accelerator='Ctrl+F',compound='left',image=findImage,command=find)

datetimeImage=PhotoImage(file='images/calender.png')
editmenu.add_command(label='Time/Date',accelerator='Ctrl+D',compound='left',image=datetimeImage,command=date_time)

menubar.add_cascade(label='Edit',menu=editmenu)



#--------------------------------------------------------------#
show_toolbar=BooleanVar()
show_statusbar=BooleanVar()

viewmenu=Menu(menubar,tearoff=False)

toolImage=PhotoImage(file='images/tool_bar.png')
viewmenu.add_checkbutton(label='Tool Bar',variable=show_toolbar,onvalue=True,offvalue=False,image=toolImage,compound='left',
command=toolbarFunc)

show_toolbar.set(True)

statusImage=PhotoImage(file='images/status_bar.png')
viewmenu.add_checkbutton(label='Status Bar',variable=show_statusbar,onvalue=True,offvalue=False,image=statusImage,compound='left',
command=statusbarFunc)

show_statusbar.set(True)

menubar.add_cascade(label='View',menu=viewmenu)
#--------------------------------------------------------------#
theamsmenu=Menu(menubar,tearoff=False)
menubar.add_cascade(label='Theams',menu=theamsmenu)

theam_choice=StringVar()

lightImage=PhotoImage(file='images/light_default.png')
theamsmenu.add_radiobutton(label='Light Default',image=lightImage,variable=theam_choice,compound=LEFT,command=lambda : change_theme('white','black'))

darkImage=PhotoImage(file='images/dark.png')
theamsmenu.add_radiobutton(label='Dark',image=darkImage,variable=theam_choice,compound=LEFT,command=lambda : change_theme('gray20','white'))

pinkImage=PhotoImage(file='images/red.png')
theamsmenu.add_radiobutton(label='Pink',image=pinkImage,variable=theam_choice,compound=LEFT,command=lambda : change_theme('pink','blue'))

monokaiImage=PhotoImage(file='images/monokai.png')
theamsmenu.add_radiobutton(label='Monokai',image=monokaiImage,variable=theam_choice,compound=LEFT,command=lambda : change_theme('orange','white'))

#--------------------------------------------------------------#
status_bar=Label(root,text='Status Bar')
status_bar.pack(side=BOTTOM)
#--------------------------------------------------------------#

textarea.bind('<<Modified>>',statusBarFunction)


root.bind("<Control-o>",open_file)
root.bind("<Control-n>",new_file)
root.bind("<Control-Alt-s>",saveas_file) 
root.bind("<Control-q>",iexit) 
root.bind("<Control-p>",printout) 
root.bind("<Control-d>",date_time) 



root.mainloop()
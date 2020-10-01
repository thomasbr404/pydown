from tkinter import *
from tkinter import font , filedialog
from tkinter import messagebox as mbox

from markdown2 import Markdown
from tkhtmlview import HTMLLabel

class Window(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.master = master
		self.mfont = font.Font(family="Helvetica", size=14)
		self.init_window()

	def init_window(self):
		self.master.title("PyDown")
		self.pack(fill=BOTH, expand=1)
		
		self.mainmenu = Menu(self)
		self.filemenu = Menu(self.mainmenu)
		self.filemenu.add_command(label="Open", command=self.openfile)
		self.filemenu.add_command(label="Save as", command=self.savefile)
		self.filemenu.add_separator()
		self.filemenu.add_command(label="Exit", command=self.quit)
		self.mainmenu.add_cascade(label="File", menu=self.filemenu)
		self.master.config(menu=self.mainmenu)

		self.inputeditor = Text(self, width="1", font=self.mfont)
		self.inputeditor.pack(fill=BOTH, expand=1, side=LEFT)
		
		self.outputbox = HTMLLabel(self, width="1", background="white", html="<h1>PyDown Markdown Editor</h1>")
		self.outputbox.pack(fill=BOTH, expand=1, side=RIGHT)
		self.outputbox.fit_height()
		
		self.inputeditor.bind("<<Modified>>", self.onInputChange)
		
	def onInputChange(self , event):
		self.inputeditor.edit_modified(0)
		md2html = Markdown()
		self.outputbox.set_html(md2html.convert(self.inputeditor.get("1.0" , END)))
		
	def openfile(self):
		openfilename = filedialog.askopenfilename(filetypes=(("Markdown File", "*.md , *.mdown , *.markdown"),
                                                                  ("Text File", "*.txt"), 
                                                                  ("All Files", "*.*")))
		if openfilename:
			try:
				self.inputeditor.delete(1.0, END)
				self.inputeditor.insert(END , open(openfilename).read())
			except:
				mbox.showerror("Error Opening Selected File" , "Oops!, The file you selected : {} can not be opened!".format(openfilename))    
				
	def savefile(self):
		filedata = self.inputeditor.get("1.0" , END)
		savefilename = filedialog.asksaveasfilename(filetypes = (("Markdown File", "*.md"),
                                                                  ("Text File", "*.txt")) , title="Save Markdown File")
		if savefilename:
			try:
				f = open(savefilename , "w")
				f.write(filedata)
			except:
				mbox.showerror("Error Saving File" , "Oops!, The File : {} can not be saved!".format(savefilename))


root = Tk()
root.geometry("1050x700")
root.iconbitmap('assets/md.ico')
app = Window(root)
app.mainloop()

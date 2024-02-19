from tkinter import *
from tkinter.filedialog import askopenfilename
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.widgets import Button
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import os
import matplotlib.patches as patches
import pybedtools

ax,fig = None, None
options = [
    "chr1",
    "chr2",
    "chr3",
    "chr4",
    "chr5"
]
chr = options[0]
class BED:
    def __init__(self, color, track_height, path = ""):
        #self.df = pd.DataFrame()
        self.file_name = ''
        self.color = ''
        self.track_height = 0
        self.legend_patch = None
        self.color = color
        self.track_height = track_height
        self.path = ""
        if (path == ""):
            self.path = askopenfilename(title="Choose bed")
        else:
            self.path = path
        self.read_bed()

    def read_bed(self):
        self.df = pd.read_csv(self.path,sep="\t")
        self.file_name = os.path.basename(self.path)
        self.show_file_name()
        self.bed_to_graph()

    def bed_to_graph(self):
        global chr
        for index, row in self.df.iterrows():
            if(self.df.iloc[index,0]==chr):
                position = {'x':0,'y':self.track_height}
                position['x'] = self.df.iloc[index,1]
                size = self.df.iloc[index,2] - position['x']
                self.add_rectangle(position,size,self.color)
    def add_rectangle(self,_position, size, color):
        rectangle = patches.Rectangle((_position['x'] - size, _position['y']), size, 1, facecolor='none', fill=True,color=color)
        ax.add_patch(rectangle)

    def show_file_name(self):
        self.legend_patch = mpatches.Patch(color=self.color, label=self.file_name)
class BED_heandler:
    beds = []
    colors = ['red','orange','green','blue','purple','brown','black']
    index = 0
    def bed_loader(self,event,path=""):
        self.beds.append(BED(self.colors[self.index],self.index,path))
        self.index = self.index +1
        self.show_file_names()

    def plot(self):
        for bed in self.beds:
            bed.bed_to_graph()
    def show_file_names(self):
        legends = []
        for bed in self.beds:
            legends.append(bed.legend_patch)
        ax.legend(handles=legends)

    def intersection(self,event):
        if(len(self.beds)<2):
            print("not enough tracks")
        elif(len(self.beds)>2):
            print("already intersected")
        a = pybedtools.BedTool(self.beds[0].path)
        b = a.intersect(self.beds[1].path)
        filename = f'{self.beds[0].file_name}_VS_{self.beds[1].file_name}_intersection.bed'
        b.saveas(filename)
        self.bed_loader(None,filename)

root = Tk()
root.geometry("750x750")
root.wm_title("Embedding in Tk")

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)

    # Initial axis limits
initial_xlim = (0, 145444305)
initial_ylim = (0, 10)
ax.set_xlim(*initial_xlim)
ax.set_ylim(*initial_ylim)

B = BED_heandler()
ax_upload = fig.add_axes([0.8, 0.05, 0.1, 0.075])
b_upload = Button(ax_upload, 'upload')
b_upload.on_clicked(B.bed_loader)

ax_intersect = fig.add_axes([0.7, 0.05, 0.1, 0.075])
b_intersect = Button(ax_intersect, 'intersect')
b_intersect.on_clicked(B.intersection)

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()

# pack_toolbar=False will make it easier to use a layout manager later on.
toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
toolbar.update()

def update(*kwargs):
    global chr
    #l.config(text=clicked.get())
    chr = clicked.get()
    [p.remove() for p in reversed(ax.patches)]
    BED_heandler.plot(BED_heandler)

# Dropdown menu options
# datatype of menu text
clicked = StringVar()
#l = Label(root, text = options[0])
# initial menu text
clicked.set(options[0])
#l.pack()
# Create Dropdown menu
drop = OptionMenu(root, clicked, *options)
clicked.trace("w", update)
drop.pack()

# Create button, it will change label text

# Create Label
label = Label(root, text=" ")
label.pack()

canvas.mpl_connect("key_press_event", lambda event: print(f"you pressed {event.key}"))
canvas.mpl_connect("key_press_event", key_press_handler)


# Packing order is important. Widgets are processed sequentially and if there
# is no space left, because the window is too small, they are not displayed.
# The canvas is rather flexible in its size, so we pack it last which makes
# sure the UI controls are displayed as long as possible.
toolbar.pack(side=BOTTOM, fill=X)
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

mainloop()
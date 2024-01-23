import ipywidgets as widgets
from tkinter.filedialog import askopenfilename
global zoom
import pandas as pd
from matplotlib.widgets import Button
import matplotlib.patches as mpatches
import os
from IPython.display import display
import matplotlib.pyplot as plt
from ipywidgets import interact


import matplotlib.artist as artist
import matplotlib.patches as patches
from matplotlib.transforms import IdentityTransform
def update_scroll(val):
    ax.set_xlim(slider_scroll.val - 0.5 * slider_zoom.val, slider_scroll.val + 0.5 * slider_zoom.val)
    fig.canvas.draw_idle()
def on_scroll(event):
    if event.button == 'up':
        ax.set_xlim(ax.get_xlim()[0] + 0.1 * zoom, ax.get_xlim()[1] - 0.1 * zoom)
    elif event.button == 'down':
        ax.set_xlim(ax.get_xlim()[0] - 0.1 * zoom, ax.get_xlim()[1] + 0.1 * zoom)
    fig.canvas.draw_idle()

class BED:
    df = pd.DataFrame()
    file_name = ''
    color = ''
    track_height = 0
    legend_patch = None
    def __init__(self, color, track_height):
        self.color = color
        self.track_height = track_height
        self.df = self.read_bed()

    def read_bed(self):
        path = askopenfilename(title="Choose json")
        self.df = pd.read_csv(path,sep="\t")
        self.file_name = os.path.basename(path)
        self.show_file_name()
        self.bed_to_graph()

    def bed_to_graph(self):
        for index, row in self.df.iterrows():
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
    colors = ['red','blue','green']
    limit = 3
    index = 0
    def bed_loader(self,event):
        self.beds.append(BED(self.colors[self.index],self.index))
        self.show_file_names()
        self.index = self.index + 1

        if(self.index>self.limit):
            self.index = 0

    def show_file_names(self):
        legends = []
        for bed in self.beds:
            legends.append(bed.legend_patch)
        ax.legend(handles=legends)


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


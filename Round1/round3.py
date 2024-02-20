import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QComboBox, QLabel, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import os
import matplotlib.patches as patches
import pybedtools
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtCore import QTimer


class BED:
    def __init__(self, color, track_height, path=""):
        self.file_name = ''
        self.color = ''
        self.track_height = 0
        self.legend_patch = None
        self.color = color
        self.track_height = track_height
        if not path:
            self.path, _ = QFileDialog.getOpenFileName(None, "Choose bed", "", "Bed files (*.bed);;All Files (*)")
        else:
            self.path = path
        self.read_bed()

    def read_bed(self):
        self.df = pd.read_csv(self.path, sep="\t")
        self.file_name = os.path.basename(self.path)
        self.show_file_name()
        self.bed_to_graph()

    def bed_to_graph(self):
        global chr
        for index, row in self.df.iterrows():
            if self.df.iloc[index, 0] == chr:
                position = {'x': 0, 'y': self.track_height}
                position['x'] = self.df.iloc[index, 1]
                size = self.df.iloc[index, 2] - position['x']
                self.aon = {'x': 0, 'y': self.track_height}
                position['x'] = self.df.iloc[index, 1]
                size = self.df.iloc[index, 2] - position['x']
                self.add_rectangle(position, size, self.color)

    def add_rectangle(self, _position, size, color):
        rectangle = patches.Rectangle((_position['x'] - size, _position['y']), size, 1, facecolor='none',
                                      fill=True, color=color)
        ax.add_patch(rectangle)

    def show_file_name(self):
        self.legend_patch = mpatches.Patch(color=self.color, label=self.file_name)


class BEDHandler:
    beds = []
    colors = ['red', 'orange', 'green', 'blue', 'purple', 'brown', 'black']
    index = 0

    def bed_loader(self, path=""):
        self.beds.append(BED(self.colors[self.index], self.index, path))
        self.index = self.index + 1
        self.show_file_names()

    def plot(self):
        for bed in self.beds:
            bed.bed_to_graph()

    def show_file_names(self):
        legends = []
        for bed in self.beds:
            legends.append(bed.legend_patch)
        ax.legend(handles=legends)

    def intersection(self):
        if len(self.beds) < 2:
            print("not enough tracks")
        elif len(self.beds) > 2:
            print("already intersected")
        else:
            a = pybedtools.BedTool(self.beds[0].path)
            b = a.intersect(self.beds[1].path)
            filename = f'{self.beds[0].file_name}_VS_{self.beds[1].file_name}_intersection.bed'
            b.saveas(filename)
            self.bed_loader(filename)

class MatplotlibCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        global fig
        global ax
        fig, ax = plt.subplots(figsize=(width, height), dpi=dpi)
        super(MatplotlibCanvas, self).__init__(fig)
        self.setParent(parent)
        self.ax = ax
        self.set_initial_axis_limits()

    def set_initial_axis_limits(self):
        initial_xlim = (0, 145444305)
        initial_ylim = (0, 10)
        self.ax.set_xlim(*initial_xlim)
        self.ax.set_ylim(*initial_ylim)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.canvas = MatplotlibCanvas(self, width=5, height=4, dpi=100)
        self.main_layout.addWidget(self.canvas)

        self.toolbar = NavigationToolbar(self.canvas, self)
        self.main_layout.addWidget(self.toolbar)

        self.dropdown_label = QLabel("Select chromosome:")
        self.main_layout.addWidget(self.dropdown_label)

        self.dropdown = QComboBox(self)
        self.options = ["chr1", "chr2", "chr3", "chr4", "chr5"]
        self.dropdown.addItems(self.options)
        self.dropdown.currentIndexChanged.connect(self.update_chromosome)
        self.main_layout.addWidget(self.dropdown)

        self.bed_handler = BEDHandler()

        self.upload_button = QPushButton("Upload", self)
        self.upload_button.clicked.connect(self.bed_handler.bed_loader)
        self.main_layout.addWidget(self.upload_button)

        self.intersect_button = QPushButton("Intersect", self)
        self.intersect_button.clicked.connect(self.bed_handler.intersection)
        self.main_layout.addWidget(self.intersect_button)

        self.update_chromosome()

        self.plot_timer = QTimer(self)
        self.plot_timer.timeout.connect(self.bed_handler.plot)
        self.plot_timer.start(1000)

    def update_chromosome(self):
        global chr
        global ax
        chr = self.options[self.dropdown.currentIndex()]
        [p.remove() for p in reversed(ax.patches)]
        self.bed_handler.plot()
        self.canvas.draw()

        xlim = (0, 135444104)  # Adjust the values as needed
        ylim = (0, 15)
        self.set_axis_limits(xlim, ylim)

    def set_axis_limits(self, xlim, ylim):
        self.canvas.ax.set_xlim(*xlim)
        self.canvas.ax.set_ylim(*ylim)
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.setGeometry(100, 100, 800, 600)
    main_window.show()
    sys.exit(app.exec_())

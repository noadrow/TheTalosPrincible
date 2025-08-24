import os
import shutil
import cv2
from PIL import Image, ImageTk
import subprocess
import pybedtools
import numpy as np
from scipy.stats import wilcoxon
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import tkinter as tk
from tkinter import filedialog
import random
import itertools

class TalosPrincipleApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("The Talos Principle")
        self.geometry("2000x800")

        # Folders
        self.temp_folder = "temp_folder"
        os.makedirs(self.temp_folder, exist_ok=True)

        # Files
        self.background_file = ""
        self.target_files = [None,None]
        self.data_file = ""
        self.file_path = []

        # Input string for region view
        self.input_str = "5:135444104-135444504"


        # Text box
        self.text_box = tk.Entry(self)
        self.text_box.pack(pady=10)
        self.text_box.insert(0,self.input_str)

        # Buttons frame
        button_frame = tk.Frame(self)
        button_frame.pack(padx=20, pady=20)

        # Load file buttons
        self.load_bg_button = tk.Button(button_frame, text="Load Background BED", command=self.load_background)
        self.load_bg_button.pack(side=tk.LEFT, padx=5)

        self.load_target_button = tk.Button(button_frame, text="Load Target BED", command=self.load_target)
        self.load_target_button.pack(side=tk.LEFT, padx=5)

        self.load_data_button = tk.Button(button_frame, text="Load Data BED", command=self.load_data)
        self.load_data_button.pack(side=tk.LEFT, padx=5)

        # Analyze button
        self.analyze_button = tk.Button(button_frame, text="Analyze", command=self.analyze)
        self.analyze_button.pack(side=tk.LEFT, padx=5)

        # Other buttons
        self.run_button = tk.Button(button_frame, text="Go", command=self.run_function)
        self.run_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(button_frame, text="Clear", command=self.clear_ini)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Canvas for image
        self.canvas = tk.Canvas(self, width=800, height=400)
        self.canvas.pack(pady=10)

        # Result text box
        self.result_text = tk.Text(self, height=8, width=150)
        self.result_text.pack(pady=10)

        self.clear_ini()
        self.mainloop()

    def __del__(self):
        shutil.rmtree(self.temp_folder, ignore_errors=True)

    def load_background(self):
        self.background_file = filedialog.askopenfilename(title="Select Background BED File")

        if self.background_file:
            filepath = self.sort(self.background_file)
            self.file_path.insert(0,filepath)
            print(f"Loaded Background: {self.background_file}")
            self.make_track_files()

    def load_target(self):

        self.target_files[0] = filedialog.askopenfilename(title="Select Target BED File 1")
        self.target_files[1] = filedialog.askopenfilename(title="Select Target BED File 2")
        if self.target_files:
            for i,target_file in zip(range(len(self.target_files)),self.target_files):
                if target_file:
                    if target_file.lower().endswith(".txt"):
                        from Id_to_bed import id_to_bed
                        filepath_0 = id_to_bed(target_file)
                        filepath = self.sort(filepath_0)
                    else:
                        filepath = self.sort(target_file)

                    self.target_files[i] = filepath
                    print(f"Loaded Target: {target_file}")
                    self.make_track_files()


    def load_data(self):
        self.data_file = filedialog.askopenfilename(title="Select Data BED File")
        if self.data_file:
            filepath = self.sort(self.data_file)
            self.file_path.insert(2, filepath)
            print(f"Loaded Data: {self.data_file}")
            self.make_track_files()

    def sort(self,path):
        temp = pybedtools.BedTool(path)
        temp_sort = temp.sort()
        filename = f'temp_folder/{os.path.basename(path).replace(".bed","_sort.bed")}'
        temp_sort.saveas(filename)
        return filename

    def run_function(self):
        if self.text_box.get():
            self.input_str = self.text_box.get()
            self.pyGenomeTracks()

    def clear_ini(self):
        self.file_path = []
        self.make_track_files()
        self.pyGenomeTracks()

    def make_track_files(self):
        if self.file_path:
            run_list = ["make_tracks_file", "--trackFiles"]
            run_list.extend(self.file_path)
            run_list.extend(["-o", "test.ini"])
            subprocess.run(run_list)


    def pyGenomeTracks(self):
        if self.file_path:
            subprocess.run([
                "pyGenomeTracks", "--tracks",
                "test.ini", "--region",
                self.input_str, "-o", "bigwig.png"
            ])
            self.show_image("bigwig.png")
        else:
            self.show_image("empty.png")

    def show_image(self, img_path):
        try:
            image = cv2.imread(img_path)
            if image is None:
                print(f"Image not found: {img_path}")
                return
            height, width, _ = image.shape
            image = cv2.resize(image, (width, height))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(image)
            image_tk = ImageTk.PhotoImage(pil_image)
            self.geometry(f"{width}x{height + 500}")
            self.canvas.config(width=width, height=height)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)
            self.canvas.pack(fill=tk.BOTH, expand=True)
            self.canvas.image = image_tk
        except:
            print("Failed to show image")

    def analyze(self):
        if not self.target_files:
            print("warning! missing target file")
            return
        elif not self.background_file and not self.data_file:
            print("warning! at least upload BG or Data file!")
            return
        elif not self.background_file:
            bg_tool = pybedtools.BedTool(self.data_file)

            data_tool = pybedtools.BedTool(self.data_file)
        elif not self.data_file:
            bg_tool = pybedtools.BedTool(self.background_file)

        elif not self.data_file:
            data_tool = pybedtools.BedTool(self.background_file)
        else:
            bg_tool = pybedtools.BedTool(self.background_file)
            data_tool = pybedtools.BedTool(self.data_file)

        target_tool = pybedtools.BedTool(self.target_files[0])

        bg_data = data_tool.intersect(bg_tool, wa=True)
        target_data = data_tool.intersect(target_tool, wa=True)

        bg_values = []
        for f in bg_data:
            try:
                bg_values.append(float(f[3]))
            except:
                bg_values.append(str(f[3]))

        target_values = []
        for f in target_data:
            try:
                target_values.append(float(f[3]))
            except:
                target_values.append(str(f[3]))

        if not bg_values or not target_values:
            self.result_text.insert(tk.END, "Not enough data for analysis.\n")
            return

        if type(bg_values[0])== str and len(self.target_files)==2:

            target_tool_2 = pybedtools.BedTool(self.target_files[1])
            target_data_2 = data_tool.intersect(target_tool_2, wa=True)

            target_values_2 = []
            for f in target_data_2:
                try:
                    target_values_2.append(str(f[3]))
                except:
                    print("something wrong with target file 2")

            venn2([set(target_values), set(target_values_2)], set_labels=('Target 1', 'Target 2'))
            plt.title('Venn Diagram of Overlap Between Target 1 and Target 2')
            venn_path = os.path.join(self.temp_folder, "venn_diagram.png")
            plt.savefig(venn_path)
            plt.close()
            self.show_image(venn_path)

            # Show the plot
            plt.show()

            N = 1000
            size1 = len(target_values)
            size2 = len(target_values_2)

            overlaps = []
            for _ in range(N):
                subset1 = set(random.sample(bg_values, size1))
                subset2 = set(random.sample(bg_values, size2))
                overlap = len(subset1 & subset2)
                overlaps.append(overlap)

            target_res = len(set(target_values) & set(target_values_2))

            p_enrich = (sum(o >= target_res for o in overlaps) + 1) / (N + 1)
            p_deplete = (sum(o <= target_res for o in overlaps) + 1) / (N + 1)
            p_two_sided = 2 * min(p_enrich, p_deplete)

            result = f'Observed overlap: {target_res}\n'
            result += f'Enrichment p-value: {p_enrich:.4f}\n'
            result += f'Depletion p-value: {p_deplete:.4f}\n'
            result += f'Two-sided p-value: {p_two_sided:.4f}\n'

            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result)

            plt.hist(overlaps, bins=30, color='skyblue', edgecolor='black')
            plt.axvline(target_res, color='red', linestyle='dashed', linewidth=2,
                        label=f'Observed Overlap: {target_res}')
            plt.title('Overlap Null Distribution\nRandom BG Sets')
            plt.xlabel('Overlap Count')
            plt.ylabel('Frequency')
            plt.legend()
            plt.show()


        if type(bg_values[0])==float:
            min_len = min(len(bg_values), len(target_values))
            bg_values = bg_values[:min_len]
            target_values = target_values[:min_len]

            stat, p = wilcoxon(np.array(target_values) - np.array(bg_values))

            bg_mean = np.mean(bg_values)
            bg_std = np.std(bg_values)
            target_mean = np.mean(target_values)
            target_std = np.std(target_values)

            plt.figure(figsize=(4, 4))
            venn2(subsets=(len(bg_values), len(target_values), min_len), set_labels=('Background', 'Target'))
            venn_path = os.path.join(self.temp_folder, "venn_diagram.png")
            plt.savefig(venn_path)
            plt.close()

            self.show_image(venn_path)

            if p < 0.05:
                result = (
                    f"The comparative analysis between the background and target regions "
                    f"revealed an average value of {bg_mean:.2f} (± SD of {bg_std:.2f}) in the background, "
                    f"compared to an average of {target_mean:.2f} (± SD of {target_std:.2f}) in the target regions. "
                    f"Using the Wilcoxon signed-rank test, the results showed a statistically significant "
                    f"difference (p = {p:.4f}), indicating that the target regions differ meaningfully "
                    f"from the background."
                )
            else:
                result = (
                    f"The comparative analysis between the background and target regions "
                    f"revealed an average value of {bg_mean:.2f} (± SD of {bg_std:.2f}) in the background, "
                    f"compared to an average of {target_mean:.2f} (± SD of {target_std:.2f}) in the target regions. "
                    f"The Wilcoxon signed-rank test showed no statistically significant difference "
                    f"(p = {p:.4f}), suggesting that the target regions are similar to the background."
                )

if __name__ == "__main__":
    app = TalosPrincipleApp()


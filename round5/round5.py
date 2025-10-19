import os
import shutil
import cv2
from PIL import Image, ImageTk
import subprocess
import pybedtools
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import tkinter as tk
from tkinter import filedialog
import threading
from tkinter import ttk
import numpy as np


class LoadingScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Loading")
        self.geometry("250x100+700+400")
        self.overrideredirect(True)  # No window border

        self.configure(bg="white")

        label = tk.Label(self, text="Analyzing...", font=("Arial", 14), bg="white")
        label.pack(pady=10)

        self.progress = ttk.Progressbar(self, mode='indeterminate')
        self.progress.pack(padx=20, pady=10, fill='x')
        self.progress.start(10)

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
        self.target_names = [None,None]
        self.data_file = ""
        self.file_path = []

        self.res = [None,None,None]

        # Input string for region view
        self.input_str = "5:135444104-135444504"

        # Create a horizontal frame to hold both the text box and the button
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        # Text box inside the same frame
        self.text_box = tk.Entry(input_frame)
        self.text_box.pack(side=tk.LEFT, padx=5)
        self.text_box.insert(0, self.input_str)

        # Button inside the same frame, right next to the text box
        self.run_button = tk.Button(input_frame, text="Go", command=self.run_function)
        self.run_button.pack(side=tk.LEFT, padx=5)

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
        self.analyze_button = tk.Button(button_frame, text="Analyze", command=self.start_analysis)
        self.analyze_button.pack(side=tk.LEFT, padx=5)


        self.clear_button = tk.Button(button_frame, text="Clear", command=self.clear_ini)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.save = tk.Button(button_frame, text="Save", command=self.save)
        self.save.pack(side=tk.LEFT, padx=5)

        self.fancy = tk.BooleanVar(value=False)

        # Simple checkbutton
        self.toggle = tk.Checkbutton(
            self,
            text="Enable base-pair wise analysis (much longer analysis time)",
            variable=self.fancy,
        )
        self.toggle.pack(padx=20, pady=20)

        # When creating your canvas:
        self.canvas = tk.Canvas(self)
        self.v_scroll = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.v_scroll.set)

        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Result text box
        self.result_text = tk.Text(self, height=80, width=150)
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
        self.target_names[0] = str(self.target_files[0]).split("/")[-1].split(".")[0]
        self.target_names[1] = str(self.target_files[1]).split("/")[-1].split(".")[0]

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
        self.result_text.delete(1.0, tk.END)

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
            self.show_images(["bigwig.png"])
        else:
            self.show_images(["empty.png"])

    def show_images(self, img_paths):
        self.canvas.delete("all")  # Clear previous images

        y_offset = 0  # Starting Y position
        self.canvas_images = []  # Keep image references

        total_height = 0
        max_width = 0

        for img_path in img_paths:
            try:
                image = cv2.imread(img_path)
                if image is None:
                    print(f"Image not found: {img_path}")
                    continue

                height, width, _ = image.shape
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(image)
                image_tk = ImageTk.PhotoImage(pil_image)

                self.canvas.create_image(0, y_offset, anchor=tk.NW, image=image_tk)
                self.canvas_images.append(image_tk)  # Prevent garbage collection

                y_offset += height
                total_height += height
                max_width = max(max_width, width)

            except Exception as e:
                print(f"Failed to load image {img_path}: {e}")

        # Resize canvas to fit all images
        self.canvas.config(scrollregion=(0, 0, max_width, total_height))
        self.canvas.config(width=max_width, height=min(total_height, 800))  # or whatever height you want visible

    def start_analysis(self):
        # Show the loading screen
        self.loading = LoadingScreen(self)

        # Run the analysis in a separate thread to avoid UI freeze
        threading.Thread(target=self.analyze).start()

    def analyze(self):

        if not self.target_files:
            print("warning! missing target file")
            self.after(0, self.analysis_done)
            return
        elif not self.background_file and not self.data_file:
            print("warning! at least upload BG or Data file!")
            self.after(0, self.analysis_done)
            return

        # fill background with data or data with background if missing
        elif not self.background_file:
            bg_tool = pybedtools.BedTool(self.data_file)
            data_tool = pybedtools.BedTool(self.data_file)
        elif not self.data_file:
            bg_tool = pybedtools.BedTool(self.background_file)
            data_tool = pybedtools.BedTool(self.background_file)
        else:
            bg_tool = pybedtools.BedTool(self.background_file)
            data_tool = pybedtools.BedTool(self.data_file)

        target_tool_0 = pybedtools.BedTool(self.target_files[0])

        # use data as values for each track
        bg_data = data_tool.intersect(bg_tool, wa=True)
        target_data_0 = data_tool.intersect(target_tool_0, wa=True)


        # parse bed into the values only
        bg_values = []
        for f in bg_data:
            try:
                bg_values.append(float(f[3]))
            except:
                bg_values.append(str(f[3]))

        target_values_0 = []
        for f in target_data_0:
            try:
                target_values_0.append(float(f[3]))
            except:
                target_values_0.append(str(f[3]))


        if not bg_values or not target_values_0:
            self.result_text.insert(tk.END, "Not enough data for analysis.\n")
            self.after(0, self.analysis_done)
            return

        if len(self.target_files)==2:

            target_tool_1 = pybedtools.BedTool(self.target_files[1])
            target_data_1 = data_tool.intersect(target_tool_1, wa=True)
            intersect = target_data_0.intersect(target_data_1, u=True)

            target_values_1 = []
            for f in target_data_1:
                try:
                    target_values_1.append(str(f[3]))
                except:
                    target_values_1.append(float(f[3]))

            Target1, Target2 = self.target_names[0], self.target_names[1]

            a,b,ab = len(target_data_0),len(target_data_1),len(intersect)

            venn2(subsets=(a - ab, b - ab, ab), set_labels=(Target1, Target2))
            plt.title(f'Venn Diagram of Overlap Between {Target1} and {Target2} ')
            venn_path = os.path.join(self.temp_folder, "venn_diagram.png")
            plt.savefig(venn_path)
            plt.close()

            if(self.fancy.get()):
                overlaps = self.analyze_fancy(target_data_1, target_data_0)
            else:
                N = len(bg_tool)
                A = len(target_values_0)
                B = len(target_values_1)
                overlaps = np.random.hypergeometric(ngood=A, nbad=N - A, nsample=B, size=1000)

            target_res = len(target_data_0.intersect(target_data_1, wa=True, wb=True))

            p_enrich = (sum(o >= target_res for o in overlaps) + 1) / (N + 1)
            p_deplete = (sum(o <= target_res for o in overlaps) + 1) / (N + 1)
            p_two_sided = 2 * min(p_enrich, p_deplete)

            result = (
                f"  In this analysis, we compared the overlap between {Target1} (target 1) and {Target2} (target 2) against random expectation. "
                f"  The algorithm counts the observed overlap, then randomly samples subsets of the same size as target 1 and 2."
                f"  we fill the sequences from the background file and we randomly select for each subset 1000 times to build a distribution. From this, we compute:\n"
                f"- Enrichment p-value probability that the observed value is higher then expected \n"
                f"- Depletion p-value probability that the observed value is lower then expected \n"
                f"- Two-sided p-value in case you do not knew ahead the expected direction use this value \n\n"
                f"Results:\n"
                f"Observed overlap = {target_res}\n"
                f"Enrichment p-value = {p_enrich:.4f}\n"
                f"Depletion p-value = {p_deplete:.4f}\n"
                f"Two-sided p-value = {p_two_sided:.4f}"
            )

            plt.hist(overlaps, bins=30, color='skyblue', edgecolor='black')
            plt.axvline(target_res, color='red', linestyle='dashed', linewidth=2,
                        label=f'Observed Overlap: {target_res}')
            plt.title('Overlap Null Distribution\nRandom BG Sets')
            plt.xlabel('Overlap Count')
            plt.ylabel('Frequency')
            plt.legend()
            dis_path = os.path.join(self.temp_folder, "distribution.png")
            plt.savefig(dis_path)
            plt.close()

            self.show_images([venn_path, dis_path])

            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result)
            self.res = [dis_path, venn_path, result]

            self.after(0, self.analysis_done)


    def analyze_fancy(self,target_data_1,target_data_0):

            N = 1000
            size1 = len(target_data_0)
            size2 = len(target_data_1)

            overlaps = []
            for _ in range(N):
                subset1 = target_data_0.shuffle(genome="hg18",incl=self.background_file)
                subset2 = target_data_1.shuffle(genome="hg18",incl=self.background_file)
                overlap = subset1.intersect(subset2, wa=True, wb=True).total_coverage()
                overlaps.append(overlap)

            return overlaps

            """
                        if (type(bg_values[0]) == float or type(bg_values[0]) == int) and len(self.target_files) == 2:
                N = 1000
                size1 = len(target_values_0)
                size2 = len(target_values_1)

                means = []
                for _ in range(N):
                    subset1 = set(random.sample(bg_values, size1))
                    subset2 = set(random.sample(bg_values, size2))
                    mean = sum(subset1 & subset2)/len(subset1 & subset2)
                    means.append(mean)

                target_res = sum(set(target_values_0) & set(target_values_1))/len(set(target_values_0) & set(target_values_1))

                result += (
                    f"numerical analysis Results:\n"
                    f"Observed mean = {target_res}\n"
                    f"Enrichment p-value = {p_enrich:.4f}\n"
                    f"Depletion p-value = {p_deplete:.4f}\n"
                    f"Two-sided p-value = {p_two_sided:.4f}"
                )

                p_enrich = (sum(o >= target_res for o in means) + 1) / (N + 1)
                p_deplete = (sum(o <= target_res for o in means) + 1) / (N + 1)
                p_two_sided = 2 * min(p_enrich, p_deplete)

            
            """

    def analysis_done(self):
        self.loading.destroy()

    def make_unique_dir(self, base_dir, name="result"):
        """
        Create a new directory under base_dir with name,
        adding a number suffix if it already exists.
        """
        dir_path = os.path.join(base_dir, name)
        counter = 1
        while os.path.exists(dir_path):
            dir_path = os.path.join(base_dir, f"{name}_{counter}")
            counter += 1
        os.makedirs(dir_path)
        return dir_path

    def save(self):
        venn_path = self.res[0]
        hist_path = self.res[1]
        results_text = self.res[2]

        # Ask user to choose a directory
        save_dir = filedialog.askdirectory(title="Choose a directory to save package")
        # add unique naming in the future
        save_dir = self.make_unique_dir(save_dir,"result")
        if save_dir:
            if results_text:
                with open(f"{save_dir}/res.txt", "w") as f:
                    f.write(results_text)
            if venn_path:
                shutil.copy(venn_path, os.path.join(save_dir, "venn_res.png"))
            if hist_path:
                shutil.copy(hist_path, os.path.join(save_dir, "hist_res.png"))


if __name__ == "__main__":

    app = TalosPrincipleApp()

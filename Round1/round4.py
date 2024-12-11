import os
import shutil
import cv2
from PIL import Image, ImageTk
import subprocess
from tkinter import filedialog
import pybedtools
import time
import tkinter as tk
class TalosPrincibleApp(tk.Tk):
    def __init__(self):
        super().__init__()        # Create a style object

        self.title("The Talos Principle")
        self.geometry("2000x600")

        # Create a temporary folder
        self.temp_folder = "temp_folder"
        os.makedirs(self.temp_folder, exist_ok=True)


        self.file_path = []
        self.input_str = "X:2,500,000-3,000,000"

        # Create the text box
        self.text_box = tk.Entry(self)
        self.text_box.pack(pady=10)

        # Create a frame to hold the buttons
        button_frame = tk.Frame(self)
        button_frame.pack(padx=20, pady=20)

        # Create the "Save As" button
        self.save_as_button = tk.Button(button_frame, text="Save As", command=self.save_as)
        self.save_as_button.pack(side=tk.LEFT, padx=5)

        # Create the "Run" button
        self.run_button = tk.Button(button_frame, text="Go", command=self.run_function)
        self.run_button.pack(side=tk.LEFT, padx=5)

        # Create the "Load File" button
        self.load_button = tk.Button(button_frame, text="Load File", command=self.load_file)
        self.load_button.pack(side=tk.LEFT, padx=5)

        # Create the "Intersect" button
        self.intersect_button = tk.Button(button_frame, text="Intersect", command=self.intersection)
        self.intersect_button.pack(side=tk.LEFT, padx=5)

        # Create the "Clear INI" button
        self.clear_button = tk.Button(button_frame, text="Clear", command=self.clear_ini)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Create the "-x100" button
        self.zoom_out_100_button = tk.Button(button_frame, text="-x100", command=lambda: self.zoom_function(100, "out"))
        self.zoom_out_100_button.pack(side=tk.LEFT, padx=5)

        # Create the "-x10" button
        self.zoom_out_10_button = tk.Button(button_frame, text="-x10", command=lambda: self.zoom_function(10, "out"))
        self.zoom_out_10_button.pack(side=tk.LEFT, padx=5)

        # Create the "+x10" button
        self.zoom_in_10_button = tk.Button(button_frame, text="+x10", command=lambda: self.zoom_function(0.1, "in"))
        self.zoom_in_10_button.pack(side=tk.LEFT, padx=5)

        # Create the "+x100" button
        self.zoom_in_100_button = tk.Button(button_frame, text="+x100", command=lambda: self.zoom_function(0.01, "in"))
        self.zoom_in_100_button.pack(side=tk.LEFT, padx=5)

        # Create a canvas to display the image
        self.canvas = tk.Canvas(self, width=400, height=400)
        self.canvas.pack(pady=10)

        self.clear_ini()

        # Start the main event loop
        self.mainloop()

    def __del__(self):
        # Delete the temporary folder and its contents
        shutil.rmtree(self.temp_folder, ignore_errors=True)
    def parse_genome(self,str):
        if ":" in str and "-" in str:
            try:
                return [str.split(":")[0],int(str.split(":")[1].split("-")[0].replace(",","")),int(str.split(":")[1].split("-")[1].replace(",",""))]
            except:
                print([str.split(":")[0],int(str.split(":")[1].split("-")[0].replace(",","")),int(str.split(":")[1].split("-")[1].replace(",",""))])
        else:
            return []

    def zoom_function(self, zoom_factor, zoom_direction):
        loc = self.parse_genome(self.input_str)
        if loc:
            chrom, start, end = loc
            center = (start + end) // 2
            span = end - start

            if zoom_direction == "out":
                new_span = int(span * zoom_factor)
                new_start = max(0, center - new_span // 2)
                new_end = new_start + new_span
            elif zoom_direction == "in":
                new_span = int(span / zoom_factor)
                new_start = center - new_span // 2
                new_end = new_start + new_span

            self.input_str = f"{chrom}:{new_start}-{new_end}"
            self.text_box.delete(0, tk.END)
            self.text_box.insert(0, self.input_str)
            self.pyGenomeTracks()

        # Code to handle zooming operation
        # zoom_factor will be 10 or 100 based on the button clicked
        # zoom_direction will be "in" or "out" based on the button clicked
        pass
    def load_bed_files(self):
        bed_files = [s for s in self.file_path if s.endswith(".bed")]
        return bed_files

    def intersection(self):
        beds = self.load_bed_files()
        if len(beds) < 2:
            print("Not enough tracks")
        else:
            result = pybedtools.BedTool(beds[0])
            for bed in beds[1:]:
                result = result.intersect(bed)

            filename = f'temp_folder/intersection_{time.time()}.bed'
            result.saveas(filename)
            self.load_file(filename)
    def make_track_files(self):
        run_list = ["make_tracks_file", "--trackFiles"]
        run_list.extend(self.file_path)
        run_list.extend(["-o", "test.ini"])
        subprocess.run(run_list)

    def save_as(self):
        # Open a file dialog to get the save location and filename
        file_path = filedialog.asksaveasfilename(defaultextension=".png")

        if file_path:
            # Save the image to the specified location
            cv2.imwrite(file_path, cv2.imread("bigwig.png"))

    def load_file(self,path=""):
        # Use the filedialog module to open a file dialog
        if path=="":
            path = filedialog.askopenfilename(filetypes=[("Any File", "*")])

        if path:
            if ".bedGraph" in path or "wig" in path:
                path = self.convert_to_bigwig(path)

            self.file_path.append(path)
            self.make_track_files()
            # Call the your_function to process the file
            self.pyGenomeTracks()
            self.show_image()

    def convert_to_bigwig(self,path):
        subprocess.run(["./bedGraphToBigWig", path, "hg19.chrom.sizes", f"./temp_folder/output_{time.time()}.bw"])
        return "output.bw"
    def run_function(self):
        # Get the input from the text box
        if  self.text_box.get():
            self.input_str = self.text_box.get()
            self.pyGenomeTracks()

    def clear_ini(self):
        image = cv2.imread("empty.png")

        # Resize the image to fit the canvas
        image = cv2.resize(image, (2000, 400))

        # Convert the image to a Tkinter-compatible format
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image_Tk = ImageTk.PhotoImage(image)

        # Display the image in the Tkinter canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=image_Tk)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Keep a reference to the image_Tk object to prevent it from being garbage collected
        self.canvas.image_Tk = image_Tk
    def pyGenomeTracks(self):
        # This is the function that will be executed when the button is clicked
        # Replace this with your own function
        subprocess.run(["pyGenomeTracks", "--tracks",
                        "test.ini", "--region",
                        self.input_str, "-o", "bigwig.png"])
        self.show_image()

        return f"You entered: {self.input_str}"

    def show_image(self):
        # Load the image using OpenCV
        # does not support linux
        print(self.file_path)
        image = cv2.imread(self.file_path)

        # Invert the colors of the image - darkmod
        # image = cv2.bitwise_not(image)

        # Get the original size of the image
        height, width, channels = image.shape

        # Resize the image to fit the window
        image = cv2.resize(image, (width, height))

        # Convert the image to a Tkinter-compatible format
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Create a PIL Image object from the OpenCV image
        pil_image = Image.fromarray(image)

        # Create a Tkinter-compatible PhotoImage object
        image_tk = ImageTk.PhotoImage(pil_image)

        # Set the window geometry to the size of the image
        self.geometry(f"{width}x{height + 500}")

        # Resize the canvas to the size of the image
        self.canvas.config(width=width, height=height)

        # Display the image in the Tkinter canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Keep a reference to the image_tk object to prevent it from being garbage collected
        self.canvas.image = image_tk

if __name__ == "__main__":
    app = TalosPrincibleApp()

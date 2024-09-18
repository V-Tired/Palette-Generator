from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image

"""An app that allows the user to select a file and then  extract pixel color percentages to get top 20
colors in image. Displays a block for each color and its hex code. Creates textbox list below for copying."""


# Font and Colors for GUI
LIGHT = "#FFE6E6"
PINK = "#E1AFD1"
MID = "#AD88C6"
DARK = "#7469B6"
GREY = "#4c545c"
FONT = ("georgia", 12, "bold")


class PaletteGenerator:
    """Handles all image processing"""
    def __init__(self):
        self.file = ""
        self.colors = []
        self.palette = []
        self.positions = [
            [0, 4], [1, 4], [2, 4], [3, 4], [4, 4],
            [0, 5], [1, 5], [2, 5], [3, 5], [4, 5],
            [0, 6], [1, 6], [2, 6], [3, 6], [4, 6],
            [0, 7], [1, 7], [2, 7], [3, 7], [4, 7]]
        self.square_count = 0

    def get_file(self):
        """Opens file manager to get file path of desired image. Image must be .jpg or .png"""
        self.file = askopenfilename()
        if self.file != "" and self.file.endswith('.jpg') or self.file.endswith('.png'):
            file_name.config(text=self.file)
            file_name.grid(column=0, row=2, columnspan=5, pady=10)
            select.config(text="Change File")
            all_colors.delete("1.0", END)

    def get_colors(self):
        """Use PIL to get the colors from the image. Sort them by highest value count, and only use the top 20."""
        self.colors = []
        img_object = Image.open(self.file).convert("RGB")
        reduced = img_object.convert("P", palette=Image.WEB)
        pal = reduced.getpalette()
        palet = [pal[3 * n:3 * n + 3] for n in range(256)]
        color_count = [(n, palet[m]) for n, m in reduced.getcolors()]
        color_count.sort(reverse=True)

        self.colors = [i[1] for i in color_count][0:20]
        self.to_hex()

    def to_hex(self):
        """Convert the list of generated colors into a hex code for easy searching."""
        self.palette = []
        for each in self.colors:
            hex_code = "#%02x%02x%02x" % tuple(each)
            self.palette.append(hex_code)
        self.create_palette()

    def create_palette(self):
        """Create a square of each color in the top 20 colors. Display its hex code on top."""
        square_count = 0
        for color in self.palette:
            column = self.positions[square_count][0]
            row = self.positions[square_count][1]
            square = Label(
                width=7,
                font=("arial", 10, "bold"),
                height=1,
                text=color,
                bg=color,
                padx=5,
                pady=15,
                highlightthickness=2,
                highlightbackground="black"
            )
            square.grid(column=column, row=row, pady=5)
            square_count += 1
        i = 5
        new_palette = self.palette
        while i < len(new_palette):
            new_palette.insert(i, '\n\n')
            i += (5 + 1)
        text = ",".join(new_palette)
        text = text.replace(",", "   ")
        text.strip()

        all_colors.insert("1.0", f"   {text}")
        all_colors.grid(column=0, row=8, columnspan=5, pady=20)


palette = PaletteGenerator()

# Window Config
window = Tk()
window.minsize(300, 400)
window.config(bg=GREY, padx=20, pady=20)

# Button Config
select = Button(text="Select File", command=palette.get_file, bg=DARK, fg=PINK, font=FONT,)
select.grid(column=0, row=1, columnspan=5)

generate = Button(text="Generate Color Palette", command=palette.get_colors, bg=DARK, fg=PINK, font=FONT,)
generate.grid(column=0, row=3, pady=5, padx=10, columnspan=5)

# Label Config
header = Label(text="Color Palette Generator", font=("georgia", 16, "bold"), bg=GREY, fg=LIGHT, pady=10)
header.grid(column=0, row=0, columnspan=5)

file_name = Label(text="", font=("georgia", 8, "bold"), bg=GREY, fg=LIGHT, wraplength=350)

all_colors = Text(font=("georgia", 10, "bold"), bg=GREY, fg=LIGHT, wrap="word", width=40, height=8,
                  padx=5, pady=5, relief="flat")

window.mainloop()

from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image, ImageFont, ImageDraw

photo_image: PhotoImage
final_image: Image
file: str
is_photo = False
filetypes = [("image", ".jpeg"), ("image", ".jpg"), ("image", ".png")]


def resize_photo(image: Image):
    width = image.size[0]
    height = image.size[1]

    if width < 100 and height < 75:
        return image.resize((int(round(width*3)), int(round(height*3))), Image.LANCZOS)

    elif width < 200 and height < 150:
        return image.resize((int(round(width*3)), int(round(height*3))), Image.LANCZOS)

    elif width < 400 and height < 300:
        return image

    elif width < 800 and height < 600:
        return image.resize((int(round(width/2)), int(round(height/2))), Image.LANCZOS)

    elif width < 1200 and height < 900:
        return image.resize((int(round(width/3)), int(round(height/3))), Image.LANCZOS)

    elif width < 1600 and height < 1200:
        return image.resize((int(round(width/4)), int(round(height/4))), Image.LANCZOS)

    else:
        return "too large"


def upload_action(event=None):
    global photo_image, is_photo, file
    file = filedialog.askopenfilename(filetypes=filetypes)

    with Image.open(file) as img:
        img = Image.open(file)
        warning.config(fg=BG_COLOR)

        if resize_photo(img) != "too large":
            img = resize_photo(img)
            photo_image = ImageTk.PhotoImage(img)
            canvas.config(height=img.size[1], width=img.size[0], bg="#fff")
            canvas.itemconfig(canvas_image, image=photo_image, state="normal")
            is_photo = True
            mark_entry.config(state="normal")

        else:
            canvas.config(height=303, width=404, bg=CANVAS_COLOR)
            canvas.itemconfig(canvas_image, state="hidden")
            warning.config(text=SIZE_ERROR, fg=WARNING_COLOR)
            is_photo = False
            mark_entry.config(state="disabled")

    save_button.config(state="disabled")


def watermark(event=None):
    global photo_image, final_image
    if is_photo:
        save_button.config(state="normal")

        with Image.open(file) as img:
            img = resize_photo(img)
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Italic.ttf", 14)
            draw.text((8, img.size[1] - 19), mark_entry.get(), fill=(66, 194, 255), stroke_width=1, stroke_fill="black", font=font)
            final_image = img
            photo_image = ImageTk.PhotoImage(img)
            canvas.itemconfig(canvas_image, image=photo_image)
        mark_entry.delete(0, END)


def save(event=None):
    if is_photo:
        new_file_name = file.split("/")[-1].split(".")[0] + "-watermarked." + file.split(".")[-1]
        final_image.convert("RGB").save(new_file_name)
        popup = Toplevel(screen)
        popup.config(width=550, height=80, padx=50, pady=30, bg=POPUP_COLOR)
        popup.title("Watermark Successful")
        Label(popup, text=f"File saved as '{new_file_name}'.", bg=POPUP_COLOR).pack()
        Button(popup, text="OK", width=15, highlightbackground=POPUP_COLOR, command=popup.destroy).pack(pady=20)


def check(*args):
    if is_photo and mark_entry.get() != "":
        mark_button.config(state="normal")

    else:
        mark_button.config(state="disabled")


# ------------ UI ------------
BG_COLOR = "#85F4FF"
HEADER_FONT = ("Helvetica Neue", "52", "bold italic")
HEADER_COLOR = "#EFFFFD"
WARNING_COLOR = "#e63622"
SIZE_ERROR = "Your image is too big!"
CANVAS_COLOR = "#42C2FF"
POPUP_COLOR = "#B8FFF9"

# Screen
screen = Tk()
screen.title("Watermarker")
screen.config(bg=BG_COLOR, padx=50, pady=50)

# Header
header_text = Label(text="WATERMARKER", font=HEADER_FONT, bg=BG_COLOR, fg=HEADER_COLOR)
header_text.grid(column=0, row=0, columnspan=2, pady=10)

# Canvas for image and watermark
canvas = Canvas(height=303, width=404, highlightbackground=HEADER_COLOR, bg=CANVAS_COLOR, bd=-2)
canvas_image = canvas.create_image(0, 0, anchor="nw")
canvas.grid(column=0, row=1, columnspan=2, pady=10)

# Size warning
warning = Label(text=SIZE_ERROR, bg=BG_COLOR, fg=BG_COLOR, pady=5)
warning.grid(column=0, row=2, columnspan=2)

# Upload button
button = Button(text="Open", width=32, command=upload_action, highlightbackground=BG_COLOR)
button.grid(column=0, row=3, columnspan=2)

# Watermark input
sv = StringVar()
sv.trace("w", check)
mark_entry = Entry(width=20, highlightbackground=BG_COLOR, textvariable=sv, state="disabled")
mark_entry.grid(column=0, row=4, pady=10, sticky="e")
mark_button = Button(text="Set Watermark", highlightbackground=BG_COLOR, command=watermark, state="disabled")
mark_button.grid(column=1, row=4, sticky="w")

# Save button
save_button = Button(text="Save", width=32, command=save, highlightbackground=BG_COLOR, state="disabled")
save_button.grid(column=0, row=5, columnspan=2)

screen.mainloop()

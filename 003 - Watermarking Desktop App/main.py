from tkinter import *
from tkinter import filedialog
import os 
from tkinter import messagebox
from PIL import Image,ImageTk

# ---------------------------- CONSTANTS ------------------------------- #
BUTTON_COLOR = "#93BFCF"
TEXT_COLOR = "#554994"
BACKGROUND_COLOR = "#BDCDD6"
FONT_NAME = "Courier"

description_text = "1. Select watermark image (Transparnet background, .PNG)\n2. Select the image you want to add the watermark\n3. You can change the position and size of the watermark\n4. Save your work"
image_height = 0
image_width = 0
image_path = "images/placeholder-image.png"
watermark_path = ""
watermark_height = 50
watermark_width = 50
watermark_size = 50
watermark_position = "Center"

# ---------------------------- FUNCTIONS ------------------------------ #
def openfn():
    # filename = filedialog.askopenfilename(title='open')
    filename = filedialog.askopenfilename(title="Select image file", filetypes=(("PNG file", "*.png"), ("JPG file", "*.jpg"),("JPEG file", "*.jpeg"),("ALL file", "*.txt")))
    filename = filename.replace("\\", "/")
    return filename

def create_new_image():
    global img, label_image, tkimage, image_path, watermark_path, image_height, image_width, watermark_height, watermark_width, watermark_size
    if watermark_path != "":
        # Load the image
        img = Image.open(image_path).convert("RGBA")
        size = (500, 500)   # resize the image while keeping its aspect ratio
        img.thumbnail(size)
        image_width, image_height = img.size
        print(f"image: ({image_width}, {image_height})")

        # Load the watermark
        watermark = Image.open(watermark_path).convert("RGBA")
        size = (watermark_size, watermark_size)   # resize the image while keeping its aspect ratio
        watermark.thumbnail(size)
        watermark_width, watermark_height = watermark.size
        print(f"wmark: ({watermark_height}, {watermark_width})")

        # Calculate the position
        x, y = 0, 0
        if watermark_position == "Top-Left":
            x, y = 20, 20  
        elif watermark_position == "Top-Right":
            x, y = image_width - (watermark_width+20) , 20                                     
        elif watermark_position == "Bottom-Left":
            x, y = 20, image_height - (watermark_width+20)        
        elif watermark_position == "Bottom-Right":
            x, y = image_width - (watermark_height+20), image_height - (watermark_width+20)  
        else:
            x, y = (image_width/2)-(watermark_width/2), (image_height/2)-(watermark_width/2)               

        print(f"x: {x} - y: {y}")

        # Creating the preview image
        img.paste(watermark, (int(x), int(y)), watermark) # Putting the watermark on the image
        tkimage = ImageTk.PhotoImage(img)    #Convert To photoimage
        label_image.config(image=tkimage)
    else:
        img = Image.open(image_path).convert("RGBA")
        size = (500, 500)   # resize the image while keeping its aspect ratio
        img.thumbnail(size)
        tkimage = ImageTk.PhotoImage(img)    #Convert To photoimage
        label_image.config(image=tkimage)

def add_image():
    global label_image, tkimage, image_path
    image_path = openfn()
    create_new_image()

def add_watermark():
    global tkwatermark, watermark_path
    watermark_path = openfn()
    create_new_image()

def set_wm_size():
    global watermark_height, watermark_width, watermark_size
    print(spinbox_size.get())
    watermark_size = 50 + int(spinbox_size.get())
    create_new_image()

def set_wm_position():
    global watermark_position
    print(radio_state.get())
    watermark_position = radio_state.get()
    create_new_image()

def save_work():
    save_dir = filedialog.askdirectory(title="Select the Save Folder")
    result = img.convert("RGB")
    save_path = save_dir + '/'
    result.save(os.path.join(save_path, "result.jpeg"), 'JPEG')
    messagebox.showinfo(message="Your images have been saved!\nThank you for using this tool.", title="Saving Successful")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Watermarking App")
window.config(padx=20, pady=20, bg=BACKGROUND_COLOR)

# App title and "how to use" description
label_title = Label(text="Add Watermark to your images")
label_title.config(bg=BACKGROUND_COLOR, highlightthickness=0, fg=TEXT_COLOR, font=(FONT_NAME, 16, "bold"))
label_title.grid(column=0, row=0, sticky=W, columnspan=2)
label_description = Label(text=description_text, justify=LEFT )
label_description.config(bg=BACKGROUND_COLOR, highlightthickness=0, fg=TEXT_COLOR, font=(FONT_NAME, 12, "normal"))
label_description.grid(column=0, row=1, sticky=W, columnspan=2, padx=(0, 20))

# Select watermark button
button_select_watermark = Button(text="Select Watermark", command=add_watermark, highlightbackground=BACKGROUND_COLOR, fg=TEXT_COLOR, bg=BUTTON_COLOR,width=20, font=(FONT_NAME, 10, "bold"))
button_select_watermark.grid(column=0, row=2)

# Select image button
button_select_image = Button(text="SelectImage", command=add_image, highlightbackground=BACKGROUND_COLOR, fg=TEXT_COLOR, bg=BUTTON_COLOR, width=20, font=(FONT_NAME, 10, "bold"))
button_select_image.grid(column=1, row=2)

# Load the image
img = Image.open("images/placeholder-image.png").convert("RGBA")
size = (500, 500)   # resize the image while keeping its aspect ratio
img.thumbnail(size)
tkimage = ImageTk.PhotoImage(img)    #Convert To photoimage
label_image=Label(window, image=tkimage)   #Display the Image
label_image.grid(column=2, row=0, rowspan=10)

# Watermark size settings
label_size = Label(text="Size:", justify=RIGHT )
label_size.config(bg=BACKGROUND_COLOR, highlightthickness=0, fg=TEXT_COLOR, font=(FONT_NAME, 12, "normal"))
label_size.grid(column=0, row=3, sticky=E, padx=(0, 20))
spinbox_size = Spinbox(from_=1, to=50, increment=1, width=5, command=set_wm_size)
spinbox_size.grid(column=1, row=3, sticky=W, padx=(0, 20))


# Watermark position settings
label_position = Label(text="Position:", justify=RIGHT )
label_position.config(bg=BACKGROUND_COLOR, highlightthickness=0, fg=TEXT_COLOR, font=(FONT_NAME, 12, "normal"))
label_position.grid(column=0, row=5, sticky=E, padx=(0, 20))
radio_state = StringVar()   # create a StringVar to store the selected option
radio_state.set("Center")   # set the initial value of the StringVar
radiobutton1 = Radiobutton(text="Top Left", value="Top-Left", variable=radio_state, command=set_wm_position, background=BACKGROUND_COLOR, fg=TEXT_COLOR, font=(FONT_NAME, 10, "bold"))
radiobutton2 = Radiobutton(text="Top Right", value="Top-Right", variable=radio_state, command=set_wm_position, background=BACKGROUND_COLOR, fg=TEXT_COLOR, font=(FONT_NAME, 10, "bold"))
radiobutton3 = Radiobutton(text="Center", value="Center", variable=radio_state, command=set_wm_position, background=BACKGROUND_COLOR, fg=TEXT_COLOR, font=(FONT_NAME, 10, "bold"))
radiobutton4 = Radiobutton(text="Bottom Left", value="Bottom-Left", variable=radio_state, command=set_wm_position, background=BACKGROUND_COLOR, fg=TEXT_COLOR, font=(FONT_NAME, 10, "bold"))
radiobutton5 = Radiobutton(text="Bottom Right", value="Bottom-Right", variable=radio_state, command=set_wm_position, background=BACKGROUND_COLOR, fg=TEXT_COLOR, font=(FONT_NAME, 10, "bold"))
radiobutton1.grid(column=1, row=5, sticky=W)
radiobutton2.grid(column=1, row=6, sticky=W)
radiobutton3.grid(column=1, row=7, sticky=W)
radiobutton4.grid(column=1, row=8, sticky=W)
radiobutton5.grid(column=1, row=9, sticky=W)

# Save Final Image Button 
button_select_image = Button(text="Save Your Work", command=save_work, highlightbackground=BACKGROUND_COLOR, fg=TEXT_COLOR, bg=BUTTON_COLOR, width=20, font=(FONT_NAME, 10, "bold"))
button_select_image.grid(column=2, row=10, pady=(20, 0))


window.mainloop()
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
from keras.models import load_model

# Loading the model
model = load_model("Age_Gender_Detection.keras")

# Initializing the GUI
top = tk.Tk()
top.geometry('800x600')
top.title("Age and Gender Detector")
top.configure(background="#CDCDCD")

# Initializing the Labels (1 for age and 1 for gender)
label1 = Label(top, background="#CDCDCD", font=("arial", 15, "bold"))
label2 = Label(top, background="#CDCDCD", font=("arial", 15, "bold"))
sign_image = Label(top)

# Designing Detect function which detects the age and gender of the person in image using the model
def Detect(file_path):
    global label_packed
    image = Image.open(file_path)
    image = image.resize((48, 48))
    image = np.expand_dims(image, axis=0)
    image = np.array(image)
    image = np.delete(image, 0, 1)
    image = np.resize(image, (48, 48, 3))
    print(image.shape)
    sex_f = ["Male", "Female"]
    image = np.array(image) / 255
    pred = model.predict(np.array([image]))
    age = int(np.round(pred[1][0]))
    sex = int(np.round(pred[0][0]))
    print("Predicted Age is " + str(age))
    print("Predicted Gender is " + sex_f[sex])
    label1.configure(foreground="#011638", text=f"Predicted Age: {age}")
    label2.configure(foreground="#011638", text=f"Predicted Gender: {sex_f[sex]}")
    label1.pack(side="bottom", expand=True)
    label2.pack(side="bottom", expand=True)

# Defining Show_detect button function 
def show_Detect_button(file_path):
    global Detect_b
    if 'Detect_b' in globals():
        Detect_b.pack_forget()  # Remove the previous button if it exists
    Detect_b = Button(button_frame, text="Detect Image", command=lambda: Detect(file_path), padx=10, pady=5)
    Detect_b.configure(background="#364156", foreground="white", font=("arial", 10, "bold"))
    Detect_b.pack(side="bottom", pady=20)

# Defining Upload Image function
def upload_image():
    try:
        file_path = filedialog.askopenfilename()
        uploaded = Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width() / 2.25), (top.winfo_height() / 2.25)))
        im = ImageTk.PhotoImage(uploaded)
        sign_image.configure(image=im)
        sign_image.image = im
        label1.configure(text='')
        label2.configure(text='')
        show_Detect_button(file_path)
    except Exception as e:
        print(f"Error: {e}")

# Creating a frame to hold the buttons and labels
button_frame = Frame(top, background="#CDCDCD")
button_frame.pack(side="bottom", fill="x", pady=20)

upload = Button(button_frame, text="Upload an image", command=upload_image, padx=10, pady=5)
upload.configure(background="#364156", foreground="white", font=("arial", 10, "bold"))
upload.pack(side="bottom", pady=20)
sign_image.pack(side="bottom", expand=True)
label1.pack(side="bottom", expand=True)
label2.pack(side="bottom", pady=20, expand=True)
heading = Label(top, text="Age and Gender Detector", pady=15, font=("arial", 15, "bold"))
heading.configure(background="#CDCDCD", foreground="#364156")
heading.pack()
top.mainloop()



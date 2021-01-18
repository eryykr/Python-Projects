#IMAGE RECOGNITION

#LIBRARIES
import numpy as np
import keras

#IMPORTING DATA
(train_images, train_labels), (test_images, test_labels) = keras.datasets.mnist.load_data()

#SETTING UP NETWORK
network = keras.models.Sequential()
network.add(keras.layers.Dense(512, activation='relu', input_shape=(28*28,)))
network.add(keras.layers.Dense(10, activation='softmax'))
#THE COMPILATION STEP
network.compile(optimizer='rmsprop',
                loss='categorical_crossentropy',
                metrics=['accuracy'])

#PREPARING THE IMAGES
train_images = train_images.reshape((60000,28*28))
train_images = train_images.astype('float32')/255

test_images = test_images.reshape((10000,28*28))
test_images = test_images.astype('float32')/255

#PREPARING THE LABELS
train_labels = keras.utils.to_categorical(train_labels)
test_labels = keras.utils.to_categorical(test_labels)

#TRAINING
network.fit(train_images, train_labels, epochs=2, batch_size=128, verbose=0)





#INTERFACE AND IMAGE PROCESSING
import tkinter as tk
from PIL import ImageGrab
import matplotlib.pyplot as plt



#CANVAS PARAMETERS
CANVAS_HEIGHT = 500
CANVAS_WIDTH = 500
BRUSH_SIZE = 15

#FUNCTION FOR DRAWING
def paint(event):
	colour='black'
	x1,y1=(event.x-BRUSH_SIZE), (event.y-BRUSH_SIZE)
	x2,y2=(event.x+BRUSH_SIZE), (event.y+BRUSH_SIZE)
	c.create_oval(x1,y1,x2,y2, fill=colour, outline=colour)

#OTHER FUNCTIONS
def rebin(a, shape):
    sh = shape[0],a.shape[0]//shape[0],shape[1],a.shape[1]//shape[1]
    return a.reshape(sh).mean(-1).mean(1)

def crop(array, amount):
    array = array[0+amount:len(array)-1-amount, 0+amount:len(array)-1-amount]
    return array  

def clear():
    c.delete("all")
    txt_prediction.delete("1.0")

def exit():
	window.quit()

def get_digit(a):
    a = list(a)
    return a.index(max(a))

def reverse(a):
    for i in range(len(a)):
        a[i] = (255-a[i])/255
    return np.array(a)
	
def prediction(widget):
    #capturing
    x=window.winfo_rootx()+widget.winfo_x()
    y=window.winfo_rooty()+widget.winfo_y()
    x1=x+widget.winfo_width()
    y1=y+widget.winfo_height()
    img = ImageGrab.grab().crop((x,y,x1+139,y1+139))
    
    #turning greyscale
    img = img.convert('L')
    
    #converting to array
    img = np.asarray(img)
    
    #cropping
    img = crop(img,69)
    
    #downsampling to 28 by 28 and reshaping
    img = rebin(img, (28,28))
    img = img.reshape(784)
    
    #'reversing' and normalising
    img = reverse(img)

    #prediction
    prediction = get_digit(network.predict(np.array([img]))[0])
    txt_prediction.delete("1.0", tk.END)
    txt_prediction.insert(tk.END, prediction)
    
#CREATING WINDOW FOR DRAWING
window = tk.Tk()
window.title("Digit Indentifier")

c=tk.Canvas(master=window, width=CANVAS_WIDTH, height=CANVAS_HEIGHT,bg='white')
c.pack(expand=True, fill=tk.BOTH)
c.bind('<B1-Motion>', paint)

#USER INTERFACE
frm_buttons = tk.Frame(borderwidth=5, relief=tk.SUNKEN)
frm_buttons.pack()

#CREATING BUTTONS AND TEXT BOX
btn_predict = tk.Button(master=frm_buttons, width=20, height=3, text="PREDICT", command=lambda: prediction(c))
btn_clear = tk.Button(master=frm_buttons, width=20, height=3, text="CLEAR", command=clear)
btn_exit = tk.Button(master=frm_buttons, width=20, height=3, text="EXIT", command=exit)
txt_prediction = tk.Text(master=frm_buttons, width=5, height=2)
txt_prediction.configure(font=("Arial", 15, "bold"))

#ARRANGING IN GRID
txt_prediction.grid(row=0, column=1, pady=5, padx=5)
btn_predict.grid(row=1, column=0, padx=5, pady=5)
btn_clear.grid(row=1, column=1, padx=5, pady=5)
btn_exit.grid(row=1, column=2, padx=5, pady=5)


    
    













window.mainloop()
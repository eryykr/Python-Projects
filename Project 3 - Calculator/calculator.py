import tkinter as tk 



#UI
#WINDOW FOR WHOLE CALCULATOR
window = tk.Tk()
window.title("Calculator")

#DISPLAY
#creating frame for display
frm_display = tk.Frame(relief=tk.SUNKEN, borderwidth=5)
frm_display.pack()

#adding text widget to act as a display
OUTPUT = ""
txt_display = tk.Text(master=frm_display, width=35, height=5)
txt_display.configure(font=("Arial", 10, "bold"))
txt_display.insert(tk.END, OUTPUT)
txt_display.pack()

#BUTTONS
#function for button presses

#displaying button's symbol
def press(sym):
	txt_display.insert(tk.END, OUTPUT+sym)

#closing window
def quit():
	window.quit()

#clearing calculator display
def clear():
	txt_display.delete("1.0", tk.END)

#calculating result and displaying it
def equals(string):
	try:
		#splitting string by operators
		string = string.replace("+", " + ").replace("-", " - ").replace("x", " x ").replace("÷", " ÷ ")
		string = string.split()
		#replacing operations by their results
		while string.count("÷") > 0:
			for i in string:
				if i == "÷":
					new_index = string.index(i)-1
					new_item = str(float(string[string.index(i)-1])/float(string[string.index(i)+1]))
					del(string[string.index(i)-1:string.index(i)+2])
					string.insert(new_index, new_item)
		while string.count("x") > 0:
			for i in string:
				if i == "x":
					new_index = string.index(i)-1
					new_item = str(float(string[string.index(i)-1])*float(string[string.index(i)+1]))
					del(string[string.index(i)-1:string.index(i)+2])
					string.insert(new_index, new_item)
		while string.count("+") > 0:
			for i in string:
				if i == "+":
					new_index = string.index(i)-1
					new_item = str(float(string[string.index(i)-1])+float(string[string.index(i)+1]))
					del(string[string.index(i)-1:string.index(i)+2])
					string.insert(new_index, new_item)
		while string.count("-") > 0:
			for i in string:
				if i == "-":
					new_index = string.index(i)-1
					new_item = str(float(string[string.index(i)-1])-float(string[string.index(i)+1]))
					del(string[string.index(i)-1:string.index(i)+2])
					string.insert(new_index, new_item)
		#clearing display and displaying result
		txt_display.delete("1.0", tk.END)
		txt_display.insert(tk.END, string[0])
	except:
		txt_display.delete("1.0", tk.END)
		txt_display.insert(tk.END, "ERROR")




#creating frame for buttons
frm_buttons = tk.Frame(borderwidth=5)
frm_buttons.pack()

#creating buttons
BUTTON_WIDTH = 10
BUTTON_HEIGHT = 3
btn_0 = tk.Button(master=frm_buttons, text="0", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=lambda: press("0"))
btn_1 = tk.Button(master=frm_buttons, text="1", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=lambda: press("1"))
btn_2 = tk.Button(master=frm_buttons, text="2", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=lambda: press("2"))
btn_3 = tk.Button(master=frm_buttons, text="3", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=lambda: press("3"))
btn_4 = tk.Button(master=frm_buttons, text="4", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=lambda: press("4"))
btn_5 = tk.Button(master=frm_buttons, text="5", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=lambda: press("5"))
btn_6 = tk.Button(master=frm_buttons, text="6", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=lambda: press("6"))
btn_7 = tk.Button(master=frm_buttons, text="7", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=lambda: press("7"))
btn_8 = tk.Button(master=frm_buttons, text="8", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=lambda: press("8"))
btn_9 = tk.Button(master=frm_buttons, text="9", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=lambda: press("9"))

btn_plus = tk.Button(master=frm_buttons, text="+", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=lambda: press("+"))
btn_minus = tk.Button(master=frm_buttons, text="-", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=lambda: press("-"))
btn_multiply = tk.Button(master=frm_buttons, text="x", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=lambda: press("x"))
btn_divide = tk.Button(master=frm_buttons, text="÷", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=lambda: press("÷"))
btn_exit = tk.Button(master=frm_buttons, text="EXIT", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=quit)

btn_equals = tk.Button(master=frm_buttons, text="=", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=lambda: equals(txt_display.get("1.0", tk.END)))
btn_point = tk.Button(master=frm_buttons, text=".", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=lambda: press("."))
btn_clear = tk.Button(master=frm_buttons, text="AC", width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=clear)

#arranging buttons in grid
btn_1.grid(row=0, column=0, padx=5, pady=5)
btn_2.grid(row=0, column=1, padx=5, pady=5)
btn_3.grid(row=0, column=2, padx=5, pady=5)

btn_4.grid(row=1, column=0, padx=5, pady=5)
btn_5.grid(row=1, column=1, padx=5, pady=5)
btn_6.grid(row=1, column=2, padx=5, pady=5)

btn_7.grid(row=2, column=0, padx=5, pady=5)
btn_8.grid(row=2, column=1, padx=5, pady=5)
btn_9.grid(row=2, column=2, padx=5, pady=5)

btn_0.grid(row=3, column=0, padx=5, pady=5)
btn_point.grid(row=3, column=1, padx=5, pady=5)
btn_equals.grid(row=3, column=2, padx=5, pady=5)

btn_plus.grid(row=4, column=0, padx=5, pady=5)
btn_minus.grid(row=4, column=1, padx=5, pady=5)
btn_multiply.grid(row=4, column=2, padx=5, pady=5)

btn_divide.grid(row=5, column=0, padx=5, pady=5)
btn_clear.grid(row=5, column=1, padx=5, pady=5)
btn_exit.grid(row=5, column=2, padx=5, pady=5)

m_s = 70
frm_buttons.columnconfigure(0, weight=1, minsize=m_s)
frm_buttons.columnconfigure(1, weight=1, minsize=m_s)
frm_buttons.columnconfigure(2, weight=1, minsize=m_s)

frm_buttons.rowconfigure(0, weight=1, minsize=m_s)
frm_buttons.rowconfigure(1, weight=1, minsize=m_s)
frm_buttons.rowconfigure(2, weight=1, minsize=m_s)
frm_buttons.rowconfigure(3, weight=1, minsize=m_s)
frm_buttons.rowconfigure(4, weight=1, minsize=m_s)



window.mainloop()
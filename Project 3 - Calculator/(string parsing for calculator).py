output = "12+12/5.544-69.8-55+22/5-"



def parse(string):
	#splitting string by operators
	string = string.replace("+", " + ").replace("-", " - ").replace("*", " * ").replace("/", " / ")
	string = string.split()
	#replacing operations by their results
	while string.count("/") > 0:
		for i in string:
			if i == "/":
				new_index = string.index(i)-1
				new_item = str(float(string[string.index(i)-1])/float(string[string.index(i)+1]))
				del(string[string.index(i)-1:string.index(i)+2])
				string.insert(new_index, new_item)
	while string.count("*") > 0:
		for i in string:
			if i == "*":
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
	return string[0]

try:
	print(parse(output))
except:
	print("ERROR")
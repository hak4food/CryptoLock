#This code was written by Bryan Gonzalez
#gonzalez.bryan@gmail.com 
#This was intented for educational purposes.


import tkinter as tk
import time
import sys
import collections


#variables
numSamples=0
maxSamples=10
numTypo=0
maxTypo=15

idx = 0
sEqual=0
aList = []
aList1 = []
tMesureList = []
keyList = []

t0 = time.perf_counter()
#keyword = "wortman."
keyword = sys.argv[1] + "."

def mesureList():
	global tMesureList
	global keyList
	sumValue = 0.0
	for k in range(0,(len(aList)-1)):
		j = aList[k+1] - aList[k]
		tMesureList.append(j)
		sumValue = sumValue + j
	avgValue =  sumValue /len(tMesureList)
	binList = []	
	for item in tMesureList:
		if avgValue > item:
			binList.append('1')
		else:
			binList.append('0') 
	binV = ''.join(binList) #coverts to string
	hexV = hex(int(binV,2))
	text.insert('end', hexV)
	text.insert('end', '\n')
	keyList.append(hexV)
	keyDulo()

def keyDulo():
	o = collections.Counter(keyList).most_common(1)
	#print(w)
	print("\n")
	#print(o[0][0])
	if o[0][1] == 4:
		#print("you key is: ",o[0][0])
		print(o[0][0])
		quitProgram()
	text.insert('end', o)
	text.insert('end', '\n')

def helloCallBack():
	text.insert('end', '\n')	
	list2string()

def compareAnswer():
	global sEqual
	sList = ''.join(aList1)
	if sList == keyword:
		#text.insert('end', 'Sucessful\n')
		sEqual = 1
		return sEqual
	else:
		#text.insert('end', 'no equals\n')
		sEqual = 0
		return sEqual
	
def onKeyPress(event):
	global idx 
	if str(keyword[idx]) != str(event.char):
		 clearRedo()
	else:
		idx+=1
		text.insert('end', '%s' % (event.char, )) #text.insert('end', 'You pressed %.8f\n' % (time.perf_counter() - t0, ))
		aList.append(time.perf_counter() - t0)
		aList1.append(event.char)
		if '.' == str(event.char):
			idx=0
			text.insert('end', '\nProcessing..\n') #text.insert('end', '\nfound period\n')
			compareAnswer()
			if sEqual:
				mesureList()
				printList()
				if numSamples >= maxSamples:
					print("Failed: Please try again")
					quitProgram()
	
def list2string():
	sList = ''.join(aList1)
	text.insert('end', sList)
	if sList == keyword:
		printList()
	else:
		aList[:] = []
		aList1[:] = []
		tMesureList[:] = []
		idx=0

def printList():
	global aList
	global aList1
	global numSamples
	global tMesureList
	#filename = 'data'+str(numSamples)+'.txt'
	#f = open(filename,'w')
	#for item in aList:
	#	f.write("%f\n" % item)
	#for item in aList1:
	#	f.write("%s\n" % item)	
	#for item in tMesureList:
	#	f.write("%f\n" % item)	
	#f.close()
	aList[:] = []
	aList1[:] = []
	tMesureList[:] = []
	idx=0
	numSamples += 1
	
def clearRedo():
	global idx
	global numTypo
	aList[:] = []
	aList1[:] = []
	tMesureList[:] = []
	idx=0
	text.insert('end', '\nTypo Failed Attempt\n')
	numTypo += 1
	if numTypo > maxTypo:
		print("Failed: Please try again")
		quitProgram()	

def quitProgram():
		sys.exit()
	
#_______________________start of main_________________________

#tk declare instance
root = tk.Tk()
root.geometry('500x600')

#create 3 objects for tk
w = tk.Label(root, text=keyword, font=('Comic Sans MS', 18))
sc = tk.Scrollbar(root)
text = tk.Text(root, background='black', foreground='white', font=('Comic Sans MS', 10))
#B = tk.Button(root, text ="done", command = helloCallBack)

#pack the object

w.pack()
#B.pack()
sc.pack(side=tk.RIGHT,fill=tk.Y)
text.pack(side=tk.LEFT,fill=tk.Y)
sc.config(command=text.yview)
text.config(yscrollcommand=sc.set)

#run program
root.bind('<KeyPress>', onKeyPress)
root.mainloop()

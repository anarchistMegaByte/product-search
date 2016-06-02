import mysql.connector as m
import re
# search.models 
cxn=m.connect(user='root',password='manav1993',host='127.0.0.1',database='test_paytm')
cursor=cxn.cursor()
cursor.execute("select * from main_Jabong;")
result=cursor.fetchall() 
final=[]
for i in range(len(result)):
    final.append(list(result[i]))
f = open("final3.txt","w")

globaltemp = ""
for li in final:
	#print (li)
	temp = ''
	for x in li:
		if str(x).isdigit():
			temp+=str(x)
			temp+=','
		else:
			try:
				if x[0]==' ':
					x = x[1:]
			except:
				print ("lol")
			try:
				if x[0:4]=="http":
					t = x[0:4]+':'+x[4:]
					x = t
			except:
				print ("lol again")		
			try:
				if x[0:11]=="android-app":
					t = x[0:11]+':'+x[11:]
					x = t
			except:
				print ("lol again")		
			try:
				re.sub(' +','',x)
			except:
				print ("lol lol")	
			temp+=x
			temp+=','	
	temp=temp[:-1]	
	temp+="\n"
	globaltemp+=temp	
f.write(globaltemp)	






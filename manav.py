import search.models as sp
f = open("final2.txt","r")
l = f.readlines()
li = []
for x in l:
	li.append(x[:-1].split(','))
for x in li:
	try:
		x[4] = int(x[4])
		x[6] = int(x[6])
		x[14] = int(x[14])
	except:
		print ("Maa chuda tu")
cnt = 0
for i in range(len(li)):
	if len(li[i])==18:
		cnt+=1
		a = sp.ProductInformation(cnt,li[i][0],li[i][1],li[i][2],li[i][3],li[i][4],li[i][5],li[i][6],li[i][7],li[i][8],li[i][9],li[i][10],li[i][11],li[i][12],li[i][13],li[i][14],li[i][15],li[i][16],li[i][17])
		a.save()
	else:
		print(i)
import time
f = open("C:\\Users\\ADMIN\\Desktop\\testcube2801a.gcode","r")
lines = f.readlines()
f2 = open("C:\\Users\\ADMIN\\Desktop\\testcube2801b.gcode","r")
lines2 = f2.readlines()
f.close
f2.close
f3 = open("C:\\Users\\ADMIN\\Desktop\\mix1.gcode","w")
f3.write("")
f3 = open("C:\\Users\\ADMIN\\Desktop\\mix1.gcode","a")
#change youself to your value
retract=5 #retraction amount
firstlayer = 0.2
height=0.2

#temp value
maxz=0
stringreplace=""
eValue11=0.00001
eValue21=eValue11
eValue12=eValue21
eValue22=eValue21
eValue13=eValue11
eValue23=eValue11
eValueold=eValue11
layer=2
linenum=0   
linenum2=0
linenum3=0
zlimit1=0
zlimit2=0
zlimit3=0
zlimit4=0
if firstlayer==0.2:
    zlimit1 =round(height*layer-(height/2),1)
    zlimit2 =round(height*layer,1)
    zlimit3 =round(height*layer+(height/2),1)
    zlimit4 =round(height*(layer+1),1)
else:
    zlimit1 =round(height*layer,1)
    zlimit2 =round(height*layer+(height/2),1)
    zlimit3 =round(height*(layer+1),1)
    zlimit4 =round(height*(layer+1)+(height/2),1)
# if firstlayer==0.2:
#     txt1 ="Z"+str(round(height*layer-(height/2),1))
#     txt2 ="Z"+str(round(height*layer,1))
# else:
#     txt1 ="Z"+str(round(height*layer,1))
#     txt2 ="Z"+str(round(height*layer+(height/2),1))
txt1 = "Z"+ str(zlimit1)
txt2 = "Z"+ str(zlimit2)


#find maxZ
linenum=0
while lines[linenum].find("MAXZ")==-1:
    linenum+=1
arrayXYE = lines[linenum].split(":")
maxz = float(arrayXYE[1])


#copy first layer frome file 0.2
for linenum in range (0,len(lines)):
    if lines[linenum+2].find(txt2)==-1:
        if (lines[linenum].find("E")!=-1 and lines[linenum][0]=="G"):
            arrayXYE = lines[linenum].split()
            indexx=len(arrayXYE)-1
            eValue11 = float(arrayXYE[indexx][1:len(arrayXYE[indexx]):1])
        f3.write(lines[linenum])
    else:
        break
eValueold = eValue11
# f3.write("---------Endfuntion1Pohuc----------\n")

#find next z in file 0.1
while lines2[linenum2+3].find(txt1)==-1:
    if (lines2[linenum2].find("E")!=-1 and lines2[linenum2][0]=="G"):
        arrayXYE = lines2[linenum2].split()
        eValue21 = float(arrayXYE[len(arrayXYE)-1][1:len(arrayXYE[len(arrayXYE)-1]):1]) 
    linenum2+=1

f3.write(lines2[linenum2]) #position before move Z +0.1
linenum2+=3
f3.write(lines2[linenum2]) #Z +0.1 line
linenum2+=1

#find last Etru Value in file 0.1
linenum3=linenum2
while lines2[linenum3].find("E")==-1 or lines2[linenum3][0]!="G" or lines2[linenum3].find("X")==-1:
    linenum3-=1
arrayXYE = lines2[linenum3].split()    
indexw = len(arrayXYE)-1
eValue21= float(arrayXYE[indexw][1:len(arrayXYE[indexw]):1])

# copy file 0.1 , stop at Z0.4
while lines2[linenum2+2].find(txt2)==-1:
    if  lines2[linenum2].find("TIME")>-1 : #lines2[linenum2].find("LAYER")>-1 or
        linenum2+=1
        continue
    if lines2[linenum2].find("M106")>-1:
        linenum2+=1
    if (lines2[linenum2].find("E")!=-1 and lines2[linenum2][0]=="G"):
        arrayXYE = lines2[linenum2].split()
        indexx=len(arrayXYE)-1
        eValue22 = float(arrayXYE[indexx][1:len(arrayXYE[indexx]):1])
        eValue22=round(eValue22-eValue21+eValueold,5)
        stringreplace = lines2[linenum2][0:lines2[linenum2].find(" E")+2:1]
        stringreplace = stringreplace + str(eValue22) + "\n" #+" ;F1 "+str(linenum2)
        f3.write(stringreplace)            
    else: f3.write(lines2[linenum2])
    linenum2+=1
eValueold=eValue22
# f3.write("---------Endfuntion2Pohuc----------\n")
######################
######################
######################

while(1):
    if (height*layer>maxz-(height*2)):break
    # if firstlayer==0.2:
    #     txt2 ="Z"+str(round(height*layer,1))
    #     txt3 ="Z"+str(round(height*layer+(height/2),1))
    #     txt4 ="Z"+str(round(height*(layer+1),1))
    # else: 
    #     txt2 ="Z"+str(round(height*layer+(height/2),1))
    #     txt3 ="Z"+str(round(height*(layer+1),1))
    #     txt4 ="Z"+str(round(height*(layer+1)+(height/2),1))
    zlimit2+=height
    zlimit3+=height
    zlimit4+=height
    txt2="Z"+str(round(zlimit2,1))
    txt3="Z"+str(round(zlimit3,1))
    txt4="Z"+str(round(zlimit4,1))
    txt5 = str(txt2)
    print (txt2,txt3,txt4,txt5)
    if (txt2[len(txt2)-1]=="0"): txt2 = txt2[0:len(txt2)-2:1]
    if (txt3[len(txt3)-1]=="0"): txt3 = txt3[0:len(txt3)-2:1]
    if (txt4[len(txt4)-1]=="0"): txt4 = txt4[0:len(txt4)-2:1]
    
    
    
    # if retract
    if 54950>linenum>54800: print(linenum,lines[linenum])
    if (lines[linenum].find("E")!=-1 and lines[linenum][0]=="G"):
        arrayXYE = lines[linenum].split()
        stringreplace = lines[linenum][0:lines[linenum].find(" E")+2:1]
        stringreplace = stringreplace + str(eValueold-retract)+ "\n"
        f3.write(stringreplace)
        eValueold-=retract
    else:linenum+=1
    linenum+=1

    #copy Z0.2 without X Y
    if lines[linenum].find("Z")==-1:
        linenum+=1
    while lines[linenum].find("Z")==-1:
        linenum-=1
    
    arrayXYE = lines[linenum].split()
    stringreplace = arrayXYE[0]+" "+arrayXYE[1]+" "+arrayXYE[len(arrayXYE)-1]+"\n"
    f3.write(stringreplace)
    linenum+=1

    #find last Etru Value
    linenum3=linenum
    while lines[linenum3].find("E")==-1 or lines[linenum3][0]!="G" : #or lines[linenum3].find("X")==-1
        linenum3-=1
    arrayXYE = lines[linenum3].split()    
    indexw = len(arrayXYE)-1
    eValue11= float(arrayXYE[indexw][1:len(arrayXYE[indexw]):1])
    # eValueold=eValue11

    #copy all from 0.2 file, stop befor Z0.6, skip outer lines
    while lines[linenum+2].find(txt4)==-1 :
        if 54950>linenum>54800: print(linenum,lines[linenum])
        if lines[linenum].find(txt4)!=-1 :
            break
        if lines[linenum].find("G92 E0")!=-1 : 
            eValueold=0
            eValue11=0
            f3.write(lines[linenum])
            linenum+=1
            continue
        #when meet outer, find next line type
        if lines[linenum+1].find("OUTER")!=-1:
            linenum+=2
            eValueold=eValue12
            while lines[linenum].find("SKIN")==-1 and lines[linenum].find("FILL")==-1 and lines[linenum].find("INNER")==-1 and lines[linenum][0]=="G": 
                if (lines[linenum].find("E")!=-1 and lines[linenum][0]=="G" and lines[linenum].find("X")!=-1)  :
                    arrayXYE = lines[linenum].split()
                indexx=len(arrayXYE)-1
                eValue11 = float(arrayXYE[indexx][1:len(arrayXYE[indexx]):1])
                linenum+=1
           
            while lines[linenum-1].find("E")==-1 or lines[linenum-1][0]!="G":
                linenum-=1
            if 54950>linenum>54800: print(linenum,lines[linenum])
            while lines[linenum-1].find("X")==-1 or lines[linenum-1].find("E")==-1:
                linenum-=1
            while lines[linenum+2].find("Z")!=-1 and lines[linenum+2][0]=="G":
                linenum+=1
            # f3.write("------AFTER-OUTER--------\n")
            if 54950>linenum>54800: print(linenum,lines[linenum])
        if (lines[linenum].find("E")!=-1 and lines[linenum][0]=="G"):
            arrayXYE = lines[linenum].split()
            indexx=len(arrayXYE)-1
            eValue12 = float(arrayXYE[indexx][1:len(arrayXYE[indexx]):1])
            eValue12=round(eValue12-eValue11+eValueold,5)
            stringreplace = lines[linenum][0:lines[linenum].find(" E")+2:1]
            stringreplace = stringreplace + str(eValue12)+ "\n"
            f3.write(stringreplace)
        else: f3.write(lines[linenum])
        linenum+=1
        if linenum>32000 : 
            print (linenum)
            time.sleep(0.5)
    eValueold=eValue12
    # f3.write("---------Endfuntion3Pohuc----------\n")

    #copy 0.4 outer, and 0.5 outer
    if linenum>32000 : 
            print (linenum2)
    if (height*layer<=maxz):
        #find last Etru value
        linenum3=linenum2
        while lines2[linenum3].find("E")==-1 or lines2[linenum3][0]!="G" or lines2[linenum3].find("X")==-1:
            linenum3-=1
        arrayXYE = lines2[linenum3].split()    
        indexw = len(arrayXYE)-1
        eValue21= float(arrayXYE[indexw][1:len(arrayXYE[indexw]):1])
        #copy 0.4 outer, and 0.5 outer
        isZHop = False
        while lines2[linenum2+2].find(txt4)==-1 or isZHop==True:
            if lines2[linenum2].find("LAYER")>-1 or lines2[linenum2].find("TIME")>-1:
                linenum2+=1
                continue
            if lines2[linenum2].find(txt5)>-1 and lines2[linenum2-2].find(txt4)==-1:
                linenum2+=1
                continue
            
            if (lines2[linenum2].find("E")!=-1 and lines2[linenum2][0]=="G"):
                arrayXYE = lines2[linenum2].split()
                indexx=len(arrayXYE)-1
                eValue22 = float(arrayXYE[indexx][1:len(arrayXYE[indexx]):1])
                eValue23=eValue22
                eValue22=round(eValue22-eValue21+eValueold,5)
                stringreplace = lines2[linenum2][0:lines2[linenum2].find(" E")+2:1]
                stringreplace = stringreplace + str(eValue22)+ "\n"
                f3.write(stringreplace)
            else: 
                f3.write(lines2[linenum2])
            linenum2+=1
            
            if lines2[linenum2+2].find(txt4)!=-1 and lines2[linenum2+4].find(txt4)!=-1:
                isZHop=True
            if lines2[linenum2-1].find(txt4)!=-1 and lines2[linenum2-3].find(txt4)!=-1:
                isZHop=False
            if lines2[linenum2+2].find(txt4)!=-1 and lines2[linenum2+3].find(txt4)!=-1:
                isZHop=True
            if lines2[linenum2-1].find(txt4)!=-1 and lines2[linenum2-2].find(txt4)!=-1:
                isZHop=False
        isZHop = False
        # f3.write("---------Endfuntion4Pohuc----------\n")
        # print("qwqwqwqw",linenum2,lines2[linenum2])
    eValueold=eValue22
    #increase layer, back again
    layer+=1


#copy top layer from 0.1 file
linenum3=linenum2
while lines2[linenum3].find("E")==-1 or lines2[linenum3][0]!="G":
    linenum3-=1
arrayXYE = lines2[linenum3].split()    
indexw = len(arrayXYE)-1
eValue11= float(arrayXYE[indexw][1:len(arrayXYE[indexw]):1])
for i in range(linenum2+1,len(lines2)-1):
    if lines2[i].find("LAYER")>-1 or lines2[i].find("TIME")>-1:
        i+=1
        continue
    if (lines2[i].find("E")!=-1 and lines2[i][0]=="G"):
            arrayXYE = lines2[i].split()
            indexx=len(arrayXYE)-1
            eValue22 = float(arrayXYE[indexx][1:len(arrayXYE[indexx]):1])
            eValue22=round(eValue22-eValue21+eValueold,5)
            stringreplace = lines2[i][0:lines2[i].find(" E")+2:1]
            stringreplace = stringreplace + str(eValue22)+ "\n"
            f3.write(stringreplace)
    else: 
        f3.write(lines2[i])
    
exit


import math
from tkinter import ttk
from tkinter import *
import tkinter.font as tkFont
from sys import exec_prefix, is_finalizing
from typing import ClassVar
import serial.tools.list_ports
import serial
import csv
import os
from _thread import start_new_thread as snt
from time import sleep
import pygame


pygame.mixer.init()
pygame.mixer.music.load("callbuttonbeep.mp3")



class GetPort_SerialData:
    

    csvdata = []
    global connection

    def ports():
        try:

            ports = list(serial.tools.list_ports.comports())
            if ports:
                for p in ports:
                    print(p.vid,p.pid)
                
                    
                    if p.vid == 4292 and p.pid == 60000 or p.vid == 1240 and p.pid==61336:
                        global vid, pid, device
                        vid = p.vid
                        pid = p.pid
                        device = p.device
                        GetPort_SerialData.connection=1
                    else:
                        print("print")
                        GetPort_SerialData.connection=0    
            else:
                    print("no")
                    GetPort_SerialData.connection=0
            

               
        except:
            print("connect")    
            GetPort_SerialData.connection=0       
                

    def readcsv():

        with open(os.getcwd()+'/carecalldata.csv', 'rt')as f:
            data = csv.reader(f)
            for row in data:
                x.csvdata.append(row)
            # snt(x.readserial,())
            # snt(y.display_card,())

    def readserial():
        # snt(y.display_card,())
        

        while True:
            try:
                global exec,ser
                exec = 0
                ser = serial.Serial()
                ser.baudrate = 9600
                ser.port = device
                ser.bytesize = 8
                ser.open()
                ser.timeout = 1
                GetPort_SerialData.connection=1

                sleep(1)
                exec = 0
                ser_bytes = ser.readline().decode("utf-8")
                
                if(len(ser_bytes) > 1):

                    #  for  value in ser_bytes:
                    splitdata = ser_bytes.split("<")
                    splitdata = splitdata[1].split(">")
                    ser_bytes = splitdata[1]
                    splitdata = splitdata[1].split("-")
                    for value in x.csvdata:
                        
                        for datas in value:
                            csvdatas = datas.split("-")
                           
                            if splitdata[0] == csvdatas[1]:
                                # print(csvdatas[1])

                                call = splitdata[2]
                                
                                if call == 'C':
                                    print(ackdata,"callC",splitdata[0])
                                    
                                    
                                    if len(ackdata)>0:
                                        
                                        
                                        if not any(d['deviceid'] == splitdata[0]  for d in ackdata):
                                           
                                                
                                            
                                            x.checkacktxdata(splitdata[0])
                                            ackdata.append({"deviceid":splitdata[0],"ack":"ack"})
                                            # else:
                                            #     print("none")    
                                            msg=splitdata[0]+"-0-ack"                
                                            ser.write(msg.encode("ascii")) 
                                            print(ackdata,"not in list--------------------",splitdata[0])
                                            x.checkdeletedata(splitdata[0])
                                            x.checkackdata(splitdata[0])
                                            x.checkcalldata(splitdata[0])
                                            rxdata.insert(
                                                0, {"deviceid": splitdata[0], "calltype": splitdata[2], "batterypercent": splitdata[5], "newcall": splitdata[4], "bedname": csvdatas[2],"location": csvdatas[3],"ack":"ack","ackstat":"n"})
                                            pygame.mixer.music.play(loops=0)
                                        else:
                                            
                                            x.checkackvaluedata(splitdata[0],splitdata[2], splitdata[5], splitdata[4],csvdatas[2], csvdatas[3])
                                            
                                              
                                    else:
                                        
                                        ackdata.append({"deviceid":splitdata[0],"ack":"ack"})                
                                        msg=splitdata[0]+"-0-ack"                
                                        ser.write(msg.encode("ascii"))
                                        # x.ackvalue="ack"
                                        
                                        x.checkdeletedata(splitdata[0])
                                        x.checkackdata(splitdata[0])
                                        x.checkcalldata(splitdata[0])
                                        rxdata.insert(
                                            0, {"deviceid": splitdata[0], "calltype": splitdata[2], "batterypercent": splitdata[5], "newcall": splitdata[4], "bedname": csvdatas[2],"location": csvdatas[3],"ack":"ack","ackstat":"n"})
                                        pygame.mixer.music.play(loops=0)
                                        
                                elif call == 'A':
                                    
                                    x.checkdeletedata(splitdata[0])
                                    x.checkcalldata(splitdata[0])
                                    x.checkackdata(splitdata[0])
                                    rxdata.append(
                                        {"deviceid": splitdata[0], "calltype": splitdata[2], "batterypercent": splitdata[5], "newcall": splitdata[4], "bedname": csvdatas[2],"location": csvdatas[3],"ack":"ack"})
                                    
                                    msg=splitdata[0]+"-0-ack"
                                    
                                    ser.write(msg.encode("ascii"))
                                    try:
                                        for d in ackdata:

                                                
                                                if splitdata[0] in d.values():
                                                    d['ack']="ack"
                                    except StopIteration:
                                        None
                                                    
                                elif call == 'D':
                                    x.checkackdata(splitdata[0])
                                    x.checkcalldata(splitdata[0])
                                    x.checkdeletedata(splitdata[0])
                                    rxdata.append(
                                        {"deviceid": splitdata[0], "calltype": splitdata[2], "batterypercent": splitdata[5], "newcall": splitdata[4], "bedname": csvdatas[2],"location": csvdatas[3],"ack":"ack","ackstat":"n"})
                                    
                                    msg=splitdata[0]+"-0-ack"
                                    
                                    ser.write(msg.encode("ascii"))

                                    try:
                                        for d in ackdata:

                                                
                                                if splitdata[0] in d.values():
                                                    d['ack']="ack"
                                    except StopIteration:
                                        None

            except:
                # ser.close()
                # GetPort_SerialData.connection=0
                
                x.ports()
                sleep(1)
                
                

                # while vid != 4292 and pid != 60000:
                #     x.ports()
                #     x.readcsv()
                #     y.display_card()
                    

                print("Check Connection",)
    

    def checkdeletedata(deviceid):

        try:
            value = next(i for i, item in enumerate(rxdata)
                         if item["deviceid"] == deviceid)
                        

            for d in rxdata:

                if d['calltype'] == 'D' and d['deviceid']==deviceid:
                    rxdata.remove(rxdata[value])
                    

        except StopIteration:
            None

    def checkackdata(deviceid):

        try:
            # to get position in dictionary
            value = next(i for i, item in enumerate(rxdata)
                         if item["deviceid"] == deviceid)
             

            for d in rxdata:

                if d['calltype'] == 'A' and d['deviceid']==deviceid:

                    rxdata.remove(rxdata[value])
                    

        except StopIteration:
            None

    def checkcalldata(deviceid):

        try:
            # to get position in dictionary
            value = next(i for i, item in enumerate(rxdata)
                         if item["deviceid"] == deviceid)
                        

            for d in rxdata:

                if d['calltype'] == 'C' and d['deviceid']==deviceid:

                    rxdata.remove(rxdata[value])
                   

        except StopIteration:
            None

    def checkacktxdata(deviceid):
        

        try:
        # to get position in dictionary
            value = next(i for i, item in enumerate(ackdata)
                            if item["deviceid"] == deviceid)
                         

            for d in ackdata:

                if d['calltype'] == 'C' and d['deviceid']==deviceid:

                    ackdata.remove(ackdata[value])
                    

        except StopIteration:
            None

    def checkackvaluedata(deviceid,calltype,batterypercent,newcall,bedname,location):
        

        try:
        # to get position in dictionary
            value = next(i for i, item in enumerate(ackdata)
                            if item["deviceid"] == deviceid)
                       

            for d in ackdata:
                

                if d['ack'] == 'ack' and d['deviceid']==deviceid:
                   

                    # ackdata[value].ack="ack"
                    d['ack']='ack'
                    
                    msg=deviceid+"-0-ack"
                    
                    ser.write(msg.encode("ascii"))
                    x.checkdeletedata(deviceid)
                    x.checkackdata(deviceid)
                    x.checkcalldata(deviceid)
                    rxdata.insert(
                            0, {"deviceid": deviceid, "calltype": calltype, "batterypercent": batterypercent, "newcall": newcall, "bedname": bedname,"location": location,"ack":"ack","ackstat":"n"})
                    pygame.mixer.music.play(loops=0)        
                    
                elif d['ack'] == 'ackT' and d['deviceid']==deviceid  :
                    
                    if newcall == '0':

                        d['ack']="ackT"
                       
                        msg=deviceid+"-0-ackT"   
                       
                        ser.write(msg.encode("ascii"))
                        x.checkdeletedata(deviceid)
                        x.checkackdata(deviceid)
                        x.checkcalldata(deviceid) 
                        rxdata.append(
                            {"deviceid": deviceid, "calltype": 'A', "batterypercent": batterypercent, "newcall": newcall, "bedname": bedname,"location": location,"ack":"ackT","ackstat":"n"})
                        

                    elif newcall == '1':
                        d['ack']="ack"
                        
                        msg=deviceid+"-0-ack"   
                        
                        ser.write(msg.encode("ascii"))
                        x.checkdeletedata(deviceid)
                        x.checkackdata(deviceid)
                        x.checkcalldata(deviceid) 
                        rxdata.append(
                            {"deviceid": deviceid, "calltype": 'C', "batterypercent": batterypercent, "newcall": newcall, "bedname": bedname,"location": location,"ack":"ack","ackstat":"y"})
                      
                        pygame.mixer.music.play(loops=0)


                # elif d['ack'] == 'ackT' and d['deviceid']==deviceid and newcall==1:

                    # d['ack']="ack"
                    # print(deviceid,value,"138")
                    # msg=deviceid+"-0-ack"   
                    # print(msg,"call2")
                    # ser.write(msg.encode("ascii"))
                    # x.checkdeletedata(deviceid)
                    # x.checkackdata(deviceid)
                    # x.checkcalldata(deviceid) 
                    # rxdata.insert(
                    #      0,{"deviceid": deviceid, "calltype": 'C', "batterypercent": batterypercent, "newcall": newcall, "bedname": bedname,"location": location,"ack":"ack"})
                    # print(rxdata)

        except StopIteration:
            
            None        



rxdata = []
ackdata =[]


class Display_Data:
    # global buttonstat
    
    def display_card():
        snt(GetPort_SerialData.readserial, ())
        
        # from tkinter import *
        # from tkinter import ttk
        # import math
        # from threading import *

        root = Tk()
        root.title('Evelabs Monitor')
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry("%dx%d" % (screen_width, screen_height))

        # create all of the main containers
        # top_frame = Frame(root, bg='grey', width=screen_width, height=20, pady=3).grid(row=0, sticky="ew")
        mainframe = Frame(root, bg='white', width=screen_width,
                          height=screen_height, padx=4, pady=4)
                          
        # btm_frame = Frame(root, bg='yellow', width=screen_width, height=10, pady=3).grid(row=3, sticky="ew")
        mainframe.pack(fill=BOTH, expand=1)
        # mainframe.pack()
        
        

        maincanvas = Canvas(mainframe,bg="white", width=screen_width,height=.9*screen_height)#main frame
        #maincanvas.pack(side=LEFT, fill=BOTH)
        maincanvas.pack(side=LEFT,anchor="s")
        

        # if GetPort_SerialData.connection == 1:


        #     largeframe = Frame(root,bg="green", width=screen_width,height=screen_height/2)#main frame
        #     #maincanvas.pack(side=LEFT, fill=BOTH)
        #     largeframe.pack(side=LEFT,anchor="n")
        #     largecanvas = Canvas(root,bg="green", width=screen_width,height=screen_height/2)#main frame
        #     #maincanvas.pack(side=LEFT, fill=BOTH)
        #     largecanvas.pack(side=LEFT,anchor="n")

        # elif GetPort_SerialData.connection == 0:
        #     largeframe = Frame(root,bg="red", width=screen_width,height=screen_height/2)#main frame
        #     #maincanvas.pack(side=LEFT, fill=BOTH)
        #     largeframe.pack(side=LEFT,anchor="n")
        #     largecanvas = Canvas(root,bg="red", width=screen_width,height=screen_height/2)#main frame
        #     #maincanvas.pack(side=LEFT, fill=BOTH)
        #     largecanvas.pack(side=LEFT,anchor="n")

        scrlbar = ttk.Scrollbar(
            mainframe, orient=VERTICAL, command=maincanvas.yview)
        scrlbar.pack(side=RIGHT, fill=Y)

        maincanvas.configure(yscrollcommand=scrlbar.set)
        maincanvas.bind('<Configure>', lambda e: maincanvas.configure(
            scrollregion=maincanvas.bbox("all")))

        secondaryframe = Frame(maincanvas)
        maincanvas.create_window((0, 0), window=secondaryframe, anchor="nw")
        

        secondarycanvas = Canvas(secondaryframe)#set card border color
        
        secondarycanvas.pack(side=LEFT, fill=BOTH, expand=1)

        # parsing classes
        # sixthFrame = Canvas(secondarycanvas,bg="red" ,width=screen_width,
        #                               height=screen_height/20, bd=0,highlightthickness=0).grid(row=0, column=0,padx=0,pady=0,sticky='s' )
        # topLabel = Label(secondarycanvas, text=f"CARE CALL", fg="#979797", bg='red').grid(
        #                 row=0, column=0, pady=30, padx=5, sticky="n")
       
        
               
       
        largecanvas = Canvas(root,bg="white", width=screen_width,height=.1*screen_height)
               
        largecanvas.pack(side=LEFT,anchor="n")
      

        while TRUE:

            # room_num = [{'John': 4, 'Liz': 4, 'Isaac': 345},{'John': 1, 'Liz': 1, 'Isaac': 345},{'John': 2, 'Liz': 2, 'Isaac': 345},{'John': 5, 'Liz': 5, 'Isaac': 345},{'John': 6, 'Liz': 6, 'Isaac': 345},{'John': 1, 'Liz': 1, 'Isaac': 345},{'John': 2, 'Liz': 2, 'Isaac': 345},{'John': 1, 'Liz': 1, 'Isaac': 345},{'John': 2, 'Liz': 2, 'Isaac': 345},{'John': 1, 'Liz': 1, 'Isaac': 345},{'John': 2, 'Liz': 2, 'Isaac': 345},{'John': 1, 'Liz': 1, 'Isaac': 345},{'John': 2, 'Liz': 2, 'Isaac': 345},{'John': 1, 'Liz': 1, 'Isaac': 345},{'John': 2, 'Liz': 2, 'Isaac': 345},{'John': 1, 'Liz': 1, 'Isaac': 345},{'John': 2, 'Liz': 2, 'Isaac': 345}]

            
            room_num = rxdata
            print(room_num)
            roomlength = len(room_num)
         
            if roomlength == 4:
                rows = 0
            else:
                rows = math.trunc(roomlength/4)
            reminder = roomlength % 4

            

            if GetPort_SerialData.connection == 1:
                

                # largeframe = Frame(root,bg="green", width=screen_width,height=screen_height/2)#main frame
                #maincanvas.pack(side=LEFT, fill=BOTH)
                
                newLabel = Label(largecanvas, text=f"CARE CALL", fg="#979797", bg='green',width=screen_width).grid(
                        row=0, column=1, pady=0, padx=0, sticky="n")

                # largeframe.pack(side=LEFT,anchor="n")
                
                # largecanvas = Canvas(root,bg="green", width=screen_width,height=screen_height/2)#main frame
                # #maincanvas.pack(side=LEFT, fill=BOTH)
                # largecanvas.pack(side=LEFT,anchor="n")

            elif GetPort_SerialData.connection == 0:
              
                newLabel = Label(largecanvas, text=f"CARE CALL", fg="red", bg='red' ,width=screen_width).grid(
                        row=0,  column=1, pady=0, padx=0, sticky="n")
                # largecanvas.pack(side=LEFT,anchor="s")
                # largecanvas.delete
                # largeframe.destroy
                
                # largeframe.configure(bg="red")
            
            

            if roomlength == 0:
                # print("null")
                sleep(1.5)
                # img=PhotoImage(file='justanimage.jpg')
                # tertiaryFrame=Label(root,image=img).pack()
                

                tertiaryFrame = Canvas(secondarycanvas,bg="white" ,width=screen_width/4,
                                      height=screen_height/4, bd=0,highlightthickness=0).grid(row=0, column=0,padx=0,pady=0 )

                
                root.update()
            elif rows == 0 and roomlength >0:
                # print("row=1",rxdata, "228")
                
                for x in range(roomlength):
                    # print(x,"row2")
                    # if room_num[x].calltype != 'D' :
                    titlefontStyle = tkFont.Font(
                        family="Roboto", size=18, weight="bold")
                    callfontstyle = tkFont.Font(
                        family="Roboto", size=20, weight="bold")
                    locationfont=tkFont.Font(
                        family="Roboto", size=14, weight="bold")
                    buttonfont = tkFont.Font(family="Roboto", size=10)

                    tertiaryFrame = Canvas(secondarycanvas, bg='#fafafa', width=screen_width/4,
                                          height=screen_height/4,bd=3,relief="groove").grid(row=0, column=x)

                    topLabel = Label(secondarycanvas, text=f"CARE CALL", fg="#979797", bg='#fafafa', font=titlefontStyle).grid(
                        row=0, column=x, pady=30, padx=5, sticky="n")
                    
                    if room_num[x].get('calltype') == 'C':
                        
                       
                         
                        

                        def buttonclick(deviceid,x,calltype,batterypercent,newcall,bedname,location):    #button click function
                            print(room_num[x].get('deviceid'),"button click",x)
                            
                            # global  buttonstat
                            
                            
                            
                            print(ackdata,"beforeloopack")
                            for d in ackdata:

                        
                                if deviceid in d.values():
                                    
                                    print(ackdata,"ackdata")
                                    if deviceid == d["deviceid"]:
                                        d['ack']="ackT"
                                        print(d['ack'],deviceid,ackdata,"buttonclick")
                                        msg=deviceid+"-0-ackTbuttonstat"
                                        print(msg)
                                        # print(d,"buttontx",deviceid)
                                        ser.write(msg.encode("ascii"))

                            
                           
                            
                            
                            GetPort_SerialData.checkcalldata(
                            deviceid)
                            rxdata.insert(
                            0, {"deviceid": deviceid, "calltype": calltype, "batterypercent": batterypercent, "newcall": newcall, "bedname": bedname,"location": location,"ack":"ack","ackstat":"y"})
                            
                        
                            
                            tertiaryFrame = Canvas(secondarycanvas,bg='white' ,width=screen_width/4,
                                    height=screen_height/4, bd=4,highlightthickness=0).grid(row=0, column=x,padx=0,pady=0 ) 
                            
                        
                        
                        midLabel = Label(secondarycanvas, text=f"{room_num[x].get('bedname')}", fg="#eb5757", bg='#fafafa', font=callfontstyle).grid(
                            row=0, column=x, pady=80, padx=5, sticky="n")
                        locationLabel = Label(secondarycanvas, text=f"{room_num[x].get('location')}", fg="#979797", bg='#fafafa', font=locationfont).grid(
                            row=0, column=x, pady=90, padx=5, sticky="s")
                    
                       
                        if room_num[x].get('ackstat') == 'y':
                            btn=Button(secondarycanvas, text="  Acknowledged ", fg="white", bg="#f2c94c",activebackground="#eb5757", font=buttonfont ,command=(lambda x=x: buttonclick(room_num[x].get('deviceid'),x,room_num[x].get('calltype'),room_num[x].get('batterypercent'),room_num[x].get('newcall'),room_num[x].get('bedname'),room_num[x].get('location'))))
                            
                            btn.grid(
                                row=0, column=x, pady=30, padx=5, sticky="s")   
                        else:         
                            btn=Button(secondarycanvas, text="  Acknowledge ", fg="white", bg="#eb5757",activebackground="#eb5757", font=buttonfont ,command=(lambda x=x: buttonclick(room_num[x].get('deviceid'),x,room_num[x].get('calltype'),room_num[x].get('batterypercent'),room_num[x].get('newcall'),room_num[x].get('bedname'),room_num[x].get('location'))))
                            
                            btn.grid(
                                row=0, column=x, pady=30, padx=5, sticky="s") 
                       

                        
                        
                            
                           
                           
                    # elif room_num[x].get('calltype') == 'D':
                    #     midLabel = Label(secondarycanvas, text=f"{room_num[x].get('bedname')}", fg="#f2c94c", bg='#fafafa', font=callfontstyle).grid(
                    #         row=0, column=x, pady=80, padx=5, sticky="n")
                    #     locationLabel = Label(secondarycanvas, text=f"{room_num[x].get('location')}", fg="grey", bg='#fafafa', font=locationfont).grid(
                    #         row=0, column=x, pady=90, padx=5, sticky="s")
                    #     Button(secondarycanvas, text=f"  Cancelled  ", fg="black", bg="yellow", font=buttonfont).grid(
                    #         row=0, column=x, pady=30, padx=5, sticky="s")
                        
                    # elif room_num[x].get('calltype') == 'A':
                    #     midLabel = Label(secondarycanvas, text=f"{room_num[x].get('bedname')}", fg="#f2c94c", bg='#fafafa', font=callfontstyle).grid(
                    #         row=0, column=x, pady=80, padx=5, sticky="n")
                    #     locationLabel = Label(secondarycanvas, text=f"{room_num[x].get('location')}", fg="grey", bg='#fafafa', font=locationfont).grid(
                    #         row=0, column=x, pady=90, padx=5, sticky="s")
                    #     Button(secondarycanvas, text=f"  Acknowledged  ", fg="black", bg="yellow", font=buttonfont).grid(
                    #         row=0, column=x, pady=30, padx=5, sticky="s")
                    
                    

                    if room_num[x].get('calltype') == 'D':
                        
                        GetPort_SerialData.checkdeletedata(
                            room_num[x].get('deviceid'))
                           
                        tertiaryFrame = Canvas(secondarycanvas,bg="white" ,width=screen_width/4,
                                      height=screen_height/4, bd=4,highlightthickness=0).grid(row=0, column=x,padx=0,pady=0 )  
                                                    
                        
                        
                       
                    elif room_num[x].get('calltype') == 'A':
                        
                        GetPort_SerialData.checkackdata(
                            room_num[x].get('deviceid'))
                        
                        tertiaryFrame = Canvas(secondarycanvas,bg="white" ,width=screen_width/4,
                                      height=screen_height/4, bd=4,highlightthickness=0).grid(row=0, column=x,padx=0,pady=0 )    

                        
                    
                sleep(1)

                root.update()

                # else:
                #     None
              
            else:
                try:
                    for y in range(rows):
                        for x in range(4):
                            for n in range(reminder):
                                r = math.floor(x/4)

                                def buttonclk(deviceid,x,y,n,calltype,batterypercent,newcall,bedname,location):    #button click function
                                         # print(room_num[x].get('deviceid'),"button click",x)
                                    print(deviceid,"buttonclk",x,y,n,)

                                    for d in ackdata:

                                
                                        if deviceid in d.values():
                                            print(ackdata,"ackdata")
                                            if deviceid == d["deviceid"]:
                                                d['ack']="ackT"
                                                print(d['ack'],deviceid,ackdata,"buttonclk")
                                                msg=deviceid+"-0-ackT"
                                                print(msg)
                                                # print(d,"buttontx",deviceid)
                                                # ser.write(msg.encode("ascii"))

                                    
                                
                                    
                                    
                                    GetPort_SerialData.checkcalldata(
                                    deviceid)  
                                    rxdata.insert(
                                        0, {"deviceid": deviceid, "calltype": calltype, "batterypercent": batterypercent, "newcall": newcall, "bedname": bedname,"location": location,"ack":"ack","ackstat":"y"})
                                    tertiaryFrame = Canvas(secondarycanvas,bg="white" ,width=screen_width/4,
                                            height=screen_height/4, bd=4,highlightthickness=0).grid(row=y, column=x,padx=0,pady=0 )
                                    tertiaryFrame = Canvas(secondarycanvas,bg="white" ,width=screen_width/4,
                                                height=screen_height/4, bd=4,highlightthickness=0).grid(row=5, column=n,padx=0,pady=0 )
                                              
                                                
                                tertiaryFrame = Canvas(secondarycanvas,bg="white" ,width=screen_width/4,
                                            height=screen_height/4, bd=4,highlightthickness=0).grid(row=y, column=x,padx=0,pady=0 )
                                tertiaryFrame = Canvas(secondarycanvas,bg="white" ,width=screen_width/4,
                                            height=screen_height/4, bd=4,highlightthickness=0).grid(row=5, column=x,padx=0,pady=0 )
                                # print(rows, 246)

                                
                                if room_num[(4*y)+x].get('calltype') == 'C':
                                    


                                    tertiaryFrame = Frame(secondarycanvas, bg='#fafafa', width=screen_width/4,
                                                        height=screen_height/4, bd=3,relief="groove").grid(row=y, column=x, pady=4, padx=4)

                                    topLabel = Label(secondarycanvas, text=f"CARECALL", fg="black", bg='#fafafa',font=titlefontStyle).grid(
                                        row=y, column=x, pady=30, padx=5, sticky="n")

                                        
                                    midLabel = Label(secondarycanvas, text=f"{room_num[(4*y)+x].get('bedname')} ",fg="#eb5757", bg='#fafafa', font=callfontstyle).grid(
                                        row=y, column=x, pady=70, padx=5, sticky="n")

                                    locationLabel = Label(secondarycanvas, text=f"{room_num[(4*y)+x].get('location')}", fg="#979797", bg='#fafafa', font=locationfont).grid(
                                    row=y, column=x, pady=90, padx=5, sticky="s")    
                                    
                                    if room_num[x].get('ackstat') == 'y':
                                        Button(secondarycanvas, text=f"Acknowledged {(4*y)+x}",fg="white", bg="#f2c94c",font=buttonfont ,command=(lambda x=x: buttonclk(room_num[(4*y)+x].get('deviceid'),x,y,n,room_num[(4*y)+x].get('calltype'),room_num[(4*y)+x].get('batterypercent'),room_num[(4*y)+x].get('newcall'),room_num[(4*y)+x].get('bedname'),room_num[(4*y)+x].get('location')))).grid(
                                                    row=y, column=x, pady=30, padx=5, sticky="s") 
                                    else:         
                                        Button(secondarycanvas, text=f"Acknowledge {(4*y)+x}",fg="white", bg="#eb5757",font=buttonfont ,command=(lambda x=x: buttonclk(room_num[(4*y)+x].get('deviceid'),x,y,n,room_num[(4*y)+x].get('calltype'),room_num[(4*y)+x].get('batterypercent'),room_num[(4*y)+x].get('newcall'),room_num[(4*y)+x].get('bedname'),room_num[(4*y)+x].get('location')))).grid(
                                        row=y, column=x, pady=30, padx=5, sticky="s")
                                                # Button(secondarycanvas, text=f"Acknowledge {(4*y)+x}",fg="white", bg="#eb5757",font=buttonfont ,command=(lambda x=x: buttonclk(room_num[(4*y)+x].get('deviceid'),x,y,n,room_num[(4*y)+x].get('calltype'),room_num[(4*y)+x].get('batterypercent'),room_num[(4*y)+x].get('newcall'),room_num[(4*y)+x].get('bedname'),room_num[(4*y)+x].get('location')))).grid(
                                                #     row=y, column=x, pady=30, padx=5, sticky="s")

                                if room_num[(4*y)+x].get('calltype') == 'D':   
                                    GetPort_SerialData.checkdeletedata(
                                    room_num[(4*y)+x].get('deviceid'))
                                
                                    tertiaryFrame = Canvas(secondarycanvas,bg="white" ,width=screen_width/4,
                                            height=screen_height/4, bd=4,highlightthickness=0).grid(row=y, column=x,padx=0,pady=0 )


                                if room_num[(4*y)+x].get('calltype') == 'A':   
                                    GetPort_SerialData.checkackdata(
                                    room_num[(4*y)+x].get('deviceid'))
                                
                                    tertiaryFrame = Canvas(secondarycanvas,bg="white" ,width=screen_width/4,
                                            height=screen_height/4, bd=4,highlightthickness=0).grid(row=y, column=x,padx=0,pady=0 )






                                if room_num[n+(rows*4)].get('calltype') == 'C':
                                    fourthFrame = Frame(secondarycanvas, bg='#fafafa', width=screen_width/4,
                                                        height=screen_height/4, bd=3,relief="groove").grid(row=5, column=n, pady=3, padx=3)

                                    topLabel = Label(secondarycanvas, text=f"CARECALL", fg="black", bg='#fafafa',font=titlefontStyle).grid(
                                        row=5, column=n, pady=30, padx=5, sticky="n")
                                    midLabel = Label(secondarycanvas, text=f"{room_num[n+(rows*4)].get('bedname')} ",fg="#eb5757", bg='#fafafa', font=callfontstyle).grid(
                                        row=5, column=n, pady=70, padx=5, sticky="n")
                                    locationLabel = Label(secondarycanvas, text=f"{room_num[n+(rows*4)].get('location')}", fg="#979797", bg='#fafafa', font=locationfont).grid(
                                    row=5, column=n, pady=90, padx=5, sticky="s") 
                                    if room_num[x].get('ackstat') == 'y':
                                        Button(secondarycanvas, text=f"Acknowledged {n+(rows*4)}",fg="white", bg="#f2c94c",font=buttonfont ,command=(lambda n=n: buttonclk(room_num[n+(rows*4)].get('deviceid'),x,y,n,room_num[n+(rows*4)].get('calltype'),room_num[n+(rows*4)].get('batterypercent'),room_num[n+(rows*4)].get('newcall'),room_num[n+(rows*4)].get('bedname'),room_num[n+(rows*4)].get('location')))).grid(
                                        row=5, column=n, pady=30, padx=5, sticky="s")

                                    else:         
                                        Button(secondarycanvas, text=f"Acknowledge {n+(rows*4)}",fg="white", bg="#eb5757",font=buttonfont ,command=(lambda n=n: buttonclk(room_num[n+(rows*4)].get('deviceid'),x,y,n,room_num[n+(rows*4)].get('calltype'),room_num[n+(rows*4)].get('batterypercent'),room_num[n+(rows*4)].get('newcall'),room_num[n+(rows*4)].get('bedname'),room_num[n+(rows*4)].get('location')))).grid(
                                        row=5, column=n, pady=30, padx=5, sticky="s")

                                   
                                    # Button(secondarycanvas, text=f"Acknowledge {n+(rows*4)}",fg="white", bg="#eb5757",font=buttonfont ,command=(lambda n=n: buttonclk(room_num[n+(rows*4)].get('deviceid'),x,y,n,room_num[n+(rows*4)].get('calltype'),room_num[n+(rows*4)].get('batterypercent'),room_num[n+(rows*4)].get('newcall'),room_num[n+(rows*4)].get('bedname'),room_num[n+(rows*4)].get('location')))).grid(
                                    #     row=5, column=n, pady=30, padx=5, sticky="s")

                                if room_num[n+(rows*4)].get('calltype') == 'D':   
                                    GetPort_SerialData.checkdeletedata(
                                    room_num[n+(rows*4)].get('deviceid'))
                                
                                    tertiaryFrame = Canvas(secondarycanvas,bg="white" ,width=screen_width/4,
                                            height=screen_height/4, bd=4,highlightthickness=0).grid(row=5, column=n,padx=0,pady=0 )

                                if room_num[n+(rows*4)].get('calltype') == 'A':   
                                    GetPort_SerialData.checkackdata(
                                    room_num[n+(rows*4)].get('deviceid'))
                                
                                    tertiaryFrame = Canvas(secondarycanvas,bg="white" ,width=screen_width/4,
                                            height=screen_height/4, bd=4,highlightthickness=0).grid(row=5, column=n,padx=0,pady=0 )            
                
            # sleep(2)      
                        sleep(1)
                        root.update()
                except:
                        print("loopbreak")
                #     root.update()  
                # root.update()      
            root.update()


        sleep(1)
        root.mainloop()
    

x = GetPort_SerialData
y = Display_Data


# run these to get array for frontend
x.ports()
x.readcsv()
# x.readserial()
y.display_card()



if exec == 1:
    x.ports()
    x.readcsv()
    y.display_card()

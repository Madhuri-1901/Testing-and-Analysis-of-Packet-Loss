#!/usr/bin/env python
# coding: utf-8




import sys
import subprocess
import re
import itertools
import socket
import os
import platform
import traceback
import re
import numpy
import matplotlib.pyplot as plt
import pandas as pd
import csv

print("\n")
print("-"*100)
print(" "*41,"PACKET LOSS TESTING")
print("-"*100)
print("\n")
plat=platform.system()
scriptDir=sys.path[0]
print()
regex='''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?\.(
25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?\.(
25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?\.(
25[0-5|2[0-4][0-9]|[0-1]?[0-9][0-9]?))))$'''


"""input option checking"""
    
def ip_option():
    try:
        print("-"*75)
        print("1.Enter 1 to enter website name\n2.enter 2 for ip address")
        print("-"*75)
        op_wip=(int(input("Enter any option 1 or 2: ")))
        if op_wip==0 or op_wip in range(3,9999):
            print("Please enter value 1 or 2\n")
        else:
            return op_wip
    except:
        print()
        print("Please enter a int value\n")
            
"""getting IP address"""
            
def ip_check():
    if op_host==1:
        try:
            host=str(input("Enter the website name: "))
            print()
            https='https://'
            http='http://'
            www='www.'
            if https in host:
                host=host[8:]
            if http in host:
                host=host[7:]
            if www not in host:
                host=www+host
            h=host.find('/')
            if h!=-1:
                host=host[:h]
            hosts=socket.gethostbyname(host)
            return hosts
        except:
            print()
            print("Unable to get website IP address please check the website name and try again")
            print()
    elif op_host==2:
        print("-"*75)
        print()
        hosts=input("Enter IP address: ")
        print()
        if(re.search(regex,hosts)):
            return hosts
        else:
            print("please check the IP address")
        print()
    
    else:
        print("please enter a valid ip address")
        print()
            
""" optioncheck function that contains a while loop that runs until it gets a valid input """
    
def optioncheck():
    global hostop
    hostop=None
    while(hostop==None):
        hostop=ip_option()
        return hostop
    
""" hostcheck function that contains a while loop that runs until it gets a valid IP address """  
    
def hostcheck():
    global hostsop
    hostsop=None
    while(hostsop==None):
        hostsop=ip_check()
        return hostsop
    
"""checking input option for count and size"""
    
def cs_option():
    try:
        print("-"*100)
        print(" "*30,"Default values for count is 10 and size is 32")
        print("-"*100)
        print()
        opcs=int(input("Enter 1 to change default values.Enter 2 to proceed with default values : "))
        print()
        print("-"*75)
        print()
        if opcs==0 or opcs in range(3,9999):
            print("Please enter value 1 or 2\n")
        else:
            return opcs
    except:
        print()
        print("Please enter a int value\n")
        
"""checking number of packets"""
        
def cs_checka():
    if op_cs==1:
        try:
            x=int(input("Enter the count: "))
            print()
            return str(x)
        except:
            print("Please enter int value")
            print()
    elif op_cs==2:
        x=10
        return str(x)
    print()
    
"""checking the packet size"""
    
def cs_checkb():
    if op_cs==1:
        try:
            y=int(input("Enter the size: "))
            print()
            return str(y)
            print()
        except:
            print()
            print("Please enter int value")
            print()
    elif op_cs==2:
        y=32
        return str(y)
    print()
    
""" Checking the input option for count and size """
    
def cs_option_Check():
    global cs_op
    cs_op=None
    while(cs_op==None):
        cs_op=cs_option()
        return cs_op
    
""" check_count function that contains a while loop that runs until it gets a valid input for count """
    
def check_count():
    global count
    count=None 
    while(count==None):
        count=cs_checka()
        return count

""" check_size function that contains a while loop that runs until it gets a valid input for size """
    
def check_size():
    global size
    size=None
    while(size==None):
        size=cs_checkb()
        return size
    
""" Checking the input option for saving the results or not """
    
def ping_option():
    try:
        op_ping=int(input("1.Enter 1 to save results.\n2.Enter 2 if don't want to save results: "))
        print()
        if op_ping==0 or op_ping in range(3,9999):
            print("Please enter value 1 or 2\n")
        else:
            return op_ping
    except:
        print()
        print("Please enter a int vaue\n")
        
""" check_save function that contains a while loop that runs until it gets a valid input for save """
    
def check_ping():
    global op_pi
    op_pi=None
    while(op_pi==None):
        op_pi=ping_option()
        return op_pi
    
    """main function"""
    
def packet_loss_testing():
 
    """ global variables are defined"""
    global op_host
    global hosts
    global op_cs
    global a
    global b
    global op_pings
 
    """ Getting values for variables """
 
    high_ping=[]
 
    op_host=optioncheck()
    hosts= hostcheck()
    op_cs=cs_option_Check()
    a=check_count()
    b=check_size()
    op_pings=check_ping()
    print("-"*100)
 
    """ Checking the platform is windows or not and running the ping command that gives the results """
 
    try:
        if plat == "Windows":
            args = ["ping", "-n", a , "-l", b , "-w", "1000", hosts]
        ping = subprocess.Popen(
            args,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
            )
        out, error = ping.communicate()
        results=str(out)
        """ If all packets sent are lost then we dont get the minimum,maximum and average values """
 
        try:
            minimum = str(re.findall(r"Minimum = (\d+)", results)[0])
            maximum = str(re.findall(r"Maximum = (\d+)", results)[0])
            average = str(re.findall(r"Average = (\d+)", results)[0])
        except:
            minimum = "All packets sent are lost because minimum response > 1000 ms"
            maximum = "All packets sent are lost"
            average = "All packets sent are lost"
   
        packets_lost = str(re.findall(r"Lost = (\d+)", results)[0])
        packets_sent = str(re.findall(r"Packets: Sent = (\d+)", results)[0])
        packets_received = str(re.findall(r"Received = (\d+)", results)[0])
  
  
        """ Graph """
 
        if os.path.exists('text.txt'):
            os.remove('text.txt')
        if os.path.exists('text.csv'):
            os.remove('text.csv')
 
        results=results.replace("\\r\\n","\n \n")
        x = re.split("\\n ", results)
 
        try:
            if average == "All packets sent are lost":
                with open("text.txt", "w") as file1:
                    file1.writelines(x[1:-4])
            else:
                with open("text.txt", "w") as file1:
                    file1.writelines(x[1:-8])
            left=[]
            for i in range(1,int(count)+1):
                left.append(i)
            with open("text.csv", "w") as csv_file:
                dataping = pd.read_csv("text.txt",sep="=|ms|Pinging|with|bytes|of|data|Request timed out.",engine='python')
                dataping.to_csv('text.csv', index = None)
                dataping.columns=['reply','time','a','ping','b','TTL']
            with open("text.csv", "r") as csv_file:
                csv_reader = csv.reader(csv_file)
                for lines in csv_reader:
                    height=list(dataping.ping)
            for i in range(len(height)):
                if pd.isna(height[i])==True:
                    height[i]=1000
            high_ping=height
            
            plt.plot(left,height,color='green',linestyle='solid',linewidth=1,marker='o',markerfacecolor='blue',markersize=4)
            plt.xlabel('count')
            plt.ylabel('ping')
            plt.title('Packet loss testing')
            plt.show()
        except:
            print("Graph plotting error ")
 
        Packet_loss_percentage=(100-((int(packets_received)/int(packets_sent))*100))
        count_high_ping=0
        for i in range(len(high_ping)):
            if high_ping[i]>=300:
                count_high_ping+=1
                count_high_ping_percentage=round(((count_high_ping/int(count))*100),2)
 
        """ Save the results in ping.txt """
 
        if op_pings==1:
            print()
            if os.path.exists('ping.txt'):
                os.remove('ping.txt')
            f = open('ping.txt', 'a')
            f.write("Hostname : " + hosts + "\n")
            f.write("Packets sent : " + packets_sent + " packets" + "\n")
            f.write("Packets received : " + packets_received + " packets" + "\n")
            f.write("Packet Loss : " + packets_lost + " packets" + "\n")

            print("Hostname : ", hosts)
            print("Packets sent : ",packets_sent,"packets")
            print("Packets received : ",packets_received,"packets")
            print("Packets lost : ",packets_lost,"packets")
            print("Packet Loss percentage : ",(100-((int(packets_received)/int(packets_sent))*100)),"%")
 
            if minimum == "All packets sent are lost because minimum response > 1000 ms":
                f.write("Minumum Response : " + minimum + "\n")
            else:
                f.write("Minumum Response : " + minimum + "ms" + "\n")
 
            if maximum == "All packets sent are lost":
                f.write("Maximum Response : " + maximum + "\n")
            else:
                f.write("Maximum Response : " + maximum + "ms" + "\n")
 
            if average == "All packets sent are lost":
                f.write("Average Response : " + average + "\n")
            else:
                f.write("Average Response : " + average + "ms" + "\n")

            if Packet_loss_percentage<=1.0:
                f.write("Connection : Excellent connection"+"\n")
                print("Connection : Excellent connection"+"\n")
            elif Packet_loss_percentage>1.0 and Packet_loss_percentage<=5.0:
                f.write("Connection : Good connection and packet loss may not be noticeable"+"\n")
                print("Connection : Good connection and packet loss may not be noticeable"+"\n")
            elif Packet_loss_percentage>5.0 and Packet_loss_percentage<=10.0:
                f.write("Connection : Good connection and packet loss may be slightly noticeable"+"\n")
                print("Connection : Good connection and packet loss may be slightly noticeable"+"\n")
            elif Packet_loss_percentage>10.0 and Packet_loss_percentage<=20.0:
                f.write("Connection : Poor connection and packet loss will be noticeable"+"\n")
                print("Connection : Poor connection and packet loss will be noticeable"+"\n")
            elif Packet_loss_percentage>20.0:
                f.write("Connection : Bad connection and high packet loss"+"\n")
                print("Connection : Bad connection and high packet loss"+"\n")
                f.write("Number of Packets that took more than 300 ms : "+str(count_high_ping)+"\n")
                print("Number of Packets that took more than 300 ms : "+str(count_high_ping)+"\n")
                f.write("Percentage of Number of Packets that took more than 300 ms : "+str(count_high_ping_percentage)+"%"+"\n")
                print("Percentage of Number of Packets that took more than 300 ms : "+str(count_high_ping_percentage)+"%"+"\n")
            

            f.write("\n")
            f.close()
 
    except:
        print('Error processing line: ', hosts)
        print('Error message: ', traceback.format_exc())
        

packet_loss_testing()
print("\n")
print("-"*100)
print(" "*30,"PACKET LOSS TESTING COMPLETED SUCCESSFULLY")
print("-"*100)
print("\n")








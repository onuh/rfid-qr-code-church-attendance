# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## https://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.grid as gridlib
import wx.xrc
import wx.adv
import winreg
from wx.adv import Animation, AnimationCtrl
import subprocess
from subprocess import check_output
import psutil
import serial.tools.list_ports
import serial
import time
from datetime import datetime
import fileinput, re
import threading
import wx.html2
#from threading import Thread
import requests
from urllib3.exceptions import InsecureRequestWarning
import  win32api, win32gui, win32con
# import pyautogui
import ctypes
import keyboard
import os
import copy
import os.path
import sqlite3 as churchdb
import sys
import winsound
import atexit
from configparser import ConfigParser
from mycipher import MyCipher
import shutil
from shutil import copyfile
import ast
from glob import glob
# from glob import iglob
# from win10toast import ToastNotifier
from wakepy import set_keepawake, unset_keepawake


# pyautogui.FAILSAFE = False
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
#controls label2 and text change
global infoStatus
infoStatus = "startup"

global browser_monitor
browser_monitor = 0

global count
count = 0

global mode
mode = "None"

global blocked
blocked = 0

global Dialogucount
Dialogucount = 0

global attendee
attendee = 0

# global toaster
# toaster = ToastNotifier()       

def update_local_db(card_id, firstname, lastname, event, date, gender, time_attend, action):

        data = (card_id, firstname, lastname, event, date, gender, time_attend)
        query_data2 = (event, date, card_id)
        del_data = (card_id, event, date)

        try:
                db = churchdb.connect('c:/ProgramData/SmartChurchApp/offline_data/attendancedata.db')
                cur = db.cursor()

                attendancetable = "CREATE TABLE IF NOT EXISTS attendance (card_id TEXT, firstname TEXT, lastname TEXT, event TEXT, attend_date TEXT, gender TEXT, time_attend TEXT)"

                cur.execute(attendancetable)

                if action == 'insert':

                        query2 = ''' SELECT card_id FROM attendance WHERE event= ? AND attend_date= ? AND card_id= ? '''
                        cur.execute(query2,query_data2)
                        rows = cur.fetchall()
                        if not rows:
                                query = ''' INSERT INTO attendance (card_id,firstname,lastname,event,attend_date,gender,time_attend) VALUES(?,?,?,?,?,?,?) '''
                                cur.execute(query, data)
                                db.commit()


                elif action == 'delete':

                        query = ''' DELETE FROM attendance WHERE card_id = ? AND event = ? AND attend_date = ? '''
                        cur.execute(query,del_data)
                        db.commit()

        except Exception as conn_err:

                print("local database error: ", conn_err)

        finally:

                db.close()




def refresh_timer_gif(timer):

        BrowserFrame = win32gui.FindWindow(None, "SMART Church App")
        if timer and BrowserFrame:
                
                timer.ctrl.Stop()
                anim = Animation(resource_path('Timer.gif'))
                timer.ctrl = AnimationCtrl(timer, -1, anim, pos=(25, 25))
                timer.ctrl.Play()
                x0, y0, x1, y1 = win32gui.GetWindowRect(BrowserFrame)
                timer.SetPosition(pt=(x0+50, y1-220))
                timer.ShowModal()
        
        return

def run_count(self,BrowserFrame,mode):
        time.sleep(1)
        global count
        global browser_monitor
        global Dialogucount
        global attendee
        # x, y = pyautogui.size()
        # x = x/2 + 300
        # y = y/2 + 20

        while 1:
                # keyboard.send('windows+m')
                if BrowserFrame and mode == "Offline_attendance":
                        # keyboard.send('esc')
                        time.sleep(0.5)        
                        if Dialogucount != 16:
                                keyboard.release('ctrl')
                                keyboard.send('esc')
                                keyboard.release('ctrl')
                           
                        try:
                                count = count+1
                                if count >= 60 and attendee == 1:
                                        count = 10
                                        
                                if count == 10 and attendee == 1:
                                        
                                        attendee = 0
                                        html = '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>SmartChurch Offline Attendance</title></head><body style="background-color:#c9c9c9; font-family: Arial Narrow;" ondragstart="return false;"><div style="position: absolute;top: 0; right: 0;left: 0; height: 30px; font-size: 24px; color: #ffffff; background-color: red; text-align: center; padding: 10px;">OFFLINE ATTENDANCE</div><div style="height: 100%; padding: 10px; border:none; margin-left: 5%; margin-right: 5%; background-color: #cbcbcbcb;"><img style="display: block; margin: 0px auto; margin-top: 50px;" src="rfid_load.gif"><div style="text-align: center; margin-top: -150px;"><h1 class="name">PLACE YOUR CARD ON SMART READER</h1><br></div></div><footer style="position: fixed; text-align: center; width: 100%; bottom: 5px; left:0;">SmartChurch Attendance System Copyright &copy; '+str(datetime.now().year)+'.</footer><style type="text/css">body{user-select: none;}</style></body></html>'
                                        log = open(resource_path("smart-church/resources/app/index.html"),"w")
                                        log.write(html)
                                        log.close()
                                        # pyautogui.click(x,y)
                                        win_title = win32gui.GetWindowText(win32gui.GetForegroundWindow())
                                        if win_title != 'SMART Church App':
                                                keyboard.release('windows')
                                                keyboard.send('windows+m')
                                                time.sleep(0.5)

                                                         
                                        # pyautogui.click(x,y)
                                        keyboard.send('esc')
                                        win32gui.SetForegroundWindow(BrowserFrame)
                                        keyboard.send('ctrl+r')

                                elif count >= 60 and attendee == 0:
                                        
                                        attendee = 0
                                        count = 10
                                        # pyautogui.click(x,y)
                                        win_title = win32gui.GetWindowText(win32gui.GetForegroundWindow())
                                        if win_title != 'SMART Church App':
                                                keyboard.release('windows')
                                                keyboard.send('windows+m')
                                                time.sleep(0.5)

                                                         
                                        # pyautogui.click(x,y)
                                        keyboard.send('esc')
                                        win32gui.SetForegroundWindow(BrowserFrame)
                                        keyboard.send('ctrl+r')
                                        
                                if browser_monitor == 2 or Dialogucount == 16:
                                        obfuscate_url()
                                        return
        
                        except Exception as b_err:
                                time.sleep(0.5)
                                keyboard.send('esc')
                                
                # keyboard.release('windows')        
                if Dialogucount == 16 or browser_monitor == 2:
                        obfuscate_url()
                        return

        

def clean_upDir():
        
        temp_dir = 'C:\\ProgramData\\SmartChurchApp\\Cleaner'
        import glob
        dir_list = glob.iglob(os.path.join(temp_dir, "_MEI*"))
        for path in dir_list:

                if os.path.isdir(path):

                        try:
                                shutil.rmtree(path)

                        except Exception as m:

                                print("Error Cleaning Up: "+str(m))
        return

def obfuscate_url():

        file_content = '{"alwaysOnTop":true,"backgroundColor":null,"basicAuthPassword":null,"basicAuthUsername":null,"bounce":false,"clearCache":true,"counter":false,"darwinDarkModeSupport":false,"disableGpu":false,"diskCacheSize":null,"enableEs3Apis":false,"fastQuit":false,"flashPluginDir":null,"fullScreen":false,"globalShortcuts":null,"height":800,"ignoreCertificate":false,"ignoreGpuBlacklist":false,"insecure":false,"internalUrls":null,"blockExternalUrls":true,"name":"SMART Church App","nativefierVersion":"10.1.0","proxyRules":null,"showMenuBar":false,"singleInstance":true,"targetUrl":"","userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.87 Safari/537.36","width":1280,"win32metadata":{},"zoom":1}'
        with open(resource_path("smart-church/resources/app/nativefier.json"), "w") as browser_config:
                browser_config.write(file_content)

        with open(resource_path("smart-church/resources/app/nativefier.json.bak"), "w") as browser_config2:
                browser_config2.write(file_content)

        # with fileinput.FileInput(resource_path("smart-church/resources/app/nativefier.json"), inplace=True, backup='.bak') as file:
        #         for line in file:
        #                 print(re.sub('"targetUrl":\S+,', '"targetUrl":"",',line), end='')

def verification():

        running_name_of_reader = []
        for process in psutil.process_iter():
                if process.name()== "CSAS.exe":
                        
                        running_name_of_reader.append(process.name())
                        
        running = running_name_of_reader.count("CSAS.exe")
        
        if running >= 2:
                
                sys.exit(0)
        else:

                running_name_of_cleaner = []
                for process in psutil.process_iter():
                        
                        if process.name()== "CSASHouseKeep.exe":
                                
                                running_name_of_cleaner.append(process.name())
                                
                running = running_name_of_cleaner.count("CSASHouseKeep.exe")
                
                if running >= 1:
                        
                        return
                else:
                        clean_upDir()
                

def is_admin():

        try:
                return ctypes.windll.shell32.IsUserAnAdmin()
        except:
                sys.exit()


def upload_offline_attendance(cpt_name,hardware_id):
        
        date = datetime.today().strftime('%Y-%m-%d')
        subprocess.Popen(['Toast/CSAToast.exe', 'Attempting To Upload Offline Attendance Data...'])
        time.sleep(2)
        try:
                # toaster = ToastNotifier()
                # toaster.show_toast("Smart Church","Attempting To Upload Offline Attendance Data...",icon_path=resource_path("ClipartKey_1167914.ico"),duration=5, threaded=True)
                # time.sleep(6)
                #Verify Device
                URL = 'https://smartchurchattendance.com.ng/smartChurch/api/RegisterDevice'
                data = '['+'"'+cpt_name+'"'+','+'"'+hardware_id+'"'+']'
                cipher = MyCipher()
                data = cipher.encrypt_includes_iv(data)
                data = data.decode()
                resp = requests.post(URL, data, verify=False)               

                if "Already" in resp.text:
                        
                        offline_path = 'c:/ProgramData/SmartChurchApp/offline_data/'
                        upload_success = []
                        upload_failure = []
                        server_error_responses = []
                        
                        for i in os.listdir(offline_path):

                                if os.path.isfile(os.path.join(offline_path,i)) and i.startswith('attendance_') and os.path.getsize(offline_path+i)!=0:
                                        attendance_data = open("c:/ProgramData/SmartChurchApp/offline_data/"+i,"r")
                                        

                                        
                                        
                                        URL = 'https://smartchurchattendance.com.ng/smartChurch/api/SubmitOfflineAttendance'
                                        
                                        try:
                                                upload_attendance = requests.post(URL, data=attendance_data, verify=False)
                                                upload_success.append("success")
                                                attendance_data.close()
                                                if "<html" not in upload_attendance.text:
                                                        
                                                        server_error_responses.append(upload_attendance.text)
                                                        time.sleep(1)
                                                        current_time = datetime.now().time()
                                                        current_time = current_time.strftime('%I:%M %p')
                                                        smartchurch_log = str(date)+" "+str(current_time)+" : "+upload_attendance.text
                                                        with open("c:/ProgramData/SmartChurchApp/SmatChurch.log", "a") as mylog:
                                                                mylog.write("\r")
                                                                mylog.write(smartchurch_log)
                                                        #wx.CallAfter(print,upload_attendance.text)
                                                
                                                        #delete file
                                                        try:
                                                                time.sleep(1)
                                                                os.remove(offline_path+i)
                                                        
                                                        except Exception as delete_err:
                                                        
                                                                pass
                                                        
                                                elif "<html" in upload_attendnace.text:
                                                        upload_attendance.text = "Invalid Server Response, Could Not Upload Offline Attendance"
                                                        server_error_responses.append(upload_attendance.text)
                                                        time.sleep(1)
                                                        current_time = datetime.now().time()
                                                        current_time = current_time.strftime('%I:%M %p')
                                                        smartchurch_log = str(date)+" "+str(current_time)+" : "+upload_attendance.text
                                                        with open("c:/ProgramData/SmartChurchApp/SmatChurch.log", "a") as mylog:
                                                                mylog.write("\r")
                                                                mylog.write(smartchurch_log)
                                                        
                                                
                                        except Exception as upload_err:

                                                upload_failure.append("Failure")
                                                current_time = datetime.now().time()
                                                current_time = current_time.strftime('%I:%M %p')
                                                smartchurch_log = str(date)+" "+str(current_time)+" : "+str(upload_err)
                                                with open("c:/ProgramData/SmartChurchApp/SmatChurch.log", "a") as mylog:
                                                        mylog.write("\r")
                                                        mylog.write(smartchurch_log)
                                                
                                                
                                                   
                        if upload_failure:
                                 
                                 # time.sleep(6)
                                 # toaster = ToastNotifier()
                                 # toaster.show_toast("Smart Church","Failure Uploading Offline Attendance. Retrying...",icon_path=resource_path("ClipartKey_1167914.ico"),duration=5, threaded=True)
                                 # time.sleep(6)
                                 subprocess.Popen(['Toast/CSAToast.exe', 'Failure Uploading Offline Attendance. Retrying...'])
                                 # time.sleep(6)
                                 notification_thread = threading.Thread(target=upload_offline_attendance,args=(cpt_name,hardware_id))
                                 notification_thread.daemon = True
                                 notification_thread.start()
                                 
                        elif upload_success:
                                  # time.sleep(6)
                                  # toaster = ToastNotifier()
                                  # toaster.show_toast("Smart Church","Offline Attendance Upload Success!",icon_path=resource_path("ClipartKey_1167914.ico"),duration=5, threaded=True)
                                  subprocess.Popen(['Toast/CSAToast.exe', 'Offline Attendance Upload Success!'])
                                  if server_error_responses:
                                        time.sleep(5)
                                        subprocess.Popen(['Toast/CSAToast.exe', '\n'.join(server_error_responses)])
                                          # time.sleep(6)
                                          # toaster = ToastNotifier()
                                          # toaster.show_toast("Smart Church Server Response","\n".join(server_error_responses),icon_path=resource_path("ClipartKey_1167914.ico"),duration=25, threaded=True)


                        return
                
                else:

                        # toaster = ToastNotifier()
                        # toaster.show_toast("Smart Church","Your Device is Unathorized To Send Attendance Data.",icon_path=resource_path("ClipartKey_1167914.ico"),duration=5, threaded=True)
                        # time.sleep(5)
                        subprocess.Popen(['Toast/CSAToast.exe', 'Your Device is Unathorized To Send Attendance Data.'])
                        wx.CallAfter(clean_up,"c:/ProgramData/SmartChurchApp/offline_data")
                        wx.CallAfter(clean_up,resource_path("smart-church/resources/app/offline_data"))
                        current_time = datetime.now().time()
                        current_time = current_time.strftime('%I:%M %p')
                        smartchurch_log = str(date)+" "+str(current_time)+" : Your Device is Unathorized To Send Attendance Data."
                        time.sleep(1)
                        with open("c:/ProgramData/SmartChurchApp/SmatChurch.log", "a") as mylog:
                                mylog.write("\r")
                                mylog.write(smartchurch_log)
                        return
                        


        except Exception as toastEx:
                #wx.CallAfter(print,str(toastEx))
                # time.sleep(6)
                # toaster = ToastNotifier()
                # if "<html" in resp.text:
                #         toastEx = "Invalid Server Response.... Try Upload Again After Some time"
                # toaster.show_toast("Smart Church","Error Uploading Offline Attendance Data:\n"+str(toastEx),icon_path=resource_path("ClipartKey_1167914.ico"),duration=5, threaded=True)
                # time.sleep(6)
                subprocess.Popen(['Toast/CSAToast.exe', 'Error Uploading Offline Attendance Data:\n'+str(toastEx)])
                current_time = datetime.now().time()
                current_time = current_time.strftime('%I:%M %p')
                smartchurch_log = str(date)+" "+str(current_time)+" : Error Uploading Offline Attendance Data: "+str(toastEx)
                time.sleep(1)
                with open("c:/ProgramData/SmartChurchApp/SmatChurch.log", "a") as mylog:
                        mylog.write("\r")
                        mylog.write(smartchurch_log)
                return

        

def get_online_events(self,wxChoice,Choice):

        global toaster
        Choice = ["--SELECT EVENT--"]

        try:
                URL2 = 'https://smartchurchattendance.com.ng/smartChurch/api/DownloadEvents'
                data2 = '['+'"'+self.cpt_name+'"'+','+'"'+self.hardwrid+'"'+']'
                cipher2 = MyCipher()
                data2 = cipher2.encrypt_includes_iv(data2)
                data2 = data2.decode()
                resp2 = requests.post(URL2, data=data2, verify=False)
                
                
                if "Blocked" in resp2.text:
                        wx.CallAfter(clean_up,"c:/ProgramData/SmartChurchApp/offline_data")
                        wx.CallAfter(clean_up,resource_path("smart-church/resources/app/offline_data"))
                        subprocess.Popen(['Toast/CSAToast.exe', 'Could Not Fetch Events, This Device is Blocked By Church Administrator. Contact Church Admin'])
                        # toaster.show_toast("Smart Church","Could Not Fetch Events, This Device is Blocked By Church Administrator. Contact Church Admin",icon_path=resource_path("ClipartKey_1167914.ico"),duration=5, threaded=True)
                        # time.sleep(6)
                        
                        date = datetime.today().strftime('%Y-%m-%d')
                        current_time = datetime.now().time()
                        current_time = current_time.strftime('%I:%M %p')
                        smartchurch_log = str(date)+" "+str(current_time)+" : Could Not Fetch Events, This Device is Blocked By Church Administrator. Contact Church Admin"
                        with open("c:/ProgramData/SmartChurchApp/SmatChurch.log", "a") as mylog:
                                mylog.write("\r")
                                mylog.write(smartchurch_log)
                        return
                
                elif "error" in resp2.text:

                        # toaster.show_toast("Smart Church","Could Not Fetch Events, Server Experienced An Error",icon_path=resource_path("ClipartKey_1167914.ico"),duration=5, threaded=True)
                        subprocess.Popen(['Toast/CSAToast.exe', 'Could Not Fetch Events, Server Experienced An Error'])
                        # time.sleep(6)
                        
                        date = datetime.today().strftime('%Y-%m-%d')
                        current_time = datetime.now().time()
                        current_time = current_time.strftime('%I:%M %p')
                        smartchurch_log = str(date)+" "+str(current_time)+" : Could Not Fetch Events, Server Experienced An Error"
                        with open("c:/ProgramData/SmartChurchApp/SmatChurch.log", "a") as mylog:
                                mylog.write("\r")
                                mylog.write(smartchurch_log)
                        return

                elif "No event" in resp2.text:

                        # toaster.show_toast("Smart Church","Could Not Fetch Events, Administrator Is Yet To Add Events",icon_path=resource_path("ClipartKey_1167914.ico"),duration=5, threaded=True)
                        subprocess.Popen(['Toast/CSAToast.exe', 'Could Not Fetch Events, Administrator Is Yet To Add Events'])
                        # time.sleep(6)
                        
                        date = datetime.today().strftime('%Y-%m-%d')
                        current_time = datetime.now().time()
                        current_time = current_time.strftime('%I:%M %p')
                        smartchurch_log = str(date)+" "+str(current_time)+" : Could Not Fetch Events, Administrator Is Yet To Add Events"
                        with open("c:/ProgramData/SmartChurchApp/SmatChurch.log", "a") as mylog:
                                mylog.write("\r")
                                mylog.write(smartchurch_log)
                        return

                elif resp2.text == "Data Not In Correct Format":
                        return

                elif "No Record Found" in resp2.text:
                        wx.CallAfter(clean_up,"c:/ProgramData/SmartChurchApp/offline_data")
                        wx.CallAfter(clean_up,resource_path("smart-church/resources/app/offline_data"))
                        subprocess.Popen(['Toast/CSAToast.exe', 'Could Not Fetch Events, This Device is Not Registered Yet, Please Click on Register Device'])
                        # toaster.show_toast("Smart Church","Could Not Fetch Events, This Device is Not Registered Yet, Please Click on Register Device",icon_path=resource_path("ClipartKey_1167914.ico"),duration=5, threaded=True)
                        # time.sleep(6)
                        
                        date = datetime.today().strftime('%Y-%m-%d')
                        current_time = datetime.now().time()
                        current_time = current_time.strftime('%I:%M %p')
                        smartchurch_log = str(date)+" "+str(current_time)+" : Could Not Fetch Events, This Device is Not Registered Yet, Please Click on Register Device"
                        with open("c:/ProgramData/SmartChurchApp/SmatChurch.log", "a") as mylog:
                                mylog.write("\r")
                                mylog.write(smartchurch_log)
                        return
                elif "Not Registered" in resp2.text:

                        wx.CallAfter(clean_up,"c:/ProgramData/SmartChurchApp/offline_data")
                        wx.CallAfter(clean_up,resource_path("smart-church/resources/app/offline_data"))
                        subprocess.Popen(['Toast/CSAToast.exe', 'Could Not Fetch Events, This Device is Not Yet Approved By Church Administrator'])
                        # toaster.show_toast("Smart Church","Could Not Fetch Events, This Device is Not Yet Approved By Church Administrator",icon_path=resource_path("ClipartKey_1167914.ico"),duration=5, threaded=True)
                        # time.sleep(6)
                        
                        date = datetime.today().strftime('%Y-%m-%d')
                        current_time = datetime.now().time()
                        current_time = current_time.strftime('%I:%M %p')
                        smartchurch_log = str(date)+" "+str(current_time)+" : Could Not Fetch Events, This Device is Yet Approved By Church Administrattor"
                        with open("c:/ProgramData/SmartChurchApp/SmatChurch.log", "a") as mylog:
                                mylog.write("\r")
                                mylog.write(smartchurch_log)
                        return
                
                elif resp2.text == "No Data Sent To API":
                        subprocess.Popen(['Toast/CSAToast.exe', 'Could Not Fetch Events, This Device Did Not Send Data to Server'])
                        # toaster.show_toast("Smart Church","Could Not Fetch Events, This Device Did Not Send Data to Server",icon_path=resource_path("ClipartKey_1167914.ico"),duration=5, threaded=True)
                        # time.sleep(6)
                        
                        date = datetime.today().strftime('%Y-%m-%d')
                        current_time = datetime.now().time()
                        current_time = current_time.strftime('%I:%M %p')
                        smartchurch_log = str(date)+" "+str(current_time)+" : Could Not Fetch Events, This Device Did Not Send Data to Server"
                        with open("c:/ProgramData/SmartChurchApp/SmatChurch.log", "a") as mylog:
                                mylog.write("\r")
                                mylog.write(smartchurch_log)
                        return
                else:
                        cipher = MyCipher()
                        events = cipher.decrypt_includes_iv(resp2.text)
                        events = events.decode()
                        events = ast.literal_eval(events)
                        n = 4
                        events = [events[i:i+n] for i in range(0, len(events),n)]
                        for item in events:
                                data = item[0]+"("+item[1]+','+item[2]+'-'+item[3]+")"
                                wx.CallAfter(Choice.append,data)
                                
                        wx.CallAfter(wxChoice.SetItems,Choice)
                        wx.CallAfter(wxChoice.SetSelection,0)
                        wx.CallAfter(wxChoice.SetToolTip,Choice[0])
                        wx.CallAfter(wxChoice.Enable)
                        return
                
                        
        except Exception as m:
                subprocess.Popen(['Toast/CSAToast.exe', 'Could Not Fetch Events From Server, No Internet Connection'])
                # toaster.show_toast("Smart Church","Could Not Fetch Events From Server, No Internet Connection",icon_path=resource_path("ClipartKey_1167914.ico"),duration=2, threaded=True)
                return
                        
def get_offline_events(self,wxChoice,Choice):

        Choice = ["--SELECT EVENT--"]
        
        if os.path.exists(resource_path("smart-church/resources/app/offline_data")):

                file_path = resource_path("smart-church/resources/app/offline_data/events.file")

                if os.path.isfile(file_path) and os.path.getsize(file_path) != 0:

                        try:
                                with open(resource_path("smart-church/resources/app/offline_data/events.file"), "r") as f_content:

                                        cipher = MyCipher()
                                        events = cipher.decrypt_includes_iv(f_content.read())
                                        events = events.decode()
                                        events = ast.literal_eval(events)
                                        n = 4
                                        events = [events[i:i+n] for i in range(0, len(events),n)]
                                        for item in events:
                                                data = item[0]+"("+item[1]+','+item[2]+'-'+item[3]+")"
                                                wx.CallAfter(Choice.append,data)
                                            
                                        wx.CallAfter(wxChoice.SetItems,Choice)
                                        wx.CallAfter(wxChoice.SetSelection,0)
                                        wx.CallAfter(wxChoice.SetToolTip,Choice[0])
                                        wx.CallAfter(wxChoice.Enable)
                                        
                        except Exception as j:
                                wx.CallAfter(print,str(j))
                                wx.CallAfter(wxChoice.SetItems,Choice)
                                wx.CallAfter(wxChoice.SetSelection,0)
                                wx.CallAfter(wxChoice.SetToolTip,Choice[0])
                                wx.CallAfter(wxChoice.Disable)
     
        return

def delete_file(file_path):
        
        try:
                os.remove(file_path)

        except Exception as error:

                pass

def clean_up(path):

        if os.path.isdir(path):

            try:

                shutil.rmtree(path)
                
            except Exception as m:
                pass

    
def load_modal(self,dlg,infoStatus):
    
    #wx.CallAfter(print,self.hardwrid)
    #wx.CallAfter(print,self.cpt_name)
    
    if infoStatus == "startup":
        
        time.sleep(3)
        wx.CallAfter(dlg.text2.SetPosition,pt=(25, 175))
        wx.CallAfter(dlg.text2.SetLabel,"Checking Offline Attendance Data...")
        time.sleep(3)
        offline_path = 'c:/ProgramData/SmartChurchApp/offline_data/'
        offline_attendance_notice = []
        try:
                
                for i in os.listdir(offline_path):

                        if os.path.isfile(os.path.join(offline_path,i)) and i.startswith('attendance_')and os.path.getsize(offline_path+i)!=0:
                                
                                offline_attendance_notice.append('Offline Attendance Found')
        except Exception as e:
                pass

                        
        if offline_attendance_notice:
                
                wx.CallAfter(dlg.text2.SetPosition,pt=(50, 175))
                wx.CallAfter(dlg.text2.SetLabel,"Attendance Data Found!")
                notification_thread = threading.Thread(target=upload_offline_attendance,args=(self.cpt_name,self.hardwrid))
                notification_thread.daemon = True
                notification_thread.start()
                
                
        if not offline_attendance_notice:

                wx.CallAfter(dlg.text2.SetPosition,pt=(40, 175))
                wx.CallAfter(dlg.text2.SetLabel,"No Attendance Data Found.")
                       
        time.sleep(3)
        wx.CallAfter(dlg.text2.SetPosition,pt=(25, 175))
        wx.CallAfter(dlg.text2.SetLabel,"Checking Offline Membership  Data...")
        time.sleep(3)
        if os.path.exists("c:/ProgramData/SmartChurchApp/offline_data"):
            ret = check_output('attrib +s +h c:/ProgramData/SmartChurchApp/offline_data',shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            try:

                log_offline_data = open("c:/ProgramData/SmartChurchApp/offline_data/offline.file","r")
                
                if log_offline_data !="":
                    wx.CallAfter(dlg.text2.SetPosition,pt=(40, 175))
                    wx.CallAfter(dlg.text2.SetLabel,"Moving Offline Data Into App")
                    log_offline_data.close()
                    time.sleep(2)
                    if not os.path.exists(resource_path("smart-church/resources/app/offline_data")):
                        os.makedirs(resource_path("smart-church/resources/app/offline_data"))
                        ret = check_output('attrib +s +h c:/ProgramData/SmartChurchApp/offline_data',shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                        os.makedirs(resource_path("smart-church/resources/app/offline_data/images"))
                        copyfile("c:/ProgramData/SmartChurchApp/offline_data/offline.file",resource_path("smart-church/resources/app/offline_data/offline.file"))
                        copyfile("c:/ProgramData/SmartChurchApp/offline_data/events.file",resource_path("smart-church/resources/app/offline_data/events.file"))
                        path = "c:/ProgramData/SmartChurchApp/offline_data/images"
                        for file in os.listdir(path):
                            if file.endswith(".png"):
                                copyfile("c:/ProgramData/SmartChurchApp/offline_data/images/"+file,resource_path("smart-church/resources/app/offline_data/images/"+file))
                        dlg.Parent.Show()
                        wx.CallAfter(dlg.Parent.SetSize,wx.Size(300, 400))
                        wx.CallAfter(dlg.Parent.Center,wx.BOTH)
                        wx.CallAfter(dlg.Destroy)
                            
                    elif os.path.exists(resource_path("smart-church/resources/app/offline_data")):
                        ret = check_output('attrib +s +h c:/ProgramData/SmartChurchApp/offline_data',shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                        copyfile("c:/ProgramData/SmartChurchApp/offline_data/offline.file",resource_path("smart-church/resources/app/offline_data/offline.file"))
                        copyfile("c:/ProgramData/SmartChurchApp/offline_data/events.file",resource_path("smart-church/resources/app/offline_data/events.file"))
                        path = "c:/ProgramData/SmartChurchApp/offline_data/images"
                        for file in os.listdir(path):
                            if file.endswith(".png"):
                                copyfile("c:/ProgramData/SmartChurchApp/offline_data/images/"+file,resource_path("smart-church/resources/app/offline_data/images/"+file))
                        dlg.Parent.Show()
                        wx.CallAfter(dlg.Parent.SetSize,wx.Size(300, 400))
                        wx.CallAfter(dlg.Parent.Center,wx.BOTH)
                        wx.CallAfter(dlg.Destroy)
                else:
                        
                    os.makedirs("c:/ProgramData/SmartChurchApp/offline_data")
                    ret = check_output('attrib +s +h c:/ProgramData/SmartChurchApp/offline_data',shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                    wx.CallAfter(dlg.text2.SetPosition,pt=(40, 175))
                    wx.CallAfter(dlg.text2.SetLabel,"Offline Data is Empty")
                    time.sleep(2)
                    dlg.Parent.Show()
                    wx.CallAfter(dlg.Parent.SetSize,wx.Size(300, 400))
                    wx.CallAfter(dlg.Parent.Center,wx.BOTH)
                    wx.CallAfter(dlg.Destroy)
                    
            except Exception as e:

                wx.CallAfter(dlg.text2.SetPosition,pt=(25, 175))
                wx.CallAfter(dlg.text2.SetLabel,"Some Data Was Not Loaded Into App.")
                time.sleep(3)
                dlg.Parent.Show()
                wx.CallAfter(dlg.Parent.SetSize,wx.Size(300, 400))
                wx.CallAfter(dlg.Parent.Center,wx.BOTH)
                wx.CallAfter(dlg.Destroy)
        elif not os.path.exists("c:/ProgramData/SmartChurchApp/offline_data"):
            
            wx.CallAfter(dlg.text2.SetPosition,pt=(40, 175))
            wx.CallAfter(dlg.text2.SetLabel,"No Membership Data Was Found.")
            time.sleep(3)
            dlg.Parent.Show()
            wx.CallAfter(dlg.Parent.SetSize,wx.Size(300, 400))
            wx.CallAfter(dlg.Parent.Center,wx.BOTH)
            wx.CallAfter(dlg.Destroy)
        return
    
    elif infoStatus == "download_offline_data":
        
        wx.CallAfter(dlg.text2.SetPosition,pt=(5, 175))
        wx.CallAfter(dlg.text2.SetLabel,"Attempting Connection To Remote Server....")
        time.sleep(2)
        #download Members Data
        try:
            
            URL = 'https://smartchurchattendance.com.ng/smartChurch/api/FetchAlldata'
            data = '['+'"'+self.cpt_name+'"'+','+'"'+self.hardwrid+'"'+']'
            cipher = MyCipher()
            data = cipher.encrypt_includes_iv(data)
            data = data.decode()
            resp = requests.post(URL, data=data, verify=False, timeout=3)
            #wx.CallAfter(print,data)
            time.sleep(2)
            
            if resp.status_code==200:
                
                wx.CallAfter(dlg.text2.SetPosition,pt=(30, 175))
                wx.CallAfter(dlg.text2.SetLabel,"Server Connection Established.")
                #wx.CallAfter(clean_up,"c:/ProgramData/SmartChurchApp/offline_data")
                #wx.CallAfter(clean_up,resource_path("smart-church/resources/app/offline_data"))
            time.sleep(2)
            wx.CallAfter(dlg.text2.SetPosition,pt=(20, 175))
            wx.CallAfter(dlg.text2.SetLabel,"Downloading Members Personal Data...")
            time.sleep(2)

            if "<html" in resp.text:
                    wx.CallAfter(dlg.Destroy)
                    # toaster = ToastNotifier()
                    # toaster.show_toast("Smart Church","Invalid Server Response. Could Not Download Attendance Data, Try Again After Some time..",icon_path=resource_path("ClipartKey_1167914.ico"),duration=5, threaded=True)
                    # time.sleep(6)
                    subprocess.Popen(['Toast/CSAToast.exe', 'Invalid Server Response. Could Not Download Attendance Data, Try Again After Some time..'])
                    # time.sleep(6)
                    current_time = datetime.now().time()
                    current_time = current_time.strftime('%I:%M %p')
                    smartchurch_log = str(date)+" "+str(current_time)+" : Invalid Server Response. Could Not Download Attendance Data, Try Again After Some time.."
                    with open("c:/ProgramData/SmartChurchApp/SmatChurch.log", "a") as mylog:
                            mylog.write("\r")
                            mylog.write(smartchurch_log)
                    return
            
            elif "error" in resp.text:

                wx.CallAfter(dlg.Destroy)
                wx.CallAfter(wx.MessageBox,'There is an Error with Server, Try Again later.', 'Smart Church Server Error', wx.OK | wx.ICON_ERROR)
                return
            
            elif "Blocked" in resp.text:
                    
                wx.CallAfter(clean_up,"c:/ProgramData/SmartChurchApp/offline_data")
                wx.CallAfter(clean_up,resource_path("smart-church/resources/app/offline_data"))
                
                wx.CallAfter(dlg.Destroy)
                wx.CallAfter(wx.MessageBox,resp.text, 'Smart Church Server Response', wx.OK | wx.ICON_ERROR)
                #wx.MessageBox(resp.text, 'Server Response', wx.OK | wx.ICON_ERROR)
                
            elif resp.text == "Data Not In Correct Format":

                wx.CallAfter(dlg.Destroy)
                wx.CallAfter(wx.MessageBox,"One or More Computer Parameter Not Sent", 'Smart Church Server Response', wx.OK | wx.ICON_ERROR)
                
            elif resp.text == "No Data Sent To API":

                wx.CallAfter(dlg.Destroy)
                wx.CallAfter(wx.MessageBox,resp.text, 'Smart Church Server Response', wx.OK | wx.ICON_ERROR)
                
            elif "Not Registered" in resp.text:
                    
                wx.CallAfter(clean_up,"c:/ProgramData/SmartChurchApp/offline_data")
                wx.CallAfter(clean_up,resource_path("smart-church/resources/app/offline_data"))
                wx.CallAfter(dlg.Destroy)
                wx.CallAfter(wx.MessageBox,resp.text, 'Smart Church Server Response', wx.OK | wx.ICON_ERROR)
                
            elif "No Record Found" in resp.text:
                
                wx.CallAfter(clean_up,"c:/ProgramData/SmartChurchApp/offline_data")
                wx.CallAfter(clean_up,resource_path("smart-church/resources/app/offline_data"))
                
                wx.CallAfter(dlg.Destroy)
                wx.CallAfter(wx.MessageBox,resp.text, 'Smart Church Server Response', wx.OK | wx.ICON_ERROR)
                #wx.MessageBox(resp.text, 'Server Response', wx.OK | wx.ICON_ERROR)
                
            else:
                
                #we want file to be saved after downloading images, so save in a variable
                updated_data = resp.text 
                """
                if not os.path.exists("c:/ProgramData/SmartChurchApp/offline_data"):
                    os.makedirs("c:/ProgramData/SmartChurchApp/offline_data")
                    ret = check_output('attrib +s +h c:/ProgramData/SmartChurchApp/offline_data',shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                    log_offline_data = open("c:/ProgramData/SmartChurchApp/offline_data/offline.file","w")
                    log_offline_data.write(resp.text)
                    log_offline_data.close()
                    
                elif os.path.exists("c:/ProgramData/SmartChurchApp/offline_data"):
                    ret = check_output('attrib +s +h c:/ProgramData/SmartChurchApp/offline_data',shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                    log_offline_data = open("c:/ProgramData/SmartChurchApp/offline_data/offline.file","w")
                    log_offline_data.write(resp.text)
                    log_offline_data.close()
                    
                if not os.path.exists(resource_path("smart-church/resources/app/offline_data")):
                    os.makedirs(resource_path("smart-church/resources/app/offline_data"))
                    log_offline_data = open(resource_path("smart-church/resources/app/offline_data/offline.file"),"w")
                    log_offline_data.write(resp.text)
                    log_offline_data.close()
                    
                elif os.path.exists(resource_path("smart-church/resources/app/offline_data")):
                    log_offline_data = open(resource_path("smart-church/resources/app/offline_data/offline.file"),"w")
                    log_offline_data.write(resp.text)
                    log_offline_data.close()
                """
                    
                #Download Images
                wx.CallAfter(dlg.text2.SetPosition,pt=(30, 175))
                wx.CallAfter(dlg.text2.SetLabel,"Downloading Members Images")
                time.sleep(2)
                resp = cipher.decrypt_includes_iv(resp.text)
                resp = resp.decode()
                resp = ast.literal_eval(resp)
                #load existing images into array
                exist_images = []
                online_images = []
                images_folder = "c:/ProgramData/SmartChurchApp/offline_data/images"
                if not os.path.exists(images_folder):
                        os.makedirs(images_folder)
                if not os.path.exists(resource_path("smart-church/resources/app/offline_data/images")):
                        os.makedirs(resource_path("smart-church/resources/app/offline_data/images"))
                for image in os.listdir(images_folder):
                        if image.endswith(".png"):
                                exist_images.append(image) #move image name into array
                                
                not_downloaded_images = []
                
                for item in resp:
                    
                    if item.endswith(".png"):

                        online_images.append(item)
                        
                        if item not in exist_images:

                                try:
                                               
                                        response = requests.get("https://smartchurchattendance.com.ng/smartChurch/images/"+item, verify=False, timeout=3) #limit timeout.This seems to hang download of images
                            
                                        if not os.path.exists("c:/ProgramData/SmartChurchApp/offline_data/images"):
                                                
                                                os.makedirs("c:/ProgramData/SmartChurchApp/offline_data/images")
                                                
                                        elif os.path.exists("c:/ProgramData/SmartChurchApp/offline_data/images"):
                                                
                                                pass
                                            
                                        if not os.path.exists(resource_path("smart-church/resources/app/offline_data/images")):
                                                
                                                os.makedirs(resource_path("smart-church/resources/app/offline_data/images"))
                                                            
                                        elif os.path.exists(resource_path("smart-church/resources/app/offline_data/images")):
                                                     
                                                pass

                                        img_file = open("c:/ProgramData/SmartChurchApp/offline_data/images/"+item,"wb")
                                        img_file.write(response.content)
                                        img_file.close()

                                        img_file2 = open(resource_path("smart-church/resources/app/offline_data/images/"+item),"wb")
                                        img_file2.write(response.content)
                                        img_file2.close()
                            
                                except Exception as e:

                                        not_downloaded_images.append(item)
                                        wx.CallAfter(dlg.text2.SetLabel,"Error Downloading Member Image")
                                        time.sleep(1)
                                        wx.CallAfter(dlg.text2.SetLabel,"Downloading Members Images")
                                        time.sleep(1)
                                        if not_downloaded_images:
                                                
                                                wx.CallAfter(dlg.Destroy)
                                                wx.CallAfter(wx.MessageBox,"Bad Internet Network!\nCould Not Download Images. Please Restart Download of Offline Data", 'Smart Church Server Response', wx.OK | wx.ICON_ERROR)
                                                return
                        else:

                                pass
                    else:
                            pass
                            #wx.CallAfter(print, str(e))
                #save offline data now since we are sure the images are fully updated
                if not os.path.exists("c:/ProgramData/SmartChurchApp/offline_data"):
                    os.makedirs("c:/ProgramData/SmartChurchApp/offline_data")
                    ret = check_output('attrib +s +h c:/ProgramData/SmartChurchApp/offline_data',shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                    log_offline_data = open("c:/ProgramData/SmartChurchApp/offline_data/offline.file","w")
                    log_offline_data.write(updated_data)
                    log_offline_data.close()
                    
                elif os.path.exists("c:/ProgramData/SmartChurchApp/offline_data"):
                    ret = check_output('attrib +s +h c:/ProgramData/SmartChurchApp/offline_data',shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                    log_offline_data = open("c:/ProgramData/SmartChurchApp/offline_data/offline.file","w")
                    log_offline_data.write(updated_data)
                    log_offline_data.close()
                    
                if not os.path.exists(resource_path("smart-church/resources/app/offline_data")):
                    os.makedirs(resource_path("smart-church/resources/app/offline_data"))
                    log_offline_data = open(resource_path("smart-church/resources/app/offline_data/offline.file"),"w")
                    log_offline_data.write(updated_data)
                    log_offline_data.close()
                    
                elif os.path.exists(resource_path("smart-church/resources/app/offline_data")):
                    log_offline_data = open(resource_path("smart-church/resources/app/offline_data/offline.file"),"w")
                    log_offline_data.write(updated_data)
                    log_offline_data.close()
                    
                #Delete Images Not in online Database
                for offline_image in exist_images:
                        
                        if offline_image not in online_images:
                                #wx.CallAfter(wx.MessageBox, offline_image, 'Image Exists', wx.OK | wx.ICON_ERROR)
                                wx.CallAfter(delete_file,"c:/ProgramData/SmartChurchApp/offline_data/images/"+offline_image)
                                wx.CallAfter(delete_file,resource_path("smart-church/resources/app/offline_data/images/"+offline_image))
                        else:
                                pass
                                
                #Download Events
                wx.CallAfter(dlg.text2.SetPosition,pt=(60, 175))
                wx.CallAfter(dlg.text2.SetLabel,"Downloading Events...")
                time.sleep(2)
                
                try:
                        URL2 = 'https://smartchurchattendance.com.ng/smartChurch/api/DownloadEvents'
                        data2 = '['+'"'+self.cpt_name+'"'+','+'"'+self.hardwrid+'"'+']'
                        cipher2 = MyCipher()
                        data2 = cipher2.encrypt_includes_iv(data2)
                        data2 = data2.decode()
                        resp2 = requests.post(URL2, data=data2, verify=False, timeout=3)
                        log_events_data1 = open("c:/ProgramData/SmartChurchApp/offline_data/events.file","w")

                        if "<html" in resp2.text:

                                # toaster = ToastNotifier()
                                # toaster.show_toast("Smart Church","Invalid Server Response. Try Again After Some time..",icon_path=resource_path("ClipartKey_1167914.ico"),duration=5, threaded=True)
                                # time.sleep(6)
                                subprocess.Popen(['Toast/CSAToast.exe', 'Invalid Server Response. Try Again After Some time..'])
                                # time.sleep(6)
                                current_time = datetime.now().time()
                                current_time = current_time.strftime('%I:%M %p')
                                smartchurch_log = str(date)+" "+str(current_time)+" : Invalid Server Response. Try Again After Some time.."
                                with open("c:/ProgramData/SmartChurchApp/SmatChurch.log", "a") as mylog:
                                        mylog.write("\r")
                                        mylog.write(smartchurch_log)

                        elif "No event" in resp2.text:

                                # toaster = ToastNotifier()
                                # toaster.show_toast("Smart Church","No Events Available. Administrator Is Yet To Add Events on Portal.",icon_path=resource_path("ClipartKey_1167914.ico"),duration=5, threaded=True)
                                # time.sleep(6)
                                subprocess.Popen(['Toast/CSAToast.exe', 'No Events Available. Administrator Is Yet To Add Events on Portal.'])
                                # time.sleep(6)
                                current_time = datetime.now().time()
                                current_time = current_time.strftime('%I:%M %p')
                                smartchurch_log = str(date)+" "+str(current_time)+" : Administrator Is Yet To Add Events on Portal"
                                with open("c:/ProgramData/SmartChurchApp/SmatChurch.log", "a") as mylog:
                                        mylog.write("\r")
                                        mylog.write(smartchurch_log)

                        else:

                                log_events_data1.write(resp2.text)
                                log_events_data1.close()
                                time.sleep(2)
                                log_events_data2 = open(resource_path("smart-church/resources/app/offline_data/events.file"),"w")
                                log_events_data2.write(resp2.text)
                                log_events_data2.close()

                        
                        
                        
                except Exception as m:

                        wx.CallAfter(dlg.text2.SetPosition,pt=(55, 175))
                        wx.CallAfter(dlg.text2.SetLabel,"Error Downloading Events")
                        time.sleep(2)
                                        
                if not not_downloaded_images:

                    wx.CallAfter(dlg.Destroy)
                    global self2
                    global m_choice2Choices
                    global m_choices
                    fetch_events = threading.Thread(target=get_offline_events,args=(self2,m_choices,m_choice2Choices))
                    fetch_events.daemon = True
                    fetch_events.start()
                    wx.CallAfter(wx.MessageBox,"Data Download Success!", 'Smart Church Server Response', wx.OK | wx.ICON_INFORMATION)
                    
                   
                else:

                    wx.CallAfter(dlg.Destroy)
                    wx.CallAfter(wx.MessageBox,"Data Download Error!\nSome Images Failed To Download", 'Smart Church Server Response', wx.OK | wx.ICON_ERROR)
                    
              
        except Exception as e:
            
            wx.CallAfter(dlg.Destroy)
            wx.CallAfter(wx.MessageBox,'Server Error:\nConnection To Server Could Not Be Established.', 'Smart Church Server Error', wx.OK | wx.ICON_ERROR)
            #wx.MessageBox('Server Error:'+str(e)+'', 'Smart Church Portal Error', wx.OK | wx.ICON_ERROR)
                
        return
    
    elif infoStatus == "register_device":

        wx.CallAfter(dlg.text2.SetPosition,pt=(5, 175))
        wx.CallAfter(dlg.text2.SetLabel,"Attempting Connection To Remote Server....")
        
        try:
            
            URL = 'https://smartchurchattendance.com.ng/smartChurch/api/RegisterDevice'
            data = '['+'"'+self.cpt_name+'"'+','+'"'+self.hardwrid+'"'+']'
            cipher = MyCipher()
            data = cipher.encrypt_includes_iv(data)
            data = data.decode()
            resp = requests.post(URL, data=data, verify=False, timeout=3)
            #wx.CallAfter(print,data)
            time.sleep(2)
            
            if resp.status_code==200:
                
                wx.CallAfter(dlg.text2.SetPosition,pt=(30, 175))
                wx.CallAfter(dlg.text2.SetLabel,"Server Connection Established.")
            time.sleep(2)
            wx.CallAfter(dlg.text2.SetPosition,pt=(25, 175))
            wx.CallAfter(dlg.text2.SetLabel,"Submitting Device Details To Server..")
            time.sleep(2)
            
            if "<html" in resp.text:
                    wx.CallAfter(dlg.Destroy)
                    # toaster = ToastNotifier()
                    # toaster.show_toast("Smart Church","Invalid Server Response. Could Not Register Device, Try Again After Some time..",icon_path=resource_path("ClipartKey_1167914.ico"),duration=5, threaded=True)
                    # time.sleep(6)
                    subprocess.Popen(['Toast/CSAToast.exe', 'Invalid Server Response. Could Not Register Device, Try Again After Some time..'])
                    # time.sleep(6)
                    current_time = datetime.now().time()
                    current_time = current_time.strftime('%I:%M %p')
                    smartchurch_log = str(date)+" "+str(current_time)+" : Invalid Server Response. Could Not Register Device, Try Again After Some time.."
                    with open("c:/ProgramData/SmartChurchApp/SmatChurch.log", "a") as mylog:
                            mylog.write("\r")
                            mylog.write(smartchurch_log)
                    return
                
            elif "error" in resp.text:

                wx.CallAfter(dlg.Destroy)
                wx.CallAfter(wx.MessageBox,'There is an Error with Server, Try Again later.', 'Smart Church Server Error', wx.OK | wx.ICON_ERROR)
                return
                 
            elif "Already" in resp.text:
                #print(resp.text)
                time.sleep(3)
                wx.CallAfter(dlg.Destroy)
                wx.CallAfter(wx.MessageBox,resp.text, 'Smart Church Server Response', wx.OK | wx.ICON_INFORMATION)
                #wx.MessageBox(resp.text, 'Server Response', wx.OK | wx.ICON_INFORMATION)
                
            elif "Blocked" in resp.text:
                    
                wx.CallAfter(clean_up,"c:/ProgramData/SmartChurchApp/offline_data")
                wx.CallAfter(clean_up,resource_path("smart-church/resources/app/offline_data"))

                wx.CallAfter(dlg.Destroy)
                wx.CallAfter(wx.MessageBox,resp.text, 'Smart Church Server Response', wx.OK | wx.ICON_ERROR)
                #wx.MessageBox(resp.text, 'Server Response', wx.OK | wx.ICON_ERROR)
                
            elif resp.text == "Data Not In Correct Format":

                wx.CallAfter(dlg.Destroy)
                wx.CallAfter(wx.MessageBox,"One or More Computer Parameter Not Sent", 'Smart Church Server Response', wx.OK | wx.ICON_ERROR)
                
            elif resp.text == "No Data Sent To API":

                wx.CallAfter(dlg.Destroy)
                wx.CallAfter(wx.MessageBox,resp.text, 'Smart Church Server Error', wx.OK | wx.ICON_ERROR)
                #wx.MessageBox(resp.text, 'Server Response', wx.OK | wx.ICON_ERROR)
                
            else:
                
                wx.CallAfter(dlg.Destroy)
                wx.CallAfter(wx.MessageBox,resp.text, 'Smart Church Server Response', wx.OK | wx.ICON_INFORMATION)
                
        except Exception as e:
            
            wx.CallAfter(dlg.Destroy)
            wx.CallAfter(wx.MessageBox,'Server Error:\nConnection To Server Could Not Be Established', 'Smart Church Server Error', wx.OK | wx.ICON_ERROR)
            #wx.MessageBox('Server Error:'+str(e)+'', 'Smart Church Portal Error', wx.OK | wx.ICON_ERROR)
            
        return

        
    elif infoStatus == "upload_offline_attendance":

            wx.CallAfter(dlg.text2.SetPosition,pt=(5, 175))
            wx.CallAfter(dlg.text2.SetLabel,"Attempting Data Upload To Remote Server....")
            time.sleep(2)
            notification_thread = threading.Thread(target=upload_offline_attendance,args=(self.cpt_name,self.hardwrid))
            notification_thread.daemon = True
            notification_thread.start()
            wx.CallAfter(dlg.Destroy)
            wx.CallAfter(wx.MessageBox,"Watch Notification Area For Offline Attendance Upload Progress", 'Smart Church PC Client Response', wx.OK | wx.ICON_INFORMATION)
            return
        
    elif infoStatus == "check_for_browser":
        
        wx.CallAfter(dlg.text2.SetLabel,"Loading Embedded Web Browser..")
        wx.CallAfter(dlg.text2.SetPosition,pt=(30, 175))
        
        while 1:
            
            BrowserFrame = win32gui.FindWindow(None, "SMART Church App")
            if BrowserFrame:
                time.sleep(3)
                global blocked
                if blocked == 1:
                        win32gui.PostMessage(BrowserFrame, win32con.WM_CLOSE,0,0)
                        
                wx.CallAfter(dlg.Destroy)
                break
                return
            
            else:
                
                pass
        
    elif infoStatus == "reg_visitor":

        wx.CallAfter(dlg.text2.SetPosition,pt=(5, 175))
        wx.CallAfter(dlg.text2.SetLabel,"Attempting Connection To Remote Server....")
        time.sleep(3)
        
        try:
            
            URL = 'https://smartchurchattendance.com.ng/smartChurch/api/RegisterVisitors'
            data = '['+'"'+self.cpt_name+'"'+','+'"'+self.hardwrid+'"'+','+'"'+firstname+'"'+','+'"'+lastname+'"'+','+'"'+address+'"'+','+'"'+phone_number+'"'+','+'"'+email+'"'+','+'"'+date+'"'+','+'"'+membership+'"'+']'
            cipher = MyCipher()
            data = cipher.encrypt_includes_iv(data)
            data = data.decode()
            
            resp = requests.post(URL, data=data, verify=False, timeout=3)
            time.sleep(1)
            if resp.status_code==200:
                
                wx.CallAfter(dlg.text2.SetPosition,pt=(30, 175))
                wx.CallAfter(dlg.text2.SetLabel,"Server Connection Established.")
                time.sleep(1)
                
            if "<html" in resp.text:
                    wx.CallAfter(dlg.Destroy)
                    # toaster = ToastNotifier()
                    # toaster.show_toast("Smart Church","Invalid Server Response. Could Not Register Visitor, Try Again After Some time..",icon_path=resource_path("ClipartKey_1167914.ico"),duration=5, threaded=True)
                    # time.sleep(6)
                    subprocess.Popen(['Toast/CSAToast.exe', 'Invalid Server Response. Could Not Register Device, Try Again After Some time..'])
                    # time.sleep(6)
                    current_time = datetime.now().time()
                    current_time = current_time.strftime('%I:%M %p')
                    smartchurch_log = str(date)+" "+str(current_time)+" : Invalid Server Response. Could Not Register Visitor, Try Again After Some time.."
                    with open("c:/ProgramData/SmartChurchApp/SmatChurch.log", "a") as mylog:
                            mylog.write("\r")
                            mylog.write(smartchurch_log)
                    return

            elif "error" in resp.text:

                wx.CallAfter(dlg.Destroy)
                wx.CallAfter(wx.MessageBox,'There is an Error with Server, Try Again later.', 'Smart Church Server Error', wx.OK | wx.ICON_ERROR)
                return
                
            if "Unknown" in resp.text:
                wx.CallAfter(clean_up,"c:/ProgramData/SmartChurchApp/offline_data")
                wx.CallAfter(clean_up,resource_path("smart-church/resources/app/offline_data"))
                wx.CallAfter(dlg.Destroy)
                wx.CallAfter(wx.MessageBox,resp.text, 'Smart Church Server Response', wx.OK | wx.ICON_ERROR)
                
            elif "Cannot Be Empty" in resp.text:

                wx.CallAfter(dlg.Destroy)
                wx.CallAfter(wx.MessageBox,resp.text, 'Smart Church Server Response', wx.OK | wx.ICON_ERROR)
                
            elif "Cannot Both Be Empty" in resp.text:
                
                wx.CallAfter(dlg.Destroy)
                wx.CallAfter(wx.MessageBox,resp.text, 'Smart Church Server Responser', wx.OK | wx.ICON_ERROR)
                
            elif "Wrong Format" in resp.text:

                wx.CallAfter(dlg.Destroy)
                wx.CallAfter(wx.MessageBox,resp.text, 'Smart Church Server Response', wx.OK | wx.ICON_ERROR)
                
            elif resp.text == "Data Not In Correct Format":

                wx.CallAfter(dlg.Destroy)
                wx.CallAfter(wx.MessageBox,"One or More Computer Parameter Not Sent", 'Smart Church Server Response', wx.OK | wx.ICON_ERROR)

            elif "Blocked" in resp.text:
                    
                wx.CallAfter(clean_up,"c:/ProgramData/SmartChurchApp/offline_data")
                wx.CallAfter(clean_up,resource_path("smart-church/resources/app/offline_data"))

                wx.CallAfter(dlg.Destroy)
                wx.CallAfter(wx.MessageBox,resp.text, 'Smart Church Server Response', wx.OK | wx.ICON_ERROR)
                
            elif "Not Registered" in resp.text:

                wx.CallAfter(dlg.Destroy)
                wx.CallAfter(wx.MessageBox,resp.text, 'Smart Church Server Response', wx.OK | wx.ICON_ERROR)
                
            elif "Invalid" in resp.text:
                
                wx.CallAfter(dlg.Destroy)
                wx.CallAfter(wx.MessageBox,resp.text, 'Smart Church Server Response', wx.OK | wx.ICON_ERROR)

            elif "Already" in resp.text:

                wx.CallAfter(dlg.Destroy)
                wx.CallAfter(wx.MessageBox,resp.text, 'Smart Church Server Response', wx.OK | wx.ICON_ERROR)

            else:

                wx.CallAfter(dlg.Destroy)
                wx.CallAfter(wx.MessageBox,resp.text, 'Smart Church Server Response', wx.OK | wx.ICON_INFORMATION)
                
        except Exception as e:

            wx.CallAfter(dlg.Destroy)
            wx.CallAfter(wx.MessageBox,'Server Error:\nConnection To Server Could Not Be Established', 'Smart Church Server Error', wx.OK | wx.ICON_ERROR)
            

        return
                

    
def save_com_port_data(com_port):

    config = ConfigParser()
    config.add_section('main')
    config.set('main','com',com_port)
    
    if not os.path.exists("c:/ProgramData/SmartChurchApp"):
        
        os.makedirs("c:/ProgramData/SmartChurchApp")
        file = open('c:/ProgramData/SmartChurchApp/config.ini','w+')
        file.close()
        
    with open('c:/ProgramData/SmartChurchApp/config.ini','w') as f:

        config.write(f)
        return

        
def check_saved_reader_data(textCtrl):

    if os.path.exists("c:/ProgramData/SmartChurchApp"):
        
        try:
            
            config = ConfigParser()
            config.read('c:/ProgramData/SmartChurchApp/config.ini')
            prev_comPort = config.get('main','com')
            textCtrl.SetValue(prev_comPort)
            
        except Exception as m:
            #wx.CallAfter(print,str(m))
            return
        
    return

def get_com_port_lists_offline(self,self2):

    try:
        
        ports = list(serial.tools.list_ports.comports())
        
        if not ports:

            wx.CallAfter(self.m_textCtrl33.SetValue,"")
            wx.CallAfter(self.m_textCtrl33.SetValue,"No Smart Card Reader Connected to COM Ports")
            wx.CallAfter(self.m_textCtrl33.SetForegroundColour,wx.Colour( 217, 0, 0 ))
            wx.CallAfter(self.m_button9.Enable)
            
                        
        else:

            wx.CallAfter(self.m_textCtrl33.SetValue,"")
            wx.CallAfter(self.m_button9.Enable)
            for p in ports:
                port = str(p)
                #track reader COM Port change to smart reader
                if "Arduino Uno" in port:
                        port = port.replace("Arduino Uno","Smart Church Card Reader")
                        wx.CallAfter(self.m_textCtrl33.AppendText," "+port+'\n')
                        wx.CallAfter(self.m_textCtrl33.SetForegroundColour,wx.BLUE)
                        return
            wx.CallAfter(self.m_textCtrl33.SetValue,"")
            wx.CallAfter(self.m_textCtrl33.SetValue,"No Valid Smart Church Card Reader Found.")
            wx.CallAfter(self.m_textCtrl33.SetForegroundColour,wx.Colour( 217, 0, 0 ))
            wx.CallAfter(self.m_button9.Enable)
            return
    
    except Exception as e:

        return

                
def get_com_port_lists_bind_cards(self,self2):

    try:
        
        ports = list(serial.tools.list_ports.comports())
        
        if not ports:

            wx.CallAfter(self.m_textCtrl35.SetValue,"")
            wx.CallAfter(self.m_textCtrl35.SetValue,"No Smart Card Reader Connected to COM Ports")
            wx.CallAfter(self.m_textCtrl35.SetForegroundColour,wx.Colour( 217, 0, 0 ))
            wx.CallAfter(self.m_button13.Enable)
            
                        
        else:

            wx.CallAfter(self.m_textCtrl35.SetValue,"")
            wx.CallAfter(self.m_button13.Enable)
            for p in ports:
                port = str(p)
                #track reader COM Port change to smart reader
                if "Arduino Uno" in port:
                        port = port.replace("Arduino Uno","Smart Church Card Reader")
                        wx.CallAfter(self.m_textCtrl35.AppendText," "+port+'\n')
                        wx.CallAfter(self.m_textCtrl35.SetForegroundColour,wx.BLUE)
                        return
            wx.CallAfter(self.m_textCtrl35.SetValue,"")
            wx.CallAfter(self.m_textCtrl35.SetValue,"No Valid Smart Church Card Reader Found.")
            wx.CallAfter(self.m_textCtrl35.SetForegroundColour,wx.Colour( 217, 0, 0 ))
            wx.CallAfter(self.m_button13.Enable)
            return
    
    except Exception as e:

        return

                
def get_com_port_lists_online(self,self2):

    try:
        
        ports = list(serial.tools.list_ports.comports())
        
        if not ports:

            wx.CallAfter(self.m_textCtrl35.SetValue,"")
            wx.CallAfter(self.m_textCtrl35.SetValue,"No Smart Card Reader Connected to COM Ports")
            wx.CallAfter(self.m_textCtrl35.SetForegroundColour,wx.Colour( 217, 0, 0 ))
            wx.CallAfter(self.m_button13.Enable)
            
                        
        else:

            wx.CallAfter(self.m_textCtrl35.SetValue,"")
            wx.CallAfter(self.m_button13.Enable)
            for p in ports:
                port = str(p)
                #track reader COM Port change to smart reader
                if "Arduino Uno" in port:
                        
                        port = port.replace("Arduino Uno","Smart Church Card Reader")
                        wx.CallAfter(self.m_textCtrl35.AppendText," "+port+'\n')
                        wx.CallAfter(self.m_textCtrl35.SetForegroundColour,wx.BLUE)
                        return
            wx.CallAfter(self.m_textCtrl35.SetValue,"")
            wx.CallAfter(self.m_textCtrl35.SetValue,"No Valid Smart Church Card Reader Found.")
            wx.CallAfter(self.m_textCtrl35.SetForegroundColour,wx.Colour( 217, 0, 0 ))
            wx.CallAfter(self.m_button13.Enable)
            return
    
    except Exception as e:

        return

    
def monitor_web_browser(self,selfobj,com_port):
    global browser_monitor
    browser_monitor = 1
    while 1:
        BrowserFrame = win32gui.FindWindow(None, "SMART Church App")
        if not BrowserFrame:
            global timer
            unset_keepawake()
            try:
                global s
                word = "WORKEDED"
                word = word.encode()
                s.write(word)
                time.sleep(0.5)
                #res = s.read(8)
                wx.CallAfter(self.Parent.Show)
                if timer:
                        wx.CallAfter(timer.Destroy)
                browser_monitor = 2
                obfuscate_url()
                #wx.CallAfter(print, "success")
                #wx.CallAfter(print, res)
            except Exception as err:
                wx.CallAfter(self.Parent.Show)
                if timer:
                        wx.CallAfter(timer.Destroy)
                browser_monitor = 2
                obfuscate_url()
                #wx.CallAfter(print, str(err))
                pass

            break


def offline_attendance2(com_port,hardware_id,computer_name,attendance_event,mode,date,name,offline_list,userdata,file,BrowserFrame):
        
        global count
        count = 2
        global attendee
        attendance_event2 = attendance_event.split("(")[0]
        current_time = datetime.now().time()
        current_time = current_time.strftime('%I:%M %p')
        #wx.CallAfter(print,"hello")
        # x, y = pyautogui.size()
        # x = x/2 + 300
        # y = y/2 + 20
        
        try:
                
                if any(userdata in y for y in offline_list):

                        card_index = offline_list.index(userdata)
                        pic =  offline_list[card_index + 3]
                        fname = offline_list[card_index + 1]
                        lname =  offline_list[card_index + 2]
                        gender =  offline_list[card_index + 4]
                        #wx.CallAfter(print,"hello")
                        
                        #check in attendance array if name already there, else append details
                        if any(userdata in z for z in attendance_data):

                                card_index2 = attendance_data.index(userdata)
                                del_val = card_index2 + 1

                                del attendance_data[del_val]
                                del attendance_data[del_val]
                                del attendance_data[del_val]
                                del attendance_data[del_val]
                                del attendance_data[del_val]
                                del attendance_data[del_val]
                                del attendance_data[card_index2]
                                #wx.CallAfter(print,attendance_data)
                                if attendance_data:
                                        
                                        cipher2 = MyCipher()
                                        encrypted_storage = cipher2.encrypt_includes_iv(str(attendance_data))
                                        encrypted_storage = encrypted_storage.decode()
                                        log_offline_attendance = open("c:/ProgramData/SmartChurchApp/offline_data/"+file,"w")
                                        #wx.CallAfter(log_offline_attendance.writ,encrypted_storage)
                                        #wx.CallAfter(log_offline_attendance.close)
                                        log_offline_attendance.write(encrypted_storage)
                                        log_offline_attendance.close()
                                        
                                elif not attendance_data :

                                        log_offline_attendance = open("c:/ProgramData/SmartChurchApp/offline_data/"+file,"w")
                                        #wx.CallAfter(log_offline_attendance.write,"")
                                        #wx.CallAfter(log_offline_attendance.close)
                                        log_offline_attendance.write("")
                                        log_offline_attendance.close()
                                        

                                html = '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>SmartChurch Offline Attendance</title></head><body style="background-color:#c9c9c9; font-family: Arial Narrow;" ondragstart="return false;"><div style="position: absolute;top: 0; right: 0;left: 0; height: 30px; font-size: 24px; color: #ffffff; background-color: red; text-align: center; padding: 10px;">OFFLINE ATTENDANCE</div><div style="height: 100%; padding: 10px; border:none; margin-left: 5%; margin-right: 5%; background-color: #ffffff;"><img style="display: block; margin: 0px auto; margin-top: 50px;" src="offline_data/images/'+pic+'"><div style="text-align: center; margin-top: -20px;"><h1 class="name">'+fname+' '+lname+'</h1><h2 class="event">'+attendance_event2+'</h2><h2 class="status"><img style="margin-top: -20px;" height="80" width="80" src="cancel.gif"><div style="margin-top: -40px;"><p style="color: red;">Attendance Revoked</p></h2><p class="date">'+date+'</p><p class="time">'+current_time+'</p></div><br></div></div><footer style="position: fixed; text-align: center; width: 100%; bottom: 5px; left:0;">SmartChurch Attendance System Copyright &copy; '+str(datetime.now().year)+'.</footer><style type="text/css">body{user-select: none;}</style></body></html>'
                                #write to html file and reload browser 
                                log = open(resource_path("smart-church/resources/app/index.html"),"w")
                                log.write(html)
                                log.close()
                                update_local_db(userdata, fname, lname, attendance_event2, date, gender, current_time, "delete")
                                # pyautogui.click(x,y)
                                win_title = win32gui.GetWindowText(win32gui.GetForegroundWindow())
                                if win_title != 'SMART Church App':

                                        keyboard.release('windows')
                                        keyboard.send('windows+m')
                                        time.sleep(0.5)
                                                
                                # pyautogui.click(x,y)
                                keyboard.send('esc')
                                win32gui.SetForegroundWindow(BrowserFrame)       
                                keyboard.send('ctrl+r')
                                count = 0
                                attendee = 1

                        else:
                                attendance_data.append(userdata)
                                attendance_data.append(fname)
                                attendance_data.append(lname)
                                attendance_data.append(gender)
                                attendance_data.append(attendance_event2)
                                attendance_data.append(date)
                                attendance_data.append(current_time)
                                #wx.CallAfter(print,attendance_data)
                                cipher2 = MyCipher()
                                encrypt_storage = cipher2.encrypt_includes_iv(str(attendance_data))
                                encrypted_storage = encrypt_storage.decode()
                                log_offline_attendance = open("c:/ProgramData/SmartChurchApp/offline_data/"+file,"w")
                                #wx.CallAfter(log_offline_attendance.write,encrypted_storage)
                                #wx.CallAfter(log_offline_attendance.close)
                                log_offline_attendance.write(encrypted_storage)
                                log_offline_attendance.close()
        
                                html = '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>SmartChurch Offline Attendance</title></head><body style="background-color:#c9c9c9; font-family: Arial Narrow;" ondragstart="return false;"><div style="position: absolute;top: 0; right: 0;left: 0; height: 30px; font-size: 24px; color: #ffffff; background-color: red; text-align: center; padding: 10px;">OFFLINE ATTENDANCE</div><div style="height: 100%; padding: 10px; border:none; margin-left: 5%; margin-right: 5%; background-color: #ffffff;"><img style="display: block; margin: 0px auto; margin-top: 50px;" src="offline_data/images/'+pic+'"><div style="text-align: center; margin-top: -20px;"><h1 class="name">'+fname+' '+lname+'</h1><h2 class="event">'+attendance_event2+'</h2><h2 class="status"><img style="margin-top: -20px;" height="100" width="100" src="tick.gif"><div style="margin-top: -50px;"><p style="color: green;">Attendance Success</p></h2><p class="date">'+date+'</p><p class="time">'+current_time+'</p></div><br></div></div><footer style="position: fixed; text-align: center; width: 100%; bottom: 5px; left:0;">SmartChurch Attendance System Copyright &copy; '+str(datetime.now().year)+'.</footer><style type="text/css">body{user-select: none;}</style></body></html>'
                                #write to html file and reload browser 
                                log = open(resource_path("smart-church/resources/app/index.html"),"w")
                                #wx.CallAfter(log.write,html)
                                #wx.CallAfter(log.close)
                                log.write(html)
                                log.close()
                                update_local_db(userdata, fname, lname, attendance_event2, date, gender, current_time, "insert")
                                # pyautogui.click(x,y)
                                win_title = win32gui.GetWindowText(win32gui.GetForegroundWindow())
                                if win_title != 'SMART Church App':
                                        keyboard.release('windows')        
                                        keyboard.send('windows+m')
                                        time.sleep(0.5)
                                                
                                # pyautogui.click(x,y)
                                keyboard.send('esc')
                                win32gui.SetForegroundWindow(BrowserFrame)        
                                keyboard.send('ctrl+r')
                                count = 0
                                attendee = 1
                else:
                        
                    html = '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>SmartChurch Offline Attendance</title></head><body style="background-color:#c9c9c9; font-family: Arial Narrow;" ondragstart="return false;"><div style="position: absolute;top: 0; right: 0;left: 0; height: 30px; font-size: 24px; color: #ffffff; background-color: red; text-align: center; padding: 10px;">OFFLINE ATTENDANCE</div><div style="height: 100%; padding: 10px; border:none; margin-left: 5%; margin-right: 5%; background-color: #ffffff;"><img style="display: block; margin: 0px auto; margin-top: 50px;" height="300" width="300" src="unknown-user.png"><div style="text-align: center; margin-top: -20px;"><h1 class="name">MEMBER NOT FOUND</h1><h2 class="status"><img style="margin-top: -20px;" height="80" width="80" src="cancel.gif"><div style="margin-top: -40px;"><p style="color: red;">UNKNOWN / UNREGISTERD USER</p></h2></div><br></div></div><footer style="position: fixed; text-align: center; width: 100%; bottom: 5px; left:0;">SmartChurch Attendance System Copyright &copy; '+str(datetime.now().year)+'.</footer><style type="text/css">body{user-select: none;}</style></body></html>'
                    # write to html file and reload browser
                    log = open(resource_path("smart-church/resources/app/index.html"), "w")
                    log.write(html)
                    log.close()
                    # pyautogui.click(x,y)
                    win_title = win32gui.GetWindowText(win32gui.GetForegroundWindow())
                    if win_title != 'SMART Church App':

                        keyboard.release('windows')    
                        keyboard.send('windows+m')
                        time.sleep(0.5)
                                
                    # pyautogui.click(x,y)
                    keyboard.send('esc')
                    win32gui.SetForegroundWindow(BrowserFrame)
                    keyboard.send('ctrl+r')
                    count = 0
                    attendee = 1


        except Exception as k:

                #wx.CallAfter(print,str(k))
                
                html = '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>SmartChurch Offline Attendance</title></head><body style="background-color:#c9c9c9; font-family: Arial Narrow;" ondragstart="return false;"><div style="position: absolute;top: 0; right: 0;left: 0; height: 30px; font-size: 24px; color: #ffffff; background-color: red; text-align: center; padding: 10px;">OFFLINE ATTENDANCE</div><div style="height: 100%; padding: 10px; border:none; margin-left: 5%; margin-right: 5%; background-color: #ffffff;"><img style="display: block; margin: 0px auto; margin-top: 50px;" height="300" width="300" src="unknown-user.png"><div style="text-align: center; margin-top: -20px;"><h1 class="name">MEMBER NOT FOUND</h1><h2 class="status"><img style="margin-top: -20px;" height="80" width="80" src="cancel.gif"><div style="margin-top: -40px;"><p style="color: red;">UNKNOWN / UNREGISTERD USER</p></h2></div><br></div></div><footer style="position: fixed; text-align: center; width: 100%; bottom: 5px; left:0;">SmartChurch Attendance System Copyright &copy; '+str(datetime.now().year)+'.</footer><style type="text/css">body{user-select: none;}</style></body></html>'
                #write to html file and reload browser
                log = open(resource_path("smart-church/resources/app/index.html"),"w")
                log.write(html)
                log.close()
                # pyautogui.click(x,y)
                win_title = win32gui.GetWindowText(win32gui.GetForegroundWindow())
                if win_title != 'SMART Church App':
                        keyboard.release('windows')
                        keyboard.send('windows+m')
                        time.sleep(0.5)
                                
                # pyautogui.click(x,y)
                keyboard.send('esc')
                win32gui.SetForegroundWindow(BrowserFrame)
                keyboard.send('ctrl+r')
                count = 0
                attendee = 1

        return

                

                                



def find_web_browser(self,com_port,hardware_id,computer_name,attendance_event,mode,date,timer):

        
    Error = 0
    if mode == "Offline_attendance":
            name = attendance_event.split("(")[0]
            name = name.replace(" ","")
            #wx.CallAfter(print,name)
            try:
                    
                    
                    with open(resource_path("smart-church/resources/app/offline_data/offline.file"), "r") as f_content:
                            
                            cipher = MyCipher()
                            offline_list = cipher.decrypt_includes_iv(f_content.read())
                            offline_list = offline_list.decode()
                            offline_list = ast.literal_eval(offline_list)
                            #wx.CallAfter(print,offline_list)
                            
            except Exception as decrypt_error:
                    Error = 1
                    wx.CallAfter(self.Parent.Show)
                    time.sleep(0.5)
                    wx.CallAfter(wx.MessageBox,'Membership Data As Stored on This Machine Was Maliciously Modified.\nPlease Kindly Re-Download', 'Membership Offline Data Corruption', wx.OK | wx.ICON_ERROR)
                    sys.exit()
                    
                    
            global attendance_data
            if not glob('c:/ProgramData/SmartChurchApp/offline_data/attendance_'+name+'_'+date+'.file'):

                    file = "attendance_"+name+"_"+date+".file"

                    offline_attendance = open("c:/ProgramData/SmartChurchApp/offline_data/"+file,"w")
                    attendance_data = []
                    offline_attendance.close()
                    
            else:
                    file = "attendance_"+name+"_"+date+".file"
                                    
                    if os.path.getsize('c:/ProgramData/SmartChurchApp/offline_data/'+file)==0:
                            
                            attendance_data = []
                            
                    else:
                             with open("c:/ProgramData/SmartChurchApp/offline_data/"+file,"r") as f_content:

                                     try:
                                             
                                   
                                             cipher = MyCipher()
                                             offline_attendance = cipher.decrypt_includes_iv(f_content.read())
                                             offline_attendance = offline_attendance.decode()
                                             offline_attendance = ast.literal_eval(offline_attendance)
                                             attendance_data = offline_attendance
                                             
                                     except Exception as err:
                                             Error = 1
                                             attendance_data = []
                                             wx.CallAfter(self.Parent.Show)
                                             time.sleep(0.5)
                                             wx.CallAfter(wx.MessageBox,'The Offline Attendance Data For This Event Was Maliciously Modified.\nPlease Kindly Ask Those Who Have Marked Their Attendance To Have It Retaken.', 'Offline Attendance Data Corruption', wx.OK | wx.ICON_ERROR)
                                             log_offline_attendance = open("c:/ProgramData/SmartChurchApp/offline_data/"+file,"w")
                                             log_offline_attendance.write("")
                                             log_offline_attendance.close()
                                             
                                             
                            
                            
                    
           
    while 1:
        
        BrowserFrame = win32gui.FindWindow(None, "SMART Church App")
        hwnd = win32gui.FindWindowEx(None,None,None,"Smart Church Loader")
        if BrowserFrame:
            if Error == 1:
                    win32gui.PostMessage(BrowserFrame, win32con.WM_CLOSE,0,0)
                    sys.exit()
            if hwnd:

                time.sleep(3)
                win32gui.ShowWindow(BrowserFrame, win32con.SW_MAXIMIZE)
                self.Parent.Hide()
                browser_window = 2
                break

            
            else:
                win32gui.ShowWindow(BrowserFrame, win32con.SW_MAXIMIZE)
                self.Parent.Hide()
                browser_window = 2
                break

        else:

            pass
        
    # start thread to monitor web browser and to display main app if it is closed
    global browser_monitor
    set_keepawake(keep_screen_awake=True)
    if browser_monitor == 0 or browser_monitor == 2:

        monitor_browser_thread = threading.Thread(target=monitor_web_browser, args=(self, BrowserFrame,com_port))
        monitor_browser_thread.daemon = True
        monitor_browser_thread.start()
    global s
    global retryconnect
    #start thread to monitor browser window
    while browser_window == 2 or retryconnect == 1:
            
        #Try disconnect reader if connected
        try:
            s = serial.Serial(com_port, 9600, timeout=1, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
            s.flush()
            time.sleep(0.5)
            s.close()
            #wx.CallAfter(print, "Attempt Reader Connection..")

            if BrowserFrame:
                win32gui.ShowWindow(BrowserFrame, win32con.SW_MAXIMIZE)
                browser_window = 3
                break


            else:

                browser_window = 3
                break

        except Exception as p:
            #wx.CallAfter(print,"Error  Connecting..")
            #wx.CallAfter(print, mode)

            try:
                    
                time.sleep(0.5)
                s.flush()
                s.close()

                if BrowserFrame:
                    
                    win32gui.ShowWindow(BrowserFrame, win32con.SW_MAXIMIZE)
                    browser_window = 3
                    break


                else:
                    browser_window = 3
                    break

            except Exception as k:

                if BrowserFrame:
                        
                    win32gui.ShowWindow(BrowserFrame, win32con.SW_MAXIMIZE)
                    browser_window = 3
                    break

                else:
                    browser_window = 3
                    break

    #wx.CallAfter(print,mode)
    if attendance_event == "Admin_card_binding":

            URL = 'https://smartchurchattendance.com.ng/smartChurch/api/RegisterDevice'
            data = '['+'"'+computer_name+'"'+','+'"'+hardware_id+'"'+']'
            cipher = MyCipher()
            data = cipher.encrypt_includes_iv(data)
            data = data.decode()
            try:
                    resp = requests.post(URL, data=data, verify=False)
                    if "Already" not in resp.text:
                            
                            wx.CallAfter(clean_up,"c:/ProgramData/SmartChurchApp/offline_data")
                            wx.CallAfter(clean_up,resource_path("smart-church/resources/app/offline_data"))
                            #close browser with error warning
                            if BrowserFrame:

                                    response = win32gui.MessageBox(BrowserFrame,"This Device is Not Registered Or Awaiting Church Leadership Approval And Therefore Cannot Bind Cards.","Smart Church Device Registration Error",win32con.MB_OK|win32con.MB_ICONERROR)
                                    win32gui.PostMessage(BrowserFrame, win32con.WM_CLOSE,0,0)
                                    wx.CallAfter(self.Parent.Show)
                                    return
                    else:
                            pass

            except Exception as connect_err:
                    #Retry Connection or Exit
                    if BrowserFrame:

                            # toaster = ToastNotifier()
                            # toaster.show_toast("Smart Church", "Could Not Conect to Server, Please Try After Some Time...",
                            #                    icon_path=resource_path("ClipartKey_1167914.ico"), duration=5, threaded=True)
                            # win32gui.PostMessage(BrowserFrame, win32con.WM_CLOSE, 0, 0)
                            # wx.CallAfter(self.Parent.Show)
                            # return

                            response = win32gui.MessageBox(BrowserFrame,"Could Not Connect To Remote Server\nWould You like To Retry Connection or Try Again Later?","Smart Church Connection Error",win32con.MB_RETRYCANCEL|win32con.MB_ICONQUESTION)
                            if response == win32con.IDRETRY:

                                    #wx.CallAfter(find_web_browser,self,com_port,hardware_id,computer_name,attendance_event,mode,date)
                                    absl = threading.Thread(target=find_web_browser,args=(self, com_port,hardware_id,computer_name,attendance_event,mode,date,timer))
                                    absl.daemon = True
                                    absl.start()
                                    return

                            elif response == win32con.IDCANCEL:

                                    win32gui.PostMessage(BrowserFrame, win32con.WM_CLOSE,0,0)
                                    wx.CallAfter(self.Parent.Show)
                                    return

    
    global count
    count = 0
    #time.sleep(1)
    global Dialogucount
    monitor_count = threading.Thread(target=run_count, args=(self,BrowserFrame,mode))
    monitor_count.daemon = True
    monitor_count.start()
    
    while browser_window == 3:
        count = count + 1

        if BrowserFrame:
                
                if Dialogucount == 16:
                        monitor_count = threading.Thread(target=run_count, args=(self,BrowserFrame,mode))
                        monitor_count.daemon = True
                        monitor_count.start()
                        
                try:
                        tup = win32gui.GetWindowPlacement(BrowserFrame)
                        if tup[1] == win32con.SW_SHOWMINIMIZED:
                                win32gui.ShowWindow(BrowserFrame, win32con.SW_MAXIMIZE)
                                #win32gui.SetForegroundWindow(BrowserFrame)
                        else:
                                
                                win_title = win32gui.GetWindowText(win32gui.GetForegroundWindow())

                                if win_title != 'SMART Church App':

                                        keyboard.send('esc')

                except Exception as d:

                       # wx.CallAfter(print,str(d))
                        pass
                try:
                        Dialogucount = 0
                        if not timer:
                                return
                        s = serial.Serial(com_port, 9600, timeout=None, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
                        res = s.read(8)
                        res = res.rstrip()
                        #wx.CallAfter(print,res)
                        s.flush()
                        time.sleep(0.5)
                        s.close()

                        BrowserFrame2 = win32gui.FindWindow(None, "SMART Church App")

                        if not BrowserFrame2:

                                wx.CallAfter(self.Parent.Show)
                                return
                                #time.sleep(0.5)
                                #wx.MessageBox('Connection To Smart Church Reader Was Lost.\nReason: Embedded Web Browser Was Closed.', 'Smart Reader Disconnection Notice', wx.OK | wx.ICON_INFORMATION)

                        if res != "":
                                frequency = 2500
                                duration = 300
                        if str(res) != "b''":
                                #wx.CallAfter(print,res)
                                winsound.Beep(frequency, duration)
                                userdata = res.decode()
                                userdata = str(userdata)# data recieved from RFID through USB PORT
                                userdata = userdata.replace("'","")
                                userdata= userdata.rstrip()
                                

                                if mode == "Offline_attendance":
                                        
                                        offline_thread = threading.Thread(target=offline_attendance2,args=(com_port,hardware_id,computer_name,attendance_event,mode,date,name,offline_list,userdata,file,BrowserFrame))
                                        offline_thread.daemon = True
                                        offline_thread.start()

                                elif mode == "Online_attendance":

                                        URL = 'https://smartchurchattendance.com.ng/smartChurch/api/OnlineAttendance'
                                        attendance_event2 = attendance_event.split("(")[0]

                                        data2 = '['+'"'+computer_name+'"'+','+'"'+hardware_id+'"'+','+'"'+userdata+'"'+','+'"'+attendance_event2+'"'+']'
                                        try:

                                                cipher2 = MyCipher()
                                                data2 = cipher2.encrypt_includes_iv(data2)
                                                data2 = data2.decode()
                                                resp2 = requests.post(URL, data=data2, verify=False, timeout=3)
                                                #wx.CallAfter(print,resp2.text)

                                        except Exception as e:
                                                Dialogucount = 16
                                                
                                                if BrowserFrame:
                                                        
                                                        try:
                                                                if not timer:
                                                                        return
                                                                # toaster = ToastNotifier()
                                                                # toaster.show_toast("Smart Church", "Could Not Conect to Server, Please Swipe Card Again in 5 seconds, Retrying Connection....", icon_path=resource_path("ClipartKey_1167914.ico"), duration=5, threaded=True)
                                                                # subprocess.Popen(['Toast/CSAToast.exe', 'Could Not Conect to Server, Please Swipe Card Again in 5 seconds, Retrying Connection....'])
                                                                wx.CallAfter(subprocess.Popen,['Toast/CSAToast.exe', 'Could Not Conect to Server, Please Swipe Card Again, Retrying Connection....'])
                                                                wx.CallAfter(refresh_timer_gif,timer)
                                                                time.sleep(5)
                                                                wx.CallAfter(timer.Hide)
                                                                s.close()
                                                                Dialogucount = 0


                                                                 # response = win32gui.MessageBox(BrowserFrame,"Could Not Connect To Remote Server\nWould You like To Retry Connection or Start Offline Attendance Session?","Smart Church Online Attendance Error",win32con.MB_RETRYCANCEL|win32con.MB_ICONQUESTION)
                                                                 # if response == win32con.IDRETRY:
                                                                 #         Dialogucount = 0
                                                                 #         pass
                                                                 #
                                                                 # elif response == win32con.IDCANCEL:
                                                                 #        Dialogucount = 0
                                                                 #        win32gui.PostMessage(BrowserFrame, win32con.WM_CLOSE,0,0)
                                                                 #        wx.CallAfter(self.Parent.Show)
                                                                 #        return

                                                        except Exception as h:
                                                                 
                                                                 wx.CallAfter(self.Parent.Show)
                                                                 wx.CallAfter(wx.MessageBox,'Connection To Smart Church Reader Was Lost.\nReason: Embedded Web Browser was Closed.', 'Smart Reader Error', wx.OK | wx.ICON_INFORMATION)
                                                                 return

                                elif mode == "Bind_Smart_Cards":

                                        URL = 'https://smartchurchattendance.com.ng/smartChurch/api/BindCards'
                                        data = '['+'"'+computer_name+'"'+','+'"'+hardware_id+'"'+','+'"'+userdata+'"'+']'

                                        try:

                                                cipher3 = MyCipher()
                                                data = cipher3.encrypt_includes_iv(data)
                                                data = data.decode()
                                                resp2 = requests.post(URL, data=data, verify=False, timeout=3)
                                                #wx.CallAfter(print,resp2.text)

                                        except Exception as e:

                                                Dialogucount = 16
                                                
                                                if BrowserFrame:

                                                        try:
                                                                if not timer:
                                                                        return
                                                                # toaster = ToastNotifier()
                                                                # toaster.show_toast("Smart Church", "Could Not Conect to Server, Please Swipe Card Again in 5 seconds, Retrying Connection....", icon_path=resource_path("ClipartKey_1167914.ico"), duration=5, threaded=True)
                                                                wx.CallAfter(subprocess.Popen,['Toast/CSAToast.exe', 'Could Not Conect to Server, Please Swipe Card Again, Retrying Connection....'])
                                                                # subprocess.Popen(['Toast/CSAToast.exe', 'Could Not Conect to Server, Please Swipe Card Again in 5 seconds, Retrying Connection....'])
                                                                wx.CallAfter(refresh_timer_gif,timer)
                                                                time.sleep(5)
                                                                wx.CallAfter(timer.Hide)
                                                                s.close()
                                                                Dialogucount = 0
                                                                
                                                        
                                                                # response = win32gui.MessageBox(BrowserFrame,"Could Not Connect To Remote Server\nWould You like To Retry Connection or Try Again Later?","Smart Church Card Binding Error",win32con.MB_RETRYCANCEL|win32con.MB_ICONQUESTION)
                                                                # if response == win32con.IDRETRY:
                                                                #         Dialogucount = 0
                                                                #         pass
                                                                #
                                                                # elif response == win32con.IDCANCEL:
                                                                #         Dialogucount = 0
                                                                #         win32gui.PostMessage(BrowserFrame, win32con.WM_CLOSE,0,0)
                                                                #         wx.CallAfter(self.Parent.Show)
                                                                #         return



                                                        except Exception as n:
                                                                
                                                                win32gui.PostMessage(BrowserFrame, win32con.WM_CLOSE,0,0)
                                                                wx.CallAfter(self.Parent.Show)
                                                                time.sleep(0.5)
                                                                wx.CallAfter(wx.MessageBox,'Connection To Smart Church Reader Was Lost.\nReason: Embedded Web Browser was Closed.', 'Smart Reader Error', wx.OK | wx.ICON_INFORMATION)
                                                                return







                except Exception as e:
                         
                         if BrowserFrame:

                                 try:
                                         
                                         Dialogucount = 16
                                         response = win32gui.MessageBox(BrowserFrame,"Unable To Connect Smart Card Reader To: "+com_port+".\nWould You like To Retry Connection or Start Your Session All Over Again?","Smart Church Card Reader Conection Error",win32con.MB_RETRYCANCEL|win32con.MB_ICONQUESTION)
                                         if response == win32con.IDRETRY:
                                                 time.sleep(0.5)
                                                 s.close()
                                                 Dialogucount = 0
                                                 absl = threading.Thread(target=find_web_browser,args=(self, com_port,hardware_id,computer_name,attendance_event,mode,date,timer))
                                                 absl.daemon = True
                                                 absl.start()
                                                 #wx.CallAfter(find_web_browser,self,com_port,hardware_id,computer_name,attendance_event,mode,date)
                                                 retryconnect = 1
                                                 return


                                         elif response == win32con.IDCANCEL:

                                                Dialogucount = 0
                                                win32gui.PostMessage(BrowserFrame, win32con.WM_CLOSE,0,0)
                                                wx.CallAfter(self.Parent.Show)
                                                retryconnect = 0
                                                return

                                 except Exception as h:
                                        
                                        pass


                         elif not BrowserFrame:
                                 
                                 wx.CallAfter(self.Parent.Show)
                                 time.sleep(0.5)
                                 wx.CallAfter(wx.MessageBox,'Could Not Connect Smart Church Card Reader', 'Smart Reader Error', wx.OK | wx.ICON_ERROR)
                                 return


        else:
                
                
                wx.CallAfter(self.Parent.Show)
                time.sleep(0.5)
                wx.CallAfter(wx.MessageBox,'Could Not Connect Smart Church Card Reader', 'Smart Reader Error', wx.OK | wx.ICON_ERROR)
                return


        
def resource_path(relative_path):
    
        
    try:

        base_path = sys._MEIPASS
            
    except Exception:

        base_path = os.path.abspath(".")
            
    return os.path.join(base_path, relative_path)

def set_reg(name, reg_path, value):
            
            try:
                    
                    winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)
                    registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_WRITE)
                    winreg.SetValueEx(registry_key, name, 0, winreg.REG_DWORD, value)
                    winreg.CloseKey(registry_key)
                    return True
            except WindowsError:
                    return False
def get_reg(name, reg_path):

        try:
                registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_READ)
                value, regtype = winreg.QueryValueEx(registry_key, name)
                winreg.CloseKey(registry_key)
                return value
        
        except WindowsError:
                
                return None

###########################################################################
## Class Smart Church Clinent
###########################################################################

class Smart_Church_Clinent ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Smart Church Client", pos = wx.DefaultPosition, size = wx.Size( 0,0 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.FRAME_NO_TASKBAR|wx.SYSTEM_MENU|wx.BORDER_NONE|wx.TAB_TRAVERSAL|wx.STAY_ON_TOP )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.Colour( 207, 207, 207 ) )
        self.SetIcon(wx.Icon(resource_path("ClipartKey_1167914.ico")))
        self.Bind(wx.EVT_CLOSE, self.close_app)

        ###
        bSizer2 = wx.BoxSizer( wx.VERTICAL )

        bSizer9 = wx.BoxSizer( wx.VERTICAL )

        gbSizer1 = wx.GridBagSizer( 0, 0 )
        gbSizer1.SetFlexibleDirection( wx.BOTH )
        gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_staticText24 = wx.StaticText( self, wx.ID_ANY, u"                  ", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText24.Wrap( -1 )

        gbSizer1.Add( self.m_staticText24, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        self.m_staticText25 = wx.StaticText( self, wx.ID_ANY, u"                        ", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText25.Wrap( -1 )

        gbSizer1.Add( self.m_staticText25, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        self.m_staticText26 = wx.StaticText( self, wx.ID_ANY, u"               ", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText26.Wrap( -1 )

        gbSizer1.Add( self.m_staticText26, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )


        self.m_bpButton2 = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_NONE|wx.BU_AUTODRAW|0 )
        self.m_bpButton2.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_PRINT, wx.ART_BUTTON ) )
        gbSizer1.Add( self.m_bpButton2, wx.GBPosition( 0, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        self.m_bpButton2.SetBackgroundColour( wx.Colour( 207, 207, 207 ) )
        self.m_bpButton2.SetToolTip( u"Print Offline Report" )

        self.m_bitmap7 = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_NONE|wx.BU_AUTODRAW|0 )
        self.m_bitmap7.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_FILE_OPEN, wx.ART_BUTTON ) )
        gbSizer1.Add( self.m_bitmap7, wx.GBPosition( 0, 4 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        self.m_bitmap7.SetBackgroundColour( wx.Colour( 207, 207, 207 ) )
        self.m_bitmap7.SetToolTip( u"Offline Log" )

        self.m_bpButton1 = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_NONE|wx.BU_AUTODRAW|0 )
        self.m_bpButton1.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_TIP, wx.ART_BUTTON ) )
        gbSizer1.Add( self.m_bpButton1, wx.GBPosition( 0, 5 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        self.m_bpButton1.SetBackgroundColour( wx.Colour( 207, 207, 207 ) )
        self.m_bpButton1.SetToolTip( u"About Software" )
        
        bSizer9.Add( gbSizer1, 1, wx.EXPAND, 5 )


        bSizer2.Add( bSizer9, 1, wx.EXPAND, 5 )
        #####

        #self.m_bpButton1 = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 20,20 ), wx.BORDER_NONE )

        #self.m_bpButton1.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_TIP, wx.ART_BUTTON ) )
        #bSizer2.Add( self.m_bpButton1, 0, wx.ALIGN_RIGHT|wx.ALIGN_TOP|wx.ALL|wx.SHAPED|wx.TOP, 5 )
        #self.m_bpButton1.SetBackgroundColour( wx.Colour( 207, 207, 207 ) )
        #self.m_bpButton1.SetToolTip( u"About Software" )

        self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer2.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_bitmap1 = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap( resource_path(u"ClipartKey_1167914.bmp"), wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BORDER_NONE )
        bSizer2.Add( self.m_bitmap1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"SMART Church App", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.BORDER_THEME )
        self.m_staticText1.Wrap( -1 )

        self.m_staticText1.SetFont( wx.Font( 15, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        #self.m_staticText1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHTTEXT ) )

        bSizer2.Add( self.m_staticText1, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        self.m_staticline3 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer2.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5 )

        sbSizer9 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Attendance Actions" ), wx.VERTICAL )
        gSizer5 = wx.GridSizer( 0, 2, 0, 0 )


        bSizer2.Add( sbSizer9, 1, wx.ALL|wx.EXPAND, 5 )
        sbSizer9.Add( gSizer5, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_button2 = wx.Button( self, wx.ID_ANY, u"Register Visitors", wx.DefaultPosition, wx.DefaultSize, wx.BORDER_NONE|wx.BU_EXACTFIT )
        self.m_button2.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        self.m_button2.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )
        self.m_button2.SetBackgroundColour( wx.Colour( 48, 203, 39 ) )
        self.m_button2.SetToolTip( u"Add Visitors" )

        gSizer5.Add( self.m_button2, 0, wx.ALL|wx.ALIGN_LEFT, 5 )

        self.m_button3 = wx.Button( self, wx.ID_ANY, u"Online Attendance", wx.DefaultPosition, wx.DefaultSize, wx.BORDER_NONE|wx.BU_EXACTFIT )
        self.m_button3.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        self.m_button3.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )
        self.m_button3.SetBackgroundColour( wx.Colour( 0, 128, 255 ) )
        self.m_button3.SetToolTip( u"Connect For Online Attendance" )

        gSizer5.Add( self.m_button3, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )

        self.m_button4 = wx.Button( self, wx.ID_ANY, u"Offline Attendance", wx.DefaultPosition, wx.DefaultSize, wx.BORDER_NONE|wx.BU_EXACTFIT )
        self.m_button4.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        #self.m_button4.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )
        self.m_button4.SetBackgroundColour( wx.Colour( 131, 188, 222 ) )
        self.m_button4.SetToolTip( u"Take Attendance on Local Machine" )

        gSizer5.Add( self.m_button4, 0, wx.ALL|wx.ALIGN_LEFT, 5 )

        self.m_button9 = wx.Button( self, wx.ID_ANY, u"Bind Smart Card", wx.DefaultPosition, wx.DefaultSize, wx.BORDER_NONE|wx.BU_EXACTFIT )
        self.m_button9.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        #self.m_button9.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )
        self.m_button9.SetBackgroundColour( wx.Colour( 255, 151, 47 ) )
        self.m_button9.SetToolTip( u"Register Members Smart Card" )

        sbSizer9.Add( self.m_button9, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )

        self.m_button5 = wx.Button( self, wx.ID_ANY, u"Download Data", wx.DefaultPosition, wx.DefaultSize, wx.BORDER_NONE|wx.BU_EXACTFIT )
        self.m_button5.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        self.m_button5.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )
        self.m_button5.SetBackgroundColour( wx.Colour( 255, 40, 40 ) )
        self.m_button5.SetToolTip( u"Download Membership Data To Local machine" )

        sbSizer9.Add( self.m_button5, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
        self.m_button5.Hide()
        

        self.m_button51 = wx.Button( self, wx.ID_ANY, u"Register Device", wx.DefaultPosition, wx.DefaultSize, wx.BORDER_NONE|wx.BU_EXACTFIT )
        self.m_button51.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        #self.m_button51.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )
        self.m_button51.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNSHADOW ) )
        self.m_button51.SetToolTip( u"Register Device Online" )

        gSizer5.Add( self.m_button51, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
        #self.m_button3.Hide()

        self.loading = wx.Button( self, wx.ID_ANY, u"", wx.DefaultPosition, wx.Size(0,0),wx.BORDER_NONE )
        self.loading.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        sbSizer9.Add( self.loading, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
        self.loading.Hide()

        gSizer1 = wx.GridSizer( 0, 2, 0, 0 )

        self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText11.Wrap( -1 )

        gSizer1.Add( self.m_staticText11, 0, wx.ALL, 5 )

        self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, u"       Copyright © "+str(datetime.now().year), wx.DefaultPosition, wx.DefaultSize, 0|wx.BORDER_NONE )
        self.m_staticText12.Wrap( -1 )

        self.m_staticText12.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL, False, "Arial Rounded MT Bold" ) )
        #self.m_staticText12.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )

        gSizer1.Add( self.m_staticText12, 0, wx.ALL, 5 )


        bSizer2.Add( gSizer1, 1, wx.EXPAND, 5 )

        wSizer1 = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )


        bSizer2.Add( wSizer1, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer2 )
        self.Layout()

        self.Centre( wx.BOTH )
        
        self.hardwrid = check_output('wmic csproduct get uuid',shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        self.hardwrid = self.hardwrid.decode().strip()
        self.hardwrid = self.hardwrid.replace('UUID','')
        self.hardwrid = self.hardwrid.replace('-','')
        self.hardwrid = self.hardwrid.strip()
        self.cpt_name = os.environ['COMPUTERNAME']
        self.cpt_name = self.cpt_name.replace('-','')
        self.cpt_name = self.cpt_name.replace('_','')
        self.cpt_name= self.cpt_name.strip()
        #time.sleep(0.5)
        #dlg = InfoDialogue(self)
        #dlg.ShowModal()


        # Connect Events
        self.loading.Bind( wx.EVT_BUTTON, self.start_modal )
        self.m_bpButton1.Bind( wx.EVT_BUTTON, self.About_Software )
        self.m_bitmap7.Bind( wx.EVT_BUTTON, self.launch_browser )
        self.m_button2.Bind( wx.EVT_BUTTON, self.add_visitors )
        self.m_button3.Bind( wx.EVT_BUTTON, self.launchOnlinDialogue )
        self.m_button4.Bind( wx.EVT_BUTTON, self.LaunchOfflineDialogue )
        self.m_button5.Bind( wx.EVT_BUTTON, self.DownloadOnlineData )
        self.m_button9.Bind( wx.EVT_BUTTON, self.bind_card )
        self.m_button51.Bind( wx.EVT_BUTTON, self.RegisterDevice )
        self.m_bpButton2.Bind( wx.EVT_BUTTON, self.lauchLocalAttendanceDialogue )
        
        evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId,self.loading.GetId())
        wx.PostEvent(self.loading, evt)
        
       

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class

    def launch_browser(self,event):
            file_path = 'c:/ProgramData/SmartChurchApp/SmatChurch.log'
            
            try:
                    with open(file_path, "r") as f_content:

                            data = f_content.readlines()   
                            log = open(resource_path("smart-church/resources/app/offline_log.html"),"w")
                            log.write('<!DOCTYPE html><!-- saved from url=(0016)http://localhost -->\n<html><head><meta charset="UTF-8"><title>SmartChurch Offline Attendance Logs</title><style>.highlight{ background:yellow; padding:1px; border:#00CC00 dotted 1px; }</style></head><body oncontextmenu="return false;" style="background-color:#c9c9c9; font-family: Arial Narrow;" ondragstart="return false;"><br><h2 style="text-align: center;">OFFLINE APPLICATION LOG</h2><br><div id="search" align="center"><input style="padding: 8px;" type="text" id="search_data" placeholder="Enter Search Keyword" />&nbsp;&nbsp;&nbsp;<button style="cursor: pointer; padding: 8px;" id="search_data_key" type="button" onclick="var box = document.getElementById(\'search_area\'); var textbox = textarea; var search = document.getElementById(\'search_data\');var searchText = search.value; if(searchText == \'\' || searchText.length <=2){alert(\'Search Keyword length Must Be Greater Than Two.\'); return;}var regex = new RegExp(searchText, \'gi\');   var newText = textbox.replace(regex, \'<mark class=\\\'highlight\\\'>$&</mark>\'); box.innerHTML = newText; if(box.innerHTML == textarea){alert(\'Search Keyword Not Found\');}">Search Keyword</button></div><br><div id="search_area" style="margin-left:5%; margin-right:5%; padding: 10px; background-color:#ffffff; border-top:2px solid blue;">')
                            log.write('<hr>'.join(data))
                            log.write('</div><br><br><script>var textarea = document.getElementById(\'search_area\').innerHTML;</script></body></html>')
                            log.close()
                            time.sleep(0.5)
                            fr = wx.Dialog(self, id = wx.ID_ANY, title = u"SMART CHURCH OFFLINE APP DATA LOG", pos = wx.DefaultPosition, size = wx.Size(wx.DisplaySize()), style = wx.CAPTION|wx.CLOSE_BOX|wx.FRAME_NO_TASKBAR|wx.SYSTEM_MENU|wx.BORDER_NONE|wx.TAB_TRAVERSAL|wx.STAY_ON_TOP)
                            fr.SetIcon(wx.Icon(resource_path("ClipartKey_1167914.ico")))
                            reg_path = r"Software\\Microsoft\\Internet Explorer\\Main\\FeatureControl\\FEATURE_BROWSER_EMULATION"
                            set_reg(os.path.basename(sys.executable), reg_path, 11001)
                            #print(get_reg(sys.executable, reg_path))
                            #wx.CallAfter(wx.MessageBox,str(get_reg(os.path.basename(sys.executable), reg_path)), 'No Offline Log(s) Error', wx.OK | wx.ICON_ERROR)
                            #print(get_reg(os.path.basename(sys.executable), reg_path))
                            tester = wx.html2.WebView.New(fr, size=(460,460)) 
                            tester.LoadURL(resource_path("smart-church/resources/app/offline_log.html"))
                            fr.ShowModal()
                            fr.Maximize(True)
                            
                            
                            
                            
            except Exception as file_read_error:
                    time.sleep(0.5)
                    wx.CallAfter(wx.MessageBox,"No Offline App Log Available", 'No Offline Log(s) Error', wx.OK | wx.ICON_ERROR)

            
                
            
            
    def close_app(self,event):
            
            BrowserFrame3 = win32gui.FindWindow(None, "Smart Church Client")
            ask = win32gui.MessageBox(BrowserFrame3, "Are You Sure You Want To Exit Smart Church PC Client?\nClick YES To Exit Application, Click NO To Restart Application, Click CANCEL To Stay On Application.","Smart Church PC Client Exit Notice", win32con.MB_YESNOCANCEL|win32con.MB_ICONQUESTION)
            if ask == win32con.IDYES:
                    # check_output('taskkill /f /im SMARTChurchApp.exe',shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                    obfuscate_url()
                    time.sleep(0.5)
                    sys.exit()
            elif ask == win32con.IDNO:
                    # check_output('taskkill /f /im SMARTChurchApp.exe',shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                    obfuscate_url()
                    time.sleep(0.5)
                    #check_output('start CSAS.exe',shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                    subprocess.Popen(['CSAS.exe'], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
                    sys.exit()
            elif ask == win32con.IDCANCEL:
                    return
                
    def start_modal(self, event):
        
        global infoStatus
        dlg = InfoDialogue(self)
        loading_status = threading.Thread(target=load_modal,args=(self,dlg,infoStatus))
        loading_status.daemon = True
        loading_status.start()
        dlg.ShowModal()
        
        
        #dlg.ShowModal()
    def lauchLocalAttendanceDialogue(self, event):
        dlg = localAttendanceDialogue(self)
        dlg.ShowModal()

    def About_Software( self, event ):
        dlg = AboutSoftware(self)
        dlg.ShowModal()

    def add_visitors( self, event ):
        dlg = VisitorDialog(self)
        dlg.ShowModal()

    def launchOnlinDialogue( self, event ):
        dlg = OnlineAttendanceDialogue(self)
        dlg.ShowModal()

    def LaunchOfflineDialogue( self, event ):
        dlg = OfflineEventsDialogue(self)
        dlg.ShowModal()

    def DownloadOnlineData( self, event ):
        ask = wx.MessageDialog(self, "Ensure That This Device is Already Registered Online.\nAny Previous Data Available on Device Will Be Overwritten.\nContinue?",'Data Download Notice', wx.YES_NO | wx.ICON_INFORMATION)
        result = ask.ShowModal()
        
        if result == wx.ID_YES:
            global infoStatus
            infoStatus = "download_offline_data"
            evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId,self.loading.GetId())
            wx.PostEvent(self.loading, evt)
            
        elif result == wx.ID_NO:
            ask.Destroy()
            return

    def bind_card( self, event ):
        #event.Skip()
        dlg = Bind_Card(self)
        dlg.ShowModal()
        
    def RegisterDevice( self, event ):
        
        ask = wx.MessageDialog(self, "This Computer Unique Details will be Sent to Portal\nComputer Name: "+self.cpt_name+".\nComputer ID: "+self.hardwrid+"\nNote That Only Approved Device Will Send Attendance Data.\nContinue?",'Device Registration request', wx.YES_NO | wx.ICON_INFORMATION)
        result = ask.ShowModal()
        
        if result == wx.ID_YES:
            
            global infoStatus
            infoStatus = "register_device"
            evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId,self.loading.GetId())
            wx.PostEvent(self.loading, evt)
        elif result == wx.ID_NO:

            ask.Destroy()
            return




###########################################################################
## Class localAttendanceDialogue
###########################################################################

class localAttendanceDialogue ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Offline Attendnce Report", pos = wx.DefaultPosition, size = wx.Size( 280,240 ), style = wx.DEFAULT_DIALOG_STYLE|wx.FRAME_FLOAT_ON_PARENT )
        
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.Colour( 207, 207, 207 ) )

        bSizer14 = wx.BoxSizer( wx.VERTICAL )

        sbSizer32 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Event Date Range" ), wx.VERTICAL )

        fgSizer9 = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizer9.SetFlexibleDirection( wx.BOTH )
        fgSizer9.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_staticText56 = wx.StaticText( sbSizer32.GetStaticBox(), wx.ID_ANY, u"Attendance Event:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText56.Wrap( -1 )

        self.m_staticText56.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        #self.m_staticText56.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )

        fgSizer9.Add( self.m_staticText56, 0, wx.ALL, 5 )
        global self2
        self2 = self
        global m_choice2Choices
        m_choice2Choices = ["-- LOADING ---"]
        global m_choices
        self.m_choice2 = wx.Choice( sbSizer32.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice2Choices, 0|wx.BORDER_NONE )
        self.m_choice2.SetSelection( 0 )
        fgSizer9.Add( self.m_choice2, 0, wx.ALL|wx.EXPAND, 5 )
        m_choices = self.m_choice2
        fetch_events = threading.Thread(target=get_offline_events,args=(self,self.m_choice2,m_choice2Choices))
        fetch_events.daemon = True
        fetch_events.start()
        self.m_choice2.Disable()

        self.m_staticText15 = wx.StaticText( sbSizer32.GetStaticBox(), wx.ID_ANY, u"Report Start Date: ", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText15.Wrap( -1 )

        self.m_staticText15.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        #self.m_staticText15.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )

        fgSizer9.Add( self.m_staticText15, 0, wx.ALL, 5 )

        self.m_datePicker1 = wx.adv.DatePickerCtrl( sbSizer32.GetStaticBox(), wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.Size( 110,-1 ), wx.adv.DP_DROPDOWN|wx.BORDER_NONE )
        fgSizer9.Add( self.m_datePicker1, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText16 = wx.StaticText( sbSizer32.GetStaticBox(), wx.ID_ANY, u"Report End Date: ", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText16.Wrap( -1 )

        self.m_staticText16.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        #self.m_staticText15.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )

        fgSizer9.Add( self.m_staticText16, 0, wx.ALL, 5 )

        self.m_datePicker2 = wx.adv.DatePickerCtrl( sbSizer32.GetStaticBox(), wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.Size( 110,-1 ), wx.adv.DP_DROPDOWN|wx.BORDER_NONE )
        fgSizer9.Add( self.m_datePicker2, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText17 = wx.StaticText( sbSizer32.GetStaticBox(), wx.ID_ANY, u"Abesentee Report: ", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText17.Wrap( -1 )

        self.m_staticText17.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        #self.m_staticText15.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )

        fgSizer9.Add( self.m_staticText17, 0, wx.ALL, 5 )

        self.m_checkBox2 = wx.CheckBox( sbSizer32.GetStaticBox(), wx.ID_ANY, u"", wx.DefaultPosition, wx.Size( 110,-1 ), 0 )
        fgSizer9.Add( self.m_checkBox2, 0, wx.ALL|wx.EXPAND, 5 )


        # sbSizer30.Add( fgSizer8, 1, wx.EXPAND, 5 )

        # bSizer12.Add( sbSizer30, 1, wx.ALIGN_BOTTOM|wx.ALL|wx.EXPAND, 5 )

        sbSizer32.Add( fgSizer9, 1, wx.EXPAND, 5 )
        bSizer6 = wx.BoxSizer( wx.VERTICAL )
        self.m_button13 = wx.Button(sbSizer32.GetStaticBox(), wx.ID_ANY, u"Generate Report", wx.DefaultPosition, wx.DefaultSize, 0|wx.BORDER_NONE )
        self.m_button13.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        self.m_button13.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )
        self.m_button13.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
        self.m_button13.SetToolTip("Generate Attendance Report")
        bSizer6.Add( self.m_button13, 0, wx.ALL|wx.EXPAND, 5 )
        sbSizer32.Add( bSizer6, 1, wx.EXPAND, 5 )
        bSizer14.Add( sbSizer32, 1,  wx.ALL|wx.EXPAND, 5 )

        # bSizer14.Add( sbSizer32, 1, wx.ALL|wx.EXPAND|wx.RIGHT, 5 )

        self.SetSizer( bSizer14 )
        self.Layout()

        # Connect Events
        self.m_button13.Bind( wx.EVT_BUTTON, self.GeneratelocalReport )
        self.m_choice2.Bind( wx.EVT_CHOICE, self.SetTolTip )
        self.m_choice2.Bind( wx.EVT_MOTION,  self.getString )

    def __del__( self ):
        pass

    def getString(self, event):

        # event.GetEventObject().SetToolTipString("This Works!")
        event.Skip()

    def SetTolTip(self, event):

            self.m_choice2.SetToolTip(self.m_choice2.GetStringSelection())

    def GeneratelocalReport(self, event):

        selectedEventValue = self.m_choice2.GetSelection()
        
        if selectedEventValue == 0:

                wx.MessageBox('Please Select An Attendance Event From DropDown.\nIf It Is Greyed Out, You Must Download Data From Online Database.', 'Event Selection Error', wx.OK | wx.ICON_ERROR)
                return

        self.selected_event = self.m_choice2.GetStringSelection()
        self.attendance_event = self.selected_event
        self.start_date = self.m_datePicker1.GetValue()
        self.end_date = self.m_datePicker2.GetValue()
        self.start_date_formatted = self.start_date.Format("%Y-%m-%d")
        self.end_date_formatted = self.end_date.Format("%Y-%m-%d")

        if self.start_date_formatted > self.end_date_formatted:

                wx.MessageBox('Report Start Date Should Not Be Future To Report End Date.', 'Report Date Error', wx.OK | wx.ICON_ERROR)
                return

        # local_attendance_report(self, start_date_formatted, end_date_formatted, selected_event)
        if self.m_checkBox2.GetValue():

                dlg = AbsenteeReport(self)
                dlg.ShowModal()
        else:
                dlg = LocalReport(self)
                dlg.ShowModal()
        # self.Destroy()
        return

###########################################################################
## Class Absentee Report Grid
###########################################################################
class MyAbsenteeGrid(gridlib.Grid):
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent, size = wx.Size(wx.DisplaySize()))

        # Connecting to database
        def getData():

                event = parent.attendance_event.split("(")[0]
                query_data = (event, parent.start_date_formatted, parent.end_date_formatted)

                try:


                        db = churchdb.connect('c:/ProgramData/SmartChurchApp/offline_data/attendancedata.db')
                        cur = db.cursor()

                        attendancetable = "CREATE TABLE IF NOT EXISTS attendance (card_id TEXT, firstname TEXT, lastname TEXT, event TEXT, attend_date TEXT, gender TEXT, time_attend TEXT)"

                        cur.execute(attendancetable)

                        # fetch all results from db here
                        try:
                                data = []
                                recorded_dates = []
                                query = ''' SELECT event, attend_date FROM attendance WHERE event= ? AND attend_date BETWEEN ? AND ? '''
                                cur.execute(query,query_data)
                                rows = cur.fetchall()

                                for row in rows:

                                        if row[1] not in recorded_dates:

                                                recorded_dates.append(row[1])

                                if recorded_dates:

                                        if os.path.exists("c:/ProgramData/SmartChurchApp/offline_data"):

                                                try:

                                                        with open("c:/ProgramData/SmartChurchApp/offline_data/offline.file", "r") as f_content:

                                                                cipher = MyCipher()
                                                                offline_list = cipher.decrypt_includes_iv(f_content.read())
                                                                offline_list = offline_list.decode()
                                                                offline_list = ast.literal_eval(offline_list)
                                                                first_names = []
                                                                last_names = []
                                                                card_ids = []
                                                                genders = []

                                                                for index, member_detail in enumerate(offline_list):

                                                                        if  member_detail.endswith(".png"):

                                                                                genders.append(offline_list[index+1])
                                                                                last_names.append(offline_list[index-1])
                                                                                first_names.append(offline_list[index-2])
                                                                                card_ids.append(offline_list[index-3])

                                                                # run loop for the dates
                                                                for attendance_date in recorded_dates:
                                                                        i = 0
                                                                        for card_id in card_ids:
                                                                                query_data2 = (event, attendance_date, card_id)
                                                                                no_attendance_data = []
                                                                                query2 = ''' SELECT card_id FROM attendance WHERE event= ? AND attend_date= ? AND card_id= ? '''
                                                                                cur.execute(query2,query_data2)
                                                                                rows = cur.fetchall()
                                                                                if not rows:
                                                                                        no_attendance_data.append(first_names[i])
                                                                                        no_attendance_data.append(last_names[i])
                                                                                        no_attendance_data.append(event)
                                                                                        no_attendance_data.append(attendance_date)
                                                                                        no_attendance_data.append(genders[i])
                                                                                        no_attendance_data.append("")
                                                                                        record = tuple(no_attendance_data)
                                                                                        data.append(record)
                                                                                i= i+1


                                                                return data
                    
                                                except Exception as no_data:

                                                        return data
                                return data
                                    
                        except Exception as file_read_error:
                                time.sleep(0.5)
                                wx.CallAfter(wx.MessageBox,"No Offline Report Available", 'No Offline Report', wx.OK | wx.ICON_ERROR)

                except Exception as dbconerr:
                        time.sleep(0.5)
                        wx.CallAfter(wx.MessageBox,"Local Database Error Occurred", 'Database Error', wx.OK | wx.ICON_ERROR)

                finally:

                        db.close()  
                
        #Column name
        colnames = ["FIRST NAME", "LAST NAME", "EVENT NAME", "DATE", "GROUP", "ABSENCE REASON"]

        #Setup
        data = getData()
        self.data = data
        self.colnames = colnames
        self.EnableEditing(True)

        #Number of rows
        def GetNumberRows(self):
            return int(len(self.data))

        #Number of columns
        def GetNumberCols(self):
            return int(len(self.colnames))

        #Grid creation
        col = GetNumberCols(self)
        row = GetNumberRows(self)
        self.CreateGrid(row, col)
        self.ChangedValue = False

        #Seting up name of columns
        self.SetColLabelValue(0, "FIRST NAME")
        self.SetColLabelValue(1, "LAST NAME")
        self.SetColLabelValue(2, "EVENT NAME")
        self.SetColLabelValue(3, "DATE")
        self.SetColLabelValue(4, "GROUP")
        self.SetColLabelValue(5, "ABSENCE REASON")

        #Insertind data

        def GetValue(self, row, col):
            return str(self.data[row][1].get(self.GetColLabelValue(col), ""))

        def SetValue(self, row, col, value):
            self.data[row][0][self.GetColLabelValue(col)] = value
            
        #Here is where I am stuck
        # self.DisableCellEditControl()
        for i, seq in enumerate(data):
            for j, v in enumerate(seq):
                self.SetCellValue(i, j, v)

                if j != 5:
                        self.SetReadOnly(i, j, True)
                
        width, height = self.GetClientSize()
        width1 = width-10
        height1 = height-80

        
        self.SetSize(wx.Size(width1, height1))
        for col in range(6):
                self.SetColSize(col, width1/(5.4 + 1))
       
        #Events
        # self.Bind(gridlib.EVT_GRID_CELL_CHANGE, self.onCellChange)
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)

    def onCellChange(self, evt):
        pass

    #Enter key down
    def onKeyDown(self, evt):
        if evt.GetKeyCode() != wx.WXK_RETURN:
            evt.Skip()
            return

        if evt.ControlDown():  # the edit control needs this key
            evt.Skip()
            return

        success = self.MoveCursorRight(evt.ShiftDown())

        if not success:
            newRow = self.GetGridCursorRow() + 1

            if newRow < self.GetTable().GetNumberRows():
                self.SetGridCursor(newRow, 0)
                self.MakeCellVisible(newRow, 0)
            else:
                newRow = self.GetGridCursorRow() + 1
                self.appendRow()
                self.SetGridCursor(newRow, 0)
                self.MakeCellVisible(newRow, 0)
                self.ChangedValue = False

    def appendRow(self):
        pass




###########################################################################
## Class Report Grid
###########################################################################
class MyGrid(gridlib.Grid):
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent, size = wx.Size(wx.DisplaySize()))

        # Connecting to database
        def getData():

                event = parent.attendance_event.split("(")[0]
                query_data = (event, parent.start_date_formatted, parent.end_date_formatted)

                try:


                        db = churchdb.connect('c:/ProgramData/SmartChurchApp/offline_data/attendancedata.db')
                        cur = db.cursor()

                        attendancetable = "CREATE TABLE IF NOT EXISTS attendance (card_id TEXT, firstname TEXT, lastname TEXT, event TEXT, attend_date TEXT, gender TEXT, time_attend TEXT)"

                        cur.execute(attendancetable)

                        # fetch all results from db here
                        try:
                                data = []
                                query = ''' SELECT firstname, lastname, event, attend_date, gender, time_attend FROM attendance WHERE event= ? AND attend_date BETWEEN ? AND ? '''
                                cur.execute(query,query_data)
                                rows = cur.fetchall()

                                for row in rows:

                                        data.append(row)

                                return data

                                    
                        except Exception as file_read_error:
                                time.sleep(0.5)
                                wx.CallAfter(wx.MessageBox,"No Offline Report Available", 'No Offline Report', wx.OK | wx.ICON_ERROR)

                except Exception as dbconerr:

                        time.sleep(0.5)
                        wx.CallAfter(wx.MessageBox,"Local Database Error Occurred", 'Database Error', wx.OK | wx.ICON_ERROR)

                finally:

                        db.close()  
                
        #Column name
        colnames = ["FIRST NAME", "LAST NAME", "EVENT NAME", "DATE", "GROUP", "CLOCKIN TIME"]

        #Setup
        data = getData()
        self.data = data
        self.colnames = colnames
        self.EnableEditing(False)

        #Number of rows
        def GetNumberRows(self):
            return int(len(self.data))

        #Number of columns
        def GetNumberCols(self):
            return int(len(self.colnames))

        #Grid creation
        col = GetNumberCols(self)
        row = GetNumberRows(self)
        self.CreateGrid(row, col)
        self.ChangedValue = False

        #Seting up name of columns
        self.SetColLabelValue(0, "FIRST NAME")
        self.SetColLabelValue(1, "LAST NAME")
        self.SetColLabelValue(2, "EVENT NAME")
        self.SetColLabelValue(3, "DATE")
        self.SetColLabelValue(4, "GROUP")
        self.SetColLabelValue(5, "CLOCKIN TIME")

        #Insertind data

        def GetValue(self, row, col):
            return str(self.data[row][1].get(self.GetColLabelValue(col), ""))

        def SetValue(self, row, col, value):
            self.data[row][0][self.GetColLabelValue(col)] = value
            
        #Here is where I am stuck
        for i, seq in enumerate(data):
            for j, v in enumerate(seq):
                self.SetCellValue(i, j, v)
        
        width, height = self.GetClientSize()
        width1 = width-10
        height1 = height-80

        self.SetSize(wx.Size(width1, height1))
        for col in range(6):
                self.SetColSize(col, width1/(5.4 + 1))
        #Events
        # self.Bind(gridlib.EVT_GRID_CELL_CHANGE, self.onCellChange)
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)

    def onCellChange(self, evt):
        pass

    #Enter key down
    def onKeyDown(self, evt):
        if evt.GetKeyCode() != wx.WXK_RETURN:
            evt.Skip()
            return

        if evt.ControlDown():  # the edit control needs this key
            evt.Skip()
            return

        self.DisableCellEditControl()
        success = self.MoveCursorRight(evt.ShiftDown())

        if not success:
            newRow = self.GetGridCursorRow() + 1

            if newRow < self.GetTable().GetNumberRows():
                self.SetGridCursor(newRow, 0)
                self.MakeCellVisible(newRow, 0)
            else:
                newRow = self.GetGridCursorRow() + 1
                self.appendRow()
                self.SetGridCursor(newRow, 0)
                self.MakeCellVisible(newRow, 0)
                self.ChangedValue = False

    def appendRow(self):
        pass



###########################################################################
## Class Report Dialogue
###########################################################################

class LocalReport(wx.Dialog):

    def __init__( self, parent ):
        
        
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Attendance Report For "+parent.attendance_event.split('(')[0]+" From "+parent.start_date_formatted+" To "+parent.end_date_formatted, pos = wx.DefaultPosition, size = wx.Size(wx.DisplaySize()), style = wx.CAPTION|wx.CLOSE_BOX|wx.FRAME_NO_TASKBAR|wx.SYSTEM_MENU|wx.BORDER_NONE|wx.TAB_TRAVERSAL )
        
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.Colour( 207, 207, 207 ) )
        self.SetIcon(wx.Icon(resource_path("ClipartKey_1167914.ico")))
        bSizer14 = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )
        self.m_button13 = wx.Button( self, wx.ID_ANY, u"PRINT REPORT", wx.DefaultPosition, wx.DefaultSize, 0|wx.BORDER_NONE )
        self.m_button13.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        self.m_button13.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )
        self.m_button13.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
        self.m_button13.SetToolTip("Print Local Report")
        bSizer14.Add( self.m_button13, 0, wx.ALL|wx.ALIGN_LEFT, 5 )

        self.m_button14 = wx.Button( self, wx.ID_ANY, u"PRINT PREVIEW", wx.DefaultPosition, wx.DefaultSize, 0|wx.BORDER_NONE )
        self.m_button14.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        self.m_button14.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )
        self.m_button14.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
        self.m_button14.SetToolTip("Preview Print")
        bSizer14.Add( self.m_button14, 0, wx.ALL|wx.ALIGN_LEFT, 5 )
        self.m_button14.Hide()

        self.m_staticText61 = wx.StaticText( self, wx.ID_ANY, u"                                                                                    ", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText61.Wrap( -1 )
        self.m_staticText61.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        bSizer14.Add( self.m_staticText61, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        self.m_staticText62 = wx.StaticText( self, wx.ID_ANY, u"ATTENDANCE REPORT FOR "+parent.attendance_event.upper(), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText62.Wrap( -1 )
        self.m_staticText62.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        bSizer14.Add( self.m_staticText62, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        self.panel = wx.Panel(self)
        self.panel.start_date_formatted = parent.start_date_formatted
        self.panel.end_date_formatted = parent.end_date_formatted
        self.panel.attendance_event = parent.attendance_event
        self.mygrid = MyGrid(self.panel)
        bSizer14.Add( self.panel, 0, wx.ALL, 5 )
        self.SetSizer( bSizer14 )
        self.Layout()

        # Event Handlers
        self.m_button13.Bind( wx.EVT_BUTTON, self.OnPrint )
        self.m_button14.Bind(wx.EVT_BUTTON, self.OnPrintPreview)

        
    def on_close(self, event):
        self.Destroy()

        #self.Centre( wx.BOTH )
    def OnPrintPreview(self, event):
        self.CreatePrintData()
        self.grdprt.Preview()

    def OnPrint(self, event):

        testgrid = self.mygrid

        if testgrid.GetNumberRows() == 0:

                 wx.MessageBox("Cannot print an empty report", "Empty Report!", wx.OK)
                

        else:
                self.CreatePrintData()
                self.grdprt.Print()

    def CreatePrintData(self):
        """
        Create printing data.
        """
        testgrid = self.mygrid

        self.grdprt = PrintGrid(self, testgrid, rowLabels=True, colLabels=True)
        self.grdprt.SetAttributes()

        #------------

        self.table = self.grdprt.GetTable()
        self.table.SetPortrait()
        event = self.panel.attendance_event.split("(")[0]
        self.table.SetHeader('ATTENDANCE REPORT FOR '+event.upper()+' FROM '+self.panel.start_date_formatted+' TO '+self.panel.end_date_formatted)
        self.table.SetFooter()

def __del__( self ):
        
        pass



###########################################################################
## Class Absentee Report Dialogue
###########################################################################

class AbsenteeReport(wx.Dialog):

    def __init__( self, parent ):
        
        
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Absentee Report For "+parent.attendance_event.split('(')[0]+" From "+parent.start_date_formatted+" To "+parent.end_date_formatted, pos = wx.DefaultPosition, size = wx.Size(wx.DisplaySize()), style = wx.CAPTION|wx.CLOSE_BOX|wx.FRAME_NO_TASKBAR|wx.SYSTEM_MENU|wx.BORDER_NONE|wx.TAB_TRAVERSAL )
        
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.Colour( 207, 207, 207 ) )
        self.SetIcon(wx.Icon(resource_path("ClipartKey_1167914.ico")))
        bSizer14 = wx.WrapSizer( wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS )
        self.m_button13 = wx.Button( self, wx.ID_ANY, u"PRINT REPORT", wx.DefaultPosition, wx.DefaultSize, 0|wx.BORDER_NONE )
        self.m_button13.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        self.m_button13.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )
        self.m_button13.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
        self.m_button13.SetToolTip("Print Local Report")
        bSizer14.Add( self.m_button13, 0, wx.ALL|wx.ALIGN_LEFT, 5 )

        self.m_button14 = wx.Button( self, wx.ID_ANY, u"PRINT PREVIEW", wx.DefaultPosition, wx.DefaultSize, 0|wx.BORDER_NONE )
        self.m_button14.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        self.m_button14.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )
        self.m_button14.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
        self.m_button14.SetToolTip("Preview Print")
        bSizer14.Add( self.m_button14, 0, wx.ALL|wx.ALIGN_LEFT, 5 )
        self.m_button14.Hide()

        self.m_staticText61 = wx.StaticText( self, wx.ID_ANY, u"                                                                                    ", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText61.Wrap( -1 )
        self.m_staticText61.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        bSizer14.Add( self.m_staticText61, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        self.m_staticText62 = wx.StaticText( self, wx.ID_ANY, u"ABSENTEE REPORT FOR "+parent.attendance_event.upper(), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText62.Wrap( -1 )
        self.m_staticText62.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        bSizer14.Add( self.m_staticText62, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        self.panel = wx.Panel(self)
        self.panel.start_date_formatted = parent.start_date_formatted
        self.panel.end_date_formatted = parent.end_date_formatted
        self.panel.attendance_event = parent.attendance_event
        self.mygrid = MyAbsenteeGrid(self.panel)
        bSizer14.Add( self.panel, 0, wx.ALL, 5 )
        self.SetSizer( bSizer14 )
        self.Layout()

        # Event Handlers
        self.m_button13.Bind( wx.EVT_BUTTON, self.OnPrint )
        self.m_button14.Bind(wx.EVT_BUTTON, self.OnPrintPreview)

        
    def on_close(self, event):
        self.Destroy()

        #self.Centre( wx.BOTH )
    def OnPrintPreview(self, event):
        self.CreatePrintData()
        self.grdprt.Preview()

    def OnPrint(self, event):

        testgrid = self.mygrid

        if testgrid.GetNumberRows() == 0:

                 wx.MessageBox("Cannot print an empty report", "Empty Report!", wx.OK)
                

        else:
                self.CreatePrintData()
                self.grdprt.Print()

    def CreatePrintData(self):
        """
        Create printing data.
        """
        testgrid = self.mygrid

        self.grdprt = PrintGrid(self, testgrid, rowLabels=True, colLabels=True)
        self.grdprt.SetAttributes()

        #------------

        self.table = self.grdprt.GetTable()
        self.table.SetPortrait()
        event = self.panel.attendance_event.split("(")[0]
        self.table.SetHeader('ABSENTEE REPORT FOR '+event.upper()+' FROM '+self.panel.start_date_formatted+' TO '+self.panel.end_date_formatted)
        self.table.SetFooter()

def __del__( self ):
        
        pass


###########################################################################
## Class Set Printout
###########################################################################

class SetPrintout(wx.Printout):
    """
    ...
    """
    def __init__(self, canvas):
        wx.Printout.__init__(self)
        self.canvas = canvas
        self.end_pg = 1000

    #---------------------------------------------------------------------------

    def OnBeginDocument(self, start, end):
        return super(SetPrintout, self).OnBeginDocument(start, end)


    def OnEndDocument(self):
        super(SetPrintout, self).OnEndDocument()


    def HasPage(self, page):
        try:
            end = self.canvas.HasPage(page)
            return end
        except:
            return True


    def GetPageInfo(self):
        try:
            self.end_pg = self.canvas.GetTotalPages()
        except:
            pass

        end_pg = self.end_pg
        str_pg = 1
        return (str_pg, end_pg, str_pg, end_pg)


    def OnPreparePrinting(self):
        super(SetPrintout, self).OnPreparePrinting()


    def OnBeginPrinting(self):
        dc = self.GetDC()

        self.preview = self.IsPreview()
        if self.preview:
            self.pixelsPerInch = self.GetPPIScreen()
        else:
            self.pixelsPerInch = self.GetPPIPrinter()

        (w, h) = dc.GetSize()
        scaleX = float(w) / 1000
        scaleY = float(h) / 1000
        self.printUserScale = min(scaleX, scaleY)

        super(SetPrintout, self).OnBeginPrinting()


    def GetSize(self):
        self.psizew, self.psizeh = self.GetPPIPrinter()
        return self.psizew, self.psizeh


    def GetTotalSize(self):
        self.ptsizew, self.ptsizeh = self.GetPageSizePixels()
        return self.ptsizew, self.ptsizeh


    def OnPrintPage(self, page):
        dc = self.GetDC()
        (w, h) = dc.GetSize()
        scaleX = float(w) / 1000
        scaleY = float(h) / 1000
        self.printUserScale = min(scaleX, scaleY)
        dc.SetUserScale(self.printUserScale, self.printUserScale)

        self.preview = self.IsPreview()

        self.canvas.SetPreview(self.preview, self.printUserScale)
        self.canvas.SetPage(page)

        self.ptsizew, self.ptsizeh = self.GetPageSizePixels()
        self.canvas.SetTotalSize(self.ptsizew, self.ptsizeh)

        self.psizew, self.psizeh = self.GetPPIPrinter()
        self.canvas.SetPageSize(self.psizew, self.psizeh)

        self.canvas.DoDrawing(dc)
        return True




###########################################################################
## Class Print Table
###########################################################################

class PrintTable(object):
    """
    ...
    """
    def __init__(self, parentFrame=None, rowLabels=True, colLabels=True):
        self.data = []
        self.set_column = []
        self.label = []
        self.header = []
        self.footer = []
        self.rowLabels = rowLabels
        self.colLabels = colLabels

        self.set_column_align = {}
        self.set_column_bgcolour = {}
        self.set_column_txtcolour = {}
        self.set_cell_colour = {}
        self.set_cell_text = {}
        self.column_line_size = {}
        self.column_line_colour = {}
        self.row_line_size = {}
        self.row_line_colour = {}

        self.parentFrame = parentFrame
        self.SetPreviewSize()

        self.printData = wx.PrintData()
        self.scale = 1.0

        self.SetParms()
        self.SetColors()
        self.SetFonts()
        self.TextSpacing()

        self.SetPrinterOffset()
        self.SetHeaderValue()
        self.SetFooterValue()
        self.SetMargins()
        self.SetPortrait()

    #---------------------------------------------------------------------------

    def SetPreviewSize(self, position = wx.Point(0, 0), size="Full"):
        if size == "Full":
            r = wx.GetClientDisplayRect()
            self.preview_frame_size = r.GetSize()
            self.preview_frame_pos = r.GetPosition()
        else:
            self.preview_frame_size = size
            self.preview_frame_pos = position


    def SetPaperId(self, paper):
        self.printData.SetPaperId(paper)


    def SetOrientation(self, orient):
        self.printData.SetOrientation(orient)


    def SetColors(self):
        self.row_def_line_colour = wx.Colour('BLACK')
        self.row_def_line_size = 1

        self.column_def_line_colour = wx.Colour('BLACK')
        self.column_def_line_size = 1
        self.column_colour = wx.Colour('WHITE')

        self.label_colour = wx.Colour('LIGHT GREY')


    def SetFonts(self):
        self.label_font = {"Name": self.default_font_name,
                           "Size": 12,
                           "Colour": [0, 0, 0],
                           "Attr": [0, 0, 0]
                           }
        self.text_font = {"Name": self.default_font_name,
                          "Size": 10,
                          "Colour": [0, 0, 0],
                          "Attr": [0, 0, 0]
                          }


    def TextSpacing(self):
        self.label_pt_adj_before = 0     # point adjustment before and after the label text
        self.label_pt_adj_after = 0

        self.text_pt_adj_before = 0     # point adjustment before and after the row text
        self.text_pt_adj_after = 0


    def SetLabelSpacing(self, before, after):        # method to set the label space adjustment
        self.label_pt_adj_before = before
        self.label_pt_adj_after = after


    def SetRowSpacing(self, before, after):         # method to set the row space adjustment
        self.text_pt_adj_before = before
        self.text_pt_adj_after = after


    def SetPrinterOffset(self):        # offset to adjust for printer
        self.vertical_offset = -0.1
        self.horizontal_offset = -0.1


    def SetHeaderValue(self):
        self.header_margin = 0.25
        self.header_font = {"Name": self.default_font_name,
                            "Size": 11,
                            "Colour": [0, 0, 0],
                            "Attr": [0, 0, 0]
                            }
        self.header_align = wx.ALIGN_CENTRE
        self.header_indent = 0
        self.header_type = "Text"


    def SetFooterValue(self):
        self.footer_margin = 0.7
        self.footer_font = {"Name": self.default_font_name,
                            "Size": 11,
                            "Colour": [0, 0, 0],
                            "Attr": [0, 0, 0]
                            }
        self.footer_align = wx.ALIGN_CENTRE
        self.footer_indent = 0
        self.footer_type = "Pageof"


    def SetMargins(self):
        self.left_margin = 0.5
        self.right_margin = 0.2    # only used if no column sizes

        self.top_margin  = 0.8
        self.bottom_margin = 1.0
        self.cell_left_margin = 0.5
        self.cell_right_margin = 0.5


    def SetPortrait(self):
        self.printData.SetPaperId(wx.PAPER_A4)
        self.printData.SetOrientation(wx.PORTRAIT)
        self.page_width = 8.267716535433071
        self.page_height = 11.69291338582677


    def SetLandscape(self):
        self.printData.SetOrientation(wx.LANDSCAPE)
        self.page_width = 8.267716535433071
        self.page_height = 11.69291338582677


    def SetParms(self):
        self.ymax = 1
        self.xmax = 1
        self.page = 1
        self.total_pg = 100

        self.preview = None
        self.page = 0

        self.default_font_name = "Arial"
        self.default_font = {"Name": self.default_font_name,
                             "Size": 10,
                             "Colour": [0, 0, 0],
                             "Attr": [0, 0, 0]
                             }


    def SetColAlignment(self, col, align=wx.ALIGN_LEFT):
        self.set_column_align[col] = align


    def SetColBackgroundColour(self, col, colour):
        self.set_column_bgcolour[col] = colour


    def SetColTextColour(self, col, colour):
        self.set_column_txtcolour[col] = colour


    def SetCellColour(self, row, col, colour):      # cell background colour
        try:
            set = self.set_cell_colour[row]     # test if row already exists
            try:
                set[col] = colour       # test if column already exists
            except:
                set = { col: colour }       # create the column value
        except:
            set = { col: colour }           # create the column value

        self.set_cell_colour[row] = set    # create dictionary item for colour settings


    def SetCellText(self, row, col, colour):        # font colour for custom cells
        try:
            set = self.set_cell_text[row]     # test if row already exists
            try:
                set[col] = colour       # test if column already exists
            except:
                set = { col: colour }       # create the column value
        except:
            set = { col: colour }           # create the column value

        self.set_cell_text[row] = set    # create dictionary item for colour settings


    def SetColumnLineSize(self, col, size):      # column line size
        self.column_line_size[col] = size    # create dictionary item for column line settings


    def SetColumnLineColour(self, col, colour):
        self.column_line_colour[col] = colour


    def SetRowLineSize(self, row, size):
        self.row_line_size[row] = size


    def SetRowLineColour(self, row, colour):
        self.row_line_colour[row] = colour


    def GetColour(self, colour):        # returns colours based from wxColour value
        red = colour.Red()
        blue = colour.Blue()
        green = colour.Green()
        return [red, green, blue ]


    def SetHeader(self, text="", type="Text", font=None, align=None,
                  indent=None, colour=None, size=None):
        set = {"Text": text}

        if font is None:
            set["Font"] = copy.copy(self.default_font)
        else:
            set["Font"] = font

        if colour is not None:
            setfont = set["Font"]
            setfont["Colour"] = self.GetColour(colour)

        if size is not None:
            setfont = set["Font"]
            setfont["Size"] = size

        if align is None:
            set["Align"] = self.header_align
        else:
            set["Align"] = align

        if indent is None:
            set["Indent"] = self.header_indent
        else:
            set["Indent"] = indent

        if type is None:
            set["Type"] = self.header_type
        else:
            set["Type"] = type

        self.header.append(set)


    def SetFooter(self, text="", type=None, font=None, align=None,
                  indent=None, colour=None, size=None):
        set = { "Text": text }

        if font is None:
            set["Font"] = copy.copy(self.default_font)
        else:
            set["Font"] = font

        if colour is not None:
            setfont = set["Font"]
            setfont["Colour"] = self.GetColour(colour)

        if size is not None:
            setfont = set["Font"]
            setfont["Size"] = size

        if align is None:
            set["Align"] = self.footer_align
        else:
            set["Align"] = align

        if indent is None:
            set["Indent"] = self.footer_indent
        else:
            set["Indent"] = indent

        if type is None:
            set["Type"] = self.footer_type
        else:
            set["Type"] = type

        self.footer.append(set)


    def Preview(self):
        data = wx.PrintDialogData(self.printData)
        printout = SetPrintout(self)
        printout2 = SetPrintout(self)
        self.preview = wx.PrintPreview(printout, printout2, data)
        if not self.preview.IsOk():
            wx.MessageBox("There was a problem printing!", "Printing", wx.OK)
            return

        self.preview.SetZoom(85)        # initial zoom value
        frame = wx.PreviewFrame(self.preview, self.parentFrame, "Print preview", style=wx.FRAME_NO_TASKBAR|wx.STAY_ON_TOP)

        frame.Initialize()
        if self.parentFrame:
            frame.SetPosition(self.preview_frame_pos)
            frame.SetSize(self.preview_frame_size)
        frame.Show(True)


    def Print(self):
        pdd = wx.PrintDialogData(self.printData)
        printer = wx.Printer(pdd)
        printout = SetPrintout(self)
        if not printer.Print(self.parentFrame, printout):
            if wx.Printer.GetLastError() == wx.PRINTER_ERROR:
                wx.MessageBox("There was a problem printing.\n"
                              "Perhaps your current printer is not set correctly?",
                              "Printing", wx.OK)
        else:
            self.printData = wx.PrintData( printer.GetPrintDialogData().GetPrintData() )
        printout.Destroy()


    def DoDrawing(self, DC):
        size = DC.GetSize()

        table = PrintTableDraw(self, DC, size, self.colLabels)
        table.data = self.data
        table.set_column = self.set_column
        table.label = self.label
        table.SetPage(self.page)

        if self.preview is None:
            table.SetPSize(size[0]/self.page_width, size[1]/self.page_height)
            table.SetPTSize(size[0], size[1])
            table.SetPreview(False)
        else:
            if self.preview == 1:
                table.scale = self.scale
                table.SetPSize(size[0]/self.page_width, size[1]/self.page_height)
            else:
                table.SetPSize(self.pwidth, self.pheight)

            table.SetPTSize(self.ptwidth, self.ptheight)
            table.SetPreview(self.preview)

        table.OutCanvas()
        self.page_total = table.total_pages     # total display pages

        self.ymax = DC.MaxY()
        self.xmax = DC.MaxX()

        self.sizeh = size[0]
        self.sizew = size[1]


    def GetTotalPages(self):
        self.page_total = 100
        return self.page_total


    def HasPage(self, page):
        if page <= self.page_total:
            return True
        else:
            return False


    def SetPage(self, page):
        self.page = page


    def SetPageSize(self, width, height):
        self.pwidth, self.pheight = width, height


    def SetTotalSize(self, width, height):
        self.ptwidth, self.ptheight = width, height


    def SetPreview(self, preview, scale):
        self.preview = preview
        self.scale = scale


    def SetTotalSize(self, width, height):
        self.ptwidth = width
        self.ptheight = height

###########################################################################
## Class Print Grid
###########################################################################

class PrintGrid(object):
    """
    ...
    """
    def __init__(self, parent, grid, format=[], total_col=None,
                 total_row=None, rowLabels=True, colLabels=True):
        if total_row is None:
            total_row = grid.GetNumberRows()
        if total_col is None:
            total_col = grid.GetNumberCols()

        self.total_row = total_row
        self.total_col = total_col
        self.grid = grid
        self.rowLabels = rowLabels
        self.colLabels = colLabels

        data = []
        for row in range(total_row):
            row_val = []
            if rowLabels:
                row_val.append(grid.GetRowLabelValue(row))

            for col in range(total_col):
                try:
                    row_val.append(grid.GetCellValueAsString(row, col))
                except:
                    row_val.append(grid.GetCellValue(row, col))
            data.append(row_val)


        if colLabels:
            label = [""] if rowLabels else []
            for col in range(total_col):
                value = grid.GetColLabelValue(col)
                label.append(value)

        d = float(grid.GetColSize(0))

        if format == []:
            if rowLabels:
                format.append(grid.GetRowLabelSize())
            for col in range(total_col):
                col_size = grid.GetColSize(col)
                # print("Column size:", col,'\t',col_size)
                format.append(140) # 30 to reduce column width

        self.table = PrintTable(parent, rowLabels, colLabels)
        if colLabels: self.table.label = label
        self.table.cell_left_margin = 0.1
        self.table.cell_right_margin = 0.1

        self.table.set_column = format
        self.table.data = data

    #---------------------------------------------------------------------------

    def GetTable(self):
        return self.table


    def SetAttributes(self):
        for row in range(self.total_row):
            for col in range(self.total_col):
                colour = self.grid.GetCellTextColour(row, col)
                self.table.SetCellText(row, col+self.rowLabels, colour)

                colour = self.grid.GetCellBackgroundColour(row, col)
                self.table.SetCellColour(row, col+self.rowLabels, colour)

                #self.table.


    def Preview(self):
        self.table.Preview()


    def Print(self):
        self.table.Print()

###########################################################################
## Class Print Base
###########################################################################

class PrintBase(object):
    """
    ...
    """
    def SetPrintFont(self, font):      # set the DC font parameters
        fattr = font["Attr"]
        if fattr[0] == 1:
            weight = wx.BOLD
        else:
            weight = wx.NORMAL

        if fattr[1] == 1:
            set_style = wx.ITALIC
        else:
            set_style = wx.NORMAL

        underline = fattr[2]
        fcolour = self.GetFontColour(font)
        self.DC.SetTextForeground(fcolour)

        setfont = wx.Font(font["Size"], wx.SWISS, set_style, weight, underline)
        setfont.SetFaceName(font["Name"])
        self.DC.SetFont(setfont)

    #---------------------------------------------------------------------------

    def GetFontColour(self, font):
        fcolour = font["Colour"]
        return wx.Colour(fcolour[0], fcolour[1], fcolour[2])


    def OutTextRegion(self, textout, txtdraw = True):
        textlines = textout.split('\n')
        y = copy.copy(self.y) + self.pt_space_before
        for text in textlines:
            remain = 'X'
            while remain != "":
                vout, remain = self.SetFlow(text, self.region)
                if self.draw == True and txtdraw == True:
                    test_out = self.TestFull(vout)
                    if self.align == wx.ALIGN_LEFT:
                        self.DC.DrawText(test_out, int(self.indent+self.pcell_left_margin), int(y))

                    elif self.align == wx.ALIGN_CENTRE:
                        diff = self.GetCellDiff(test_out, self.region)
                        self.DC.DrawText(test_out, self.indent+diff/2, y)

                    elif self.align == wx.ALIGN_RIGHT:
                        diff = self.GetCellDiff(test_out, self.region)
                        self.DC.DrawText(test_out, self.indent+diff, y)

                    else:
                        self.DC.DrawText(test_out, int(self.indent+self.pcell_left_margin), int(y))
                text = remain
                y = y + self.space
        return y - self.space + self.pt_space_after


    def GetCellDiff(self, text, width):      # get the remaining cell size for adjustment
        w, h = self.DC.GetTextExtent(text)
        diff = width - w
        if diff < 0:
            diff = 0
        return diff


    def TestFull(self, text_test):
        w, h = self.DC.GetTextExtent(text_test)
        if w > self.region:     # trouble fitting into cell
            return self.SetChar(text_test, self.region)     # fit the text to the cell size
        else:
            return text_test


    def SetFlow(self, ln_text, width):
        width = width - self.pcell_right_margin
        text = ""
        split = ln_text.split()
        if len(split) == 1:
            return ln_text, ""

        try:
            w, h = self.DC.GetTextExtent(" " + split[0])
            if w >= width:
                return ln_text, ""
        except:
            pass

        cnt = 0
        for word in split:
            bword = " " + word  # blank + word
            length = len(bword)

            w, h = self.DC.GetTextExtent(text + bword)
            if w < width:
                text = text + bword
                cnt = cnt + 1
            else:
                remain = ' '.join(split[cnt:])
                text = text.strip()
                return text, remain

        remain = ' '.join(split[cnt:])
        vout = text.strip()
        return vout, remain


    def SetChar(self, ln_text, width):  # truncate string to fit into width
        width = width - self.pcell_right_margin - self.pcell_left_margin
        text = ""
        for val in ln_text:
            w, h = self.DC.GetTextExtent(text + val)
            if w > width:
                text = text + ".."
                return text     # fitted text value
            text = text + val
        return text


    def OutTextPageWidth(self, textout, y_out, align, indent, txtdraw = True):
        textlines = textout.split('\n')
        y = copy.copy(y_out)

        pagew = self.parent.page_width * self.pwidth        # full page width
        w, h = self.DC.GetTextExtent(textout)
        y_line = h

        for text in textlines:
            remain = 'X'
            while remain != "":
                vout, remain = self.SetFlow(text, pagew)
                if self.draw == True and txtdraw == True:
                    test_out = vout
                    if align == wx.ALIGN_LEFT:
                        self.DC.DrawText(test_out, indent, y)

                    elif align == wx.ALIGN_CENTRE:
                        diff = self.GetCellDiff(test_out, pagew)
                        self.DC.DrawText(test_out, int(indent+diff/2), int(y))

                    elif align == wx.ALIGN_RIGHT:
                        diff = self.GetCellDiff(test_out, pagew)
                        self.DC.DrawText(test_out, int(indent+diff), int(y))

                    else:
                        self.DC.DrawText(test_out, indent, y_out)
                text = remain
                y = y + y_line
        return y - y_line


    def GetDate(self):
        date, time = self.GetNow()
        return date


    def GetDateTime(self):
        date, time = self.GetNow()
        return date + ' ' + time


    def GetNow(self):
        now = wx.DateTime.Now()
        date = now.FormatDate()
        time = now.FormatTime()
        return date, time


    def SetPreview(self, preview):
        self.preview = preview


    def SetPSize(self, width, height):
        self.pwidth = width/self.scale
        self.pheight = height/self.scale


    def SetScale(self, scale):
        self.scale = scale


    def SetPTSize(self, width, height):
        self.ptwidth = width
        self.ptheight = height


    def getWidth(self):
        return self.sizew


    def getHeight(self):
        return self.sizeh



###########################################################################
## Class Print Table Draw
###########################################################################

class PrintTableDraw(wx.ScrolledWindow, PrintBase):
    """
    ...
    """
    def __init__(self, parent, DC, size, colLabels=True):
        self.parent = parent
        self.DC = DC
        self.scale = parent.scale
        self.width = size[0]
        self.height = size[1]
        self.colLabels = colLabels
        self.SetDefaults()

    #---------------------------------------------------------------------------

    def SetDefaults(self):
        self.page = 1
        self.total_pages = None

        self.page_width = self.parent.page_width
        self.page_height = self.parent.page_height

        self.left_margin = self.parent.left_margin
        self.right_margin = self.parent.right_margin

        self.top_margin  = self.parent.top_margin
        self.bottom_margin = self.parent.bottom_margin
        self.cell_left_margin = self.parent.cell_left_margin
        self.cell_right_margin = self.parent.cell_right_margin

        self.label_colour = self.parent.label_colour

        self.row_line_colour = self.parent.row_line_colour
        self.row_line_size = self.parent.row_line_size

        self.row_def_line_colour = self.parent.row_def_line_colour
        self.row_def_line_size = self.parent.row_def_line_size

        self.column_line_colour = self.parent.column_line_colour
        self.column_line_size = self.parent.column_line_size

        self.column_def_line_size = self.parent.column_def_line_size
        self.column_def_line_colour = self.parent.column_def_line_colour

        self.text_font = self.parent.text_font

        self.label_font = self.parent.label_font


    def AdjustValues(self):
        self.vertical_offset = self.pheight * self.parent.vertical_offset
        self.horizontal_offset = self.pheight * self.parent.horizontal_offset

        self.pcell_left_margin = self.pwidth * self.cell_left_margin
        self.pcell_right_margin = self.pwidth * self.cell_right_margin
        self.ptop_margin = self.pheight * self.top_margin
        self.pbottom_margin = self.pheight * self.bottom_margin

        self.pheader_margin = self.pheight * self.parent.header_margin
        self.pfooter_margin = self.pheight * self.parent.footer_margin

        self.cell_colour = self.parent.set_cell_colour
        self.cell_text = self.parent.set_cell_text

        self.column = []
        self.column_align = []
        self.column_bgcolour = []
        self.column_txtcolour = []

        set_column_align = self.parent.set_column_align
        set_column_bgcolour = self.parent.set_column_bgcolour
        set_column_txtcolour = self.parent.set_column_txtcolour

        pos_x = self.left_margin * self.pwidth + self.horizontal_offset     # left margin
        self.column.append(pos_x)

        # Module logic expects two dimensional data -- fix input if needed
        if isinstance(self.data, str):
            self.data = [[copy.copy(self.data)]] # a string becomes a single cell
        try:
            rows = len(self.data)
        except TypeError:
            self.data = [[str(self.data)]] # a non-iterable becomes a single cell
            rows = 1
        first_value = self.data[0]

        if isinstance(first_value, str): # A sequence of strings
            if self.label == [] and self.set_column == []:
                data = []
                for x in self.data:     # Becomes one column
                    data.append([x])
            else:
                data = [self.data]      # Becames one row
            self.data = data
            first_value = data[0]
        try:
            column_total = len(first_value)
        except TypeError:    # a sequence of non-iterables
            if self.label == [] and self.set_column == []:
                data = []       #becomes one column
                for x in self.data:
                    data.append([str(x)])
                column_total = 1
            else:
                data = [self.data] #becomes one row
                column_total = len(self.data)
            self.data = data
            first_value = data[0]

        if self.set_column == []:
            table_width = self.page_width - self.left_margin - self.right_margin
            if self.label == []:
                temp = first_value
            else:
                temp = self.label
            width = table_width/(len(temp))
            for val in temp:
                column_width = width * self.pwidth
                pos_x = pos_x + column_width
                self.column.append(pos_x)   # position of each column
        else:
            for val in self.set_column:
                column_width = val
                pos_x = pos_x + column_width
                self.column.append(pos_x)   # position of each column

        if pos_x > self.page_width * self.pwidth:    # check if it fits in page
            print("Warning, Too Wide for Page")
            print(pos_x, self.page_width * self.pwidth)
            pos_x = self.page_width * self.pwidth
            return

        if self.label != []:
            if len(self.column) -1 != len(self.label):
                print("Column Settings Incorrect", "\nColumn Value: " + str(self.column), "\nLabel Value: " + str(self.label))
                return

        if column_total != len(self.column) -1:
            print("Cannot fit", first_value, 'in', len(self.column)-1, 'columns.')
            return

        for col in range(column_total):
            try:
                align = set_column_align[col]       # check if custom column alignment
            except:
                align = wx.ALIGN_LEFT
            self.column_align.append(align)

            try:
                colour = set_column_bgcolour[col]     # check if custom column background colour
            except:
                colour = self.parent.column_colour
            self.column_bgcolour.append(colour)

            try:
                colour = set_column_txtcolour[col]     # check if custom column text colour
            except:
                colour = self.GetFontColour(self.parent.text_font)
            self.column_txtcolour.append(colour)


    def SetPointAdjust(self):
        f = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL)     # setup using 10 point
        self.DC.SetFont(f)
        f.SetFaceName(self.text_font["Name"])
        x, y = self.DC.GetTextExtent("W")

        self.label_pt_space_before = self.parent.label_pt_adj_before * y/10        # extra spacing for label per point value
        self.label_pt_space_after = self.parent.label_pt_adj_after * y/10

        self.text_pt_space_before = self.parent.text_pt_adj_before * y/10        # extra spacing for row text per point value
        self.text_pt_space_after = self.parent.text_pt_adj_after * y/10


    def SetPage(self, page):
        self.page = page


    def SetColumns(self, col):
        self.column = col


    def OutCanvas(self):
        self.AdjustValues()
        self.SetPointAdjust()

        self.y_start = self.ptop_margin + self.vertical_offset
        self.y_end = self.parent.page_height * self.pheight - self.pbottom_margin + self.vertical_offset

        self.SetPrintFont(self.label_font)

        x, y = self.DC.GetTextExtent("W")
        self.label_space = y

        self.SetPrintFont(self.text_font)

        x, y = self.DC.GetTextExtent("W")
        self.space = y

        if self.total_pages is None:
            self.GetTotalPages()    # total pages for display/printing

        self.data_cnt = self.page_index[self.page-1]

        self.draw = True
        self.PrintHeader()
        self.PrintFooter()
        self.OutPage()


    def GetTotalPages(self):
        self.data_cnt = 0
        self.draw = False
        self.page_index = [0]

        cnt = 0
        while 1:
            test = self.OutPage()
            self.page_index.append(self.data_cnt)
            if  test == False:
                break
            cnt = cnt + 1

        self.total_pages = cnt + 1


    def OutPage(self):
        self.y = self.y_start
        self.end_x = self.column[-1]

        if self.data_cnt < len(self.data):  # if there data for display on the page
            if self.colLabels and self.label != []:        # check if header defined
                self.PrintLabel()
        else:
            return False

        for val in self.data:
            try:
                row_val = self.data[self.data_cnt]
            except:
                self.FinishDraw()
                return False

            max_y = self.PrintRow(row_val, False)       # test to see if row will fit in remaining space
            test = max_y + self.space

            if test > self.y_end:
                break

            self.ColourRowCells(max_y-self.y+self.space)       # colour the row/column
            max_y = self.PrintRow(row_val, True)      # row fits - print text
            self.DrawGridLine()     # top line of cell
            self.y = max_y + self.space

            if self.y > self.y_end:
                break

            self.data_cnt = self.data_cnt + 1

        self.FinishDraw()

        if self.data_cnt == len(self.data):    # last value in list
            return False

        return True


    def PrintLabel(self):
        self.pt_space_before = self.label_pt_space_before   # set the point spacing
        self.pt_space_after = self.label_pt_space_after

        self.LabelColorRow(self.label_colour)
        self.SetPrintFont(self.label_font)

        self.col = 0
        max_y = 0
        for vtxt in self.label:
            self.region = self.column[self.col+1] - self.column[self.col]
            self.indent = self.column[self.col]

            self.align = wx.ALIGN_LEFT

            max_out = self.OutTextRegion(vtxt, True)
            if max_out > max_y:
                max_y = max_out
            self.col = self.col + 1

        self.DrawGridLine()     # top line of label
        self.y = max_y + self.label_space


    def PrintHeader(self):      # print the header array
        if self.draw == False:
            return

        for val in self.parent.header:
            self.SetPrintFont(val["Font"])

            header_indent = val["Indent"] * self.pwidth
            text = val["Text"]

            htype = val["Type"]
            if htype == "Date":
                addtext = self.GetDate()
            elif htype == "Date & Time":
                addtext = self.GetDateTime()
            else:
                addtext = ""

            self.OutTextPageWidth(text+addtext, self.pheader_margin, val["Align"], header_indent, True)


    def PrintFooter(self):      # print the header array
        if self.draw == False:
            return

        footer_pos = self.parent.page_height * self.pheight - self.pfooter_margin + self.vertical_offset
        for val in self.parent.footer:
            self.SetPrintFont(val["Font"])

            footer_indent = val["Indent"] * self.pwidth
            text = val["Text"]

            ftype = val["Type"]
            if ftype == "Pageof":
                addtext = "Page " + str(self.page) + " of " + str(self.total_pages)
            elif ftype == "Page":
                addtext = "Page " + str(self.page)
            elif ftype == "Num":
                addtext = str(self.page)
            elif ftype == "Date":
                addtext = self.GetDate()
            elif ftype == "Date & Time":
                addtext = self.GetDateTime()
            else:
                addtext = ""

            self.OutTextPageWidth(text+addtext, footer_pos, val["Align"], footer_indent, True)


    def LabelColorRow(self, colour):
        brush = wx.Brush(colour, wx.SOLID)
        self.DC.SetBrush(brush)
        height = self.label_space + self.label_pt_space_before + self.label_pt_space_after
        self.DC.DrawRectangle(self.column[0], self.y,
                              self.end_x-self.column[0]+1, height)

    def ColourRowCells(self, height):
        if self.draw == False:
            return

        col = 0
        for colour in self.column_bgcolour:
            cellcolour = self.GetCellColour(self.data_cnt, col)
            if cellcolour is not None:
                colour = cellcolour

            brush = wx.Brush(colour, wx.SOLID)
            self.DC.SetBrush(brush)
            self.DC.SetPen(wx.Pen(wx.Colour('WHITE'), 0))

            start_x = self.column[col]
            width = self.column[col+1] - start_x + 2
            self.DC.DrawRectangle(int(start_x), int(self.y), int(width), int(height))
            col = col + 1


    def PrintRow(self, row_val, draw = True, align = wx.ALIGN_LEFT):
        self.SetPrintFont(self.text_font)

        self.pt_space_before = self.text_pt_space_before   # set the point spacing
        self.pt_space_after = self.text_pt_space_after

        self.col = 0
        max_y = 0
        for vtxt in row_val:
            if not isinstance(vtxt, str):
                vtxt = str(vtxt)
            self.region = self.column[self.col+1] - self.column[self.col]
            self.indent = self.column[self.col]
            try:
                self.align = self.column_align[self.col]
            except IndexError:
                self.align = wx.ALIGN_LEFT

            try:
                fcolour = self.column_txtcolour[self.col]       # set font colour
            except IndexError:
                fcolour = wx.BLACK

            celltext = self.GetCellTextColour(self.data_cnt, self.col)
            if celltext is not None:
                fcolour = celltext      # override the column colour

            self.DC.SetTextForeground(fcolour)

            max_out = self.OutTextRegion(vtxt, draw)
            if max_out > max_y:
                max_y = max_out
            self.col = self.col + 1
        return max_y


    def GetCellColour(self, row, col):      # check if custom colour defined for the cell background
        try:
            set = self.cell_colour[row]
        except:
            return None
        try:
            colour = set[col]
            return colour
        except:
            return None


    def GetCellTextColour(self, row, col):      # check if custom colour defined for the cell text
        try:
            set = self.cell_text[row]
        except:
            return None
        try:
            colour = set[col]
            return colour
        except:
            return None


    def FinishDraw(self):
        self.DrawGridLine()     # draw last row line
        self.DrawColumns()      # draw all vertical lines


    def DrawGridLine(self):
        if self.draw == True \
        and len(self.column) > 2:    #supress grid lines if only one column
            try:
                size = self.row_line_size[self.data_cnt]
            except:
                size = self.row_def_line_size

            if size < 1: return

            try:
                colour = self.row_line_colour[self.data_cnt]
            except:
                colour = self.row_def_line_colour

            self.DC.SetPen(wx.Pen(colour, size))

            y_out = self.y
            #y_out = self.y + self.pt_space_before + self.pt_space_after     # adjust for extra spacing
            self.DC.DrawLine(int(self.column[0]), int(y_out), int(self.end_x), int(y_out))


    def DrawColumns(self):
        if self.draw == True \
        and len(self.column) > 2:   #surpress grid line if only one column
            col = 0
            for val in self.column:
                try:
                    size = self.column_line_size[col]
                except:
                    size = self.column_def_line_size

                if size < 1: continue

                try:
                    colour = self.column_line_colour[col]
                except:
                    colour = self.column_def_line_colour

                indent = val

                self.DC.SetPen(wx.Pen(colour, size))
                self.DC.DrawLine(int(indent), int(self.y_start), int(indent), int(self.y))
                col = col + 1


    def DrawText(self):
        self.DoRefresh()


    def DoDrawing(self, DC):
        size = DC.GetSize()
        self.DC = DC

        self.DrawText()

        self.sizew = DC.MaxY()
        self.sizeh = DC.MaxX()


###########################################################################
## Class Bind_Card
###########################################################################

class Bind_Card ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Membership Smart Card Binding", pos = wx.DefaultPosition, size = wx.Size( 300,350 ), style = wx.DEFAULT_DIALOG_STYLE|wx.FRAME_FLOAT_ON_PARENT )
        self.hardwrid = check_output('wmic csproduct get uuid',shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        self.hardwrid = self.hardwrid.decode().strip()
        self.hardwrid = self.hardwrid.replace('UUID','')
        self.hardwrid = self.hardwrid.replace('-','')
        self.hardwrid = self.hardwrid.strip()
        self.cpt_name = os.environ['COMPUTERNAME']
        self.cpt_name = self.cpt_name.replace('-','')
        self.cpt_name = self.cpt_name.replace('_','')
        self.cpt_name= self.cpt_name.strip()
        
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.Colour( 207, 207, 207 ) )

        bSizer14 = wx.BoxSizer( wx.VERTICAL )

        sbSizer32 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Smart Reader Config" ), wx.VERTICAL )

        fgSizer9 = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizer9.SetFlexibleDirection( wx.BOTH )
        fgSizer9.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_staticText62 = wx.StaticText( sbSizer32.GetStaticBox(), wx.ID_ANY, u"Smart Reader COM Port:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText62.Wrap( -1 )

        self.m_staticText62.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        #self.m_staticText62.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )

        fgSizer9.Add( self.m_staticText62, 0, wx.ALL, 5 )

        self.m_textCtrl34 = wx.TextCtrl( sbSizer32.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer9.Add( self.m_textCtrl34, 0, wx.ALL|wx.EXPAND, 5 )

        sbSizer32.Add( fgSizer9, 1, wx.EXPAND, 5 )


        bSizer14.Add( sbSizer32, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_button13 = wx.Button( self, wx.ID_ANY, u"Connect to Portal", wx.DefaultPosition, wx.DefaultSize, 0|wx.BORDER_NONE )
        self.m_button13.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        self.m_button13.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )
        self.m_button13.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
        self.m_button13.SetToolTip("Login To Administrative Dashboard To Assign Card To Members")

        bSizer14.Add( self.m_button13, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
        self.m_button13.Disable()
        

        sbSizer33 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"AVAILABLE COM Ports" ), wx.VERTICAL )

        self.m_textCtrl35 = wx.TextCtrl( sbSizer33.GetStaticBox(), wx.ID_ANY, u"Loading Available Com Ports, Please Wait...", wx.DefaultPosition, wx.Size( 260,80 ), wx.HSCROLL| wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH )
        sbSizer33.Add( self.m_textCtrl35, 0, wx.ALL, 5 )


        bSizer14.Add( sbSizer33, 1, wx.ALL|wx.EXPAND, 5 )


        self.SetSizer( bSizer14 )
        self.Layout()
        com_ports = threading.Thread(target=get_com_port_lists_bind_cards,args=(self,self))
        com_ports.daemon = True
        com_ports.start()
        check_saved_reader_data(self.m_textCtrl34)
        
        com_port = self.m_textCtrl34.GetValue()
        if com_port !="":
            self.m_button13.Enable()

        #self.Centre( wx.BOTH )

        # Connect Events
        self.m_button13.Bind( wx.EVT_BUTTON, self.BindCardOnline )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def BindCardOnline( self, event ):

        #Get config file and autofill configuration details on next run
        com_port = self.m_textCtrl34.GetValue()
        #Get config file and autofill configuration details
        hardware_id = self.hardwrid
        computer_name = self.cpt_name
        attendance_event = "Admin_card_binding"
        mode = "Bind_Smart_Cards"
        save_com_port_data(com_port)
        date = ""
        if com_port =="":

                wx.MessageBox('Please Input COM Port Value For Smart Reader.', 'COM Port Error', wx.OK | wx.ICON_ERROR)
                return

        if os.path.isfile(resource_path("smart-church/resources/app/nativefier.json")) and os.access(resource_path("smart-church/resources/app/nativefier.json"), os.R_OK):
                
                pass

        else:
                wx.MessageBox('Embedded Browser Configuration File is Corrupted. Please Reinstall Application', 'Corrupt Configuration File', wx.OK | wx.ICON_ERROR)
                return
        
        global blocked
        blocked = 0
        global timer
        timer = TimerDialogue(self)
        #start thread to monitor when browser comes up then hide it immidiately
        absl = threading.Thread(target=find_web_browser,args=(self, com_port,hardware_id,computer_name,attendance_event,mode,date,timer))
        absl.daemon = True
        absl.start()
        #modify browser url before silently opening
        global infoStatus
        infoStatus = "check_for_browser"
        evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId,self.Parent.loading.GetId())
        wx.PostEvent(self.Parent.loading, evt)
        self.Hide()
        #self.Parent.Hide()
        SW_HIDE = 0
        info = subprocess.STARTUPINFO()
        info.dwFlags = 1#subprocess.STARTF_USESHOWWINDOW
        info.wShowWindow = SW_HIDE
        obfuscate_url()
        with fileinput.FileInput(resource_path("smart-church/resources/app/nativefier.json"), inplace=True, backup='.bak') as file:
                for line in file:
                        print(re.sub('"targetUrl":\S+,', '"targetUrl":"https://smartchurchattendance.com.ng/smartChurch/login?hid='+hardware_id+'&&cpt='+computer_name+'",',line), end='')
                        time.sleep(2)
                        
        proc = subprocess.Popen([resource_path('smart-church/SMARTChurchApp.exe')], startupinfo = info, stdin=None, stdout=None, stderr=None, close_fds=True )
        atexit.register(proc.terminate)
        pid = proc.pid
        #subprocess.check_call(resource_path('smart-church/SMART Church App.exe'))
        #self.Parent.Show()
        

        
###########################################################################
## Class OnlineAttendanceDialogue
###########################################################################

class OnlineAttendanceDialogue ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Online Attendance Config", pos = wx.DefaultPosition, size = wx.Size( 300,350 ), style = wx.DEFAULT_DIALOG_STYLE|wx.FRAME_FLOAT_ON_PARENT )

        self.hardwrid = check_output('wmic csproduct get uuid',shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        self.hardwrid = self.hardwrid.decode().strip()
        self.hardwrid = self.hardwrid.replace('UUID','')
        self.hardwrid = self.hardwrid.replace('-','')
        self.hardwrid = self.hardwrid.strip()
        self.cpt_name = os.environ['COMPUTERNAME']
        self.cpt_name = self.cpt_name.replace('-','')
        self.cpt_name = self.cpt_name.replace('_','')
        self.cpt_name= self.cpt_name.strip()

        
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.Colour( 207, 207, 207 ) )

        bSizer14 = wx.BoxSizer( wx.VERTICAL )

        sbSizer32 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Event Selection" ), wx.VERTICAL )

        fgSizer9 = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizer9.SetFlexibleDirection( wx.BOTH )
        fgSizer9.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_staticText62 = wx.StaticText( sbSizer32.GetStaticBox(), wx.ID_ANY, u"Smart Reader COM Port:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText62.Wrap( -1 )

        self.m_staticText62.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        #self.m_staticText62.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )

        fgSizer9.Add( self.m_staticText62, 0, wx.ALL, 5 )

        self.m_textCtrl34 = wx.TextCtrl( sbSizer32.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer9.Add( self.m_textCtrl34, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText63 = wx.StaticText( sbSizer32.GetStaticBox(), wx.ID_ANY, u"Attendance Event:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText63.Wrap( -1 )

        self.m_staticText63.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        #self.m_staticText63.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )

        fgSizer9.Add( self.m_staticText63, 0, wx.ALL, 5 )

        m_choice3Choices = ["--- LOADING ---"]
        self.m_choice3 = wx.Choice( sbSizer32.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice3Choices, 0 )
        self.m_choice3.SetSelection( 0 )
        fgSizer9.Add( self.m_choice3, 0, wx.ALL|wx.EXPAND, 5 )

        fetch_events = threading.Thread(target=get_online_events,args=(self,self.m_choice3,m_choice3Choices))
        fetch_events.daemon = True
        fetch_events.start()
        self.m_choice3.Disable()


        sbSizer32.Add( fgSizer9, 1, wx.EXPAND, 5 )


        bSizer14.Add( sbSizer32, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_button13 = wx.Button( self, wx.ID_ANY, u"Start Attendance", wx.DefaultPosition, wx.DefaultSize, 0|wx.BORDER_NONE )
        self.m_button13.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        self.m_button13.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )
        self.m_button13.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
        self.m_button13.SetToolTip("Commence Real Time Attendance Online")

        bSizer14.Add( self.m_button13, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
        self.m_button13.Disable()

        sbSizer33 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"AVAILABLE COM Ports" ), wx.VERTICAL )

        self.m_textCtrl35 = wx.TextCtrl( sbSizer33.GetStaticBox(), wx.ID_ANY, u"Loading Available Com Ports, Please Wait...", wx.DefaultPosition, wx.Size( 260,80 ), wx.HSCROLL| wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH )
        sbSizer33.Add( self.m_textCtrl35, 0, wx.ALL, 5 )


        bSizer14.Add( sbSizer33, 1, wx.ALL|wx.EXPAND, 5 )


        self.SetSizer( bSizer14 )
        self.Layout()
        #start thread to fetch lists of com ports
        com_ports = threading.Thread(target=get_com_port_lists_online,args=(self,self))
        com_ports.daemon = True
        com_ports.start()
        check_saved_reader_data(self.m_textCtrl34)
        
        com_port = self.m_textCtrl34.GetValue()
        
        if com_port !="":
            self.m_button13.Enable()
            
                                

        #self.Centre( wx.BOTH )

        # Connect Events
        self.m_choice3.Bind( wx.EVT_CHOICE, self.SetTolTip )
        self.m_button13.Bind( wx.EVT_BUTTON, self.StartOnlineAttendance )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def SetTolTip(self, event):

            self.m_choice3.SetToolTip(self.m_choice3.GetStringSelection())
            
    def StartOnlineAttendance( self, event ):

        #Get config file and autofill configuration details
        com_port = self.m_textCtrl34.GetValue()
        hardware_id = self.hardwrid
        computer_name = self.cpt_name
        selected_event = self.m_choice3.GetStringSelection()
        selectedEventValue = self.m_choice3.GetSelection()
        attendance_event = selected_event
        portal_event = attendance_event.split("(")[0]
        portal_event = portal_event.replace(' ','%20')
        #wx.CallAfter(print, upload_attendance.text)

        
        if selectedEventValue == 0:
                
                wx.MessageBox('Please Select An Attendance Event From DropDown.\nIf It Is Greyed Out, Check Your Internet or Be Sure Your Device is Registered and Approved.', 'Event Selection Error', wx.OK | wx.ICON_ERROR)
                return
        
        elif com_port =="":

                wx.MessageBox('Please Input COM Port Value For Smart Reader.', 'COM Port Error', wx.OK | wx.ICON_ERROR)
                return
        
        mode = "Online_attendance"
        save_com_port_data(com_port)
        date = ""
        ask = wx.MessageDialog(self, "Are You Sure You Want To Commence Online Attendance Session For:\nAttendance Event : "+attendance_event,'Online Attendance Verification', wx.YES_NO | wx.ICON_INFORMATION)
        result = ask.ShowModal()
        
        if result == wx.ID_YES:
                ask.Destroy()
                pass
                
        elif result == wx.ID_NO:
                
                ask.Destroy()
                return
        if os.path.isfile(resource_path("smart-church/resources/app/nativefier.json")) and os.access(resource_path("smart-church/resources/app/nativefier.json"), os.R_OK):
                
                pass

        else:
                wx.MessageBox('Embedded Browser Configuration File is Corrupted. Please Reinstall Application', 'Corrupt Configuration File', wx.OK | wx.ICON_ERROR)
                return

        global blocked
        blocked = 0
        global timer
        timer = TimerDialogue(self)
        #start thread to monitor when browser comes up then hide it immidiately
        absl = threading.Thread(target=find_web_browser,args=(self, com_port,hardware_id,computer_name,attendance_event,mode,date,timer))
        absl.daemon = True
        absl.start()
        #set global info status before loading modal
        global infoStatus
        infoStatus = "check_for_browser"
        evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId,self.Parent.loading.GetId())
        wx.PostEvent(self.Parent.loading, evt)
        self.Hide()
        #self.Parent.Hide()
        SW_HIDE = 0
        info = subprocess.STARTUPINFO()
        info.dwFlags = 1#subprocess.STARTF_USESHOWWINDOW
        info.wShowWindow = SW_HIDE
        #write URL for Online Voting
        obfuscate_url()
        with fileinput.FileInput(resource_path("smart-church/resources/app/nativefier.json"), inplace=True, backup='.bak') as file:
                for line in file:

                        print(re.sub('"targetUrl":\S+,', '"targetUrl":"https://smartchurchattendance.com.ng/smartChurch/Attendance?hid='+hardware_id+'&&cpt='+computer_name+'&&event='+portal_event+'",',line), end='')
                        time.sleep(2)
                        
        proc = subprocess.Popen([resource_path('smart-church/SMARTChurchApp.exe')], startupinfo = info, stdout=None, stderr=None, close_fds=True )
        atexit.register(proc.terminate)
        pid = proc.pid
        #subprocess.check_call(resource_path('smart-church/SMART Church App.exe'))
        #self.Parent.Show()
        


###########################################################################
## Class OfflineEventsDialogue
###########################################################################

class OfflineEventsDialogue ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Offline Attendance Config", pos = wx.DefaultPosition, size = wx.Size( 300,350 ), style = wx.DEFAULT_DIALOG_STYLE|wx.FRAME_FLOAT_ON_PARENT )

        self.hardwrid = check_output('wmic csproduct get uuid',shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        self.hardwrid = self.hardwrid.decode().strip()
        self.hardwrid = self.hardwrid.replace('UUID','')
        self.hardwrid = self.hardwrid.replace('-','')
        self.hardwrid = self.hardwrid.strip()
        self.cpt_name = os.environ['COMPUTERNAME']
        self.cpt_name = self.cpt_name.replace('-','')
        self.cpt_name = self.cpt_name.replace('_','')
        self.cpt_name= self.cpt_name.strip()
        
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.Colour( 207, 207, 207 ) )

        bSizer12 = wx.BoxSizer( wx.VERTICAL )
        gSizer5 = wx.GridSizer( 0, 2, 0, 0 )
        #bSizer12.Add( sbSizer30, 1, wx.ALIGN_BOTTOM|wx.ALL|wx.EXPAND, 5 )
        sbSizer30 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Event Selection" ), wx.VERTICAL )

        sbSizer30.SetMinSize( wx.Size( -1,5 ) )
        fgSizer8 = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizer8.SetFlexibleDirection( wx.BOTH )
        fgSizer8.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_staticText55 = wx.StaticText( sbSizer30.GetStaticBox(), wx.ID_ANY, u"Smart Reader Com Port:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText55.Wrap( -1 )

        self.m_staticText55.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        #self.m_staticText55.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )

        fgSizer8.Add( self.m_staticText55, 0, wx.ALL, 5 )

        self.m_textCtrl31 = wx.TextCtrl( sbSizer30.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer8.Add( self.m_textCtrl31, 0, wx.ALL, 5 )

        self.m_staticText56 = wx.StaticText( sbSizer30.GetStaticBox(), wx.ID_ANY, u"Attendance Event:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText56.Wrap( -1 )

        self.m_staticText56.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        #self.m_staticText56.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )

        fgSizer8.Add( self.m_staticText56, 0, wx.ALL, 5 )
        global self2
        self2 = self
        global m_choice2Choices
        m_choice2Choices = ["-- LOADING ---"]
        global m_choices
        self.m_choice2 = wx.Choice( sbSizer30.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice2Choices, 0|wx.BORDER_NONE )
        self.m_choice2.SetSelection( 0 )
        fgSizer8.Add( self.m_choice2, 0, wx.ALL, 5 )
        m_choices = self.m_choice2
        fetch_events = threading.Thread(target=get_offline_events,args=(self,self.m_choice2,m_choice2Choices))
        fetch_events.daemon = True
        fetch_events.start()
        self.m_choice2.Disable()

        self.m_staticText15 = wx.StaticText( sbSizer30.GetStaticBox(), wx.ID_ANY, u"Attendance Date: ", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText15.Wrap( -1 )

        self.m_staticText15.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        #self.m_staticText15.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )

        fgSizer8.Add( self.m_staticText15, 0, wx.ALL, 5 )

        self.m_datePicker1 = wx.adv.DatePickerCtrl( sbSizer30.GetStaticBox(), wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.Size( 110,-1 ), wx.adv.DP_DROPDOWN|wx.BORDER_NONE )
        fgSizer8.Add( self.m_datePicker1, 0, wx.ALL, 5 )


        sbSizer30.Add( fgSizer8, 1, wx.EXPAND, 5 )


        bSizer12.Add( sbSizer30, 1, wx.ALIGN_BOTTOM|wx.ALL|wx.EXPAND, 5 )

        self.m_button5 = wx.Button( self, wx.ID_ANY, u"Download Data", wx.DefaultPosition, wx.DefaultSize, wx.BORDER_NONE|0 )
        self.m_button5.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        self.m_button5.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )
        self.m_button5.SetBackgroundColour( wx.Colour( 255, 40, 40 ) )
        self.m_button5.SetToolTip("Download or Update Offline Data / upload local attendance data on Local Machine")
        

        gSizer5.Add( self.m_button5, 0, wx.ALL|wx.ALIGN_LEFT, 5 )

        self.m_button9 = wx.Button( self, wx.ID_ANY, u"Start Attendance", wx.DefaultPosition, wx.DefaultSize, 0|wx.BORDER_NONE )
        self.m_button9.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        self.m_button9.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )
        self.m_button9.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
        self.m_button9.SetToolTip("Commence Attendance On Local Machine Without Internet")

        gSizer5.Add( self.m_button9, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
        self.m_button9.Disable()
        
        bSizer12.Add( gSizer5, 1, wx.ALL, 5 )


        #self.m_staticText61 = wx.StaticText( self, wx.ID_ANY, u"Note: Download Online Data to Update Events", wx.DefaultPosition, wx.DefaultSize, 0 )
        #self.m_staticText61.Wrap( -1 )

        #self.m_staticText61.SetForegroundColour( wx.Colour( 255, 0, 0 ) )

        #bSizer12.Add( self.m_staticText61, 0, wx.ALL, 5 )

        sbSizer31 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Available COM Ports" ), wx.VERTICAL )

        self.m_textCtrl33 = wx.TextCtrl( sbSizer31.GetStaticBox(), wx.ID_ANY, u"Loading Available Com Ports, Please Wait...", wx.DefaultPosition, wx.Size( 260,80 ), wx.HSCROLL| wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH  )
        sbSizer31.Add( self.m_textCtrl33, 0, wx.ALL|wx.EXPAND, 5 )


        bSizer12.Add( sbSizer31, 1, wx.ALL|wx.EXPAND, 5 )
        self.loading = wx.Button( self, wx.ID_ANY, u"", wx.DefaultPosition, wx.Size(0,0),wx.BORDER_NONE )
        self.loading.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        bSizer12.Add( self.loading, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
        #self.loading.Hide()


        self.SetSizer( bSizer12 )
        #self.Layout()
        com_ports = threading.Thread(target=get_com_port_lists_offline,args=(self,self))
        com_ports.daemon = True
        com_ports.start()
        check_saved_reader_data(self.m_textCtrl31)
        
        com_port = self.m_textCtrl31.GetValue()
        if com_port !="":
            self.m_button9.Enable()

        #self.Centre( wx.BOTH )

        # Connect Events
        self.m_choice2.Bind( wx.EVT_CHOICE, self.SetTolTip )
        self.loading.Bind( wx.EVT_BUTTON, self.start_modal )
        self.m_button9.Bind( wx.EVT_BUTTON, self.startOfflineAttendance )
        self.m_button5.Bind( wx.EVT_BUTTON, self.Downloaddata )

    def __del__( self ):
        pass

    def SetTolTip(self, event):

            self.m_choice2.SetToolTip(self.m_choice2.GetStringSelection())

            
    def Downloaddata(self,event):
        global infoStatus
        ask = wx.MessageDialog(self, "Ensure That This Device is Already Registered Online.\nAny Previous Data Available on Device Will Be Overwritten. You Will Not Be Able To proceed If Offline Attendance is Present. Continue?",'Data Download Notice', wx.YES_NO | wx.ICON_INFORMATION)
        result = ask.ShowModal()
        
        if result == wx.ID_YES:
                
            if not os.path.exists("c:/ProgramData/SmartChurchApp/offline_data"):
                    os.makedirs("c:/ProgramData/SmartChurchApp/offline_data")
                    ret = check_output('attrib +s +h c:/ProgramData/SmartChurchApp/offline_data',shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                
            offline_path = 'c:/ProgramData/SmartChurchApp/offline_data/'
            for i in os.listdir(offline_path):

                    if os.path.isfile(os.path.join(offline_path,i)) and i.startswith('attendance_') and os.path.getsize(offline_path+i)!=0:

                            ask2 = wx.MessageDialog(self, "You Must Upload Offline Attendance First.\nPlease Close Application, Connect Your Internet and Launch Application Again\nOR Wait For A While For Auto Upload.\nOR Click YES To Attempt Upload Now, NO To Wait",'Offline Attendance Available!', wx.YES_NO | wx.ICON_ERROR)
                            result2 = ask2.ShowModal()
                            if result2 == wx.ID_YES:
                                    infoStatus = "upload_offline_attendance"
                                    evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId,self.loading.GetId())
                                    wx.PostEvent(self.loading, evt)
                                    return
                            elif result2 == wx.ID_NO:
                                    ask2.Destroy()
                                    return

            
            infoStatus = "download_offline_data"
            evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId,self.loading.GetId())
            wx.PostEvent(self.loading, evt)
            
        elif result == wx.ID_NO:
            ask.Destroy()
            return

        
    # Virtual event handlers, overide them in your derived class
    def start_modal(self, event):
        
        global infoStatus
        dlg = InfoDialogue(self)
        loading_status = threading.Thread(target=load_modal,args=(self,dlg,infoStatus))
        loading_status.daemon = True
        loading_status.start()
        dlg.ShowModal()
        
    def startOfflineAttendance( self, event ):
        
        #Get config file and autofill configuration details on next run
        com_port = self.m_textCtrl31.GetValue()
        #Get config file and autofill configuration details
        hardware_id = self.hardwrid
        computer_name = self.cpt_name
        selected_event = self.m_choice2.GetStringSelection()
        attendance_event = selected_event
        selectedEventValue = self.m_choice2.GetSelection()
        
        if selectedEventValue == 0:
                wx.MessageBox('Please Select An Attendance Event From DropDown.\nIf It Is Greyed Out, You Must Download Data From Online Database.', 'Event Selection Error', wx.OK | wx.ICON_ERROR)
                return
        
        elif com_port =="":

                wx.MessageBox('Please Input COM Port Value For Smart Reader.', 'COM Port Error', wx.OK | wx.ICON_ERROR)
                return
                
        mode = "Offline_attendance"
        save_com_port_data(com_port)
        date = self.m_datePicker1.GetValue()
        date = date.Format("%Y-%m-%d")
        ask = wx.MessageDialog(self, "Are You Sure You Want To Commence Attendance Session For:\nAttendance Event : "+attendance_event+"\nAttendance Date : "+date+'\nNote: Application Will Attempt To Upload Attendance Next Time You Run App.','Offline Attendance Verification', wx.YES_NO | wx.ICON_INFORMATION)
        result = ask.ShowModal()
        
        if result == wx.ID_YES:
                ask.Destroy()
                pass
                
        elif result == wx.ID_NO:
                
                ask.Destroy()
                return

        if os.path.isfile(resource_path("smart-church/resources/app/nativefier.json")) and os.access(resource_path("smart-church/resources/app/nativefier.json"), os.R_OK):
                
                pass

        else:
                wx.MessageBox('Embedded Browser Configuration File is Corrupted. Please Reinstall Application', 'Corrupt Configuration File', wx.OK | wx.ICON_ERROR)
                return

                
        #print(str(date))
        global blocked
        if not os.path.exists("c:/ProgramData/SmartChurchApp/offline_data"):
                
                blocked = 1
        else:
                blocked = 0

        if os.path.isfile(resource_path("smart-church/resources/app/nativefier.json")) and os.access(resource_path("smart-church/resources/app/nativefier.json"), os.R_OK):
                
                pass

        else:
                wx.MessageBox('Embedded Browser Configuration File is Corrupted. Please Reinstall Application', 'Corrupt Configuration File', wx.OK | wx.ICON_ERROR)
                return

        global timer
        timer = TimerDialogue(self)
        
        #modify browser url before silently opening
        global infoStatus
        infoStatus = "check_for_browser"
        evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId,self.Parent.loading.GetId())
        wx.PostEvent(self.Parent.loading, evt)
        self.Hide()
        #self.Parent.Hide()
        SW_HIDE = 0
        info = subprocess.STARTUPINFO()
        info.dwFlags = 1#subprocess.STARTF_USESHOWWINDOW
        info.wShowWindow = SW_HIDE
        #write URL for offline attendance
        obfuscate_url()
        with fileinput.FileInput(resource_path("smart-church/resources/app/nativefier.json"), inplace=True, backup='.bak') as file:
                for line in file:
                        print(re.sub('"targetUrl":\S+,', '"targetUrl":"file:///index.html",',line), end='')

        html = '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>SmartChurch Offline Attendance</title></head><body style="background-color:#c9c9c9; font-family: Arial Narrow;" ondragstart="return false;"><div style="position: absolute;top: 0; right: 0;left: 0; height: 30px; font-size: 24px; color: #ffffff; background-color: red; text-align: center; padding: 10px;">OFFLINE ATTENDANCE</div><div style="height: 100%; padding: 10px; border:none; margin-left: 5%; margin-right: 5%; background-color: #cbcbcbcb;"><img style="display: block; margin: 0px auto; margin-top: 50px;" src="rfid_load.gif"><div style="text-align: center; margin-top: -150px;"><h1 class="name">PLACE YOUR CARD ON SMART READER</h1><br></div></div><footer style="position: fixed; text-align: center; width: 100%; bottom: 5px; left:0;">SmartChurch Attendance System Copyright &copy; '+str(datetime.now().year)+'.</footer><style type="text/css">body{user-select: none;}</style></body></html>'
        log = open(resource_path("smart-church/resources/app/index.html"),"w")
        log.write(html)
        log.close()
        time.sleep(1)
        #start thread to monitor when browser comes up then hide it immidiately
        absl = threading.Thread(target=find_web_browser,args=(self, com_port,hardware_id,computer_name,attendance_event,mode,date,timer))
        absl.daemon = True
        absl.start()
        #monitor_browser = threading.Thread(target=disable_minimize,args=())
        #monitor_browser.daemon = True
        #monitor_browser.start()


        proc2 = subprocess.Popen([resource_path('smart-church/SMARTChurchApp.exe')], startupinfo = info, stdout=None, stderr=None, close_fds=True )
        atexit.register(proc2.terminate)
        pid2 = proc2.pid

        #subprocess.check_call(resource_path('smart-church/SMART Church App.exe'))
        #self.Parent.Show()


###########################################################################
## Class VisitorDialog
###########################################################################

class VisitorDialog ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Register Visitor", pos = wx.DefaultPosition, size = wx.Size( 250,350 ), style = wx.DEFAULT_DIALOG_STYLE|wx.FRAME_FLOAT_ON_PARENT )
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.hardwrid = check_output('wmic csproduct get uuid',shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        self.hardwrid = self.hardwrid.decode().strip()
        self.hardwrid = self.hardwrid.replace('UUID','')
        self.hardwrid = self.hardwrid.strip()
        self.hardwrid = self.hardwrid.replace('-','')
        self.cpt_name = os.environ['COMPUTERNAME']
        self.cpt_name = self.cpt_name.replace('-','')
        self.cpt_name = self.cpt_name.replace('_','')
        self.cpt_name= self.cpt_name.strip()
        
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.Colour( 207, 207, 207 ) )

        bSizer10 = wx.BoxSizer( wx.VERTICAL )

        sbSizer28 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Visitor Registration" ), wx.VERTICAL )

        fgSizer7 = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizer7.SetFlexibleDirection( wx.BOTH )
        fgSizer7.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_staticText48 = wx.StaticText( sbSizer28.GetStaticBox(), wx.ID_ANY, u"First Name:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText48.Wrap( -1 )

        self.m_staticText48.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        #self.m_staticText48.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )

        fgSizer7.Add( self.m_staticText48, 0, wx.ALL, 5 )

        self.m_textCtrl23 = wx.TextCtrl( sbSizer28.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer7.Add( self.m_textCtrl23, 0, wx.ALL, 5 )

        self.m_staticText49 = wx.StaticText( sbSizer28.GetStaticBox(), wx.ID_ANY, u"Last Name:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText49.Wrap( -1 )

        self.m_staticText49.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        #self.m_staticText49.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )

        fgSizer7.Add( self.m_staticText49, 0, wx.ALL, 5 )

        self.m_textCtrl24 = wx.TextCtrl( sbSizer28.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer7.Add( self.m_textCtrl24, 0, wx.ALL, 5 )

        self.m_staticText50 = wx.StaticText( sbSizer28.GetStaticBox(), wx.ID_ANY, u"Address:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText50.Wrap( -1 )

        self.m_staticText50.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        #self.m_staticText50.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )

        fgSizer7.Add( self.m_staticText50, 0, wx.ALL, 5 )

        self.m_textCtrl25 = wx.TextCtrl( sbSizer28.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_CHARWRAP )
        fgSizer7.Add( self.m_textCtrl25, 0, wx.ALL, 5 )

        self.m_staticText51 = wx.StaticText( sbSizer28.GetStaticBox(), wx.ID_ANY, u"Phone Number:", wx.DefaultPosition, wx.DefaultSize, 0|wx.BORDER_NONE )
        self.m_staticText51.Wrap( -1 )

        self.m_staticText51.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        #self.m_staticText51.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )

        fgSizer7.Add( self.m_staticText51, 0, wx.ALL, 5 )

        self.m_textCtrl26 = wx.TextCtrl( sbSizer28.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_textCtrl26.SetMaxLength( 11 )
        fgSizer7.Add( self.m_textCtrl26, 0, wx.ALL, 5 )

        self.m_staticText54 = wx.StaticText( sbSizer28.GetStaticBox(), wx.ID_ANY, u"Email Address:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText54.Wrap( -1 )

        self.m_staticText54.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        #self.m_staticText54.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )

        fgSizer7.Add( self.m_staticText54, 0, wx.ALL, 5 )

        self.m_textCtrl28 = wx.TextCtrl( sbSizer28.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer7.Add( self.m_textCtrl28, 0, wx.ALL, 5 )

        self.m_staticText16 = wx.StaticText( sbSizer28.GetStaticBox(), wx.ID_ANY, u"Visitation date:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText16.Wrap( -1 )

        self.m_staticText16.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        #self.m_staticText16.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )

        fgSizer7.Add( self.m_staticText16, 0, wx.ALL, 5 )

        self.m_datePicker2 = wx.adv.DatePickerCtrl( sbSizer28.GetStaticBox(), wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.Size( 110,-1 ), wx.adv.DP_DEFAULT|wx.adv.DP_DROPDOWN )
        fgSizer7.Add( self.m_datePicker2, 0, wx.ALL, 5 )

        self.m_staticText52 = wx.StaticText( sbSizer28.GetStaticBox(), wx.ID_ANY, u"Membership:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText52.Wrap( -1 )

        self.m_staticText52.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        #self.m_staticText52.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )

        fgSizer7.Add( self.m_staticText52, 0, wx.ALL, 5 )

        m_choice1Choices = [ u"Yes", u"No", u"Non Believer" ]
        self.m_choice1 = wx.Choice( sbSizer28.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice1Choices, 0 )
        self.m_choice1.SetSelection( 0 )
        fgSizer7.Add( self.m_choice1, 0, wx.ALL|wx.EXPAND, 5 )


        sbSizer28.Add( fgSizer7, 1, wx.EXPAND, 5 )

        self.m_button8 = wx.Button( sbSizer28.GetStaticBox(), wx.ID_ANY, u"Register", wx.DefaultPosition, wx.DefaultSize, wx.BORDER_NONE|wx.BU_EXACTFIT )
        self.m_button8.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        self.m_button8.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHTTEXT ) )
        self.m_button8.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
        self.m_button8.SetToolTip("Register Visitor Online")

        sbSizer28.Add( self.m_button8, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )


        bSizer10.Add( sbSizer28, 1, wx.ALL|wx.EXPAND|wx.RIGHT, 5 )


        self.SetSizer( bSizer10 )
        self.Layout()

        #self.Centre( wx.BOTH )

        # Connect Events
        self.m_button8.Bind( wx.EVT_BUTTON, self.RegisterVisitor )
        
    def on_close(self, event):
        self.Destroy()

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def RegisterVisitor( self, event ):
        global firstname
        firstname = self.m_textCtrl23.GetValue()
        global lastname
        lastname = self.m_textCtrl24.GetValue()
        global address
        address = self.m_textCtrl25.GetValue()
        global phone_number
        phone_number = str(self.m_textCtrl26.GetValue())
        global email
        email = self.m_textCtrl28.GetValue()
        global date
        date = self.m_datePicker2.GetValue()
        date = str(date.Format("%Y-%m-%d"))
        global membership
        membership = self.m_choice1.GetStringSelection()
        global infoStatus
        infoStatus = "reg_visitor"
        evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId,self.Parent.loading.GetId())
        wx.PostEvent(self.Parent.loading, evt)
        #self.Hide()
        
        #event.Skip()

class AboutSoftware(wx.Dialog):

    def __init__( self, parent ):
        
        
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Smart Church App", pos = wx.DefaultPosition, size = wx.Size( 280,240 ), style = wx.DEFAULT_DIALOG_STYLE )
        
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.Colour( 207, 207, 207 ) )

        bSizer5 = wx.BoxSizer( wx.VERTICAL )

        sbSizer6 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"About Smart Church" ), wx.VERTICAL )
        bSizer9 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText18 = wx.StaticText( sbSizer6.GetStaticBox(), wx.ID_ANY, u"This Application is Designed For Automated Attendance Using Smart Card Technology And Mobile QR Code Scan. Church Members Only Need to Place Smart Card 4cm Away From Hardware Device or Scan QR Code to Register their Attendance\nConfigured by Church Secretary.\nVisit Website for More.", wx.DefaultPosition, wx.Size( 260,130 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE )
        self.m_staticText18.Wrap( -1 )

        #self.m_staticText18.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )

        bSizer9.Add( self.m_staticText18, 0, wx.ALL, 5 )

        self.m_hyperlink2 = wx.adv.HyperlinkCtrl( sbSizer6.GetStaticBox(), wx.ID_ANY, u"Smart Church Website", u"https://smartchurchattendance.com.ng/", wx.DefaultPosition, wx.DefaultSize, wx.adv.HL_DEFAULT_STYLE )
        bSizer9.Add( self.m_hyperlink2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.SHAPED, 5 )


        sbSizer6.Add( bSizer9, 1, wx.EXPAND, 5 )


        bSizer5.Add( sbSizer6, 1, wx.ALL|wx.EXPAND, 5 )


        self.SetSizer( bSizer5 )
        self.Layout()
        
    def on_close(self, event):
        self.Destroy()

        #self.Centre( wx.BOTH )

def __del__( self ):
        
        pass

class TimerDialogue(wx.Dialog):
        
    def __init__(self,parent):
        
        super().__init__(parent, id = wx.ID_ANY, title = u"Smart Church Timer", size = wx.Size( 150,150 ), style = wx.TAB_TRAVERSAL|wx.FRAME_FLOAT_ON_PARENT|wx.FRAME_NO_TASKBAR)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetBackgroundColour( wx.Colour( 207, 207, 207 ) )
        self.SetSizer(self.sizer)
        anim = Animation(resource_path("Timer.gif"))
        self.ctrl = AnimationCtrl(self, -1, anim, pos=(25, 25))
        self.ctrl.Play()
        label = ("Retrying Connection In")
        self.text = wx.StaticText(self, label=label, pos=(15, 10))
        self.text.SetFont( wx.Font( 6, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial Rounded MT Bold" ) )
        #only change label2 and text position at runtime
        label2 = ("Seconds...")
        self.text2 = wx.StaticText(self, label=label2, pos=(45, 130))
        self.text2.SetFont( wx.Font( 8, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial Rounded MT Bold" ) )
        

class InfoDialogue(wx.Dialog):
 
        
    def __init__(self,parent):
        
        super().__init__(parent, id = wx.ID_ANY, title = u"Smart Church Loader", size = wx.Size( 250,200 ), style = wx.TAB_TRAVERSAL|wx.FRAME_FLOAT_ON_PARENT|wx.FRAME_NO_TASKBAR)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetBackgroundColour( wx.Colour( 207, 207, 207 ) )
        self.SetSizer(self.sizer)
        anim = Animation(resource_path("ClipartKey_1167914.gif"))
        ctrl = AnimationCtrl(self, -1, anim, pos=(100, 5))
        anim2 = Animation(resource_path("loading2.gif"))
        ctrl2 = AnimationCtrl(self, -1, anim2, pos=(100, 120))
        ctrl.Play()
        ctrl2.Play()
        label = ("Smart Church App")
        self.text = wx.StaticText(self, label=label, pos=(30, 85))
        self.text.SetFont( wx.Font( 15, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
        #self.text.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )

        #only change label2 and text position at runtime
        label2 = ("Loading Smart Church App...")
        self.text2 = wx.StaticText(self, label=label2, pos=(45, 175))
        #self.text2.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )
        self.text2.SetFont( wx.Font( 8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial Rounded MT Bold" ) )
        
        global infoStatus
        
        if infoStatus == "check_for_browser":
            
            self.Layout()
            
        elif infoStatus == "reg_visitor":
            
            visitorFrame = win32gui.FindWindowEx(None,None,None,"Register Visitor")
            x0, y0, x1, y1 = win32gui.GetWindowRect(visitorFrame)

            self.SetPosition(pt=(x1-200, y0+50))

        elif infoStatus == "startup":
                
                self.Center( wx.BOTH )

        else:

            self.Layout()
            #self.Center( wx.BOTH )
        
        

if __name__ == "__main__":
        
        if is_admin():

                pass
        else:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv[1:]), None, 1)
                sys.exit()

        verification()
        if not os.path.exists("c:/ProgramData/SmartChurchRun"):
                os.makedirs("c:/ProgramData/SmartChurchRun")
                ret = check_output('attrib +s +h c:/ProgramData/SmartChurchRun',shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
                ret = check_output('attrib +s +h c:/ProgramData/SmartChurchRun',shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                
        #os.makedirs(resource_path("smart-church"))        
        app = wx.App(redirect=True,filename="smartchurch.log")
        locale = wx.Locale(wx.LANGUAGE_ENGLISH)
        frame2 = Smart_Church_Clinent(None)
        frame2.Show()
        app.MainLoop()


from __future__ import print_function
import httplib2
import os, io

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
import auth
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
credentials = authInst.getCredentials()

http = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v3', http=http)

       
def downloadFile(file_id,filepath):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    with io.open(filepath,'wb') as f:
        fh.seek(0)
        f.write(fh.read())


def searchFile(size,query):
    results = drive_service.files().list(
    pageSize=size,fields="nextPageToken, files(id, name, kind, mimeType)",q=query).execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(item)
            print('{0} ({1})'.format(item['name'], item['id']))
            downloadFile(str.format(item['id']),str.format(item['name']))
            ########################
            #del_response = drive_service.files().delete(fileId=item['id']).execute()#刪除id檔案
            #trash_response = drive_service.files().emptyTrash().execute()#清空垃圾桶   
            #print('delete')
            ######################## 
            
            
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ObjectProperty  # at top of file
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.lang import Builder
import numpy as np
import csv
from kivy.uix.popup import Popup

from kivy.config import Config
from kivy.core.window import Window

Config.set('graphics', 'resizable', 0)
Window.size = (320, 550)

class AccountDetailsForm(AnchorLayout):

    machine_box= ObjectProperty()
    first_box = ObjectProperty()
    last_box = ObjectProperty()

    def login(self):
        #####
        tototime = []#總時長
        rank =[]#排名
        tototimesort = []
        ranksort = []
        peoplenumber = 0
        #ofname="result"
        keyword="Success "
        ####
        trash_response = drive_service.files().emptyTrash().execute()#清空垃圾桶        

        for i in range(int(self.first_box.text),int(self.last_box.text)+1):
            searchFile(1000,"name contains '"+ self.machine_box.text+str(i) +"'")
############
        for i in range(int(self.first_box.text),int(self.last_box.text)+1):
            DQ=0
            allword=""
            try:
                f = open(self.machine_box.text+str(i)+".txt", 'r')
                for line in f.readlines():
                    allword=allword+line;
                    if("DQ" in line):
                        DQ=1 
                if(DQ==1):
                    continue
                
                if(allword.rfind(keyword) !=allword.find(keyword)):
                    tototime.append(int(allword[(allword.find(keyword)+8):(allword.find(keyword)+8+2)]
                        + allword[(allword.find(keyword)+8+3):(allword.find(keyword)+8+5)]
                        + allword[(allword.find(keyword)+8+6):(allword.find(keyword)+8+8)])
                        +int(allword[(allword.rfind(keyword)+8):(allword.rfind(keyword)+8+2)]
                        + allword[(allword.rfind(keyword)+8+3):(allword.rfind(keyword)+8+5)]
                        + allword[(allword.rfind(keyword)+8+6):(allword.rfind(keyword)+8+8)]))
                    tototimesort.append(tototime[peoplenumber])
                    ms=int(allword[(allword.find(keyword)+8+6):(allword.find(keyword)+8+8)])+int(allword[(allword.rfind(keyword)+8+6):(allword.rfind(keyword)+8+8)])
                    s=int(allword[(allword.find(keyword)+8+3):(allword.find(keyword)+8+5)])+int(allword[(allword.rfind(keyword)+8+3):(allword.rfind(keyword)+8+5)])
                    m=int(allword[(allword.find(keyword)+8):(allword.find(keyword)+8+2)])+int(allword[(allword.rfind(keyword)+8):(allword.rfind(keyword)+8+2)])
                    sm=str(m+(s//60))
                    ss=str((s+(ms//100))%60)
                    sms=str(ms%100)
                    if(int(sms)<10):
                        sms="0"+sms
                    if(int(ss)<10):
                        ss="0"+ss
                    if(int(sm)<10):
                        sm="0"+sm
                    rank.append([str(i)," "+sm+":"+ss+":"+sms])
                else:
                    tototime.append(int(allword[(allword.find(keyword)+8):(allword.find(keyword)+8+2)]
                            + allword[(allword.find(keyword)+8+3):(allword.find(keyword)+8+5)]
                            + allword[(allword.find(keyword)+8+6):(allword.find(keyword)+8+8)]))
                    tototimesort.append(tototime[peoplenumber])
                    rank.append([str(i),allword[(allword.find(keyword)+8-1):(allword.find(keyword)+8+8)]])
                peoplenumber +=1
                ranksort.append([str(peoplenumber),"",""])
            except IOError:
                print('ERROR: can not found ' )
                if f:
                    f.close()
            finally:
                if f:
                    f.close()


        tototimesort.sort()

        for i in range(0,peoplenumber):
            for j in range(0,peoplenumber):
                if(tototime[i]==tototimesort[j] and ranksort[j][1]==""):
                    ranksort[j][2]=rank[i][1]
                    ranksort[j][1]=rank[i][0]
                    break
        scoretxt="Ranking   Order   Total Time\n========================\n";

        with open(self.machine_box.text+'.csv','w',newline='') as f:
            csv_write = csv.writer(f)
            csv_write.writerow(["Ranking","Order","Total Time","Minus"])
            for i in range(0,peoplenumber):
                csv_write.writerow(ranksort[i])
                scoretxt=scoretxt+"       "+ranksort[i][0]+"   "+ranksort[i][1]+" "+ranksort[i][2]+"\n"
        f.close()
###########

        #self.response.text = "All Done!"
        
        popup = Popup(title='score', content=Label(text=scoretxt), size_hint=(None, None), size=(320, 400))

        # 将弹出窗口绑定到按钮上，并显示弹出窗口
        popup.open()
        #self.clear_widgets()
        #self.add_widget(Label(text='location'))

        

class Orkiv(App):
    pass

Orkiv().run()

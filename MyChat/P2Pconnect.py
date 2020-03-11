import socket
import os
from PyQt5 import QtWidgets,QtGui,QtCore
import json
import struct
import pyaudio
import pickle
#0代表请求好友，1代表回应好友请求，2代表正常文本消息，3代表离线通知，4代表文件发送，5代表群聊添加通知,6代表群聊信息,7代表群聊文件
class P2Pconnect(QtCore.QObject):
    def __init__(self,usr,usrIP):
        super(P2Pconnect, self).__init__()
        self.usr = usr
        self.usrIP = usrIP
        self.rev_word = ''
        self.newmessage = 0
        #self.process = 0
        #self.newfile = 0
    #类内绑定信号，发送接收的字符串
    rev_Signal = QtCore.pyqtSignal(list)
    process_Signal = QtCore.pyqtSignal(int)
    group_process_Signal = QtCore.pyqtSignal(int)
    revgroup_Signal = QtCore.pyqtSignal(list)

    def Listen(self):
        P2PServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        usrport = self.usrport = int('5' + self.usr[-4:]) #绑定学号后四位
        P2PServerSocket.bind((self.usrIP, usrport))
        P2PServerSocket.listen(10)
        buffsize = 1024
        # print('My ID is ready to receive')
        while True:
            #self.process = 0
            self.newmessage = 0
            connectionSocket, addr = P2PServerSocket.accept()
            #print(connectionSocket)
            self.rev_mes = connectionSocket.recv(2048)
            if(len(self.rev_mes)==4):
                head_len = struct.unpack('i', self.rev_mes)[0]
                print(head_len)
                #friend_name = connectionSocket.recv(10).decode()
                #print(friend_name)
                head_info = connectionSocket.recv(head_len)
                head_dirc = json.loads(head_info.decode('utf-8'))
                print(head_dirc)
                if('group_id' in head_dirc.keys()):
                    file_size = head_dirc['filesize']
                    file_name = head_dirc['filename']
                    group_id = head_dirc['group_id']
                    recv_len = 0
                    recv_mesg = b''
                    sav_file_name = file_name.split('\\')
                    print(sav_file_name[-1])
                    if (not os.path.exists('users/' + self.usr)):
                        os.mkdir('users/' + self.usr)
                    if (not os.path.exists('users/' + self.usr + '/' + 'files')):
                        os.mkdir('users/' + self.usr + '/' + 'files')
                    if (not os.path.exists('users/' + self.usr + '/' + 'files/' + group_id)):
                        os.mkdir('users/' + self.usr + '/' + 'files/' + group_id)
                    with open('users/' + self.usr + '/' + 'files/' + group_id+ '/' + sav_file_name[-1], 'ab+')as f:
                        self.group_process_Signal.emit(0)
                        while recv_len < file_size:
                            if file_size - recv_len > buffsize:
                                recv_mesg = connectionSocket.recv(buffsize)
                                f.write(recv_mesg)
                                recv_len += len(recv_mesg)
                            else:
                                recv_mesg = connectionSocket.recv(file_size - recv_len)
                                recv_len += len(recv_mesg)
                                f.write(recv_mesg)
                                self.group_process_Signal.emit(1)
                else:
                    friend_name = connectionSocket.recv(10).decode()
                    print(friend_name)
                    file_size = head_dirc['filesize']
                    file_name = head_dirc['filename']
                    recv_len = 0
                    recv_mesg = b''
                    sav_file_name = file_name.split('\\')
                    print(sav_file_name[-1])
                    if (not os.path.exists('users/' + self.usr)):
                        os.mkdir('users/' + self.usr)
                    if (not os.path.exists('users/' + self.usr + '/' + 'files')):
                        os.mkdir('users/' + self.usr + '/' + 'files')
                    if (not os.path.exists('users/' + self.usr + '/' + 'files/' + friend_name)):
                        os.mkdir('users/' + self.usr + '/' + 'files/' + friend_name)
                    with open('users/' + self.usr + '/' + 'files/' + friend_name + '/' + sav_file_name[-1], 'ab+')as f:
                        self.process_Signal.emit(0)
                        while recv_len < file_size:
                            if file_size - recv_len > buffsize:
                                recv_mesg = connectionSocket.recv(buffsize)
                                f.write(recv_mesg)
                                recv_len += len(recv_mesg)
                            else:
                                recv_mesg = connectionSocket.recv(file_size - recv_len)
                                recv_len += len(recv_mesg)
                                f.write(recv_mesg)
                                self.process_Signal.emit(1)
                        #self.process = (int)(recv_len/file_size)*100
                #self.newmessage = 1
                #self.rev_Signal.emit()
            else:
                self.rev_word = self.rev_mes.decode('utf-8')
                rev_wordlist = self.rev_word.split('#')
                print(rev_wordlist)
                if (rev_wordlist[3] == str(0)):
                    # self.rev_Signal.emit(rev_wordlist)
                    self.newmessage = 1
                elif (rev_wordlist[3] == str(1)):
                    # self.rev_Signal.emit(rev_wordlist)
                    self.newmessage = 1
                elif (rev_wordlist[3] == str(2)):
                    path = 'users/' + self.usr
                    if (not os.path.exists(path)):
                        os.mkdir(path)
                    with open('users/' + self.usr + '/' + rev_wordlist[0] + '.txt', 'a+')as g:
                        data = QtCore.QDateTime.currentDateTime()
                        currTime = data.toString("yyyy-MM-dd-hh:mm")
                        g.writelines(rev_wordlist[0] + " " + rev_wordlist[1] + "\n")
                        g.writelines(rev_wordlist[2] + "\n")
                        g.close()
                    self.newmessage = 1
                    # 发送收到的信息
                    self.rev_Signal.emit(rev_wordlist)
                elif (rev_wordlist[3] == str(3)):
                    self.newmessage = 1
                elif (rev_wordlist[3] == str(5)):
                    rev_group = rev_wordlist[2]
                    self.rev_grouplist = rev_group.split('-')
                    self.newmessage = 1
                elif(rev_wordlist[3] == str(6)):
                    word = rev_wordlist[2].split("$")
                    self.group_word = word
                    path = 'users/' + self.usr
                    if (not os.path.exists(path)):
                        os.mkdir(path)
                    with open('users/' + self.usr + '/' + word[1] + '.txt', 'a+')as g:
                        data = QtCore.QDateTime.currentDateTime()
                        currTime = data.toString("yyyy-MM-dd-hh:mm")
                        g.writelines(rev_wordlist[0] + " " + rev_wordlist[1] + "\n")
                        g.writelines(word[0] + "\n")
                        g.close()
                    self.newmessage = 1
                    self.revgroup_Signal.emit(rev_wordlist)
            connectionSocket.close()

    def SendMessage(self,usr,friend,friendIP,word,type):
        P2PclientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        friendport = int('5' + friend[-4:])
        print(friend)
        print(friendIP)
        print(friendport)
        P2PclientSocket.connect((friendIP, friendport))
        data = QtCore.QDateTime.currentDateTime()
        currTime = data.toString("yyyy-MM-dd-hh:mm")
        if(type==0):
            P2PclientSocket.send((usr + "#" + currTime + "#" + word + "#" + str(0)).encode())
        elif(type==1):
            P2PclientSocket.send((usr + "#" + currTime + "#" + word + "#" + str(1)).encode())
        elif (type == 2):
            P2PclientSocket.send((usr + "#" + currTime + "#" + word + "#" + str(2)).encode())
            path = 'users/' + self.usr
            if (not os.path.exists(path)):
                os.mkdir(path)
            with open('users/' + self.usr + '/' + friend + '.txt', 'a+')as g:
                g.writelines(usr + " " + currTime + "\n")
                g.writelines(word + "\n")
                g.close()
        elif(type==3):
            P2PclientSocket.send((usr + "#" + currTime + "#" + word + "#" + str(3)).encode())
        elif(type==4):
            head_info = json.dumps(word)  # 将字典转换成字符串
            head_info_len = struct.pack('i', len(head_info))  # 将字符串的长度打包
            print(head_info_len)
            print(head_info)
            P2PclientSocket.send(head_info_len)
            P2PclientSocket.send(head_info.encode('utf-8'))
            P2PclientSocket.send(usr.encode())
            with open(word['filename'], 'rb') as f:
                content = f.read()
                P2PclientSocket.sendall(content)
                #print("文件发送成功")
        elif(type==5):
            P2PclientSocket.send((usr + "#" + currTime + "#" + word + "#" + str(5)).encode())
        elif(type==6):
            #word[0]表示群聊消息，word[1]表示群聊ID
            P2PclientSocket.send((usr + "#" + currTime + "#" + word + "#" + str(6)).encode())
        elif(type==7):
            head_info = json.dumps(word)  # 将字典转换成字符串
            head_info_len = struct.pack('i', len(head_info))  # 将字符串的长度打包
            print(head_info_len)
            print(head_info)
            P2PclientSocket.send(head_info_len)
            #P2PclientSocket.send(usr.encode())
            P2PclientSocket.send(head_info.encode('utf-8'))
            with open(word['filename'], 'rb') as f:
                content = f.read()
                P2PclientSocket.sendall(content)
                # print("文件发送成功")
        P2PclientSocket.close()


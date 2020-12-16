import socket
import config
import threading
import random
import time
import json

# parametres locals
numProcess = 1
id = random.randint(1, 100)
pSuiv = (numProcess + 1) % config.NB_PROCESSUS
pPrec = config.NB_PROCESSUS if numProcess==1 else (numProcess-1)
sendPort = config.BASE_PORT + (0 if numProcess==config.NB_PROCESSUS else (numProcess))
recvPort = config.BASE_PORT + (0 if numProcess==1 else (numProcess-1))

# liste des processus presents sous forme [(id, @),]
listeProcessus = []
leader = None

# creer une socket datagrame de reception
UDPRecvSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# UDPRecvSocket.setblocking(0)
# relier la socket a l@
addressPortRecepteur = (config.HOST, recvPort)
UDPRecvSocket.bind(addressPortRecepteur)
print("serveur UDP en attente sur {}".format(addressPortRecepteur))

# creer une socket datagrame d'envoi
UDPSendSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

class RecvThread(threading.Thread):
    def __init__(self):
        super(RecvThread, self).__init__()

    def run(self):
        # reception des datagrames
        while(True):
            # try:
            bytesAddressPair = UDPRecvSocket.recvfrom(config.BUFFER_SIZE)
            data = bytesAddressPair[0]
            temp = json.loads(data)['temp']
            senderId = json.loads(data)['id']
            address = bytesAddressPair[1]
            print('recu {} par {}'.format(temp, senderId))
            # enregistrer le processus s'il n'existe pas
            if (senderId, address) not in listeProcessus:
                listeProcessus.append((senderId, address))
                print('liste des processus :', listeProcessus)
            global leader
            if leader==None and len(listeProcessus)==config.NB_PROCESSUS:
                leader = max(listeProcessus, key=lambda x: x[0])
            # except:
            #     print('erreur de reception')

class SendThread(threading.Thread):
    def __init__(self):
        super(SendThread, self).__init__()

    def run(self):
        # envoi des datagrames
        addressPortEnvoyeur = (config.HOST, sendPort)
        i = 5
        while(i>0):
            i -= 1
            time.sleep(5)
            temp = random.randint(0, 40)
            # temp = str(temp)
            data = json.dumps({'temp':temp, 'id':id, 'to':leader[0] if leader!=None else None})
            tempBytes = str.encode(data)
            # envoyer la temperature
            try:
                UDPSendSocket.sendto(tempBytes, addressPortEnvoyeur)
                print('processus {} envoi {} a {}'.format(numProcess, temp, addressPortEnvoyeur))
            except:
                print('erreur envoi {} vers {}'.format(numProcess, addressPortEnvoyeur))

recvT = RecvThread()
sendT = SendThread()
recvT.start()
sendT.start()

recvT.join()
sendT.join()
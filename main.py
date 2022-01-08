# -imports-
import socket
import random

# -definitions-
def sendmsg(message: str):
    irc.send(("PRIVMSG " + channel + " :" + message + "\r\n").encode())

# -server settings-
server = "irc.libera.chat"
port = 6667
channel = "#channel-name"
nickname = "bot-name"
adminPass = random.randint(1, 9999999999)

# -help command list-
commandList = [
        "!ping - test that the bot is active",
        "!help - get this list",
        "!shutdown <pass> - disconnect the bot"
        ]

# -command definitions-
def commands():
    if ":!help" in recieved:
        sendmsg("Commands:")
        for i in range(0, len(commandList)):
            sendmsg(commandList[i])

    if ":!ping" in recieved:
        sendmsg("Pong!")

    if ":!shutdown" in recieved:
        if recieved.split(":!shutdown")[1].strip() == str(adminPass):
            irc.close()
            print("Quitting.")
            quit()





# ---necessary stuff: don't edit this---
# -connection to server-
print("Connecting...")
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((server, port))
irc.send(("USER " + nickname + " " + nickname + " " + nickname + " :Gbottest\r\n").encode(encoding="UTF-8"))
irc.send(("NICK " + nickname + "\r\n").encode(encoding="UTF-8"))
irc.send(("JOIN " + channel + "\r\n").encode(encoding="UTF-8"))

while True:
    recieved = irc.recv(2048).decode("UTF-8")
    if recieved.__contains__("/NAMES") :
        print("Connected.")
        print("Shutdown pass is " + str(adminPass))
        log = open("history.log", "a")
        break

# -main loop-
while True:
    # -recieve messages-
    recieved = irc.recv(2048).decode("UTF-8")

    # -logging-
    log.write(recieved)

    # -stay alive-
    if recieved.startswith("PING"):
        irc.send(("PONG " + recieved.split()[1] + "\r\n").encode())

    # -attempt commands-
    try:
        commands()
    except:
        pass

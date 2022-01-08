# -imports-
import socket
import threading

# -server settings-
server = "irc.libera.chat"
port = 6667
channel = "#Galladite"
nickname = "bot-control"

# -definitions-
def sendmsg(message: str):
    irc.send(("PRIVMSG " + channel + " :" + message + "\r\n").encode())

command = ""
def reply():
    while True:
        command = str(input("> "))
        commands(command)
        print("")

# -help command list-
commandList = [
        "activate <password> - identify, allowing you to give orders",
        "command-local <bot name> <command> - force a bot to attempt a local command using os.system",
        "command <command> - execute an IRC command as this bot",
        "help - get this list",
        "kill <bot name> - disconnect a bot and stop the script",
        "ping <bot name> - make a bot send a message to IRC to check they are available",
        "sendmsg <message> - directly send a message to the channel",
        "\nAny instance of <bot name> may also be replaced by \"all\""
        ]

# -command definitions-
def commands(command):
    global activated
    if command.split(" ")[0] == "activate":
        irc.send(("privmsg nickserv :identify bot-control " + command.split(" ")[1] + "\r\n").encode(encoding="UTF-8"))
        print("Activated.")

    if command.split(" ")[0] == "command":
        msgToSend = command.split(" ")[1:] #get the command from the message
        irc.send((msgToSend[0].upper() + " " + " ".join(msgToSend[1:]) + "\r\n").encode(encoding="UTF-8")) # prepare and send the command
        print("Command sent.")

    if command.split(" ")[0] == "command-local":
        sendmsg("!command-local " + " ".join(command.split(" ")[1:]))

    if command == "help":
        print("Commands:")
        for i in range(0, len(commandList)):
            print(commandList[i])

    if command.split(" ")[0] == "kill":
        if command.split(" ")[1] == "all":
            sendmsg("!kill all")
            print("All bots killed.")
        else:
            sendmsg("!kill " + command.split(" ")[1])
            print("Bot " + command.split(" ")[1] + " killed.")

    if command.split(" ")[0] == "ping":
        if command.split(" ")[1] == "all":
            sendmsg("!ping all")
            print("All bots pinged.")
        else:
            sendmsg("!ping " + command.split(" ")[1])
            print("Bot " + command.split(" ")[1] + " pinged.")

    if command.split(" ")[0] == "sendmsg":
        msgToSend = command.split(" ")
        msgToSend.pop(0)
        sendmsg(" ".join(msgToSend))
        print("Message sent.")


# ---necessary stuff: don't edit this---
# -connection to server-
print("Connecting...")
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((server, port))
irc.send(("USER " + nickname + " " + nickname + " " + nickname + " :bot\r\n").encode(encoding="UTF-8"))
irc.send(("NICK " + nickname + "\r\n").encode(encoding="UTF-8"))
irc.send(("JOIN " + channel + "\r\n").encode(encoding="UTF-8"))

while True:
    recieved = irc.recv(2048).decode("UTF-8")
    if "/NAMES" in recieved:
        log = open("history.log", "a")
        print("Connected.")
        break

getCommands = threading.Thread(target=reply)
getCommands.start()

# -main loop-
while True:
    # -recieve messages-
    recieved = irc.recv(2048).decode("UTF-8")

    # -logging-
    log.write(recieved)

    # -stay alive-
    if recieved.startswith("PING"):
        irc.send(("PONG " + recieved.split()[1] + "\r\n").encode())

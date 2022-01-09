# lainzine-irc-bot
Requires settings changing at the top of both scripts.
Keep the "slave" script running on a bot, use the "master" script to control them from wherever.
Only the master script can control the slaves, and also only when "activated" within the script.

"Master" requires socket and threading
"Slave" requires os, random and socket (with the current modules - only socket is strictly necessary)

Current commands:   command-local - make slaves execute commands with os.system
                    command - make the master execute an IRC command
                    help - this list
                    kill - disconnect and stop the script of slaves
                    ping - make slaves respond
                    sendmsg - make the master send any message to the irc channel
More info can be found by typing "help" within the master script.

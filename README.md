# lainzine-irc-bot
Requires settings changing at the top of both scripts.
Keep the "slave" script running on a bot, use the "master" script to control them from wherever.
Only the master script can control the slaves, and also only when "activated" within the script.

"Master" requires socket and threading.
"Slave" requires os, platform, random, socket and threadig (with the current modules - only socket is strictly necessary).

Info on commands can be found by typing "help" within the master script or near the top of master.py.

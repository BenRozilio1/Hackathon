# Hackathon_Assignment
#Intro to Nets 2020 Hackathon Assignment - Keyboard Spamming

#Battle Royale ⌨👑⌨👑⌨👑⌨

Introduction
Your objective is to write a client-server application which will implement a fast-paced Keyboard
Spamming game. The players in this game are randomly divided into two teams, which have ten
seconds to mash as many keys on the keyboard as possible.
Each team in the course will write both a client application and a server application, and
everybody’s clients and servers are expected to work together with full compatibility.
Example Run
1. Team Mystic starts their server. The server prints out “Server started,
listening on IP address 172.1.0.4” and starts automatically sending out
“offer” announcements via UDP broadcast once every second.
2. Team Valor starts their server, which prints out “Server started, listening on
IP address 172.1.0.88” and also starts automatically sending out “offer”
announcements over UDP once every second.
3. Teams Instinct, Rocket, Beitar and Katamon start their clients. The clients all print out
“Client started, listening for offer requests...”. All of the clients get
the Mystic announcement first, and print out ““Received offer from 172.1.0.4,
attempting to connect...”
4. Each client connects to the Team Mystic server over TCP. After the connection
succeeds each client sends the team name over the TCP connection, followed by a line
break (‘\n’)
5. The server records the names sent by the clients, and assigns each of the clients
randomly to group 1 or group 2 (nothing needs to be sent to the clients when this
happens)
6. 10 seconds after the server was started, the game begins - the server sends a welcome
message to all of the clients with the names of the teams, for example:
Welcome to Keyboard Spamming Battle Royale.
Group 1:
==
Instinct
Rocket
Group 2:
==
Beitar
Katamon
Start pressing keys on your keyboard as fast as you can!!
7. Each client receives this message over TCP and prints it to the screen. Now every time
the user types in a key the client sends it to the server over TCP
8. Each time the server receives a key over TCP, it increments the counter for the relevant
group.
9. After 10 seconds, the game is finished. The server calculates the winner and sends a
summary message, for example: [EDITED to clarify: this string is sent to the teams]
Game over!
Group 1 typed in 104 characters. Group 2 typed in 28 characters.
Group 1 wins!
Congratulations to the winners:
==
Instinct
Rocket
10. The server closes the TCP connection, prints “Game over, sending out offer
requests...” and goes back to sending offer messages once a second
11. The clients print “Server disconnected, listening for offer
requests...” and go back to waiting for offer messages

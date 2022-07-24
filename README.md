### SMS Poker [GitHub](https://github.com/branconn/SMSPoker)
The idea is straightforward: an application that facilitates a text-based poker game with friends. No need for players to install any software. User input is received through sms, and game events are sent through it as well.

Execution will be a bit more difficult, but the nature of the problem allows it to be subdivided cleanly. I expect the majority of the energy will be spent finding the right free/cheap services to 1) send/receive sms 2) host the application. I am planning on using pythonAnywhere for the latter, but as I type this I'm considering stopping short of that and just running it local when I want to play. Simpler and more secure but not as useful as a demo of skill.

### Services
#### Send/Recieve SMS
Vonage : [Documentation for Vonage SMS API](https://developer.vonage.com/use-cases/two-way-sms-for-customer-engagement)

Other options I've come across are Twilio and Plivo. I did not find a good inbound SMS feature for Twilio's freemium tier. Plivo seemed like it checked all the boxes until I attempted to create an account They've severely limited personal project use and required a business email (I tried in vain to go around this with an [alias email](https://support.google.com/domains/answer/3251241?hl=en), but it was flagged). I guess they're focused on acquisition through undercutting Twilio's pricing vs offering accessible options for tinkerers.
#### Game Logic
Python
#### Remote hosting
PythonAnywhere : [PythonAnywhere Homepage](https://www.pythonanywhere.com)

PythonAnywhere is a great alternative to serving locally through a service like [ngrok](https://ngrok.com). I only chose PythonAnywhere because of familiarity from a prior project (the power of letting Ed courses use your service for free).
#### Database
Hopefully a simple JSON

Debating whether I even want to bother with save states. I'll burn that bridge when I come to it. 
# program-abmegle
Simple Python script to link a local Program-AB bot to Omegle random chat so your bot can talk to random people. Logs conversations at <PROGRAM-AB_PATH>/bots/<ACTIVE_BOT>/logs/<LOGFILE> where LOGFILE is a numbered txt file.

### Running

To run the script you will need to enter the name of the bot directory on line 14 - the _BOT variable

To start, in a terminal, from your Program-AB install directory run

```
python ABOMegle.py
```

and the bot will start looking for humans to talk to, like so:

```
Starting search...
started new conversation: f5u6veaqu03442tj6dgre9mub6
Looking for humans ...
Human is typing something...
```
#### Credit

##### Program-AB

Credit to Program-AB for being an awesome Java implementation of AIML2.0!

https://code.google.com/archive/p/program-ab/

##### joelisester-sandbox

Credit to joelisester-sandbox, who's chatbot.py code was brutally butchered to write this script.

The original code, and some other interesting stuff can be found here

https://code.google.com/archive/p/joelisester-sandbox/downloads

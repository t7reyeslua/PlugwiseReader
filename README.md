# PlugwiseReader
Scripts for retrieveing data from different Plugwise products.
* All scripts read the values from the corresponding plugwise product and store them in:
- Local MYSQL database 
- Emoncms database [https://github.com/emoncms/emoncms]

##Server
* PHP scripts to connect to the local database and insert the read values to the corresponding tables.

##Readers
### [Smile]
- Polls for new values every n seconds (5 seconds).
### [Stretch]
- Polls for new values every n seconds (5 seconds).
- Stores the recently read value only if it comes from a new measurement different from the previous one.
### [Stick]
- Requires this library: https://bitbucket.org/hadara/python-plugwise
- Polls for new values every n seconds (5 seconds).

This python script enables to control lg smart tv volume by using the regular mac keys.
Also, the script enalbes to turn on the tv using the eject button on the mac keyboard, and to 
wake it in case the volume commands have failed (becuse the tv is turned off), using wol.
Also, the volume command will be send only if the mac recognizes that the current sound output is the LG TV.

Dependencies:
The script uses bscpylgtv and wakeonlan as a dependency for the script.
install them using the following command:

pip install bscpylgtv wakeonlan

link to bscpylgtv on github:

https://github.com/chros73/bscpylgtv

This script uses switchaudio-osx in order to check for the current audio ouput, make sure to install it using

brew install switchaudio-osx

At the initial connection, the TV will require enabling the connection from the Mac.

Afterwards, make sure to configure the TV ip address and MAC address.
You can do it by editing the defualt config in the script itself, or alternitvaly, you can
create a config.json file, that has your addresses. you can use the defualt config as a template
for the config.json file.

Requirements: 
- The script needs input monitoring permisssions and accesiblity permissions, otherwise it won't be able to monitor volume keys presses. 
- LG Connect Apps needs to be enables on the TV settings, so commands that are sent from the mac will be recived on the TV.

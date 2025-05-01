This python script enables to control lg smart tv volume by using the regular mac keys.
Also, the script enalbes to turn on the tv using the eject button on the mac keyboard, and to 
wake it in case the volume command have failed (becuse the tv is turned off).
Also, the volume command will be send only if the mac recognizes that the current sound 
output is the LG TV.

Dependencies:
The script uses bscpylgtv and wakeonlan as a dependency for the script.
install them using the following command:

pip install bscpylgtv wakeonlan

link to bscpylgtv on github:

https://github.com/chros73/bscpylgtv

This script uses switchaudio-osx in order to check for the current audio ouput, make sure to install it using

brew install switchaudio-osx


Also, make sure that the script has input monitoring permisssions and accesiblity permissions, otherwise it won't be able to monitor volume keys presses. 


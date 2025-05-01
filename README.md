This python script enables to control lg smart tv volume by using the regular mac keys.
Make sure to chagne to ip in the script to the ip of your tv.

Dependencies:
The script uses bscpylgtv as a dependency for the script.
install using the following command:

pip install bscpylgtv

link to bscpylgtv on github:

https://github.com/chros73/bscpylgtv

This script uses switchaudio-osx in order to check for the current audio ouput, make sure to install it using

brew install switchaudio-osx


Also, make sure that the script has input monitoring permisssions and accesiblity permissions, otherwise it won't be able to monitor volume keys presses. 


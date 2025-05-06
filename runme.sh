#!/usr/bin/env bash

# mac shell script

# set program and rom directories here 
ZESARUX_DIR=/Applications/zesarux.app/Contents/MacOS/ 
JETPAC_TZX=~/roms/Jetpac.tzx/Jetpac.tzx

# there really should be no need to change anything below... 

# store the current working directory
STARTING_DIR="$(pwd)"

# this will run jetpac on emulator with the the remote debugging options enabled
cd ${ZESARUX_DIR}
./zesarux --enable-remoteprotocol --tape ${JETPAC_TZX}
cd ${STARTING_DIR}
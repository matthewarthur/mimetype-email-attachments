#!/bin/bash 
apt-get install -y gcc. ##works
apt-get install build-essential -y g++

git clone https://github.com/pjreddie/darknet.git
cd darknet
make

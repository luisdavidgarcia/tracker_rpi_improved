# Natural Mouse Tracker (Raspberry Pi recording modules)

To clone the repository, run the following in terminal. The recursive tag is required for the RFIDTagReader submodule to work correctly.
```
git clone --recursive https://github.com/ubcbraincircuits/NaturalMouseTracker_rpi
```
To install the setup scitpt by running 

```

./ setup.sh

```
To run the tracker cage, use 
```

cd tracker_rpi

python3 main2.py
```

# Basic Concept
![](setup.png)
- Any camera can be used as long as there is an over headview of all mice
- Any number of RFID reader modules can be used. Up to 9 readers have been tested
# High frame and resolutions can be achieved 
![](performance.png)
- can be record up to 40 fpd at 960 x960 on a Raspiberry Pi 4
# Full compile of analysis TBH

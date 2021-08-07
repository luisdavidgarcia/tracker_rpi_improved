# Py-based SYstemfor Chronic monitoring of rOdent Species (Raspberry Pi recording modules)

To clone the repository, run the following in terminal. The recursive tag is required for the RFIDTagReader submodule to work correctly.
```
git clone --recursive https://github.com/ubcbraincircuits/NaturalMouseTracker_rpi
```
To install the setup scitpt by running in the cloned folder

```
sudo chmod 777 setup.sh
sudo ./setup.sh
```
To run the tracker cage, enter the command in the cloned folder
```
sudo python3 main2.py
```

Full video tutorial on setting up the software and editing recording settings:

```
https://youtu.be/E22OtdMjgwc
```

# Basic Concept and Essential Hardware
![](concept.png)
- Any Pi compatible camera can be used as long as there is an over headview of all mice
- Timestamp of each is written to a separate csv file
- RFID readings and their corresponding timestamps are also written in a csv file

# FPS at Different Resolution on Pi3/4 
![](fps.png)
- can be record up to 40 fps at 960 x960 on a Raspiberry Pi 4

# Can Record Rodents in Various Settings

## Traditional Open-Field/Three Chamber
![](open_field.PNG) | ![](!three_chamber.PNG)

## Custom Home-cage Setups
![] (home_cage_example.PNG)

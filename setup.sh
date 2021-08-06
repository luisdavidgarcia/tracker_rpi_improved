#$ sudo chmod 765 pi_video_stream_setup.sh
#$ sudo ./pi_video_stream_setup.sh
    
    echo "Changing folder permission to user"
    _path = $PWD
    cd "/home/pi"
    cd "$_path"
    sudo chown pi $_path -R

    echo "Installing python packages"
    pip3 install numpy
    pip3 install schedule
    pip3 install imutils
    pip3 install wiringpi
    pip3 install tables
    sudo pip3 install opencv-python==4.1.1.26
    echo "Install complete\n Make sure you manually ENABLE CAMERA PORT."
    exit



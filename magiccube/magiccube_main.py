'''
Upgrade to Python 3.5.0: https://stackoverflow.com/questions/38393054/installing-python-3-5-via-apt-get
sudo apt-get install libssl-dev openssl
wget https://www.python.org/ftp/python/3.5.0/Python-3.5.0.tgz
tar xzvf Python-3.5.0.tgz
cd Python-3.5.0
./configure
make
sudo make install
'''

import platform
RUN_ON_EV3 = (platform.node() == 'ev3dev')
import magiccube_device as mcd
import magiccube_solver as mcs

if __name__ == "__main__":
    try:
        # pipe graphics through ssh to windows display with xterm:
        # https://jensd.be/68/linux/remote-graphical-linux-applications-on-linux-and-windows
        mcs.main()
    except KeyboardInterrupt:
        pass

    if RUN_ON_EV3:
        mcd.motor_a.stop(stop_action="coast")
        mcd.motor_b.stop(stop_action="coast")
        #mcd.ev3.Sound.speak('Cube is solved!').wait()

#import magiccube_solver as mcs
import magiccube_device as mcd
import sys

if __name__ == "__main__":
    #mcs.main()
    args = sys.argv
    mcd.main(args[1], args[2], args[3], args[4])

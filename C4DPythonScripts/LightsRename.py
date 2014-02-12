import c4d
from c4d import gui
#Welcome to the world of Python


def main():
    lightsNull = doc.SearchObject('Lights')
    print lightsNull.GetName()
    print "\n\n"
    lights = lightsNull.GetDown()
    # i = 1
    lightsStr = ""
    while lights:
        lights.SetName("Light_" + lights.GetName()) #str(i)
        # lightsStr += lights.GetName() + "\n"
        lights = lights.GetNext()
        # i=i+1
        
    c4d.CopyStringToClipboard(lightsStr)
    

if __name__=='__main__':
    main()

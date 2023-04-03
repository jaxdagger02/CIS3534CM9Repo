#!/usr/bin/env python3
#GPA8.py
#Jon Sutton
#Friday, March 31, 2023



# importing the json module
try:
    import json

except:
    print("error")

    
#router and switch file constants
routFile = "equip_r.txt"
switFile = "equip_s.txt"


# update and error file constants
updaFile = "updated.txt"
invaFile = "invalid.txt"


#prompt constants
UPDATE = "\nWhich device would you like to update "
QUIT = "(enter x to quit)? "
NEW_IP = "What is the new IP address (111.111.111.111) "
SORRY = "Sorry, that is not a valid IP address\n"


#function to get valid device
def getValidDevice(routers, switches):
    validDevice = False
    while not validDevice:
        #prompt for device to update
        device = input(UPDATE + QUIT).lower()
        if device in routers.keys():
            return device
        elif device in switches.keys():
            return device
        elif device == 'x':
            return device  
        else:
            print("That device is not in the network inventory.")


#function to get valid IP address
def getValidIP(invalidIPCount, invalidIPAddresses):
    validIP = False
    while not validIP:
        ipAddress = input(NEW_IP)
        octets = ipAddress.split('.')
        #print("octets", octets)
        for byte in octets:
            byte = int(byte)
            if byte < 0 or byte > 255:
                invalidIPCount += 1
                invalidIPAddresses.append(ipAddress)
                print(SORRY)
                break
        else:
            #validIP = True
                return ipAddress, invalidIPCount
                #don't need to return invalidIPAddresses list - it's an object



def main():

    #opens needed files
    open(routFile)
    open(switFile)

    try:
        open(updaFile, "w")
    except:
        open("updated.txt", "w")
    #opens or creates files if necessary    
    try:  
        open(invaFile, "w")
    except:
        open("invalid.txt", "w")


    
    #dictionaries
    routers = {}

    #opens file to read > marks data to variable > converts data into dictionary
    with open(routFile) as x:
        data = x.read()
    routers = json.loads(data)


    switches = {}
    
    #opens file to read > marks data to variable > converts data into dictionary
    with open(switFile) as x:
        data = x.read() 
    switches = json.loads(data)


    #the updated dictionary holds the device name and new ip address
    updated = {}
    
    #list of bad addresses entered by the user
    invalidIPAddresses = []

    #accumulator variables
    devicesUpdatedCount = 0
    invalidIPCount = 0

    #flags and sentinels
    quitNow = False
    validIP = False

    print("Network Equipment Inventory\n")
    print("\tequipment name\tIP address")
    for router, ipa in routers.items(): 
        print("\t" + router + "\t\t" + ipa)
    for switch, ipa in switches.items():
        print("\t" + switch + "\t\t" + ipa)

    while not quitNow:

        #function call to get valid device
        device = getValidDevice(routers, switches)
        
        if device == 'x':
            quitNow = True
            break
        
        #function call to get valid IP address
        #python lets you return two or more values at one time
        ipAddress, invalidIPCount = getValidIP(invalidIPCount, invalidIPAddresses)
  
        #update device
        if 'r' in device:
            #modify the value associated with the key
            routers[device] = ipAddress 
            #print("routers", routers)
            
        else:
            switches[device] = ipAddress

        devicesUpdatedCount += 1
        #add the device and ipAddress to the dictionary
        updated[device] = ipAddress

        print(device, "was updated; the new IP address is", ipAddress)
        #loop back to the beginning

    #user finished updating devices
    print("\nSummary:")
    print()
    print("Number of devices updated:", devicesUpdatedCount)

    ##---->>>> write the updated equipment dictionary to a file
    with open(updaFile, "w") as x:
        x.write(json.dumps(updated))
        
    
    print("Updated equipment written to file 'updated.txt'")
    print()
    print("\nNumber of invalid addresses attempted:", invalidIPCount)

    ##---->>>> write the list of invalid addresses to a file
    with open(invaFile, "w") as x:
        x.write(json.dumps(invalidIPAddresses))
    
    print("List of invalid addresses written to file 'errors.txt'")

#top-level scope check
if __name__ == "__main__":
    main()





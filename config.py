import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
i = 0
for port, desc, hwid in sorted(ports):
    print(str(i) + "  | " + "{}: {} [{}]".format(port, desc, hwid))
    i = i + 1

goodInput = False
while goodInput == False:
    try:
        com = int(
            input(
                "Enter the number corresponding to the port location of the encouragement device: "
            )
        )
        if com > i - 1:
            print("Not an available port.")
        else:
            goodInput = True
    except:
        print("Must be int.")
try:
    with open("config.txt", "w") as f:
        f.write(sorted(ports)[0][0])
    print("Encouragement device location set to " + sorted(ports)[0][0] + ".")
except:
    print("Error setting encouragement device at location " + sorted(ports)[0][0] + ".")
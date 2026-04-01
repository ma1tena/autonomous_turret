import serial
import time

class SerialComm:
    def __init__(self, port, baud=115200):
        self.ser = serial.Serial(port, baud, timeout=1)
        time.sleep(2)
        print(f"Connected to ESP32 on {port}")
        # Print ESP32 ready message
        response = self.ser.readline().decode().strip()
        if response:
            print(f"ESP32 says: {response}")

    def send_angles(self, pan, tilt):
        command = f"{pan},{tilt}\n"
        self.ser.write(command.encode())

        # Read and print ESP32 acknowledgement
        response = self.ser.readline().decode().strip()
        if response:
            print(f"ESP32 confirmed: {response}")

    def close(self):
        self.ser.close()


#**To test without running the full tracker**, you can also open Arduino IDE's **Serial Monitor** (`Tools → Serial Monitor`) set to `115200` baud and manually type commands like:

#90,45


#You should see the ESP32 echo back:

#Received → pan=90° tilt=45° 
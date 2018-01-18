import subprocess
import time

class bt:
    addr = "0x0026"
    def __init__(self):
        self.out_writeable = open("tmpout", "wb")
        self.out = open("tmpout", "r")
        
        self.proc = subprocess.Popen(["sudo","gatttool",
                                      "-b","D6:88:F3:AA:42:29",
                                      "-I","-t", "random",
                                      "--sec-level=high"],
                                     stdin = subprocess.PIPE,
                                     stdout = self.out_writeable,
                                     bufsize = 1,
                                     universal_newlines = True)

        print("Connecting...")
        self.proc.stdin.write("connect \n") # \n is important!
        self.wait_for_msg("Connection successful")
        print("Connected!")
            

        print("Enabling notifications or something...")
        self.write(0)
        self.wait_for_msg("Characteristic value was written successfully")
        print("Enabled.")

    # A little hacky but basically waits for msg to appear in the gatttools output
    def wait_for_msg(self, msg):
        r = None
        while r == None or msg not in r:
            time.sleep(0.01)
            r = self.out.readline()
        return

    def write(self, msg_byte):
        if msg_byte < 0 or msg_byte >= 256:
            print("[ERROR] Write data is out of range!: "+str(msg_byte))
            return
            
        data = hex(msg_byte)[2:] # To remove "0x"
        if len(data) == 1:
            data = "0" + data
        
        self.proc.stdin.write("char-write-req " + self.addr
                              + " 03" + data
                              + "\n")

    # Reads the next message from the arduino.
    # May take a while if there has been a lot of spam that isn't notifications.
    # The real issue is that it isn't the most recent, it's the oldest unread
    def read_next(self):
        line = self.out.readline()
        while line != "" and "Notification" not in line:
            line = self.out.readline()

        if line == "":
            return None

        data_idx = line.find("value:") + len("value:") + 1
        data_str = line[data_idx:-2]
        data_arr = data_str.split(" ")
        return list(map(lambda bs: int(bs, 16), data_arr))
    
    # Reads the latest message from the arduino and discards all others.
    # May take a while if we're far behind.
    def read_last(self):
        last_good = self.read_next()
        last = self.read_next()
        
        while last != None:
            last_good = last
            last = self.read_next()

        return last_good

    def close(self):
        print("Closing and disconnecting...")
        self.proc.stdin.write("disconnect \n")
        self.proc.stdin.write("quit \n")
        self.out.close()
        self.out_writeable.close()
        print("Bye bye!")


# example usage
#b = bt()

#b.write(0x3c) # 0011 1100
#time.sleep(5)
#b.write(0x8a) # 1000 1010
    
#input("Press Enter to quit")
#b.close()


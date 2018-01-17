import time
import subprocess

out_writeable = open("tmpout", "wb")
out = open("tmpout", "r")
p = subprocess.Popen(["sudo","gatttool","-b","D6:88:F3:AA:42:29",
                      "-I","-t", "random","--sec-level=high"],
                     stdin = subprocess.PIPE,
                     stdout = out_writeable,
                     bufsize = 1,
                     universal_newlines = True)

time.sleep(1)

print(out.read())

time.sleep(2)
p.stdin.write("connect \n") # \n is important!
print(out.read())

out.close()
out_writeable.close()
input()

import numpy as np
import wrapper

bt = wrapper.bt()

ls = 0
rs = 0

while(True):
    c = input()
    if c == "k":
        bt.close()
        break
    elif c == "w":
        ls += 1
        rs += 1
    elif c == "s":
        ls -= 1
        rs -= 1
    elif c == "a":
        ls -= 1
        rs += 1
    elif c == "s":
        ls += 1
        rs -= 1

    ls = np.clip(ls, -8, 7)
    rs = np.clip(rs, -8, 7)

    lstr = hex(int(np.binary_repr(ls, width=4), 2))[2]
    rstr = hex(int(np.binary_repr(rs, width=4), 2))[2]
    bt.write(int(lstr+rstr, 16))

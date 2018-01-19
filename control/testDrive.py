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
    elif c == "d":
        ls += 1
        rs -= 1

    # ls = np.clip(ls, -8, 7)
    # rs = np.clip(rs, -8, 7)

    lstr = int("0" + np.binary_repr(-ls, width=7), 2)
    rstr = int("1" + np.binary_repr(-rs, width=7), 2)
    print(-ls)
    print(-rs)
    bt.write(int(lstr))
    bt.write(int(rstr))

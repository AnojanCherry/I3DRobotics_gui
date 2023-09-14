import os

lst = (os.listdir())

ind = 0
for i in lst:
    print(i)
    if "left" in i:
        os.rename(i,i.replace(".png","_l.png"))
    if "right" in i:
        os.rename(i,i.replace(".png","_r.png"))
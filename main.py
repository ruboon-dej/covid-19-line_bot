from province import PROVINCES
for p in PROVINCES:
    if len(p) > 20 :
        print("{}...".format(p[0:17]))
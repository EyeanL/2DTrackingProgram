import numpy as np
test = np.rad2deg(np.arctan2(-0.1,1))
if(test < 0):
    print(test)
    test = 360 + test
print(test)

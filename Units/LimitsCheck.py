#!/usr/bin/python3

import numpy as np
from numpy import average as avg
import scipy as sp

def check_y_scale(*args, **kwargs):
        need_scale = False
        make_bigger = False
        y_array=args[0]
        length_of_y = len(y_array)
        np_y_array = np.array(y_array)
        max_y = np_y_array.max()
        minimum_limit_of_y = 0.985*max_y
        array_of_greater_y = np_y_array[np_y_array>=minimum_limit_of_y]
        average = avg(np_y_array)
        if len(array_of_greater_y) > 0.05*length_of_y:
                # print("out of limits and saturated")
                # print(array_of_greater_y)
                # print(max_y)
                need_scale = True
                make_bigger = True
        elif (max_y < 1.3*average):
                need_scale = True
                make_bigger = False
                pass
        else:
                need_scale = False
                make_bigger = False
                pass
        print("DEBUG LIMITS CHECK", need_scale, max_y, make_bigger, average)
        return need_scale, max_y, make_bigger
        pass
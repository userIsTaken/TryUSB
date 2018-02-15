#!/usr/bin/python3

import numpy as np
import scipy as sp

def check_y_scale(*args, **kwargs):
        need_scale = False
        y_array=args[0]
        length_of_y = len(y_array)
        np_y_array = np.array(y_array)
        max_y = np_y_array.max()
        minimum_limit_of_y = 0.985*max_y
        array_of_greater_y = np_y_array[np_y_array>=minimum_limit_of_y]
        if len(array_of_greater_y) > 0.05*length_of_y:
                print("out of limits and saturated")
                print(array_of_greater_y)
                print(max_y)
                need_scale = True
        else:
                print("False")
                print(max_y, "max y is masyvo")
        return need_scale, max_y
        pass
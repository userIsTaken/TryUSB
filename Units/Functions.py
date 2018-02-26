#!/usr/bin/python3
#-*- coding: utf-8 -*-

def getCurrentDensity(volts:float, resistance:float, area:float):
        '''
        
        :param volts: Volts
        :param resistance: Ohms
        :param area: centimeters
        :return: j : A/cm^2
        '''
        j = volts /(resistance * area)
        return j
        pass
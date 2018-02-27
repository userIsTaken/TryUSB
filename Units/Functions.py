#!/usr/bin/python3
#-*- coding: utf-8 -*-

def getCurrentDensity(volts, resistance, area):
        '''
        
        :param volts: Volts
        :param resistance: Ohms
        :param area: centimeters
        :return: j : A/cm^2
        '''
        j = volts /(resistance * area)
        return j
        pass

def getCurrentDensity(volts_array, R, S):
        current_density = []
        newList = [x / (R*S) for x in volts_array]
        return current_density
        pass
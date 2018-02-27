#!/usr/bin/python3
#-*- coding: utf-8 -*-

def getCurrentDensity(volts, resistance, area):
        '''
        
        :param volts: Volts
        :param resistance: Ohms
        :param area: centimeters
        :return: j : mA/cm^2
        '''
        j = volts /(resistance * area)
        return j
        pass

def getCurrentDensity(volts_array, R, S):
        '''
        
        :param volts_array: volts from channel
        :param R: load in kOhms
        :param S: load in squared cm's.
        :return: array/list of current density (mA/cm^2)
        '''
        # current_density = []
        current_density = [x / (R*S) for x in volts_array]
        return current_density
        pass
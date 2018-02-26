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

def get_file_name_parameters():
        pass
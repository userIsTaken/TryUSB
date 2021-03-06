import math
def getNumberSIprefix(value:float):
        '''
        Overloaded function with possibility to pass a float instead a string

        :param value:
        :return:
        '''
        flt = None
        unit = None
        log = math.floor(math.log10(value))
        # print("1st", log, " log", value, " value")
        if log < 0:
                # value of log shows that we need multiply(!) by ten log times to get integer value
                if log>=-3:
                        flt = value*1e3
                        unit = "m"
                if log<-3  and log>=-6:
                        flt = value * 1e6
                        unit = "μ"
                        pass
                if log<-6:
                        flt = value * 1e9
                        unit = "n"
                        pass
                pass
        elif log > 0:
                # value of log shows that we need divide(!) by ten log times to get integer value
                if log <3:
                        flt = value
                        unit = ""
                        pass
                if log >= 3 and log < 6:
                        flt = value / 1e3
                        unit = "k"
                        pass
                if log >= 6:
                        flt = value / 1e6
                        unit = "M"
                        pass
                pass
                pass
        else:
                flt = value
                unit = ""
                pass
        return flt, unit
        pass


def getNumberSIprefix(val: str):
        '''
        Overloaded variant with possibility to pass a string instead float;

        :param val:
        :return:
        '''
        value = float(val)
        flt = None
        unit = None
        log = math.floor(math.log10(value))
        # print("2nd", log, " log", value, " value")
        if log < 0:
                # value of log shows that we need multiply(!) by ten log times to get integer value
                if log>=-3:
                        flt = value*1e3
                        unit = "m"
                if log<-3  and log>=-6:
                        flt = value * 1e6
                        unit = "μ"
                        pass
                if log<-6:
                        flt = value * 1e9
                        unit = "n"
                        pass
                pass
        elif log > 0:
                # value of log shows that we need divide(!) by ten log times to get integer value
                if log <3:
                        flt = value
                        unit = ""
                        pass
                if log >= 3 and log < 6:
                        flt = value / 1e3
                        unit = "k"
                        pass
                if log >= 6:
                        flt = value / 1e6
                        unit = "M"
                        pass
                pass
                pass
        else:
                flt = value
                unit = ""
                pass
        return flt, unit
        pass


def getNumberFromSIprefix(value, unit):
        ret_val = value
        if "m" in unit:
                ret_val = value * 1e-3
        elif "u" in unit or "µ" in unit:
                ret_val = value*1e-6
        elif "n" in unit:
                ret_val = value * 1e-9
        elif "k" in unit or "K" in unit:
                ret_val = value * 1e3
        elif "M" in unit:
                ret_val = value * 1e6
        else:
                ret_val = value
        return ret_val
        pass
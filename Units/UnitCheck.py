import math
def getNumberSIprefix(value:float):
        flt = None
        unit = None
        log = math.floor(math.log10(value))
        if log < 0:
                # value of log shows that we need multiply(!) by ten log times to get integer value
                if log>-3:
                        flt = value
                        unit = ""
                if log<=-3  and log>-6:
                        flt = value * 1e3
                        unit = "m"
                        pass
                if log<=-6:
                        flt = value * 1e6
                        unit = "μ"
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


def getNumberSIprefix(value: str):
        pass
import math
def getNumberSIprefix(value:float):
        flt = None
        unit = None
        log = math.floor(math.log10(value))
        if log < 0:
                # value of log shows that we need multiply(!) by ten log times to get integer value
                if log>-3:
                        pass
                if log<=-3  and log>-6:
                        pass
                if log<=-6:
                        pass
                pass
        elif log > 0:
                # value of log shows that we need divide(!) by ten log times to get integer value
                if log <3:
                        pass
                if log >= 3 and log < 6:
                        pass
                if log >= 6:
                        pass
                pass
                pass
        else:
                pass
        pass


def getNumberSIprefix(value: str):
        pass
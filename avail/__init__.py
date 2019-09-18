import math


def mttf_sw(a_sw, mttr_sw):
    return a_sw * mttr_sw / (1 - a_sw)


def availability_class(availability):
    return math.floor(-math.log10(1 - availability))


def availability(availabilityClass):
    return 1 - (pow(10, -availabilityClass))


def rf_to_avail(rf_ratio):
    if rf_ratio > 0:
        return availability_class(1/(1 + rf_ratio))
    else:
        return 'does not exist'

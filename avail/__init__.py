import math


def mttf_sw(a_sw, mttr_sw):
    return a_sw * mttr_sw / (1 - a_sw)


def availability_class(availability):
    return math.floor(-math.log10(1 - availability))


def availability(availabilityClass):
    return 1 - (pow(10, -availabilityClass))

import math


def mttf_sw(a_sw, mttr_sw):
    return a_sw * mttr_sw / (1 - a_sw)


def availability_class(availability):
    return math.floor(-math.log10(1 - availability))


def availability_class_cts(availability):
    return -math.log10(1 - availability)


def availability(availabilityClass):
    return 1 - (pow(10, -availabilityClass))


def rf_to_avail(rf_ratio):
    if rf_ratio > 0:
        return 1/(1 + rf_ratio)
    else:
        return 'does not exist'


def rf_to_avail_class(rf_ratio):
    if rf_ratio > 0:
        return availability_class(1/(1 + rf_ratio))
    else:
        return 'does not exist'


def avail_to_rf(avail):
    if 0 < avail < 1:
        return (1/avail) - 1
    else:
        return 'does not exist'


def rf_to_avail_class_cts(rf_ratio):
    if rf_ratio > 0:
        return availability_class_cts(1 / (1 + rf_ratio))
    else:
        return 'does not exist'


def overall_availability(nodes, a_class_hw, a_class_sw, failure_func):

    # getting the availability of the hardware for the availability class for hardware
    avail_monolith_hw = availability(a_class_hw)
    # getting the availability of the software for the availability class for software
    avail_monolith_sw = availability(a_class_sw)

    # getting the r_sw/f_sw ratio
    r_f_ratio_sw = avail_to_rf(avail_monolith_sw)
    # r/f ratio of a single node in a micro service for n nodes
    new_r_f_ratio_sw = r_f_ratio_sw / failure_func(nodes)
    # availability conversion
    avail_micro_sw_single_node = rf_to_avail(new_r_f_ratio_sw)

    # since the node failures are independent for both hw and sw

    avail_micro_hw_n_nodes = pow(avail_monolith_hw, nodes)
    avail_micro_sw_n_nodes = pow(avail_micro_sw_single_node, nodes)

    # since the hw and sw failures are independent we take the product for overall availability

    overall_avail = avail_micro_hw_n_nodes * avail_micro_sw_n_nodes

    return overall_avail


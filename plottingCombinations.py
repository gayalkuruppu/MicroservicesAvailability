import math
import pandas as pd
import itertools
import matplotlib.pyplot as plt
import avail

'''

*This code is used to generate(plot) availability data for different combinations of following VARIABLES,

1. number of nodes(=micro services) we break the monolith into
2. Hardware availability class
3. Software availability class
4. Mean time to recover fo software(only software because we do not change the MTTF or MTTR for hardware)
5. Factor which MTTF changes when we divide the system in to micro-services as a function of nodes
6. Factor which MTTR changes when we divide the system in to micro-services as a function of nodes. (basically the 
    reciprocals of the functions which were used in 5.)

*max_plot is used to calculate and plot upper bound for availability values we just calculated now.

PS - max_plot is executed in line 174

'''

def mttf_sw(a_sw, mttr_sw):
    return a_sw * mttr_sw / (1 - a_sw)


def availability_class(availability):
    return math.floor(-math.log10(1 - availability))


def availability(availabilityClass):
    return 1 - (pow(10, -availabilityClass))


# functions for mean time to failure

def f1_n(x):
    return x


def f1_nlogn(x):
    return x * math.log10(x)


def f1_sqrt_n(x):
    return math.sqrt(x)


def f1_sqrt_n_cube(x):
    return pow(x, 1.5)


def f1_n_pow_2over3(x):
    return pow(x, 2 / 3)


def f1_identity(x):
    return 1

# functions to mean time to recover


def f2_1_over_n(x):
    return 1 / x


def f2_1_over_nlogn(x):
    return 1 / (x * math.log10(x))


def f2_1_over_sqrt_n(x):
    return 1 / math.sqrt(x)


def f2_1_over_sqrt_n_cube(x):
    return pow(x, -1.5)


def f2_1_over_n_pow_2over3(x):
    return pow(x, -2 / 3)


# lists of column tags and their content
nodes_count = [2, 4, 8, 16, 24, 32, 64, 128]
availabilityClassHW = [3, 4, 5]
availabilityClassSW = [3, 4, 5]
mttrSW = [3600, 1800, 300, 60, 30]
function1 = [f1_identity, f1_n, f1_nlogn, f1_sqrt_n, f1_sqrt_n_cube, f1_n_pow_2over3]
function2 = [f2_1_over_n, f2_1_over_nlogn, f2_1_over_sqrt_n, f2_1_over_sqrt_n_cube, f2_1_over_n_pow_2over3]

data = []

for i in itertools.product(nodes_count, availabilityClassHW, availabilityClassSW, mttrSW, function1, function2):

    scenario = list(i)

    nodes_count = scenario[0]
    availability_class_hw = scenario[1]
    availability_class_sw = scenario[2]
    mttr_sw = scenario[3]
    f1 = scenario[4]
    f2 = scenario[5]

    # getting the availability of the hardware for the availability class for hardware
    availMonolithHW = availability(availability_class_hw)
    # getting the availability of the software for the availability class for software
    availMonolithSW = availability(availability_class_sw)

    # calculate the availability of the regarding scenario

    recover_mono_sw = mttr_sw  # Mean Time To Recover for monolith software
    failure_mono_sw = mttf_sw(availMonolithSW, recover_mono_sw)  # Mean Time To Recover for monolith hardware

    failure_micro_sw = failure_mono_sw * f1(nodes_count)  # Mean Time To Recover for micro service hardware
    recover_micro_sw = recover_mono_sw * f2(nodes_count)  # Mean Time To Recover for micro service software

    availMicroSW_single_node = failure_micro_sw / (failure_micro_sw+recover_micro_sw)

    # since the node failures are independent for both hw and sw

    availMicroHW_N_nodes = pow(availMonolithHW, nodes_count)
    availMicroSW_N_nodes = pow(availMicroSW_single_node, nodes_count)

    # since the hw and sw failures are independent we take the product for overall availability

    overallAvailability = availMicroHW_N_nodes * availMicroSW_N_nodes

    overallAvailabilityClass = avail.availability_class_cts(overallAvailability)
    data.append([nodes_count, availability_class_hw, availability_class_sw, mttr_sw, f1.__name__,
                 f2.__name__, overallAvailabilityClass])

# data here should be the list containing all the data

df = pd.DataFrame(data, columns=['nodes count', 'HW Availability', 'SW Availability', 'MTTR SW', 'function 1',
                                 'function 2', 'Overall availability'])

df.to_csv('Data/AvailabilityS.csv')


def max_plot():
    '''
    this function
    '''
    nodes = [2, 4, 8, 16, 24, 32, 64, 128]
    for i in function1:
        # filtering the data by a selected function1
        isfunction1_identity = df['function 1'] == i.__name__
        filtered_data = df[isfunction1_identity]
        plt.figure(figsize=(20, 10))  # creating a figure for the specific function1
        plt.suptitle('Maximum availability class(fixing {}) for HW classes {} and SW classes {}'.
                     format(i.__name__, availabilityClassHW, availabilityClassSW), fontsize=16)
        subplot_iteration = 0
        for j in function2:
            subplot_iteration += 1
            # filtering the data by a selected function2
            isfunction2_j = filtered_data['function 2'] == j.__name__
            function2_filtered = filtered_data[isfunction2_j]
            plt.subplot(2, 3, subplot_iteration)  # plotting a subplots for chosen function2
            plt.title(i.__name__ + ' and ' + j.__name__)
            plt.xlabel('Nodes count')
            plt.ylabel('maximum overall availability class')
            for k in nodes:
                # filtering the data by specific number of nodes count
                isNodes_count = function2_filtered['nodes count'] == k
                nodes_count_filtered = function2_filtered[isNodes_count]
                # finding the maximum overall availability class from the filtered data.
                # filtered by specific f1,f2, and node_count
                maxAvailabilityClass = nodes_count_filtered['Overall availability'].max()
                plt.plot(k, maxAvailabilityClass, 'bo')
        plt.savefig('Graphs/maxPlots/'+i.__name__)


max_plot()

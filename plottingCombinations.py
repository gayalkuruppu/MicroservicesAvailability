import math
import pandas as pd
import itertools
import matplotlib.pyplot as plt

def mttf_sw(a_sw, mttr_sw):
    return (a_sw * mttr_sw / (1 - a_sw))


def availabilityClass(availability):
    return (math.floor(-math.log10(1 - availability)))


def availability(availabilityClass):
    return (1 - (pow(10, -availabilityClass)))


# functions for mean time to failure

def f1_n(x):
    return (x)


def f1_nlogn(x):
    return (x * math.log10(x))


def f1_sqrt_n(x):
    return (math.sqrt(x))


def f1_sqrt_n_cube(x):
    return (pow(x, 1.5))


def f1_n_pow_2over3(x):
    return (pow(x, 2 / 3))


def f1_identity(x):
    return(1)

# functions to mean time to recover

def f2_1_over_n(x):
    return (1 / x)


def f2_1_over_nlogn(x):
    return (1 / (x * math.log10(x)))


def f2_1_over_sqrt_n(x):
    return (1 / math.sqrt(x))


def f2_1_over_sqrt_n_cube(x):
    return (pow(x, -1.5))


def f2_1_over_n_pow_2over3(x):
    return (pow(x, -2 / 3))


# lists of column tags and their content
nodes_count = [2, 4, 8, 16, 24, 32, 64, 128]
availabilityClassHW = [3, 4, 5]
availabilityClassSW = [3, 4, 5]
mttrSW = [3600, 1800, 300, 60, 30]
function1 = [f1_identity, f1_n, f1_nlogn, f1_sqrt_n, f1_sqrt_n_cube, f1_n_pow_2over3]
function2 = [f2_1_over_n, f2_1_over_nlogn, f2_1_over_sqrt_n, f2_1_over_sqrt_n_cube, f2_1_over_n_pow_2over3]

data = []

for i in itertools.product(nodes_count, availabilityClassHW, availabilityClassSW, mttrSW, function1, function2):
    '''
    nodes_count = temp[0]
    avialability_hw = temp[1]
    avialability_sw = temp[2]
    mttr_sw = temp[3]
    f1 = temp[4]
    f2 = temp[5]
    availability
    '''

    scenario = list(i)
    # getting the availability of the hardware for the availability class for hardware
    availability_hw = availability(scenario[1])
    # getting the availability of the software for the availability class for software
    availability_sw = availability(scenario[2])
    # calculate the availability of the regarding scenario
    overallAvailability = pow((availability_hw * mttf_sw(availability_sw, scenario[3]) * scenario[4](scenario[0]) /
                               (mttf_sw(availability_sw, scenario[3]) * scenario[4](scenario[0]) + scenario[3] *
                                scenario[5](scenario[0]))), scenario[0])
    overallAvailabilityClass = availabilityClass(overallAvailability)
    scenario.append(overallAvailabilityClass)
    data.append([scenario[0], scenario[1], scenario[2], scenario[3], scenario[4].__name__,
                 scenario[5].__name__, overallAvailabilityClass])

# data here should be the list containing all the data

df = pd.DataFrame(data, columns=['nodes count', 'HW Availability', 'SW Availability', 'MTTR SW', 'function 1',
                                 'function 2', 'Overall availability'])

df.to_csv('AvailabilityS.csv')


for i in function1:
    # filtering the data by a selected function1
    isfunction1_identity = df['function 1'] == i.__name__
    filtered_data = df[isfunction1_identity]
    # filtered_data.to_csv('csv/'+i.__name__+'_availability.csv')
    plt.figure(figsize=(20, 10))
    plt.suptitle('Maximum availability class(fixing {}) for HW classes {} and SW classes {}'.format(i.__name__, availabilityClassHW, availabilityClassSW), fontsize=16)
    subplot_iteration = 0
    for j in function2:
        subplot_iteration += 1
        # filtering the data by a selected function2
        isfunction2_j = filtered_data['function 2'] == j.__name__
        function2_filtered = filtered_data[isfunction2_j]
        plt.subplot(2, 3, subplot_iteration)
        plt.title(i.__name__ + ' and ' + j.__name__)
        plt.xlabel('Nodes count')
        plt.ylabel('maximum overall availability class')
        for k in nodes_count:
            # filtering the data by specific number of nodes count
            isNodes_count = function2_filtered['nodes count'] == k
            nodes_count_filtered = function2_filtered[isNodes_count]
            # finding the maximum overall availability class from the filtered data.
            # filtered by specific f1,f2, and node_count
            maxAvailabilityClass = nodes_count_filtered['Overall availability'].max()
            print(k, maxAvailabilityClass)
            plt.plot(k, maxAvailabilityClass, 'bo')
    plt.savefig('maxPlots/'+i.__name__)
# plt.tight_layout()
plt.show()
import avail
from avail import availability
from avail import rf_to_avail
import pandas as pd
import math

'''
After we reduce the availability expression we got the variables count low
(making some ratios instead of several variables).

Then calculated the r/f ratio(and relevant sw availability class) needed to achieve certain 
overall availabilities(micro-service based system's total availability).

Some overall availabilities were not achievable due to the limitations of other variables. 
For those cases we get negative r/f ratios. I filtered out those negative values and create a separate csv.

some of the functions are commented out. We are now considering f1/f2 ratio instead of having them separately.
 When anaylzing the function ratios there were some functions which shows almost similar behaviours.

'''


def identity(x):
    return 1


def n(x):
    return x


def square_root_n(x):
    return math.sqrt(x)


def n_squared(x):
    return pow(x, 2)


# def n_cube(x):
#     return pow(x, 3)


def n_log_n(x):
    return x*math.log10(x)


# def n_squared_log_n_squared(x):
#     return pow(x*math.log10(x), 2)


data = []
overall_availability_class = [4, 5, 6]
nodes_count = list(range(2, 128))
availability_class_hw = [4, 5, 6]
f1_over_f2 = [identity, n, square_root_n, n_squared, n_log_n]

for o in overall_availability_class:
    for n in nodes_count:
        for a in availability_class_hw:
            for f in f1_over_f2:
                overall_availability = availability(o)
                r_f_ratio = f(n)*(availability(a)/pow(overall_availability, 1/n)-1)
                data.append([o, n, a, f.__name__, r_f_ratio, avail.rf_to_avail_class_cts(r_f_ratio)])

df = pd.DataFrame(data, columns=['overall availability class', 'nodes count', 'availability class HW', 'f1(n) / f2(n)',
                                 'minimum recover/failure time ratio', 'minimum availability class SW required cts'])

isMinPositive = df['minimum recover/failure time ratio'] >= 0
positiveRatioFiltered = df[isMinPositive]

df.to_csv('Data/csv/allCombinations.csv')
positiveRatioFiltered.to_csv('Data/csv/positiveRatioFiltered.csv')
print(positiveRatioFiltered)

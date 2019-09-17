from avail import availability
import pandas as pd
import math


def n(x):
    return x


def square_root_n(x):
    return math.sqrt(x)


def n_squared(x):
    return pow(x, 2)


def n_cube(x):
    return pow(x, 3)


def n_log_n(x):
    return x*math.log10(x)


def n_squared_log_n_squared(x):
    return pow(x*math.log10(x), 2)


data = []
overall_availability_class = [4, 5, 6]
nodes_count = [2, 4, 8, 16, 32, 64, 128]
availability_class_hw = [4, 5]
f1_over_f2 = [n, square_root_n, n_squared, n_cube, n_log_n, n_squared_log_n_squared]

for o in overall_availability_class:
    for n in nodes_count:
        for a in availability_class_hw:
            for f in f1_over_f2:
                overall_availability = availability(o)
                r_f_ratio = f(n)*(availability(a)/pow(overall_availability, 1/n)-1)
                data.append([o, n, a, f.__name__, r_f_ratio])

df = pd.DataFrame(data, columns=['overall availability class', 'nodes count', 'f1(n) / f2(n)', 'availability class HW',
                                 'recover/failure time ratio'])

isMinPositive = df['recover/failure time ratio'] >= 0
positiveRatioFiltered = df[isMinPositive]

df.to_csv('csv/allCombinations.csv')
positiveRatioFiltered.to_csv('csv/positiveRatioFiltered.csv')
print(positiveRatioFiltered)
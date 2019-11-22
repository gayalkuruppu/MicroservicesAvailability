import math


def identity(x):
    return 1


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


def function_filter(df, func):
    is_function = df['f1(n) / f2(n)'] == func
    return df[is_function]

import pandas as pd
import matplotlib.pyplot as plt


def function_filter(df, func):
    is_function = df['f1(n) / f2(n)'] == func
    return df[is_function]


data = pd.read_csv('csv/positiveRatioFiltered.csv')

#  filtering overall classes 4 and 5 from the positive ratio filtered csv file

isOverallClass4 = data['overall availability class'] == 4
overallClass4_filtered = data[isOverallClass4]

isOverallClass5 = data['overall availability class'] == 5
overallClass5_filtered = data[isOverallClass5]

# filtering HW classes 5 and 6 for overall availability class 4

isHW_5 = overallClass4_filtered['availability class HW'] == 5
overall_4_and_HW_5_filtered = overallClass4_filtered[isHW_5]

isHW_6 = overallClass4_filtered['availability class HW'] == 6
overall_4_and_HW_6_filtered = overallClass4_filtered[isHW_6]

# filtering HW class 6 for overall availability class 5

isHW_6 = overallClass5_filtered['availability class HW'] == 6
overall_5_and_HW_6_filtered = overallClass5_filtered[isHW_6]


f1_over_f2 = ['n', 'square_root_n', 'n_squared', 'n_cube', 'n_log_n', 'n_squared_log_n_squared']
plots = [overall_4_and_HW_5_filtered, overall_4_and_HW_6_filtered, overall_5_and_HW_6_filtered]
plots_ylabel = ['overall class of 4 with HW 5', 'overall class of 4 with HW 6', 'overall class of 5 with HW 6']
plt.figure(figsize=(20, 10))

for p in range(len(plots)):
    plt.subplot(2, 2, p+1)
    plt.title(plots_ylabel[p])
    plt.xlabel('Concurrency')
    plt.ylabel('minimum SW class required')
    for f in f1_over_f2:
        filteredData_by_function = function_filter(plots[p], f)
        print(filteredData_by_function)
        plt.plot(filteredData_by_function['nodes count'],
                 filteredData_by_function['minimum availability class SW required'], label=f)
    plt.legend()
plt.show()

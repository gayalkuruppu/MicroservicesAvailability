import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 16})


def function_filter(df, func):
    is_function = df['f1(n) / f2(n)'] == func
    return df[is_function]


data = pd.read_csv('csv/positiveRatioFiltered.csv')

#  filtering overall classes 4 and 5 from the positive ratio filtered csv file

overallClass4_filtered = data[data['overall availability class'] == 4]
overallClass5_filtered = data[data['overall availability class'] == 5]

# filtering HW classes 5 and 6 for overall availability class 4

overall_4_and_HW_5_filtered = overallClass4_filtered[overallClass4_filtered['availability class HW'] == 5]
overall_4_and_HW_6_filtered = overallClass4_filtered[overallClass4_filtered['availability class HW'] == 5]

# filtering HW class 6 for overall availability class 5

overall_5_and_HW_6_filtered = overallClass5_filtered[overallClass5_filtered['availability class HW'] == 6]


f1_over_f2 = ['identity', 'n', 'square_root_n', 'n_squared', 'n_log_n']
plots = [overall_4_and_HW_5_filtered, overall_4_and_HW_6_filtered, overall_5_and_HW_6_filtered]
plots_ylabel = ['4 with HW availability class 5', '4 with HW availability class 6', '5 with HW availability class 6']
# plt.figure(figsize=(20, 10))

availability_class_hw = [0.9999, 0.99999, 0.999999]

for p in range(len(plots)):
    plt.figure(figsize=(20, 10))
    # plt.subplot(2, 2, p+1)
    plt.title('Target MSA System availability '+plots_ylabel[p])
    plt.xlabel('Number of nodes')
    plt.ylabel('Minimum SW availability class required')
    # for f in f1_over_f2[0]:
    f = 'identity'
    print(f)
    filteredData_by_function = function_filter(plots[p], f)
    plt.plot(filteredData_by_function['nodes count'],
             filteredData_by_function['minimum availability class SW required cts'], label=f,linestyle='dashed')
    for f in f1_over_f2[1:5]:
        filteredData_by_function = function_filter(plots[p], f)
        plt.plot(filteredData_by_function['nodes count'],
                 filteredData_by_function['minimum availability class SW required cts'], label=f)
    # plt.plot(filteredData_by_function['nodes count'], pow(availability_class_hw[p], filteredData_by_function['nodes count']), label='software availability = 1', linestyle=':')
    plt.legend()
    plt.savefig('Target SW avail class vs nodes for diff functions/'+plots_ylabel[p])

import pandas as pd
import matplotlib.pyplot as plt
import avail
import func

data = []

nodes_count = list(range(2, 128))
availabilityClassHW = [4, 5, 6]
availabilityClassSW = [4, 5, 6]
functions = [func.identity, func.n, func.square_root_n, func.n_squared, func.n_log_n]

for n in nodes_count:
    for h in availabilityClassHW:
        for s in availabilityClassSW:
            for f in functions:
                hardware_avail = avail.availability_class_cts(pow(avail.availability(h), n))
                overall_avail = avail.overall_availability(n, h, s, f)
                avail_class_cts = avail.availability_class_cts(overall_avail)
                data.append([n, h, hardware_avail, s, f.__name__, avail_class_cts])
                # print([n, h, s, f.__name__, avail_class_cts])

df = pd.DataFrame(data, columns=['nodes count', 'HW Availability class', 'HW Availability', 'SW Availability class',
                                 'failure function', 'Overall availability'])

for i in availabilityClassHW:
    hw = df[df['HW Availability class'] == i]
    for j in availabilityClassSW:
        hw_sw = hw[hw['SW Availability class'] == j]
        plt.figure(figsize=(20, 10))
        plt.title('Hardware Availability class '+str(i)+' and Software Availability class '+str(j))
        plt.xlabel('Number of nodes')
        plt.ylabel('Overall Availability class')
        # for f in functions:
        #     f_name = f.__name__
        #     hw_sw_f = hw_sw[hw_sw['failure function'] == f_name]
        #     # print(hw_f)
        #     # break
        #     plt.plot(hw_sw_f['nodes count'], hw_sw_f['Overall availability'], label=f_name)
        plt.plot(hw_sw['nodes count'], hw_sw['HW Availability'], label='HW upper bound', linestyle='dashed')
        plt.legend()
        plt.savefig('hw_upperBoundOnly/'+'hw_'+str(i)+'_and_sw_'+str(j))

# df.to_csv('csv/hwUpperBoundData.csv')

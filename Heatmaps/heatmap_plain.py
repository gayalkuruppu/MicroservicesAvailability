import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('Availability in N-Micro Service System - Heatmap using availability classes Factor N.csv')
data1 = data.iloc[7:22, :]
data2 = data1.drop([8, 9, 10, 11])
data3 = data2.iloc[1:9, 1:7]

a = data3.to_numpy()
a[0, 0] = 0
a = a.astype('float64')
print(a)
plt.imshow(a, cmap='viridis', interpolation='nearest')
plt.show()


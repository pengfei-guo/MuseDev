import numpy as np
from matplotlib import pyplot as plt

with open('output.txt') as file:
    result_list = []
    for line in file:
        line = line.strip()
        result_list.append(float(line))


MAX = max(result_list)
MIN = min(result_list)
AVERAGE = sum(result_list) / len(result_list)

# fig = plt.figure()
plt.subplot(211)
plt.plot(result_list)
plt.title('Brainwave')

plt.subplot(212)
objects = ('MIN', 'AVERAGE','MAX')
y_pos = np.arange(len(objects))
performance = [MIN, AVERAGE, MAX]
plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Concentration Level')
plt.title('Data Report')

plt.show()

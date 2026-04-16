import matplotlib.pyplot as plt

data_index = []
with open("/Users/vladislav/прога/плюсы/лабы№3_4_5/results_with_index.txt") as in_f:
    for line in in_f:
        data_index.append([float(x) for x in line.split()])
in_f.close()
print(data_index)
plt.plot(data_index)
plt.show()

data_no_index = []
with open("/Users/vladislav/прога/плюсы/лабы№3_4_5/results_with_no_index.txt") as in_f:
    for line in in_f:
        data_no_index.append([float(x) for x in line.split()])
in_f.close()
print(data_no_index)
plt.plot(data_no_index)
plt.show()
 


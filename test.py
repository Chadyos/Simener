import matplotlib.pyplot as plt
import numpy as np

from classes.battery import Battery
from classes.node import Node

x = np.linspace(1, 20, 1000)
y = np.linspace(1, 5, 1000)
gen = abs(1 * np.sin(x))  # Solar panel gen
cons = abs(np.cos(y))
batt = Battery(capacity=20)
batt2 = Battery(capacity=20)
batt_list = [batt, batt2]
node_test = Node(consumption_profile=cons, generation_profile=gen, batteries=batt_list)
node_test.update()

for element in node_test.save:
    if element == 'balance_profile':
        color = 'grey'

    if element == 'generation_profile':
        color = 'green'

    if element == 'consumption_profile':
        color = 'red'
    if element == 'Grid_total':
        color = 'blue'
    if element != 'state_of_charge':
        plt.subplot(2, 1, 1)
        print('Element : ', element)
        plt.fill_between(
            np.linspace(0, 1000, 1000), node_test.save[element], alpha=0.4, color=color
        )
        print('Size : ', len(node_test.save[element]))
        plt.plot(node_test.save[element], label=element, color=color)

    if element == 'state_of_charge':
        plt.subplot(2, 1, 2)
        plt.plot(node_test.save[element], label=element)
        plt.legend()


plt.legend()
plt.show()

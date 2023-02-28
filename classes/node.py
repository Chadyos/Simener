"""This file defines the corresponding class."""


class Node:
    """
    A node is a point in the network, it generate and consume energy depending on time.
    It can be connected to batteries to store energy.


    It is composed of :
    - a generation profile described as a list
    - a consumption profile described as a list
    - a list of batteries
    - a list of ongoing exchanges
    """

    def __init__(self, generation_profile, consumption_profile, batteries=None):
        """Initialize the node."""
        self.batteries = batteries
        self.consumption_profile = consumption_profile
        self.generation_profile = generation_profile
        self.balance_profile = [
            generation_profile[i] - consumption_profile[i] for i in range(len(generation_profile))
        ]
        self.iteration = 0
        self.max_iteration = len(generation_profile)
        self.save = {
            'balance_profile': self.balance_profile,
            'generation_profile': self.generation_profile,
            'consumption_profile': self.consumption_profile,
            'state_of_charge': [],
            'Grid_total': [],
        }

    def update(self):
        """Update the current Node."""
        while self.iteration < self.max_iteration:
            print('\n')
            print('#' * 40)
            print('Iteration : ', self.iteration)
            self.save['Grid_total'].append(0)
            i = self.iteration
            balance = self.balance_profile[i]
            energy = abs(balance)
            print('Balance : ', balance)
            if balance > 0:
                # If we generate more energy than we consume, we send the rest to batteries.
                energy = self.send_to_batteries(energy)
                if energy != 0:
                    # We can't store all energy in batteries
                    # Then we send what's missing in grid.
                    energy = self.send_to_grid(energy)
            elif balance < 0:
                # If we don't have enough energy.
                # We take what we can from batteries.

                energy = self.take_from_batteries(energy)
                if energy != 0:
                    # If it's not enough, we take it from grid.
                    energy = self.take_from_grid(energy)
            if energy != 0:
                print('Error, energy not null at the end of iteration : ', energy)
            self.iteration += 1
            for battery in self.batteries:
                print(battery)
            # Save the current state of the node.
            sum_capacities = sum([battery.capacity for battery in self.batteries])
            socs = [battery.soc / sum_capacities * 100 for battery in self.batteries]
            self.save['state_of_charge'].append(sum(socs))
        print('End of simulation.')

    def send_to_batteries(self, energy):
        """
        Send energy to batteries.
        """
        # We first do transfers.
        for battery in self.batteries:
            energy = battery.charge(energy)
            if energy == 0:
                break
        return energy

    def take_from_batteries(self, energy):
        """
        Take energy from batteries.
        """
        # We first set transfers.
        for battery in self.batteries:
            energy = battery.discharge(energy)
            if energy == 0:
                break
        return energy

    def send_to_grid(self, energy):
        """
        We throw the rest to the grid.
        FOR NOW WE SET IT TO 0 AUTO.
        """
        print('Energy sent to grid : ', energy)
        self.save['Grid_total'][-1] -= energy
        return 0

    def take_from_grid(self, energy):
        """
        We take the rest from the grid.
        FOR NOW WE SET IT TO 0 AUTO.
        """
        print('Energy taken from grid : ', energy)
        self.save['Grid_total'][-1] += energy
        return 0

    def update_batteries(self):
        """Update every battery."""
        for battery in self.batteries:
            battery.update()

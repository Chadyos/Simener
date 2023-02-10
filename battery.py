"""The battery file defines the corresponding class."""


class Battery:
    """Class ruling every battery."""

    def __init__(self, capacity=0, max_capacity=10, max_charge_rate=1):
        """Initialize the battery."""
        self.capacity = capacity
        self.charge_rate = 0
        self.max_capacity = max_capacity
        self.max_charge_rate = max_charge_rate
        self.flags = {'max_speed': False, 'full': False, 'empty': False}

    def modify_charge_rate(self, amount):
        """Modify the charge rate of the battery."""
        save = self.charge_rate
        self.charge_rate += amount
        # The charge rate can't be higher than the max charge rate.
        if self.charge_rate > self.max_charge_rate:
            self.charge_rate = self.max_charge_rate
            self.flags['max_speed'] = True
        if self.charge_rate < -self.max_charge_rate:
            self.charge_rate = -self.max_charge_rate
            self.flags['max_speed'] = True
        # Return the difference between the new charge rate and the old one
        # If the charge rate is modified then the difference is 0.
        return self.charge_rate - save

    def reset_charge_rate(self):
        """Reset the charge rate of the battery."""
        self.charge_rate = 0
        self.flags['max_speed'] = False

    def init_charge_rate(self, amount):
        """Initialize the charge rate of the battery."""
        if amount > self.max_charge_rate:
            amount = self.max_charge_rate
            print('Exception : Charge rate too high, set to max charge rate.')
            self.flags['max_speed'] = True
        if amount < -self.max_charge_rate:
            amount = -self.max_charge_rate
            self.flags['max_speed'] = True
            print('Exception : Charge rate too low, set to max charge rate.')
        else:
            self.flags['max_speed'] = False
            self.charge_rate = amount

    def update(self):
        """Update the battery's capacity."""
        if self.charge_rate != 0:
            self.capacity += self.charge_rate
            if self.capacity != self.max_capacity:
                self.flags['full'] = False
            if self.capacity != 0:
                self.flags['empty'] = False

            # If the battery is full, it can't charge anymore.
            if self.capacity >= self.max_capacity:
                self.capacity = self.max_capacity
                self.flags['full'] = True
                self.reset_charge_rate()
                print('Exception : Battery full, charge rate reset.')
            # If the battery is empty, it can't discharge anymore.
            if self.capacity <= 0:
                self.reset_charge_rate()
                self.capacity = 0
                self.flags['empty'] = True
                print('Exception : Battery empty, charge rate reset.')

    def __str__(self):
        """Return a string containing the battery's parameters."""
        return (
            'Battery : Capacity = '
            + str(self.capacity)
            + ' Charge rate = '
            + str(self.charge_rate)
            + ' max_speed = '
            + str(self.flags['max_speed'])
            + ' full = '
            + str(self.flags['full'])
            + ' empty = '
            + str(self.flags['empty'])
        )

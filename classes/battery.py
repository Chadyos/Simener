"""The battery file defines the corresponding class."""


class Battery:
    """Class ruling every battery."""

    def __init__(self, soc=0, capacity=10, max_charge_rate=1):
        """Initialize the battery."""
        self.soc = soc
        self.capacity = capacity
        self.max_charge_rate = max_charge_rate

    def charge(self, amount):
        """Charge the battery with a given amount of energy."""
        if self.soc == self.capacity:
            return amount
        amount_init = amount
        if amount > self.max_charge_rate:
            amount = self.max_charge_rate
            print('Exception : Charge rate too high, set to max charge rate.')

        if self.soc + amount <= self.capacity:
            self.soc += amount
        else:
            amount = self.capacity - self.soc

            self.soc = self.capacity

        return abs(
            amount - amount_init
        )  # Return 0 if transfer is ok, else it's the remaining amount to transfer

    def discharge(self, amount):
        """Discharge the battery with a given amount of energy."""
        if self.soc == 0:
            return amount
        amount = abs(amount)
        amount_init = amount
        if amount > self.max_charge_rate:
            amount = self.max_charge_rate
            print('Exception : Charge rate too high, set to max charge rate.')

        if self.soc - amount < 0:
            self.soc = 0
            return abs(self.soc - amount_init)

        else:
            self.soc -= amount

        return abs(
            amount - amount_init
        )  # Return 0 if transfer is ok, else it's the remaining amount to transfer

    def __str__(self):
        """Return a string containing the battery's parameters."""
        return 'Battery : soc = ' + str(self.soc)

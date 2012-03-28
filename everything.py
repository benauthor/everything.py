class UnitsError(Exception):
    pass

class Simulator:
    """Stepwise stock/flow simulator.

    Set step_time to number of seconds per step."""
    def __init__(self, objects, step_time=1, steps=10):
        self.objects = objects
        self.step_time = step_time
        self.steps = steps

    def reconcile_time_units(self):
        for o in self.objects:
            try:
                if o.time_step in ["Second", "second", "Seconds", "seconds"]:
                    print "Units OK"
                else:
                    raise UnitsError("Your time units don't match.")
            except AttributeError:
                pass


    def print_objects(self):
        for o in self.objects:
            print o

    def run(self):
        self.reconcile_time_units()
        print "Beginning quantities:"
        self.print_objects()
        for step in xrange(self.steps):
            print "Step " + str(step+1)
            for o in self.objects:
                o.step()
                print o


class Stock:
    """
    A stock is a container for a quantity.

    Incoming and outgoing flows may increase or decrease the quantity over time.
    A stock's unit should be a measure of quantity: distance, volume, energy, etc.
    """
    def __init__(self, flows=[], quantity=0, unit="Units", name=""):
        self.flows = flows
        self.quantity = quantity
        self.unit = unit
        self.name = name

    def __str__(self):
        return "Stock '{0}': {1} {2}".format(self.name, self.quantity, self.unit)

    def step(self):
        for f in self.flows:
            self.quantity = self.quantity + f.quantity


class Flow:
    """
    A flow is a way quantities move among stocks.

    A flow's unit is a rate unit; it involves time. Meters per second, Watt-hours.
    """
    def __init__(self, modifiers=[], quantity=0, unit="Units", time_step="Second", name=""):
        self.modifiers = modifiers
        self.quantity = quantity
        self.unit = unit
        self.time_step = time_step
        self.name = name

    def __str__(self):
        return "Flow '{0}': {1} {2}/{3}".format(self.name, self.quantity,
                                                self.unit, self.time_step)

    def step(self):
        for m in self.modifiers:
            self.quantity = self.quantity + m

# TODO flow modifiers not just a static number... give them a formula to vary
# over time.
faucet = Flow([-0.08], 1, "Ounce", "Second", "Faucet") # make some flow
cup = Stock([faucet], 2, "Ounces", "Cup") # make some stocks

s = Simulator([faucet, cup]) # put them in a simulator
s.run() # and run it

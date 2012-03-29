"""
everything.py is a stock/flow modeling kit for system dynamics


faucet = Flow(              # make a flow!
    [                       # list of modifiers
        lambda x: x + 0.1, 
        lambda x: x * 1.1
        ],
    1,                      # initial quantity
    "Ounce",                # unit
    "Second",               # per unit time
    "Faucet"                # name
    )

cup = Stock(                # make a stock!
    [faucet],               # list of flows in and out
    2,                      # initial quantity
    "Ounces",               # unit
    "Cup"                   # name
    )

s = Simulator([faucet, cup])# put them in a simulator
s.run()                     # and run it
"""


class UnitsError(Exception):
    pass

class Simulator:
    """Stepwise stock/flow simulator.

    """
    def __init__(self, objects, time_step="Second", steps=10):
        self.objects = objects
        self.time_step = time_step
        self.steps = steps

    def reconcile_time_units(self):
        m = ""
        for o in self.objects:
            try:
                if o.time_step == self.time_step:
                    m = "Units OK"
                else:
                    raise UnitsError("Your time units don't match. Simulator\
                                     time is in {0}, but {1} time is in\
                                     {2}".format(self.time_step, o.name,
                                                 o.time_step))
            except AttributeError: # Stocks won't have a time_step
                pass
        return m

    def print_objects(self):
        for o in self.objects:
            print o

    def run(self):
        print self.reconcile_time_units()
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

    A flow's unit is a rate unit; i.e. a quantity per unit time. Meters per
    second, gallons per minute, etc. 'Modifiers' are little lambda functions
    modify a flow on each step of the simulator.
    """
    def __init__(self, modifiers=[], quantity=0, unit="Units",
                 time_step="Second", name=""):
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
            self.quantity = m(self.quantity)

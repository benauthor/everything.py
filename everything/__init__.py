"""
everything.py is a stock/flow modeling kit for simulation

TODO fixup example to reflect changes!
Example:

def faucetflow(max_flow, handle_position):
    return max_flow * handle_position

faucet = Flow(                 # make a flow!
    name="Faucet",             # name
    func=faucetflow,           # the function that calculates the rate
    args=[                     # the inputs to the function.
        10.0,                  # these could be constants
        lookup('hpos')         # or looked up from the environment
    ],
    qunit="Ounce",             # unit of quantity
    tunit="Second"             # per unit time
    )

cup = Stock(                   # make a stock!
    flows=(("Faucet", "IN")),  # list of flows in and out
    quantity=2,                # initial quantity
    qunit="Ounce",             # unit
    name="Cup"                 # name
    )

s = Simulator([faucet, cup])   # put them in a simulator
s.run(10)                      # and run it for 10 steps

"""
from collections import namedtuple

PolarFlow = namedtuple('PolarFlow', ['flow', 'polarity'])


class UnitsError(Exception):
    pass


class EnvironmentError(Exception):
    pass


class Simulator(object):
    """Stepwise stock/flow simulator.

    For simulating things.
    """
    def __init__(self, objects, tunit="Second", log=True):
        self.env = {}
        self.stocks = {}
        self.flows = {}
        self.tunit = tunit
        self.log = log
        self.register(objects)

    def __iter__(self):
        return self

    def next(self):
        result = []
        for k, f in self.flows.iteritems():
            result.append(f.step())
        for k, s in self.stocks.iteritems():
            result.append(s.step())
        self.status()
        return result

    def state(self, show_ids=False):
        if show_ids:
            return [(k, v) for k, v in self.env.iteritems()]
        else:
            return [v['last'] for k, v in self.env.iteritems()]

    def entry(self, name, value):
        """Add an entry to the registry.
        """
        if self.env.get(name):
            raise EnvironmentError("Dupicate name! The environment already\
                                    contains the name {0}".format(name))
        else:
            self.env[name] = value

    def update(self, name, value):
        """Update the registry with a new value.
        """
        if not self.env.get(name):

            raise EnvironmentError("Environment does not contain name\
                                    {0}".format(name))
        else:
            self.env[name]['last'] = value

    def lookup(self, name):
        """Look up the most recent value for a name in the registry.
        """
        entry = self.env.get(name)
        if not entry:
            raise EnvironmentError("Environment does not contain name\
                                    {0}".format(name))
        else:
            return entry['last']

    def register(self, objects):
        for o in objects:
            try:
                o.quantity  # if it has a quantity, it's a stock
                self.stocks[o.name] = o
                o.simulation = self
                self.entry(o.name, {'type': 'stock',
                                    'last': o.quantity})
            except AttributeError:
                self.flows[o.name] = o
                o.simulation = self
                self.entry(o.name, {'type': 'flow',
                                    'last': o.calc()})

    def check_time_units(self):
        for k, f in self.flows.iteritems():
            if f.tunit != self.tunit:
                raise UnitsError("Your time units don't match. Simulator\
                                     time is in {0}, but {1} time is in\
                                     {2}".format(self.tunit, f.name, f.tunit))
        return True

    # TODO
    def check_quantity_units(self):
        pass

    def status(self):
        if self.log:
            for k, s in self.stocks.iteritems():
                print s
            for k, f in self.flows.iteritems():
                print f

    def run(self, n):
        for step in xrange(n):
            yield self.next()


class Stock(object):
    """
    A stock is a container for a quantity.

    Incoming and outgoing flows may increase or decrease the quantity over
    time. A stock's unit should be a measure of quantity: distance, volume,
    energy, etc.
    """
    def __init__(self, flows=[], quantity=0, qunit="Unit", name=""):
        # import pdb; pdb.set_trace()
        self.flows = [PolarFlow(*f) for f in flows]
        self.quantity = quantity
        self.qunit = qunit
        self.name = name
        self.simulation = None

    def __str__(self):
        return "Stock '{0}': {1} {2}".format(self.name, self.quantity,
                                             self.qunit)

    def step(self):
        try:
            for f in self.flows:
                if f.polarity == 'OUT':
                    self.quantity -= self.simulation.flows[f.flow].calc()
                else:
                    self.quantity += self.simulation.flows[f.flow].calc()
        except KeyError as e:
            raise EnvironmentError("Flow {0} not found in environment".format(e))
        # after all is said and done, update the registry
        self.simulation.update(self.name, self.quantity)
        return self.quantity

    def check(self):
        for f in self.flows:
            if f.qunit != self.qunit:
                raise UnitsError("Your quantity units don't match. {0}\
                                     time is in {0}, but {1} time is in\
                                     {2}".format(self.name, self.tunit,
                                                 f.name, f.tunit))
        return True


class Flow(object):
    """
    A flow is a way quantities move among stocks.

    A flow's unit is a rate unit; i.e. a quantity per unit time. Meters per
    second, gallons per minute, etc.
    """
    def __init__(self, func=lambda x: x, argmap={}, qunit="Unit",
                 tunit="Second", name=""):
        self.func = func
        self.argmap = argmap
        self.qunit = qunit
        self.tunit = tunit
        self.name = name
        self.simulation = None

    def __str__(self):
        return "Flow '{0}': {1} {2}/{3}".format(self.name, self.calc(),
                                                self.qunit, self.tunit)

    def step(self):
        self.simulation.update(self.name, self.calc())
        return self.calc()

    def calc(self):
        prepared = []
        for i, v in enumerate(self.argmap):
            if isinstance(v, str):
                prepared.append(self.simulation.lookup(v))
            else:
                prepared.append(v)

        try:
            return self.func(**prepared)
        except TypeError:
            return self.func(*prepared)

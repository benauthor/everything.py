from everything import Flow, Stock, Simulator, plot

# faucet = Flow(              # make a flow!
#     [                       # list of modifiers
#         lambda x: x + 0.1,
#         lambda x: x * 1.1
#         ],
#     1,                      # initial quantity
#     "Ounce",                # unit
#     "Second",               # per unit time
#     "Faucet"                # name
#     )

# cup = Stock(                # make a stock!
#     [faucet],               # list of flows in and out
#     2,                      # initial quantity
#     "Ounces",               # unit
#     "Cup"                   # name
#     )

# s = Simulator([faucet, cup])# put them in a simulator
# s.run()                     # and run it


def faucetflow(max_flow, cup):
    return max_flow * 1.0 / cup


def overflowflow(cuplevel, maxcapacity):
    if cuplevel > maxcapacity:
        return cuplevel - maxcapacity
    else:
        return 0

s = Simulator(
    [                         # let's make a simulator
        Stock(                          # it has a stock!
            flows=(("Faucet", "IN"),    # list of flows in and out
                   ("Overflow", "OUT"),
                   ),
            quantity=2,                 # initial quantity
            qunit="Ounce",              # unit
            name="Cup"                  # name
            ),
        Flow(                           # make a flow!
            name="Faucet",              # name
            func=faucetflow,            # the function that calculates the rate
            argmap=[                    # the inputs to the function.
                2.0,                    # these could be constants
                "Cup"   # or looked up from the environment
                ],
            qunit="Ounce",              # unit of quantity
            tunit="Second"              # per unit time
            ),
        Flow(                           # another flow!
            name="Overflow",            # you know the drill!
            func=overflowflow,
            argmap=[
                "Cup",
                5
                ],
            qunit="Ounce",
            tunit="Second"
            )
        ],
    log=False
    )

print s.env
print s.state()
plotter = plot.Plotter(100)
for i in s.run(20):                      # now run it for some number of steps
    plotter.plot_dumbly(i, 0, 6)

# lines = list(s.run(20))
# print lines
# plotter = plot.Plotter(100, [])
# for line in lines:
#     plotter.plotline(line, 0, 10)
# # for line in lines:
#     plotter.addline(line[0], list(reversed(line[1])))  # yuck
# plotter.plot()
# print [s.next() for i in range(10)]
# print s.env()

"""
TODOS
=====

+ think about the api

+ simulator scope instead of global

+ config'able granularity: possible to do the transforms to change timestep?
  (sounds mathy)


"""

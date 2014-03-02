from everything import Flow, Stock, Simulator, lookup

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


def faucetflow(max_flow, handle_position):
    return max_flow * handle_position


faucet = Flow(                 # make a flow!
    name="Faucet",             # name
    func=faucetflow,           # the function that calculates the rate
    argmap=[                     # the inputs to the function.
        2.0,                  # these could be constants
        "lookup('Cup') * 0.25"    # or looked up from the environment
    ],
    qunit="Ounce",             # unit of quantity
    tunit="Second"             # per unit time
    )

cup = Stock(                   # make a stock!
    flows=(("Faucet", "IN"),),  # list of flows in and out
    quantity=2,                # initial quantity
    qunit="Ounce",             # unit
    name="Cup"                 # name
    )

s = Simulator([faucet, cup])   # put them in a simulator
s.run(10)                      # and run it for 10 steps

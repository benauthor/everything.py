from everything import Flow, Stock, Simulator

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

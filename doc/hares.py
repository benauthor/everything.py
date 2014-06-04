from everything import Flow, Stock, Simulator, plot

# http://dwb4.unl.edu/Chem/CHEM869V/CHEM869VLinks/www.supercomp.org/sc96/education/leesummit/Hare_Lynx_Instructions.html

AREA = 1000


def density(animals, area):
    return animals/area


def hare_kills(area, hares, lynx):
    return density(hares, area) * .5 * lynx


def lynx_starvation(area, hares, lynx):
    return 40 * lynx / density(hares, area)

s = Simulator(
    [
        Stock(
            name="Hares",
            flows=[("HareBirths", "IN"),
                   ("HareDeaths", "OUT")],
            quantity=50000,
            qunit="Hares"
            ),
        Stock(
            name="Lynx",
            flows=[("LynxBirths", "IN"),
                   ("LynxDeaths", "OUT")],
            quantity=1250,
            qunit="Lynx"
            ),
        Flow(
            name="HareBirths",
            qunit="Hares",
            tunit="Month",
            func=lambda h, r: h * r,
            argmap=[
                "Hares",
                1.25
                ]
            ),
        Flow(
            name="HareDeaths",
            qunit="Hares",
            tunit="Month",
            func=hare_kills,
            argmap=[
                AREA,
                "Hares",
                "Lynx"
                ]
            ),
        Flow(
            name="LynxBirths",
            qunit="Lynx",
            tunit="Month",
            func=lambda h, r: h * r,
            argmap=[
                "Lynx",
                .25
                ]
            ),
        Flow(
            name="LynxDeaths",
            qunit="Lynx",
            tunit="Month",
            func=lynx_starvation,
            argmap=[
                AREA,
                "Hares",
                "Lynx"
                ]
            )
        ],
    # log=True
    log=False
    )

plotter = plot.Plotter(100)
width = 10000
symbols = ["h", "b", "d", "L", "B", "D"]
state = s.state(show_ids=True)
print state
plotter.plot_dumbly(s.state(), -width, width, symbols=symbols)
for i in s.run(20):                      # now run it for some number of steps
    plotter.plot_dumbly(i, -width, width, symbols=symbols)

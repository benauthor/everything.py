from everything import plot

mylist = (-10, 1, 2, 3, 10, 20, 30, 60, 99, 200)
otherlist = (45, 44, 43, 42, 41)
plotter = plot.Plotter(100, [])
plotter.addline("Foo", mylist)
plotter.addline("Bar", otherlist)
plotter.plot()

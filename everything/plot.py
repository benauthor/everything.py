def plotline(value, width, minimum, maximum):
    myrange = maximum - minimum
    inc = width / float(myrange)
    if value > minimum and value < maximum:
        pos = value - minimum
        chunks = int(round(pos * inc))
        print "x" * chunks
    else:
        print ''


def plotlist(values, width, minimum, maximum):
    for v in values:
        plotline(v, width, minimum, maximum)

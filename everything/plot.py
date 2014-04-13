class Plotter(object):
    def __init__(self, width, lines=[], bg=" "):
        self.width = width
        self.lines = lines
        self.bg = bg

    def addline(self, name, values):
        self.lines.append((name, values))

    def plot(self):
        print "KEY\n==="
        for line in self.lines:
            print "{0}: {1}".format(line[0][0], line[0])
        length = max(len(line[1]) for line in self.lines)
        for i in range(length):
            self.plot_at_position(i)

    def plot_at_position(self, i):
        values = []
        for line in self.lines:
            # TODO this tuple stuff is trashy.
            sym = line[0][0]
            lvals = line[1]
            try:
                values.append((sym, lvals[i], min(lvals), max(lvals)))
            except IndexError:  # out of values
                pass
        self.plotline(values)

    def plotline(self, values, vmin=None, vmax=None):
        line = [self.bg for i in range(self.width)]
        for v in values:
            sym = v[0]
            val = v[1]
            vmin = vmin if vmin is not None else v[2]
            vmax = vmax if vmax is not None else v[3]
            vrange = vmax - vmin
            inc = self.width / float(vrange)
            if val > vmin and val < vmax:
                pos = val - vmin
                chunks = int(round(pos * inc))
                line[chunks] = sym
        print ''.join(line)

    def plot_dumbly(self, values, vmin, vmax):
        line = [self.bg for i in range(self.width)]
        for val in values:
            sym = 'o'
            vrange = vmax - vmin
            inc = self.width / float(vrange)
            if val > vmin and val < vmax:
                pos = val - vmin
                chunks = int(round(pos * inc))
                line[chunks] = sym
        print ''.join(line)

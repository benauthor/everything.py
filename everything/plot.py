class Plotter(object):
    def __init__(self, width, lines, bg=" "):
        self.width = width
        self.lines = lines
        self.bg = bg

    def addline(self, name, values):
        self.lines.append((name, values))

    def plot(self):
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

    def plotline(self, values):
        line = [self.bg for i in range(self.width)]
        for v in values:
            sym = v[0]
            val = v[1]
            vmin = v[2]
            vmax = v[3]
            vrange = vmax - vmin
            inc = self.width / float(vrange)
            if val > vmin and val < vmax:
                pos = val - vmin
                chunks = int(round(pos * inc))
                line[chunks] = sym
        print ''.join(line)

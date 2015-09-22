__author__ = 'zenbook'


class PlotModel:
    def __init__(self, key, plot_id, div):
        self.key = key
        self.plot_id = plot_id
        self.div = div

    def __str__(self):
        out = ""
        out += "key: " + self.key + "\n"
        out += "plot_id: " + self.plot_id + "\n"
        out += "div: " + self.div + "\n"
        return out

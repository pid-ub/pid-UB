from django.shortcuts import render
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components
from model.PlotModel import PlotModel


def simple_chart(request):
    figures = []
    # Mocked plot
    f = figure()
    f.circle([1, 2, 3, 4, 5], [2, 5, 8, 2, 7], size=10)
    # Insert in figures the plots given from service
    figures.append(f)

    script, plots = plot(["myPlot"], figures)
    return render(request, "test.html", {"script": script, "plots": plots})


def plot(keys, f):
    assert len(keys) == len(f)
    script, divs = components(f, CDN)
    if type(divs) is str:
        divs = [divs]
    out = {}
    for i in range(len(f)):
        out[keys[i]] = PlotModel(keys[i], f[i]._id, divs[i])
    return script, out

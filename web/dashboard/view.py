from django.shortcuts import render
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components
from model.PlotModel import PlotModel


def simple_chart(request):
    # Mocked plot
    f = figure()
    f.circle([1, 2, 3, 4, 5], [2, 5, 8, 2, 7], size=10)
    f2 = figure()
    f2.circle([2, 5, 8, 2, 7], [1, 2, 3, 4, 5], size=5)
    # Insert in figures the plots given from service
    figures = [f, f2]

    script, plots = plot(["myPlot", "myOtherPlot"], figures)
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

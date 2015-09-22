from django.shortcuts import render
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components


def simple_chart(request):
    plot = figure()
    plot.circle([1, 2, 3, 4, 5], [2, 5, 8, 2, 7], size=10)
    script, div = components(plot, CDN)

    return render(request, "test.html", {"the_script": script, "the_div": div, "the_id": plot._id})

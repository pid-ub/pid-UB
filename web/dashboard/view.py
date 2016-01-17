# coding=utf-8
from django.shortcuts import render
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components
from model.PlotModel import PlotModel
from service.clustering import clustering, estimate, renounce
from service.asignaturas import asignaturas
from settings import *
from django.shortcuts import redirect


def students_view(request):
    return redirect('#students')


def subjects_view(request):
    return redirect('#subjects')


def predictive_view(request):
    return redirect('#predictive')


def team_view(request):
    return redirect('#team')


def home_view(request):
    # Insert in figures the plots given from service
    figures = []
    figures_lbl = []

    tmp = estimate(primer_info_qual, 5)
    lbl_clusters = ["MP1", # Milors en programació de primer
                            "BN1", # Bones notes en totes les assignatures de primer
                            "S1", # Suspesos de primer
                            "A1", # Aprovats de primer
                            "MM1"] # Millors en matemátiques de primer
    colors = ['#fffea3', '#97f0aa', '#ff9f9a', '#92c6ff', '#FAC864']
    cluster_figures, donut = clustering(tmp, lbl_clusters, colors)
    figures += cluster_figures
    figures_lbl += lbl_clusters
    figures.append(donut)
    figures_lbl.append("donut1")
    figures.append(renounce(tmp, colors, df_info, s2_info, lbl_clusters))
    figures_lbl.append("renounce1")

    tmp = estimate(segon_info_qual, 4)
    lbl_clusters = ["BN2", # Bones notes de segon
                               "ISF2", #ICC i SO1 fluixes
                               "A2", # Aprovats de segon
                               "PPIE2"] #problemes amb pie
    colors = ['#97f0aa', '#fffea3', '#92c6ff', '#FAC864']
    cluster_figures, donut = clustering(tmp, lbl_clusters, colors)
    figures += cluster_figures
    figures_lbl += lbl_clusters
    figures.append(donut)
    figures_lbl.append("donut2")
    figures.append(renounce(tmp, colors, df_info, s3_info, lbl_clusters))
    figures_lbl.append("renounce2")


    figura_regresion, figura_evolucion, figura_convalidacion, numero_alumnos_regresion, num_alumnes_conv, num_alumnes_outliers, num_evolucion = asignaturas(reg, qual, assig)
    figures.append(figura_regresion)
    figures_lbl.append("regresion")
    figures.append(figura_evolucion)
    figures_lbl.append("evolucion")
    figures.append(figura_convalidacion)
    figures_lbl.append("convalidacion")

    script, plots = plot(figures_lbl, figures)
    return render(request, "index.html", {"script": script, "plots": plots, "num_reg": numero_alumnos_regresion, "num_conv": num_alumnes_conv, "num_out": num_alumnes_outliers, "num_evo":num_evolucion })


def plot(keys, f):
    assert len(keys) == len(f)
    script, divs = components(f, CDN)
    if type(divs) is str:
        divs = [divs]
    out = {}
    for i in range(len(f)):
        out[keys[i]] = PlotModel(keys[i], f[i]._id, divs[i])
    return script, out

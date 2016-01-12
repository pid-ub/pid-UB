# coding=utf-8
import numpy as np
import math
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import HoverTool
from sklearn.cluster import KMeans


def estimate(df, k):
    estimator = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=5, random_state=42)

    tmp = df.copy()


    estimator.fit(tmp.values)
    if -1 in estimator.labels_:
        print "Not clustering"
        return None
    tmp['label'] = estimator.labels_
    k = len(set(estimator.labels_))
    return tmp


def clustering(tmp, lbl_clusters, colors):
    aprobat = [5 for i in range(10)]


    data_qual = tmp.groupby('label').mean()
    describe_qual = tmp.groupby('label').describe()

    # deep, muted, pastel, bright, dark, and colorblind
    #colors = seabornpalette_to_bokeh(sbn.color_palette("pastel", k))

    data = np.array(data_qual.values)
    figures = []
    counts = []
    i=0
    for d in data:
        counts.append(int(describe_qual.ix[i].ix['count'][0]))
        std = describe_qual.ix[i].ix['std']
        source_mark = ColumnDataSource(
            data=dict(
                mean=d,
                std=std
                )
            )

        f = figure(title=lbl_clusters[i],
                x_range=tmp.columns[:-1].tolist(), y_range=[0, 10], plot_width=425, plot_height=250,
                tools=""
        )
        f.xgrid.grid_line_color = None
        f.rect(x=tmp.columns[:-1], y=d/2, width=0.8, height=d, color=colors[i], alpha=0.8, source=source_mark) #colors[k]
        f.rect(x=tmp.columns[:-1], y=d, width=0.025, height=std*2, color='black', alpha=0.5)
        f.line(x=tmp.columns[:-1], y=aprobat, line_color='red')
        hover = f.select(dict(type=HoverTool))
        hover.tooltips = [
            ("mean", " @mean"),
            ("std", " @std")
        ]
        figures.append(f)
        i+=1

    counts = [i/float(sum(counts)) for i in counts]
    percent = counts[:]
    for i in range(1,len(percent)):
        percent[i] += percent[i-1]
    percent.insert(0,0)
    starts = [p*2*math.pi for p in percent[:-1]]
    ends = [p*2*math.pi for p in percent[1:]]


    donut = figure(x_range=(-1.5,1.5), y_range=(-1.5,1.5), plot_width=450, plot_height=450, tools="")
    donut.xgrid.grid_line_color = None
    donut.ygrid.grid_line_color = None
    legend = []
    for i in counts:
        legend.append("%.2f%%" % (i*100))
    for i in range(len(starts)):
        legend[i] += " - " + lbl_clusters[i]
        donut.wedge(x=0, y=0, radius=1, start_angle=starts[i], end_angle=ends[i], color=colors[i], line_color = 'black', legend=legend[i])

    return (figures, donut)


def renounce(df, colors, register, subjects1, lbl):
    groups = []
    subjects1 = set(subjects1)
    for c in set(df['label']):
        d = df[df['label'] == c]
        count = 0.0
        for i in d.index:
            alumne = register[register['id_alumne'] == i]
            assig_alumne = set(alumne['id_assig'])
            #if
            if len(assig_alumne.intersection(subjects1)) == 0:
                count+=1
        groups.append((count/len(d.index))*100)
    groups = np.array(groups)

    source = ColumnDataSource(
        data=dict(
            percent=groups
            )
        )
    f = figure(
                x_range=lbl, y_range=[0,100], plot_width=900, plot_height=300,
                tools=""
              )
    f.xgrid.grid_line_color = None
    f.rect(x=lbl, y=groups/2, width=0.3, height=groups, color=colors, alpha=0.8, source=source)
    hover = f.select(dict(type=HoverTool))
    hover.tooltips = [
        ("percert", " @percent")
    ]
    return f

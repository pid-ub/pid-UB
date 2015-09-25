import numpy as np
import math
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import HoverTool
from sklearn.cluster import KMeans


def clustering(df, k):
    estimator = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=5, random_state=42)
    lbl_clusters = ["MP1", # Milors en programació de primer
                            "BN1", # Bones notes en totes les assignatures de primer
                            "S1", # Suspesos de primer
                            "A1", # Aprovats de primer
                            "MM1"] # Millors en matemátiques de primer
    colors = ['#fffea3', '#97f0aa', '#ff9f9a', '#92c6ff', '#FAC864']
    tmp = df.copy()
    aprobat = [5 for i in range(10)]

    estimator.fit(tmp.values)
    if -1 in estimator.labels_:
        print "Not clustering"
        return None
    tmp['label'] = estimator.labels_
    k = len(set(estimator.labels_))

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
                x_range=df.columns.tolist(), y_range=[0, 10], plot_width=425, plot_height=250,
                tools="pan,wheel_zoom,box_zoom,reset,hover",
                x_axis_label = "Assignatures",
                y_axis_label = "Nota"
        )
        f.xgrid.grid_line_color = None
        f.rect(x=df.columns, y=d/2, width=0.8, height=d, color=colors[i], alpha=0.8, source=source_mark) #colors[k]
        f.rect(x=df.columns, y=d, width=0.025, height=std*2, color='black', alpha=0.5)
        f.line(x=df.columns, y=aprobat, line_color='red')
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


    donut = figure(x_range=(-1.2,1.2), y_range=(-1.2,1.2), plot_width=450, plot_height=450, title="Distribució dels clusters")
    donut.xgrid.grid_line_color = None
    donut.ygrid.grid_line_color = None
    legend = []
    for i in counts:
        legend.append("%.2f%%" % (i*100))
    for i in range(len(starts)):
        legend[i] += " - " + lbl_clusters[i]
        donut.wedge(x=0, y=0, radius=1, start_angle=starts[i], end_angle=ends[i], color=colors[i], line_color = 'black', legend=legend[i])

    return (figures, donut)
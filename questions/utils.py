 # -*- coding: utf-8 -*-

import math
from bokeh.plotting import *
import numpy as np
import pandas as pd

def select_rows_by_columns(df, group, col):
    out = pd.DataFrame()
    tmp = df.copy()
    for s in group:
        out = pd.concat([out, tmp[tmp[col] == s]])
    out = out.reset_index(drop=True)
    return out

def table_students(df, group_subjects):

    # Amb select_rows_by_subjects, ens quedem amb només les qualificacions de les assignatures de primer
    grp = select_rows_by_columns(df, group_subjects, 'id_assig')
    grp = grp[grp["tipus_apunt"] != "Convalidat"]
    # Agrupem les assignatures per niub
    students_by_niub = grp.groupby('id_alumne').size()
    # D'aquesta agropació ens quedem amb els 'niubs' que apareixen 10 cops, les assignatures cursades a 1er
    students_by_niub = students_by_niub.index[students_by_niub >= len(group_subjects)]
    # Creem una taula tal que: alumnes-assignatures i a cada celda la nota corresponent
    grp_qual = grp.pivot_table('nota_primera_conv', index='id_alumne',columns='id_assig', aggfunc='max')
    # Ara que sabem els alumnes que han cursat les 10 assignatures de primer, els seleccionem
    grp_qual = grp_qual.ix[students_by_niub]
    grp_qual.dropna(inplace=True, axis=0)
    return grp_qual

def get_gridplot(figures):
    out = []
    n = math.sqrt(len(figures))
    n = int(math.ceil(n))
    for i in range(n):
        out.append([])
        for j in range(n):
            if i*n+j == len(figures):
                return GridPlot(children=out)
            out[i].append(figures[i*n+j])
    return GridPlot(children=out)

def seabornpalette_to_bokeh(palette):
    colors = np.array(palette)
    colors = np.multiply(colors, 255).astype('int')
    colors = tuple(map(tuple, colors))
    return ['#%02x%02x%02x' % c for c in colors]

# -*- encoding: utf-8 -*-
import numpy as np
import pandas as pd
from bokeh.plotting import figure


def select_rows(df, group, col):

    out = pd.DataFrame()
    tmp = df.copy()
    for s in group:

        out = pd.concat([out, tmp[tmp[col] == s]])
    out = out.reset_index(drop=True)
    return out


def asignaturas(registers, qualifications, assig):
    qualifications2 = qualifications

    primero = [364291, 364292, 364289, 364288, 364298, 364297, 364300, 364303, 364305, 364302, 364314, 364308, 364322, 364315, 364309]
    primero_label = ['ALGE', 'CAL', 'DDB', 'P1', 'ALGO', 'ELEC', 'AA', 'DS', 'EC', 'ICC', 'IA', 'SO2', 'TNUI','VA','XAR']

    segundo = [364294, 364290, 364293, 364301, 364299, 364296, 364295, 364306, 364304, 364307, 364311, 364323, 364328, 364310, 364312]
    segundo_label = ['FIS', 'IO', 'MD', 'ED', 'P2', 'EMP', 'PIE', 'PAE', 'PIS','SO1', 'BD', 'FHIC', 'GIVD', 'LIL', 'SD']

    info_por_curso = "primero"

    id_alumne = 11

    tot = pd.merge(registers, qualifications)
    tot = tot[["id_alumne", "id_enseny", "nota_acces", "id_assig", "nota_primera_conv"]]
    tot = tot[tot["nota_primera_conv"] > 0].reset_index(drop=True)
    if (info_por_curso == "primero"):
        tot = tot[tot['id_enseny'] == 'G1077']
        tot = select_rows(tot, primero[:4] + segundo[:4], 'id_assig')
    elif (info_por_curso == "segundo"):
        tot = tot[tot['id_enseny'] == 'G1077']
        tot = select_rows(tot, primero[5:9] + segundo[5:9], 'id_assig')
    elif (info_por_curso == "tercero"):
        tot = tot[tot['id_enseny'] == 'G1077']
        tot = select_rows(tot, primero[10:14] + segundo[10:14], 'id_assig')

    tot= tot[tot['nota_acces'] >= 5]

    alumne = tot[tot['id_alumne'] == id_alumne]

    alumne = alumne[["nota_acces", "nota_primera_conv"]].mean().values

    niub_g = tot.groupby('id_alumne').mean()

    notas_acces = niub_g['nota_acces'].values

    qualificacions = niub_g['nota_primera_conv'].values

    regression = np.polyfit(qualificacions, notas_acces, 1)

    r_x, r_y = zip(*((i, i*regression[0] + regression[1]) for i in range(len(qualificacions))))

    aux = []
    for nota in notas_acces:
        if nota > 10:
            aux.append(10)
        else:
            aux.append(nota)

    notas_acces= aux



    TOOLS="resize,crosshair,pan,wheel_zoom,box_zoom,reset,box_select,lasso_select, save"
    p = figure(title = "Regresion entre nota de acceso y media cualificaciones", background_fill="#EFE8E2", tools=TOOLS, x_range=(0, 10.1), y_range=(0, 10.1))
    p.circle(qualificacions,notas_acces, radius=0.06, fill_color='#F38630',fill_alpha=0.6, legend="Alumnos")

    p.line(r_x, r_y, color="red", line_width = 2, legend="Linea de regresión obtenida")
    p.line([0,10], [0,10], color="blue", line_width = 2, legend="Linea de regresión ideal")


    p.circle(alumne[1], alumne[0], radius = 0.07, fill_color = 'red' ,fill_alpha=0.6, line_color=None)

    p.xaxis.axis_label = 'Nota media Universidad'
    p.yaxis.axis_label = 'Nota de acceso'
    p.title_text_font_size='15pt'
    p.plot_width = 600
    p.legend.orientation = "bottom_right"




    qual = pd.merge(qualifications, assig)
    qual = qual[['any_matriculacio_assig', 'nota_primera_conv', 'desc_assig', 'curs_assig', 'id_enseny_assig']]


    # Selecionamos las calificaciones de Ingeniería Informática
    qual_info = qual[qual['id_enseny_assig'] == 'G1077']
    list_a = ["Primer Curso", "Segundo curso", "Tercer curso", "Cuarto curso"]
    x_min_range = 2009
    figures = list()

    # Indicamos el año de la introdución de la reevaluación
    any_reev = 2011
    curs = 1

    # Obtenemos las calificaciones del curso actual
    qualifications = qual_info[qual_info['curs_assig'] == curs]
    assigs_list = qualifications.desc_assig.unique()
    anys_list = qualifications.any_matriculacio_assig.unique()
    anys_list.sort()
    # Agrupamos las calificaciones en función de la asignatura y del año de la matriculación por parte del alumno
    assigs_anys = qualifications.groupby(['desc_assig', 'any_matriculacio_assig'])

    # Creamos el nuevo grafico y definimos sus caracteristicas
    p2 = figure(title = list_a[curs - 1], x_range = [x_min_range - 1 + curs, 2014], plot_width=1250)
    col = ['#8f6b51','#dfcb8c','#d8b9b4','#7e858f','#373934','#653040','#dfdcd7','#6b9fc6','#7d8790','#30394a', '#8b9068','#a8bcaa','#008ea7','#606f75','#204253']

    test = [[],[]]
    k = 0
    # Recorremos la lista de las asignaturas del curso actual
    for assig in assigs_list:
        mean = []
        anys_list_assig = []
        # Recorremos los años en los que se ha cursado la asignatura actual
        for any_ in anys_list:
            try:
                # Obtenemos la agrupación representada por la asignatura y el año de matriculación
                assig_any = assigs_anys.get_group((assig, any_)).reset_index(drop=True)
                # Calculamos la media
                mean.append(assig_any.nota_primera_conv.mean())
                # Añadimos la media a la lista global
                anys_list_assig.append(any_)

                # Verificamos si el año es el año de la introdución de la reevaluación o el año previo
                if (any_ == any_reev - 1):
                    test[0].append(assig_any.nota_primera_conv.values)
                elif (any_ == any_reev):
                    test[1].append(assig_any.nota_primera_conv.values)

            except:
                continue
        # Añadimos al grafico la media de cada asignatura representado por un circulo
        p2.circle(anys_list_assig, mean, legend=assig, line_color=col[k], line_width=8)
        # Añadimos al grafico la evolución de la media de cada asignatura
        p2.line(anys_list_assig, mean, line_width=3, line_color=col[k])
        k+=1
    # Añadimos la asignatura a la lista de asignaturas


    qualifications = qualifications2



    # Selecionamos el identificador de la asignatura que se ha convalidado
    asignatura_convalidada = 364299
    # Selecionamos el identificador de la asignatura que se ha visto afectada por las convalidaciones
    asignatura_no_convalidada = 364304
    # De las calificaciones nos quedamos solo con los campos que nos interesa
    notas = qualifications[['id_alumne', 'id_assig', 'tipus_apunt', 'nota_primera_conv']]
    # Nos quedamos con las notas de la asignatura que algunos alumnos convalidan
    notas_prog2 = notas[notas['id_assig'] == asignatura_convalidada]
    # Separamos a los alumnos en funcíon de si han convalidado la asignatura o no
    alumnes_conv_prog2 = notas_prog2[notas_prog2['tipus_apunt'] == 'Convalidat']
    alumnes_no_conv_prog2 = notas_prog2[notas_prog2['tipus_apunt'] != 'Convalidat']
    # Nos quedamos con los identificadores de los alumnos que han convalidado o no la asignatura
    id_alumnes_conv = alumnes_conv_prog2['id_alumne'].values
    id_alumnes_no_conv = alumnes_no_conv_prog2['id_alumne'].values
    # Selecionamos las calificaciones de la asignatura que afecta las convalidaciones
    notas_pis = notas[notas['id_assig'] == asignatura_no_convalidada]
    # Separamos a los alumnos en funcíon de si han convalidado la asignatura de primero de programación o no
    notas_pis_conv = select_rows(notas_pis, id_alumnes_conv, 'id_alumne')
    notas_pis_no_conv = select_rows(notas_pis, id_alumnes_no_conv, 'id_alumne')
    # Nos quedamos solo con las calificaciones mayores que 0
    notas_pis_conv = notas_pis_conv[notas_pis_conv['nota_primera_conv'] > 0]
    notas_pis_no_conv = notas_pis_no_conv[notas_pis_no_conv['nota_primera_conv'] > 0]
    # Selecionamos las notas de la asignatura de tercero
    notas_pis_conv = notas_pis_conv[['nota_primera_conv']].values
    notas_pis_no_conv = notas_pis_no_conv[['nota_primera_conv']].values
    notas_pis_conv = [item for sublist in notas_pis_conv for item in sublist]
    notas_pis_no_conv = [item for sublist in notas_pis_no_conv for item in sublist]



    s1 = pd.Series(notas_pis_conv)
    df1 = pd.DataFrame(s1, columns=['nota_primera_conv'])
    df1['convalidado'] = 'Convalidado'

    s2 = pd.Series(notas_pis_no_conv)
    df2 = pd.DataFrame(s2, columns=['nota_primera_conv'])
    df2['convalidado'] = 'No Convalidado'

    df = pd.concat([df1, df2])



    # Las categorías de los datos
    cats = ['Convalidado', 'No Convalidado']

    # Buscamos los cuartiles y el IQR para cada categoría
    groups = df.groupby('convalidado')
    q1 = groups.quantile(q=0.25)
    q2 = groups.quantile(q=0.5)
    q3 = groups.quantile(q=0.75)
    iqr = q3 - q1
    upper = q3 + 1.5*iqr
    lower = q1 - 1.5*iqr

    # Buscamos los outliers para cada categoría
    def outliers(group):
        cat = group.name
        return group[(group.nota_primera_conv > upper.loc[cat][0]) | (group.nota_primera_conv < lower.loc[cat][0])]['nota_primera_conv']
    out = groups.apply(outliers).dropna()


    # Preparamos los outliers para poder representarlos graficamente.
    outx = []
    outy = []

    for cat in cats:
        try:
            # Solo añadimos los outiers si existen
            if not out.loc[cat].empty:
                for value in out[cat]:
                    outx.append(cat)
                    outy.append(value)
        except:
            pass

    p3 = figure(tools="save", background_fill="#EFE8E2", title="", x_range=cats)

    qmin = groups.quantile(q=0.00)
    qmax = groups.quantile(q=1.00)
    upper.nota_primera_conv = [min([x,y]) for (x,y) in zip(list(qmax.iloc[:,0]),upper.nota_primera_conv) ]
    lower.nota_primera_conv = [max([x,y]) for (x,y) in zip(list(qmin.iloc[:,0]),lower.nota_primera_conv) ]

    p3.segment(cats, upper.nota_primera_conv, cats, q3.nota_primera_conv, line_width=2, line_color="black")
    p3.segment(cats, lower.nota_primera_conv, cats, q1.nota_primera_conv, line_width=2, line_color="black")

    p3.rect(cats, (q3.nota_primera_conv+q2.nota_primera_conv)/2, 0.7, q3.nota_primera_conv-q2.nota_primera_conv,
        fill_color="#E08E79", line_width=2, line_color="black")
    p3.rect(cats, (q2.nota_primera_conv+q1.nota_primera_conv)/2, 0.7, q2.nota_primera_conv-q1.nota_primera_conv,
        fill_color="#3B8686", line_width=2, line_color="black")

    p3.rect(cats, lower.nota_primera_conv, 0.2, 0.01, line_color="black")
    p3.rect(cats, upper.nota_primera_conv, 0.2, 0.01, line_color="black")

    p3.circle(outx, outy, size=6, color="#F38630", fill_alpha=0.6)

    p3.xgrid.grid_line_color = None
    p3.ygrid.grid_line_color = "white"
    p3.grid.grid_line_width = 2
    p3.xaxis.major_label_text_font_size="12pt"
    p3.title = "Notas de Proyecto Integrado de Software"




    return p, p2, p3
# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
from io import BytesIO
from matplotlib import pyplot

"""
AK8PO: Utility methods

@author: Filip Findura
"""


def get_graph():
    buffer = BytesIO()
    pyplot.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_chart(data, cols, **kwargs):
    # TODO
    msg = list()
    pyplot.switch_backend('AGG')
    fig, axs = pyplot.subplots(len(cols), figsize=(10, 4 * len(cols)))

    try:
        # d = data.groupby(order_by, as_index=False)  # ['temperature'].agg('sum')
        #
        # if chart_type == 'bar':
        #     pyplot.bar(d[order_by], d['temperature'])
        # elif chart_type == 'pie':
        #     pyplot.pie(data=d, x='temperature', labels=d[order_by])
        # elif chart_type == 'line':
        #     pyplot.plot(d[order_by], d['temperature'], color='gray', marker='o', linestyle='dashed')
        # else:
        #     msg.append("Chart typ not found.")

        data.set_index('forecast_time', inplace=True)
        d = data.groupby('datasource', as_index=False)
        for i, g in enumerate(cols):
            pyplot.sca(axs[i])
            d[g].plot(legend=True)
            pyplot.ylabel(g)

    except Exception as e:
        msg.append(f"Failed to plot charts: {e}")

    pyplot.tight_layout()
    chart = get_graph()
    return chart, msg

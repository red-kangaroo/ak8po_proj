# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
from io import BytesIO
import pandas
from matplotlib import pyplot

"""
AK8PO: Test plotting

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


def get_chart(chart_type, data, order_by, **kwargs):
    # TODO
    msg = list()
    # pyplot.switch_backend('AGG')
    # fig = pyplot.figure(figsize=(10, 4))

    try:
        # d = data.groupby(order_by, as_index=False)  # ['temperature'].agg('sum')

        # data = data.drop('wind_dir', axis=1)
        data.set_index('forecast_time', inplace=True)
        d = data.groupby(order_by, as_index=False)
        # fig, axs = pyplot.subplots(figsize=(10, 4),
        #                            nrows=4, ncols=2,
        #                            gridspec_kw=dict(hspace=0.4))

        # TODO: Django radio buttons
        groups = ['temperature', 'humidity', 'cloud_fraction', 'wind_speed', 'precipitations', 'pressure', 'chance_rain', 'chance_snow']

        # for (g, ax) in zip(groups, axs.flatten()):
        #     ax.plot(d[g])
        #     ax.set_title(g)
        fig, axs = pyplot.subplots(len(groups), figsize=(10, 4 * len(groups)))
        for i, g in enumerate(groups):
            pyplot.sca(axs[i])
            d[g].plot(legend=True)
            pyplot.ylabel(g)

        pyplot.show()

        return

        # if chart_type == 'bar':
        #     pyplot.bar(d[order_by], d['temperature'])
        # elif chart_type == 'pie':
        #     pyplot.pie(data=d, x='temperature', labels=d[order_by])
        # elif chart_type == 'line':
        #     pyplot.plot(d['forecast_time'], d['temperature'], color='gray', marker='o', linestyle='dashed')
        #     pyplot.show()
        # else:
        #     msg.append("Chart typ not found.")
    except Exception as e:
        msg.append(f"Failed to plot charts: {e}")

    # pyplot.tight_layout()
    chart = get_graph()
    return chart, msg


if __name__ == "__main__":
    weather_df = pandas.read_excel('weather_data.xlsx', 'data', index_col=None)  # index_col=[0, 1])
    get_chart('line', weather_df, 'datasource')

    pass

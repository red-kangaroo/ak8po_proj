# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
from io import BytesIO
from matplotlib import pyplot
from matplotlib.ticker import FormatStrFormatter

"""
AK8PO: Utility methods

@author: Filip Findura
"""

LABELS = {  # Percent signs need to be doubled because ticker uses old-style replacement denoted by percent signs.
    'temperature': ('Temperature', '°C'),
    'humidity': ('Humidity', '%%'),
    'cloud_fraction': ('Cloudiness', '%%'),
    'wind_speed': ('Wind Speed', 'km/h'),
    'wind_dir': ('Wind Direction', ''),
    'precipitations': ('Precipitation', 'mm'),
    'pressure': ('Pressure', 'mb'),
    'chance_rain': ('Chance of Rain', '%%'),
    'chance_snow': ('Chance of Snow', '%%'),
}
EMPTY_LABEL = ('', '')


# ==============================================================================
# Plots
# ==============================================================================
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
    msg = list()
    pyplot.switch_backend('AGG')
    fig, axs = pyplot.subplots(len(cols), figsize=(10, 4 * len(cols)))

    if kwargs.get('date_from') and kwargs.get('date_to'):
        if kwargs.get('date_from') == kwargs.get('date_to'):
            fig.suptitle(f"Weather for {kwargs.get('date_from')}")
        else:
            fig.suptitle(f"Weather from {kwargs.get('date_from')} to {kwargs.get('date_to')}")
    else:
        fig.suptitle("Weather results")

    try:
        d = data.set_index('forecast_time')
        d = d.groupby('datasource', as_index=False)

        for i, g in enumerate(cols):
            if len(cols) > 1:
                ax = axs[i]
            else:
                ax = axs

            # TODO legend
            # if i == len(cols) - 1:
            #     handles, labels = axs[i].get_legend_handles_labels()
            #     fig.legend(handles, labels, loc='upper center')

            pyplot.sca(ax)
            d[g].plot()

            l, u = LABELS.get(g, EMPTY_LABEL)
            pyplot.xlabel('')
            pyplot.ylabel(l)
            ax.get_yaxis().set_major_formatter(FormatStrFormatter(f'%d {u}'))

    except Exception as e:
        msg.append(f"Failed to plot charts: {e}")

    pyplot.tight_layout()
    pyplot.subplots_adjust(top=0.9)
    chart = get_graph()
    return chart, msg

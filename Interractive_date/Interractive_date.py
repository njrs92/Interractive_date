import numpy as np
from tornado.ioloop import IOLoop

from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.server.server import Server
from bokeh.layouts import widgetbox
from bokeh.models.widgets import DateSlider


import time
import calendar
import datetime
from datetime import date
from math import pi
from bokeh.core.properties import value
from bokeh.models import PrintfTickFormatter

import pandas as pd
from bokeh.models.widgets import Button
from bokeh.layouts import row

io_loop = IOLoop.current()
pd.options.mode.chained_assignment = None  # default='warn'
def modify_doc(doc):
    try:
        file_path = "C:/Users/stevensn2h/Desktop/2017_MetroTV_ABC main channel.csv"
        data = pd.read_csv(file_path, header=8)
    except:
        quit(0)
        
    slider = DateSlider(title="Date Range: ", start=date(2017, 1, 1), end=date(2017,12, 31), value=(date(2017, 5, 5)), step=1, width=600) 
    colors = ["#c9d9d3", "#718dbf", "#e84d60","#A9d9d3", "#218dbf"]
    button = Button(label="Update", button_type="success")
    def callback():
        date_selected = datetime.datetime.strptime(str(slider.value),'%Y-%m-%d')
        sub_set = data.loc[data['Day'] == date_selected.strftime('%d/%m/%Y').lstrip("0")]
        sub_set['Average Audience (Total People)'] = sub_set['Average Audience (Total People)'].str.replace(',', '')
        sub_set['Average Audience (Total People)'] = sub_set['Average Audience (Total People)'].astype(int)
        sub_set = sub_set.sort_values(['Average Audience (Total People)'],ascending=False)
        shows = sub_set['Program Name'].tolist()    
        number_of=1
        for x in shows:
            if x in shows: 
                shows[shows.index(x)] = str(shows[shows.index(x)]) + str(number_of)
                number_of+= 1
        demos = list(sub_set.columns.values[6:11])
        y = {'shows':shows}
        for x in demos:
            temp = sub_set[x].tolist()
            temp2 = list()
            for z in range(len(temp)):
                temp2.append(int((temp[z].replace(',', ''))) )
            y[x] = temp2

        p = figure(x_range=shows, title="Shows by Demo for "+(date_selected.strftime('%d-%m-%Y').lstrip("0")),
                toolbar_location=None, tools="hover", tooltips="$name @shows: @$name")
        p.vbar_stack(demos, x='shows', width=0.9, color=colors, source=y,legend=[value(x) for x in demos])
        p.y_range.start = 0
        p.yaxis[0].formatter = PrintfTickFormatter(format="%5d")
        p.xaxis.major_label_orientation = -pi/8
        p.xgrid.grid_line_color = None
        p.axis.minor_tick_line_color = None
        p.outline_line_color = None
        p.sizing_mode = 'stretch_both'
        p.legend.location = "top_left"
        p.legend.orientation = "horizontal"
        doc.add_root(p)
        
    button.on_click(callback)
    doc.add_root(row(slider,button))


bokeh_app = Application(FunctionHandler(modify_doc))
server = Server({'/': bokeh_app}, io_loop=io_loop)
server.start()

if __name__ == '__main__':
    print('Opening Bokeh application on http://localhost:5006/')

    io_loop.add_callback(server.show, "/")
    io_loop.start()
import plotly.plotly as py
import plotly
import plotly.graph_objs as go
from datetime import datetime
from BridgeParsing import Message
import BridgeParsing


def generate_graph(data, filename):
    print "Generating {}.html".format(filename)
    plotly.offline.plot({
        "data": data,
        "layout": go.Layout(barmode="stack"),
    }, filename="{}.html".format(filename))


def build_bar_trace_by_times_dict(times_dict, name):
    datetimes = times_dict.keys()
    datetimes.sort()

    counts = [len(times_dict[time]) for time in datetimes]

    return go.Bar(x=datetimes, y=counts, name=name)


def build_trace_by_bridge_type(messages, bridge_type):
    my_dict = Message.dict_of_messages_by_time(Message.filter_by_bridge_type(messages, bridge_type))
    return build_bar_trace_by_times_dict(my_dict, bridge_type)


def build_data_by_called_functions(messages):
    dict_by_called_funcs = Message.dict_of_messages_by_called_func(messages)
    called_funcs = dict_by_called_funcs.keys()

    data = []
    for called_func in called_funcs:
        datetimes_dict = Message.dict_of_messages_by_time(dict_by_called_funcs[called_func])
        data.append(build_bar_trace_by_times_dict(datetimes_dict, called_func))

    return data

def main():
    with open('log.txt', 'r') as opened:
        log = opened.read()
        messages = Message.messages_by_log(log)

    generate_graph(build_data_by_called_functions(Message.filter_by_bridge_type(messages, BridgeParsing.JS_TO_NATIVE)), "JS->Native")
    generate_graph(build_data_by_called_functions(Message.filter_by_bridge_type(messages, BridgeParsing.NATIVE_TO_JS)), "Native->JS")


if __name__ == "__main__":
    main()

def _general_function(params, xdata, ydata, function):
    return function(xdata, *params) - ydata

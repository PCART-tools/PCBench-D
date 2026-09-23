def _resize_rectangle(tool, xdata, ydata, xdata_new, ydata_new,
                      use_key=None):
    do_event(tool, 'press', xdata=xdata, ydata=ydata, button=1)
    if use_key is not None:
        do_event(tool, 'on_key_press', key=use_key)
    do_event(tool, 'onmove', xdata=xdata_new, ydata=ydata_new, button=1)
    if use_key is not None:
        do_event(tool, 'on_key_release', key=use_key)
    do_event(tool, 'release', xdata=xdata_new, ydata=ydata_new, button=1)

    return tool

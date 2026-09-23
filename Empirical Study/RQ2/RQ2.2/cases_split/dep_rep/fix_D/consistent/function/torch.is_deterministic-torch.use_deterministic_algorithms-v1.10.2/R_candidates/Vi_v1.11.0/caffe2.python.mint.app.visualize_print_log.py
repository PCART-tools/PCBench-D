def visualize_print_log(filename):
    try:
        data = np.loadtxt(filename)
        if data.ndim == 1:
            data = data[:, np.newaxis]
    except Exception as e:
        return 'Cannot load file {}: {}'.format(filename, str(e))
    chart_name = os.path.splitext(os.path.basename(filename))[0]
    chart = nvd3.lineChart(
        name=chart_name + '_log_chart',
        height=args.chart_height,
        y_axis_format='.03g'
    )
    if args.sample < 0:
        step = max(data.shape[0] / -args.sample, 1)
    else:
        step = args.sample
    xdata = np.arange(0, data.shape[0], step)
    # if there is only one curve, we also show the running min and max
    if data.shape[1] == 1:
        # We also print the running min and max for the steps.
        trunc_size = data.shape[0] / step
        running_mat = data[:trunc_size * step].reshape((trunc_size, step))
        chart.add_serie(
            x=xdata[:trunc_size],
            y=running_mat.min(axis=1),
            name='running_min'
        )
        chart.add_serie(
            x=xdata[:trunc_size],
            y=running_mat.max(axis=1),
            name='running_max'
        )
        chart.add_serie(x=xdata, y=data[xdata, 0], name=chart_name)
    else:
        for i in range(0, min(data.shape[1], args.max_curves)):
            # data should have 4 dimensions.
            chart.add_serie(
                x=xdata,
                y=data[xdata, i],
                name='{}[{}]'.format(chart_name, i)
            )

    return jsonify_nvd3(chart)

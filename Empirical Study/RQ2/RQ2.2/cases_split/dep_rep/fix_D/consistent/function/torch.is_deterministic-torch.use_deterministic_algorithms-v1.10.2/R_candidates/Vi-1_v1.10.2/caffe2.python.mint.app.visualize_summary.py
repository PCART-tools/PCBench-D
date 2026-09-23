def visualize_summary(filename):
    try:
        data = np.loadtxt(filename)
    except Exception as e:
        return 'Cannot load file {}: {}'.format(filename, str(e))
    chart_name = os.path.splitext(os.path.basename(filename))[0]
    chart = nvd3.lineChart(
        name=chart_name + '_summary_chart',
        height=args.chart_height,
        y_axis_format='.03g'
    )
    if args.sample < 0:
        step = max(data.shape[0] / -args.sample, 1)
    else:
        step = args.sample
    xdata = np.arange(0, data.shape[0], step)
    # data should have 4 dimensions.
    chart.add_serie(x=xdata, y=data[xdata, 0], name='min')
    chart.add_serie(x=xdata, y=data[xdata, 1], name='max')
    chart.add_serie(x=xdata, y=data[xdata, 2], name='mean')
    chart.add_serie(x=xdata, y=data[xdata, 2] + data[xdata, 3], name='m+std')
    chart.add_serie(x=xdata, y=data[xdata, 2] - data[xdata, 3], name='m-std')
    return jsonify_nvd3(chart)

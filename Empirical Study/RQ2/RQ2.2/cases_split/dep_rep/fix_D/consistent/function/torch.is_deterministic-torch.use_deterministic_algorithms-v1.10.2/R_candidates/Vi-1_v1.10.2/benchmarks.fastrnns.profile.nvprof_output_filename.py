def nvprof_output_filename(rnns, **params):
    rnn_tag = '-'.join(rnns)
    size_tag = describe_sizes(**params)
    date_tag = datetime.datetime.now().strftime("%m%d%y-%H%M")
    return '{}prof_{}_{}_{}.nvvp'.format(OUTPUT_DIR, rnn_tag,
                                         size_tag, date_tag)

def initOpts(opts):

    workspace.GlobalInit(
        ['caffe2', '--caffe2_log_level=2', '--caffe2_gpu_memory_tracking=0'])

    assert (opts['distributed']['num_gpus'] > 0 or
            opts['distributed']['num_cpus'] > 0),\
        "Need to specify num_gpus or num_cpus to decide which device to use."

    trainWithCPU = (opts['distributed']['num_gpus'] == 0)
    num_xpus = opts['distributed']['num_cpus'] if \
        trainWithCPU else opts['distributed']['num_gpus']
    first_xpu = opts['distributed']['first_cpu_id'] if \
        trainWithCPU else opts['distributed']['first_gpu_id']
    opts['distributed']['device'] = 'cpu' if trainWithCPU else 'gpu'

    opts['model_param']['combine_spatial_bn'] =\
        trainWithCPU and opts['model_param']['combine_spatial_bn']

    opts['distributed']['num_xpus'] = num_xpus
    opts['distributed']['first_xpu_id'] = first_xpu
    opts['temp_var'] = {}
    opts['temp_var']['metrics_output'] = {}

    return opts

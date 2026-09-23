def benchmark_caffe2_model(init_net, predict_net, warmup_iters=3, main_iters=10, layer_details=True):
    '''
        Run the benchmark net on the target model.
        Return the execution time per iteration (millisecond).
    '''
    ws = Workspace()
    if init_net:
        ws.RunNetOnce(init_net)
    ws.CreateNet(predict_net)
    results = ws.BenchmarkNet(predict_net.name, warmup_iters, main_iters, layer_details)
    del ws
    return results[0]

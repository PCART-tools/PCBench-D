def DataPipeToQueuesLoop(source_datapipe, req_queue, res_queue):
    if isinstance(source_datapipe, IterDataPipe):
        pipe_type = communication.iter
        protocol_type = communication.protocol.IterDataPipeQueueProtocolServer
    else:
        raise Exception('Only supports IterDataPipe, got', source_datapipe)
        # pipe_type = communication.map
        # protocol_type = communication.protocol.MapDataPipeQueueProtocolServer

    torch.set_num_threads(1)
    for _ in pipe_type.DataPipeBehindQueues(source_datapipe, protocol_type(req_queue, res_queue), blocking_request_get=True):
        pass

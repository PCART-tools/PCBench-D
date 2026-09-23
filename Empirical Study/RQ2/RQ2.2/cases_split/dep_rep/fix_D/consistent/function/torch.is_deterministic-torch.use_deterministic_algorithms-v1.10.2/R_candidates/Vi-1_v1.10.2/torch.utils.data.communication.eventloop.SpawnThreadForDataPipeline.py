def SpawnThreadForDataPipeline(datapipe):
    req_queue = communication.queue.ThreadingQueue()
    res_queue = communication.queue.ThreadingQueue()

    try:
        new_datapipe = pickle.loads(pickle.dumps(datapipe))
    except Exception as e:
        raise Exception('Unable to pickle DataPipe to make thread local copy', e)

    process = threading.Thread(target=DataPipeToQueuesLoop, args=(
        new_datapipe, req_queue, res_queue), daemon=True)
    return process, req_queue, res_queue, new_datapipe

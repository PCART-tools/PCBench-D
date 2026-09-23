def DataPipeBehindQueues(source_datapipe, protocol, full_stop=False, blocking_request_get=False):
    """
        Indefinitely iterates over req_queue and passing values from source_datapipe to res_queue
        If raise_stop is true, raises exception when StopIteration received from the source_datapipe
    """
    if not isinstance(protocol, communication.protocol.MapDataPipeQueueProtocolServer):
        raise Exception('Expecting MapDataPipeQueueProtocolServer, got', protocol)
    source_datapipe = EnsureNonBlockingMapDataPipe(source_datapipe)
    forever = True
    while forever:
        try:
            # Non-blocking call is Extremely slow here for python.mp, need to figure out a good workaround
            request = protocol.get_new_request(block=blocking_request_get)
        except communication.protocol.EmptyQueue:
            yield True
            continue

        if isinstance(request, communication.messages.TerminateRequest):
            forever = False
            protocol.response_terminate()

        elif isinstance(request, communication.messages.LenRequest):
            size = source_datapipe.nonblocking_len()
            protocol.response_len(size)

        elif isinstance(request, communication.messages.GetItemRequest):
            while forever:
                try:
                    value = source_datapipe.nonblocking_getitem(request.key)
                except NotAvailable:
                    yield True
                    continue
                except IndexError as e:
                    # Alternatively, we can just allow the underlying DataPipe to throw an exception?
                    protocol.response_index_out_of_bound()
                    if full_stop:
                        forever = False
                    else:
                        yield True
                    break
                protocol.response_item(request.key, value)
                yield True  # Returns control
                break
        else:
            raise Exception('Unrecognized type of request received', request)

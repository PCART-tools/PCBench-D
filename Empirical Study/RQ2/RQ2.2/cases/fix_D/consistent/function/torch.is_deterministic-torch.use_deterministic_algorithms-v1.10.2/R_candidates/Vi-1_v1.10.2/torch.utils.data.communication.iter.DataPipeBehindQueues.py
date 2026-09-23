def DataPipeBehindQueues(source_datapipe, protocol, full_stop=False, blocking_request_get=False):
    """
        Indefinitely iterates over req_queue and passing values from source_datapipe to res_queue
        If raise_stop is true, raises exception when StopIteration received from the source_datapipe
    """
    if not isinstance(protocol, communication.protocol.IterDataPipeQueueProtocolServer):
        raise Exception('Expecting IterDataPipeQueueProtocolServer, got', protocol)
    source_datapipe = EnsureNonBlockingDataPipe(source_datapipe)
    forever = True
    while forever:

        try:
            # Non-blocking call is Extremely slow here for python.mp, need to figureout good workaround
            request = protocol.get_new_request(block=blocking_request_get)
        except communication.protocol.EmptyQueue:
            yield True
            continue

        if isinstance(request, communication.messages.ResetIteratorRequest):
            source_datapipe.reset_iterator()
            protocol.response_reset()

        elif isinstance(request, communication.messages.TerminateRequest):
            forever = False
            protocol.response_terminate()

        elif isinstance(request, communication.messages.GetNextRequest):
            while forever:
                try:
                    value = source_datapipe.nonblocking_next()
                except NotAvailable:
                    yield True
                    continue
                except StopIteration:
                    protocol.response_stop()
                    if full_stop:
                        forever = False
                    else:
                        yield True
                    break
                except InvalidStateResetRequired:
                    protocol.response_invalid()
                    if full_stop:
                        forever = False
                    else:
                        yield True
                    break
                protocol.response_next(value)
                yield True  # Returns control
                break
        else:
            raise Exception('Unrecognized type of request received', request)

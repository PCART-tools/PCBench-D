def retrieve_step_blobs(net, prefix='rnn'):
    '''
    Retrieves blobs from step workspaces (which contain intermediate recurrent
    network computation for each timestep) and puts them in the global
    workspace. This allows access to the contents of this intermediate
    computation in python. Returns the list of extracted blob names.

    net: the net from which the step workspace blobs should be extracted

    prefix: prefix to append to extracted blob names when placing them in the
    global workspace
    '''
    count = 1
    output_list = []
    for op in net.Proto().op:
        if op.type == "RecurrentNetwork":
            blob_name = prefix + "_" + str(count)
            count = count + 1
            scratch_workspaces_blob_name = op.output[-1]
            workspace.RunOperatorOnce(
                core.CreateOperator(
                    "RecurrentNetworkBlobFetcher",
                    [scratch_workspaces_blob_name],
                    [blob_name],
                    prefix=prefix
                )
            )
            output_list += workspace.FetchBlob(blob_name).tolist()
    return output_list

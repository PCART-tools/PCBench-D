def InitFromLSTMParams(lstm_pblobs, param_values):
    '''
    Set the parameters of LSTM based on predefined values
    '''
    weight_params = GetLSTMParamNames()['weights']
    bias_params = GetLSTMParamNames()['biases']
    for input_type in viewkeys(param_values):
        weight_values = [
            param_values[input_type][w].flatten()
            for w in weight_params
        ]
        wmat = np.array([])
        for w in weight_values:
            wmat = np.append(wmat, w)
        bias_values = [
            param_values[input_type][b].flatten()
            for b in bias_params
        ]
        bm = np.array([])
        for b in bias_values:
            bm = np.append(bm, b)

        weights_blob = lstm_pblobs[input_type]['weights']
        bias_blob = lstm_pblobs[input_type]['biases']
        cur_weight = workspace.FetchBlob(weights_blob)
        cur_biases = workspace.FetchBlob(bias_blob)

        workspace.FeedBlob(
            weights_blob,
            wmat.reshape(cur_weight.shape).astype(np.float32))
        workspace.FeedBlob(
            bias_blob,
            bm.reshape(cur_biases.shape).astype(np.float32))

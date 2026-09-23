def prepare_prediction_net(filename, db_type, device_option=None):
    '''
    Helper function which loads all required blobs from the db
    and returns prediction net ready to be used
    '''
    metanet_def = load_from_db(filename, db_type, device_option)

    global_init_net = utils.GetNet(
        metanet_def, predictor_constants.GLOBAL_INIT_NET_TYPE)
    workspace.RunNetOnce(global_init_net)

    predict_init_net = utils.GetNet(
        metanet_def, predictor_constants.PREDICT_INIT_NET_TYPE)
    workspace.RunNetOnce(predict_init_net)

    predict_net = core.Net(
        utils.GetNet(metanet_def, predictor_constants.PREDICT_NET_TYPE))
    workspace.CreateNet(predict_net)

    return predict_net

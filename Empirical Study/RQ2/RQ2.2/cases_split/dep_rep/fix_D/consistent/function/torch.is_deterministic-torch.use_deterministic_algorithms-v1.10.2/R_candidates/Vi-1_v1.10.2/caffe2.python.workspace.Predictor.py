def Predictor(init_net, predict_net):
    return C.Predictor(StringifyProto(init_net), StringifyProto(predict_net))

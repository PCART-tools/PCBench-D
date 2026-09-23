def get_fc_predictor_version(fc_version):
    assert fc_version in ["fp32"], (
        "Only support fp32 for the fully connected layer "
        "in the predictor net, the provided FC precision is {}".format(fc_version)
    )
    return fc_version

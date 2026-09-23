@pytest.fixture(scope='class')
def modeldef(request, net_name, executor, fuser):
    set_fuser(fuser, executor)

    # Given a 'net_name' provided by generate_tests, build the thing
    name, rnn_creator, context = get_nn_runners(net_name)[0]
    creator_args = creator_args = {
        'seqLength': 100, 'numLayers': 1,
        'inputSize': 512, 'hiddenSize': 512,
        'miniBatch': 64, 'device': 'cuda', 'seed': None
    }
    return rnn_creator(**creator_args)

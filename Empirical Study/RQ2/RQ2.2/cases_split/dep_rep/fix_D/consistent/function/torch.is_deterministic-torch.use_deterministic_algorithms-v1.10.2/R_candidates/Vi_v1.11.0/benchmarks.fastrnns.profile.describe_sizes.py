def describe_sizes(**sizes):
    # seqLength, numLayers, inputSize, hiddenSize, miniBatch
    return 's{}-l{}-i{}-h{}-b{}'.format(
        sizes['seqLength'],
        sizes['numLayers'],
        sizes['inputSize'],
        sizes['hiddenSize'],
        sizes['miniBatch'],
    )

def main():
    random.seed(31415)
    parser = argparse.ArgumentParser(
        description='Caffe2: Seq2Seq Training'
    )
    parser.add_argument('--source-corpus', type=str, default=None,
                        help='Path to source corpus in a text file format. Each '
                        'line in the file should contain a single sentence',
                        required=True)
    parser.add_argument('--target-corpus', type=str, default=None,
                        help='Path to target corpus in a text file format',
                        required=True)
    parser.add_argument('--max-length', type=int, default=None,
                        help='Maximal lengths of train and eval sentences')
    parser.add_argument('--unk-threshold', type=int, default=50,
                        help='Threshold frequency under which token becomes '
                        'labeled unknown token')

    parser.add_argument('--batch-size', type=int, default=32,
                        help='Training batch size')
    parser.add_argument('--epochs', type=int, default=10,
                        help='Number of iterations over training data')
    parser.add_argument('--learning-rate', type=float, default=0.5,
                        help='Learning rate')
    parser.add_argument('--max-gradient-norm', type=float, default=1.0,
                        help='Max global norm of gradients at the end of each '
                        'backward pass. We do clipping to match the number.')
    parser.add_argument('--num-gpus', type=int, default=0,
                        help='Number of GPUs for data parallel model')

    parser.add_argument('--use-bidirectional-encoder', action='store_true',
                        help='Set flag to use bidirectional recurrent network '
                        'for first layer of encoder')
    parser.add_argument('--use-attention', action='store_true',
                        help='Set flag to use seq2seq with attention model')
    parser.add_argument('--source-corpus-eval', type=str, default=None,
                        help='Path to source corpus for evaluation in a text '
                        'file format', required=True)
    parser.add_argument('--target-corpus-eval', type=str, default=None,
                        help='Path to target corpus for evaluation in a text '
                        'file format', required=True)
    parser.add_argument('--encoder-cell-num-units', type=int, default=512,
                        help='Number of cell units per encoder layer')
    parser.add_argument('--encoder-num-layers', type=int, default=2,
                        help='Number encoder layers')
    parser.add_argument('--decoder-cell-num-units', type=int, default=512,
                        help='Number of cell units in the decoder layer')
    parser.add_argument('--decoder-num-layers', type=int, default=2,
                        help='Number decoder layers')
    parser.add_argument('--encoder-embedding-size', type=int, default=256,
                        help='Size of embedding in the encoder layer')
    parser.add_argument('--decoder-embedding-size', type=int, default=512,
                        help='Size of embedding in the decoder layer')
    parser.add_argument('--decoder-softmax-size', type=int, default=None,
                        help='Size of softmax layer in the decoder')

    parser.add_argument('--checkpoint', type=str, default=None,
                        help='Path to checkpoint')

    args = parser.parse_args()

    encoder_layer_configs = [
        dict(
            num_units=args.encoder_cell_num_units,
        ),
    ] * args.encoder_num_layers

    if args.use_bidirectional_encoder:
        assert args.encoder_cell_num_units % 2 == 0
        encoder_layer_configs[0]['num_units'] /= 2

    decoder_layer_configs = [
        dict(
            num_units=args.decoder_cell_num_units,
        ),
    ] * args.decoder_num_layers

    run_seq2seq_model(args, model_params=dict(
        attention=('regular' if args.use_attention else 'none'),
        decoder_layer_configs=decoder_layer_configs,
        encoder_type=dict(
            encoder_layer_configs=encoder_layer_configs,
            use_bidirectional_encoder=args.use_bidirectional_encoder,
        ),
        batch_size=args.batch_size,
        optimizer_params=dict(
            learning_rate=args.learning_rate,
        ),
        encoder_embedding_size=args.encoder_embedding_size,
        decoder_embedding_size=args.decoder_embedding_size,
        decoder_softmax_size=args.decoder_softmax_size,
        max_gradient_norm=args.max_gradient_norm,
    ))

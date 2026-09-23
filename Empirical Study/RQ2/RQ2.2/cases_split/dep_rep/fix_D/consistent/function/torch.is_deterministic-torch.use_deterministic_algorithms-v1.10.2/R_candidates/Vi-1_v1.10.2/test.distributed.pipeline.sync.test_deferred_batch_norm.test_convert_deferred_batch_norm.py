def test_convert_deferred_batch_norm():
    bn = nn.BatchNorm2d(3, track_running_stats=False)
    bn = DeferredBatchNorm.convert_deferred_batch_norm(bn, chunks=CHUNKS)
    assert type(bn) is nn.BatchNorm2d  # because of track_running_stats=False

    dbn = DeferredBatchNorm(3, chunks=CHUNKS)
    dbn_again = DeferredBatchNorm.convert_deferred_batch_norm(dbn, chunks=CHUNKS)
    assert dbn is dbn_again

    dbn_again = DeferredBatchNorm.convert_deferred_batch_norm(dbn, chunks=CHUNKS + 1)
    assert dbn is not dbn_again  # because of different chunks

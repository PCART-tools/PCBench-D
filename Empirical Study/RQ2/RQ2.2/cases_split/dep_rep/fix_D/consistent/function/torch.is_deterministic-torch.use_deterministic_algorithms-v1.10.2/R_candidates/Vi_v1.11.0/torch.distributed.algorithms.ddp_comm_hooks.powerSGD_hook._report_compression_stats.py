def _report_compression_stats(bucket, state):
    """
    Report compression stats at the frequency of `compression_stats_logging_frequency` specified in PowerSGD state.
    """
    if (
        bucket.is_last()
        and state.iter >= state.next_stats_report
    ):
        stats = state.compression_stats()
        logging.info(
            "Compression stats: iter {}, total before compression {}, total after compression {}, "
            "rate {}".format(state.iter, stats[1], stats[2], stats[0])
        )
        state.next_stats_report = state.iter + state.compression_stats_logging_frequency

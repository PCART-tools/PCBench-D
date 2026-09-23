def get_shard_based_on_S3(which_shard: int, num_shards: int, tests: List[str], test_times_file: str) -> List[str]:
    """Get sharded test allocation based on historic S3 data.
    """
    jobs_to_times = _query_past_job_times(test_times_file)

    # Got no stats from S3, returning early to save runtime
    if len(jobs_to_times) == 0:
        print('Gathered no stats from S3. Proceeding with default sharding plan.')
        return tests[which_shard - 1 :: num_shards]

    shards = calculate_shards(num_shards, tests, jobs_to_times)
    _, tests_from_shard = shards[which_shard - 1]
    return tests_from_shard

def _parse_master_summaries(summaries: Any, jobs: List[str]) -> Dict[str, List[Report]]:
    summary_dict = defaultdict(list)
    for summary in summaries:
        # master summary format: "test_time/{sha}/{job}/file"
        summary_job = summary.key.split('/')[2]
        if summary_job in jobs or len(jobs) == 0:
            binary = summary.get()["Body"].read()
            string = bz2.decompress(binary).decode("utf-8")
            summary_dict[summary_job].append(json.loads(string))
    return summary_dict

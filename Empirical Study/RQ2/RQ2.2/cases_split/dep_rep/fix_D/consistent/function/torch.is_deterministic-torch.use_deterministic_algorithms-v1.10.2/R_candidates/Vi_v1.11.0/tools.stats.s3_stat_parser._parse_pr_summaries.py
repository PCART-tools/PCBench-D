def _parse_pr_summaries(summaries: Any, job_prefix: str) -> Dict[str, List[Tuple[Report, str]]]:
    summary_dict = defaultdict(list)
    for summary in summaries:
        # PR summary format: "pr_test_time/{pr}/{sha}/{job}/file"
        summary_job = summary.key.split('/')[3]
        summary_timestamp = summary.key.split('/')[4][:len("YYYY-MM-ddTHH:mm:ss")]
        if not job_prefix or len(job_prefix) == 0 or summary_job.startswith(job_prefix):
            binary = summary.get()["Body"].read()
            string = bz2.decompress(binary).decode("utf-8")
            summary_dict[summary_job].append((json.loads(string), summary_timestamp))
    return summary_dict

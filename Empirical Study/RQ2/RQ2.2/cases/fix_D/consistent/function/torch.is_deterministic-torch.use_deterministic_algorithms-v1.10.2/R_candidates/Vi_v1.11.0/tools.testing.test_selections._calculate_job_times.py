def _calculate_job_times(reports: List["Report"]) -> Dict[str, float]:
    """Compute test runtime by filename: ("test_file_name" -> (current_avg, # values))
    """
    jobs_to_times: Dict[str, Tuple[float, int]] = dict()
    for report in reports:
        v_report = cast(Version2Report, report)
        assert 'format_version' in v_report.keys() and v_report.get('format_version') == 2, \
            "S3 format currently handled is version 2 only"
        files: Dict[str, Any] = v_report['files']
        for name, test_file in files.items():
            if name not in jobs_to_times:
                jobs_to_times[name] = (test_file['total_seconds'], 1)
            else:
                curr_avg, curr_count = jobs_to_times[name]
                new_count = curr_count + 1
                new_avg = (curr_avg * curr_count + test_file['total_seconds']) / new_count
                jobs_to_times[name] = (new_avg, new_count)

    return {job: time for job, (time, _) in jobs_to_times.items()}

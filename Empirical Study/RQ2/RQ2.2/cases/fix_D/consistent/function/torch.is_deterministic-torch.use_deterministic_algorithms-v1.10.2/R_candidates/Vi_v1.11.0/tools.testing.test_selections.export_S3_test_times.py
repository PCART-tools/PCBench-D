def export_S3_test_times(test_times_filename: Optional[str] = None) -> Dict[str, float]:
    test_times: Dict[str, float] = _pull_job_times_from_S3()
    if test_times_filename is not None:
        print(f'Exporting S3 test stats to {test_times_filename}.')
        if os.path.exists(test_times_filename):
            print(f'Overwriting existent file: {test_times_filename}')
        with open(test_times_filename, 'w+') as file:
            job_times_json = _get_job_times_json(test_times)
            json.dump(job_times_json, file, indent='    ', separators=(',', ': '))
            file.write('\n')
    return test_times

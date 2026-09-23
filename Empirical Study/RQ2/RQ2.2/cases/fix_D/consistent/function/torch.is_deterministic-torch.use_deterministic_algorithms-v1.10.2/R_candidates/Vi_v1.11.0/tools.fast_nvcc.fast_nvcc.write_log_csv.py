def write_log_csv(
    command_parts: List[List[str]],
    command_results: List[Result],
    *,
    filename: str,
) -> None:
    """
    Write a CSV file of the times and /tmp file sizes from each command.
    """
    tmp_files: List[str] = []
    for result in command_results:
        tmp_files.extend(result.get('files', {}).keys())
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['command', 'seconds'] + list(dict.fromkeys(tmp_files))
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i, result in enumerate(command_results):
            command = f'{i} {os.path.basename(command_parts[i][0])}'
            row = {'command': command, 'seconds': result.get('time', 0)}
            writer.writerow({**row, **result.get('files', {})})

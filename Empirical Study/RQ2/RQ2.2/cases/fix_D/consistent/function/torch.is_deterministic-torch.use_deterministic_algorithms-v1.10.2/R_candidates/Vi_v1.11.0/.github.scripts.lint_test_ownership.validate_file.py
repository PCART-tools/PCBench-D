def validate_file(filename: Path, pytorch_labels: List[str]) -> str:
    prefix = "# Owner(s): "
    relative_name = Path(filename).relative_to(PYTORCH_ROOT)
    with open(filename) as f:
        for line in f.readlines():
            if line.startswith(prefix):
                labels = json.loads(line[len(prefix):])
                labels_msgs = [validate_label(label, pytorch_labels) for label in labels]
                file_msg = ", ".join([x for x in labels_msgs if x != ""])
                return f"{relative_name}: {file_msg}" if file_msg != "" else ""
    return f"{relative_name}: missing a comment header with ownership information."

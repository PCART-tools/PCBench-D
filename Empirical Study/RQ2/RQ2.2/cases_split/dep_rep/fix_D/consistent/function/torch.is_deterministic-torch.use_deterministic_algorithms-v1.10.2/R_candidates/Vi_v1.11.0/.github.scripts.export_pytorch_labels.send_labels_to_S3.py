def send_labels_to_S3(labels: List[str]) -> None:
    labels_file_name = "pytorch_labels.json"
    obj = boto3.resource('s3').Object('ossci-metrics', labels_file_name)
    obj.put(Body=json.dumps(labels).encode())

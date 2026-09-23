def get_pytorch_labels() -> Any:
    bucket = S3_RESOURCE_READ_ONLY.Bucket("ossci-metrics")
    summaries = bucket.objects.filter(Prefix="pytorch_labels.json")
    for summary in summaries:
        labels = summary.get()["Body"].read()
    return json.loads(labels)

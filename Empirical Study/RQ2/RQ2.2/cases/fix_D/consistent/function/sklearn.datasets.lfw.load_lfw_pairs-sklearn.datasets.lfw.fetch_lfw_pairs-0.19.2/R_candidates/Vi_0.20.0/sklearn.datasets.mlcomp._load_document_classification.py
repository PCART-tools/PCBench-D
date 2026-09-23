def _load_document_classification(dataset_path, metadata, set_=None, **kwargs):
    if set_ is not None:
        dataset_path = os.path.join(dataset_path, set_)
    return load_files(dataset_path, metadata.get('description'), **kwargs)

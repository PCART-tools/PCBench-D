def dict_to_features(dct):
    return Features(
        title=dct['title'],
        body=dct['body'],
        pr_number=dct['pr_number'],
        files_changed=dct['files_changed'],
        labels=dct['labels'])

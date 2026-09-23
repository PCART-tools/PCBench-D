def make_test_data_loader(raw_data_file_path, processed_data_file):
    """Function to create dataset and dataloaders for the test dataset.
    Rewritten simpler version of ```make_criteo_and_loaders()``` from the dlrm_data_pytorch.py
    that makes the test dataset and dataloaders only for the ***kaggle criteo dataset***
    """
    test_data = CriteoDataset(
        "kaggle",
        -1,
        0.0,
        "total",
        "test",
        raw_data_file_path,
        processed_data_file,
        False,
        False,
    )
    test_loader = torch.utils.data.DataLoader(
        test_data,
        batch_size=16384,
        shuffle=False,
        num_workers=7,
        collate_fn=collate_wrapper_criteo_offset,
        pin_memory=False,
        drop_last=False,
    )
    return test_loader

def evaluate_metrics(test_dataloader, sparse_model_metadata):
    """Evaluates the metrics the sparsified metrics for the dlrm model on various sparsity levels,
    block shapes and norms. This function evaluates the model on the test dataset and dumps
    evaluation metrics in a csv file [model_performance.csv]
    """
    metadata = pd.read_csv(sparse_model_metadata)
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

    metrics_dict: dict[str, list] = {
        "norm": [],
        "sparse_block_shape": [],
        "sparsity_level": [],
        "precision": [],
        "recall": [],
        "f1": [],
        "roc_auc": [],
        "accuracy": [],
        "log_loss": [],
    }

    for _, row in metadata.iterrows():
        norm, sbs, sl = row["norm"], row["sparse_block_shape"], row["sparsity_level"]
        model_path = row["path"]
        model = fetch_model(model_path, device)

        model_metrics = inference_and_evaluation(model, test_dataloader, device)
        key = f"{norm}_{sbs}_{sl}"
        print(key, "=", model_metrics)

        metrics_dict["norm"].append(norm)
        metrics_dict["sparse_block_shape"].append(sbs)
        metrics_dict["sparsity_level"].append(sl)

        for key, value in model_metrics.items():
            if key in metrics_dict:
                metrics_dict[key].append(value)

    sparse_model_metrics = pd.DataFrame(metrics_dict)
    print(sparse_model_metrics)

    filename = "sparse_model_metrics.csv"
    sparse_model_metrics.to_csv(filename, index=False)
    print(f"Model metrics file saved to {filename}")

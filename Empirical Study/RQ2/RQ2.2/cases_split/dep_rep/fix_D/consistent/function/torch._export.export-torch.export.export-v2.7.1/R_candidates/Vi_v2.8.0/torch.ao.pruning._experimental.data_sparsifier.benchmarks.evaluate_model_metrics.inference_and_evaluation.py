def inference_and_evaluation(dlrm, test_dataloader, device):
    """Perform inference and evaluation on the test dataset.
    The function returns the dictionary that contains evaluation metrics such as accuracy, f1, auc,
    precision, recall.
    Note: This function is a rewritten version of ```inference()``` present in dlrm_s_pytorch.py

    Args:
        dlrm (nn.Module)
            dlrm model object
        test_data_loader (torch dataloader):
            dataloader for the test dataset
        device (torch.device)
            device on which the inference happens
    """
    nbatches = len(test_dataloader)
    scores = []
    targets = []

    for i, testBatch in enumerate(test_dataloader):
        # early exit if nbatches was set by the user and was exceeded
        if nbatches > 0 and i >= nbatches:
            break

        X_test, lS_o_test, lS_i_test, T_test, _, _ = unpack_batch(testBatch)
        # forward pass
        X_test, lS_o_test, lS_i_test = dlrm_wrap(
            X_test, lS_o_test, lS_i_test, device, ndevices=1
        )

        Z_test = dlrm(X_test, lS_o_test, lS_i_test)
        S_test = Z_test.detach().cpu().numpy()  # numpy array
        T_test = T_test.detach().cpu().numpy()  # numpy array
        scores.append(S_test)
        targets.append(T_test)

    scores = np.concatenate(scores, axis=0)
    targets = np.concatenate(targets, axis=0)
    metrics = {
        "recall": lambda y_true, y_score: sklearn.metrics.recall_score(
            y_true=y_true, y_pred=np.round(y_score)
        ),
        "precision": lambda y_true, y_score: sklearn.metrics.precision_score(
            y_true=y_true, y_pred=np.round(y_score)
        ),
        "f1": lambda y_true, y_score: sklearn.metrics.f1_score(
            y_true=y_true, y_pred=np.round(y_score)
        ),
        "ap": sklearn.metrics.average_precision_score,
        "roc_auc": sklearn.metrics.roc_auc_score,
        "accuracy": lambda y_true, y_score: sklearn.metrics.accuracy_score(
            y_true=y_true, y_pred=np.round(y_score)
        ),
        "log_loss": lambda y_true, y_score: sklearn.metrics.log_loss(
            y_true=y_true, y_pred=y_score
        ),
    }

    all_metrics = {}
    for metric_name, metric_function in metrics.items():
        all_metrics[metric_name] = round(metric_function(targets, scores), 3)

    return all_metrics

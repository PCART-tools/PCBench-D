def get_simple_regression(device: torch.device) -> GetterReturnType:
    N = 10
    K = 10

    loc_beta = 0.
    scale_beta = 1.

    beta_prior = dist.Normal(loc_beta, scale_beta)

    X = torch.rand(N, K + 1, device=device)
    Y = torch.rand(N, 1, device=device)

    # X.shape: (N, K + 1), Y.shape: (N, 1), beta_value.shape: (K + 1, 1)
    beta_value = beta_prior.sample((K + 1, 1))
    beta_value.requires_grad_(True)

    def forward(beta_value: Tensor) -> Tensor:
        mu = X.mm(beta_value)

        # We need to compute the first and second gradient of this score with respect
        # to beta_value. We disable Bernoulli validation because Y is a relaxed value.
        score = (dist.Bernoulli(logits=mu, validate_args=False).log_prob(Y).sum() +
                 beta_prior.log_prob(beta_value).sum())
        return score

    return forward, (beta_value.to(device),)

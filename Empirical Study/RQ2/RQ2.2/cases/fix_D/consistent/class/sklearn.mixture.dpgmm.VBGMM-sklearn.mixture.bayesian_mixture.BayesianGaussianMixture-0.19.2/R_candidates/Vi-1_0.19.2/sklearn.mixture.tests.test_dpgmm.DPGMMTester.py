class DPGMMTester(GMMTester):
    model = DPGMM
    do_test_eval = False

    def score(self, g, train_obs):
        _, z = g.score_samples(train_obs)
        return g.lower_bound(train_obs, z)

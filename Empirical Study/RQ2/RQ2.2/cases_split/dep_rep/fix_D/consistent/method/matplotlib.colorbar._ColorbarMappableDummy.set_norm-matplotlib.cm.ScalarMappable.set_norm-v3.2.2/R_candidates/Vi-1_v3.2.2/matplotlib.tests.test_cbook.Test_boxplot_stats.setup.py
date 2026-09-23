    def setup(self):
        np.random.seed(937)
        self.nrows = 37
        self.ncols = 4
        self.data = np.random.lognormal(size=(self.nrows, self.ncols),
                                        mean=1.5, sigma=1.75)
        self.known_keys = sorted([
            'mean', 'med', 'q1', 'q3', 'iqr',
            'cilo', 'cihi', 'whislo', 'whishi',
            'fliers', 'label'
        ])
        self.std_results = cbook.boxplot_stats(self.data)

        self.known_nonbootstrapped_res = {
            'cihi': 6.8161283264444847,
            'cilo': -0.1489815330368689,
            'iqr': 13.492709959447094,
            'mean': 13.00447442387868,
            'med': 3.3335733967038079,
            'fliers': np.array([
                92.55467075,  87.03819018,  42.23204914,  39.29390996
            ]),
            'q1': 1.3597529879465153,
            'q3': 14.85246294739361,
            'whishi': 27.899688243699629,
            'whislo': 0.042143774965502923
        }

        self.known_bootstrapped_ci = {
            'cihi': 8.939577523357828,
            'cilo': 1.8692703958676578,
        }

        self.known_whis3_res = {
            'whishi': 42.232049135969874,
            'whislo': 0.042143774965502923,
            'fliers': np.array([92.55467075, 87.03819018]),
        }

        self.known_res_percentiles = {
            'whislo':   0.1933685896907924,
            'whishi':  42.232049135969874
        }

        self.known_res_range = {
            'whislo': 0.042143774965502923,
            'whishi': 92.554670752188699

        }

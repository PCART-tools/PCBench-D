def test_wilcoxon_result_attributes():
    x = np.array([120, 114, 181, 188, 180, 146, 121, 191, 132, 113, 127, 112])
    y = np.array([133, 143, 119, 189, 112, 199, 198, 113, 115, 121, 142, 187])
    res = stats.wilcoxon(x, y, correction=False)
    attributes = ('statistic', 'pvalue')
    check_named_results(res, attributes)

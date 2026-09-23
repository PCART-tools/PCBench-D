def compare_results(res,desired):
    for i in range(len(desired)):
        assert_array_equal(res[i],desired[i])

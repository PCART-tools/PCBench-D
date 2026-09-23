def test_pointbiserial():
    # same as mstats test except for the nan
    # Test data: http://support.sas.com/ctx/samples/index.jsp?sid=490&tab=output
    x = [1,0,1,1,1,1,0,1,0,0,0,1,1,0,0,0,1,1,1,0,0,0,0,0,0,0,0,1,0,
         0,0,0,0,1]
    y = [14.8,13.8,12.4,10.1,7.1,6.1,5.8,4.6,4.3,3.5,3.3,3.2,3.0,
         2.8,2.8,2.5,2.4,2.3,2.1,1.7,1.7,1.5,1.3,1.3,1.2,1.2,1.1,
         0.8,0.7,0.6,0.5,0.2,0.2,0.1]
    assert_almost_equal(stats.pointbiserialr(x, y)[0], 0.36149, 5)

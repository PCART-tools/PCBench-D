@image_comparison(['date_empty.png'])
def test_date_empty():
    # make sure we do the right thing when told to plot dates even
    # if no date data has been presented, cf
    # http://sourceforge.net/tracker/?func=detail&aid=2850075&group_id=80706&atid=560720
    fig, ax = plt.subplots()
    ax.xaxis_date()

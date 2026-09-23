@image_comparison(['check_radio_buttons.png'], style='mpl20', remove_text=True)
def test_check_radio_buttons_image():
    # Remove this line when this test image is regenerated.
    plt.rcParams['text.kerning_factor'] = 6

    get_ax()
    plt.subplots_adjust(left=0.3)
    rax1 = plt.axes([0.05, 0.7, 0.15, 0.15])
    rax2 = plt.axes([0.05, 0.2, 0.15, 0.15])
    widgets.RadioButtons(rax1, ('Radio 1', 'Radio 2', 'Radio 3'))
    widgets.CheckButtons(rax2, ('Check 1', 'Check 2', 'Check 3'),
                         (False, True, True))

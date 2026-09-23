def update_counter_ref(prev_iter, update_counter, indices, curr_iter, counter_halflife):
    prev_iter_out = prev_iter.copy()
    update_counter_out = update_counter.copy()

    counter_neg_log_rho = np.log(2) / counter_halflife
    for i in indices:
        iter_diff = curr_iter[0] - prev_iter_out[i]
        prev_iter_out[i] = curr_iter[0]
        update_counter_out[i] = (
            1.0 + np.exp(-iter_diff * counter_neg_log_rho) * update_counter_out[i]
        )
    return prev_iter_out, update_counter_out

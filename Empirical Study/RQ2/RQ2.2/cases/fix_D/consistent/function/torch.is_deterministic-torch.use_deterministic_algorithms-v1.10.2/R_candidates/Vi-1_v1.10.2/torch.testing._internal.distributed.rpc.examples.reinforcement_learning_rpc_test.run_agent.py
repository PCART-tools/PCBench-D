def run_agent(agent, n_steps):
    for i_episode in count(1):
        agent.run_episode(n_steps=n_steps)
        last_reward = agent.finish_episode()

        if agent.running_reward > agent.reward_threshold:
            print("Solved! Running reward is now {}!".format(agent.running_reward))
            break

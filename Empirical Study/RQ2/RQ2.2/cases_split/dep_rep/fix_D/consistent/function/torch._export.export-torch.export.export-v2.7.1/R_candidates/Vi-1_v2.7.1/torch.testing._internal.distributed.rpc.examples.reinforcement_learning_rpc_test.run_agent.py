def run_agent(agent, n_steps):
    while True:
        agent.run_episode(n_steps=n_steps)
        agent.finish_episode()

        if agent.running_reward > agent.reward_threshold:
            print(f"Solved! Running reward is now {agent.running_reward}!")
            break

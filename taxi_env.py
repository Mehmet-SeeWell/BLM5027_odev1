import random as rnd
import numpy as np
from map_generator import Taximap
from taxi import Taxi

def train_taxi():
    episode_count = 100000
    max_step_count = 150
    rewards = []

    Taxi.initialize_environment(6, 6, 5, reset_q_table=True) ### Set the map
    print("Training Started!")
    for n in range(episode_count):
        terminated = False
        Taxi.random_start()

        for _ in range(max_step_count):
            terminated = Taxi.step()

            if terminated: ### Terminated
                break
        else:
            ... ### Truncated

        rewards.append(Taxi.reward)
        Taxi.epsilon = max(0.01, Taxi.epsilon * 0.99995) ### Epsilon decay

        if (n+1) % 1000 == 0: ### Report per 1000
            print(f"Episode {n+1} - Average Reward: {np.mean(rewards[-1000:]):.3f}, Epsilon value: {Taxi.epsilon:.3f}")

    print("Training Finished!")

def test_taxi():
    # Taxi.initialize_environment(6, 6, 5, reset_q_table=False) ### Set the map
    Taxi.random_start()
    Taximap.render_blank_map()
    Taxi.epsilon = 0 ### Using only exploited knowledge
    for _ in range(100):
        terminated = Taxi.step()
        # [print() for _ in range(25)]
        Taxi.render_map()
        input()
        if terminated:
            print("Testing successful!")
            break
    else:
        print("Testing failed")
        input()

train_taxi()
test_taxi()

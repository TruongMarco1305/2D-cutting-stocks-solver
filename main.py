# import gym_cutting_stock
# import gymnasium as gym
# from policy import GreedyPolicy, RandomPolicy
# from student_submissions.s2210xxx.policy2210xxx import Policy2210xxx
# import random
# import time

# # Create the environment
# env = gym.make(
#     "gym_cutting_stock/CuttingStock-v0",
#     render_mode="human",  # Comment this line to disable rendering
# )
# NUM_EPISODES = 100

# if __name__ == "__main__":
#     # Reset the environment
#     # observation, info = env, reset(seed=42)

#     # # Test GreedyPolicy
#     # gd_policy = GreedyPolicy()
#     # ep = 0
#     # while ep < NUM_EPISODES:
#     #     action = gd_policy, get_action(observation, info)
#     #     observation, reward, terminated, truncated, info = env, step(action)

#     #     if terminated or truncated:
#     #         observation, info = env, reset(seed=ep)
#     #         print(info)
#     #         ep += 1

#     # # Reset the environment
#     # observation, info = env, reset(seed=42)

#     # # Test RandomPolicy
#     # rd_policy = RandomPolicy()
#     # ep = 0
#     # while ep < NUM_EPISODES:
#     #     action = rd_policy, get_action(observation, info)
#     #     observation, reward, terminated, truncated, info = env, step(action)

#     #     if terminated or truncated:
#     #         observation, info = env, reset(seed=ep)
#     #         print(info)
#     #         ep += 1

#     # Uncomment the following code to test your policy
#     # Reset the environment
#     observation, info = env.reset(seed=42)
#     # Modify observation to a specific case

#     # num_products = 5
#     # observation["products"] = [
#     #     {"size": [1, 1], "quantity": 2},
#     #     {"size": [2, 2], "quantity": 2},
#     #     {"size": [3, 3], "quantity": 1},
#     # ]

#     # print("Products: ", observation["products"])
#     policy2210xxx = Policy2210xxx(policy_id=1)
#     list_products = observation["products"]
#     sumA = 0
#     # for prod in list_products:
#     #     sumA += prod["quantity"]
#     # print("Sum: ", sumA)
#     start_time = time.perf_counter()
#     for _ in range(300):
#         action = policy2210xxx.get_action(observation, info)
#         # for prod in observation["products"]:
#         #     if prod["size"] == action["size"] and prod["quantity"] > 0:
#         #         prod["quantity"] -= 1
#         #         break
#         # observations = observation
#         # print("Action: ", action)
#         observation, reward, terminated, truncated, info = env.step(action)
#         # observation = observations
#         # all_zero = all(prod["quantity"] == 0 for prod in observation["products"])
#         # if all_zero:
#         #     terminated = True
#         # print('Products: ', observation[])
#         print('Action: ', action)
#         # print("Observation: ", observation['products'])
#         # print("Terminated: ", terminated)
#         # print("Truncated: ", truncated)
#         if terminated:
#             print("Cutting Succesfully !")
#             end_time = time.perf_counter()
#             elapsed_time = end_time - start_time
#             print(info)
#             print(f"Elapsed time: {elapsed_time} seconds")
#             input("Press Enter to continue, , , ")
#             break

#         if terminated or truncated:
#             observation, info = env.reset()

# env.close()

import gym_cutting_stock
import gymnasium as gym
from policy import GreedyPolicy, RandomPolicy
from student_submissions.s2210xxx.policy2210xxx import Policy2210xxx

# Create the environment
env = gym.make(
    "gym_cutting_stock/CuttingStock-v0",
    render_mode="human",  # Comment this line to disable rendering
)
NUM_EPISODES = 10

if __name__ == "__main__":
    # Reset the environment
    # observation, info = env.reset(seed=42)

    # Test GreedyPolicy
    # gd_policy = GreedyPolicy()
    # ep = 0
    # while ep < NUM_EPISODES:
    #     action = gd_policy.get_action(observation, info)
    #     observation, reward, terminated, truncated, info = env.step(action)

    #     if terminated or truncated:
    #         print(info)
    #         observation, info = env.reset(seed=ep)
    #         ep += 1

    # Reset the environment
    observation, info = env.reset(seed=42)

    # Test RandomPolicy
    # policy2210xxx = Policy2210xxx(policy_id=1)
    # ep = 0
    # while ep < NUM_EPISODES:
    #     action = policy2210xxx.get_action(observation, info)
    #     observation, reward, terminated, truncated, info = env.step(action)
    #     print(action)

    #     if terminated or truncated:
    #         print(info)
    #         observation, info = env.reset(seed=ep)
    #         ep += 1

    # Uncomment the following code to test your policy
    # Reset the environment
    observation, info = env.reset(seed=42)
    print(info)

    policy2210xxx = Policy2210xxx(policy_id=1)
    for _ in range(200):
        action = policy2210xxx.get_action(observation, info)
        observation, reward, terminated, truncated, info = env.step(action)
        print(action)
        print('Terminated: ', terminated)
        print('Truncated: ', truncated)

        if terminated or truncated:
            print(info)
            break
            observation, info = env.reset()

env.close()
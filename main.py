import gym_cutting_stock
import gymnasium as gym
from policy import GreedyPolicy, RandomPolicy
from student_submissions.s2210xxx.policy2210xxx import Policy2210xxx
from test_case import test_cases
import numpy as np
import csv

# Create the environment
env = gym.make(
    "gym_cutting_stock/CuttingStock-v0",
    render_mode="human", 
)
NUM_EPISODES = 100

if __name__ == "__main__":
    results = [] 

    print(f"\nTotal number of test cases: {len(test_cases)}")
    
    for case_name, test_case in test_cases.items():
        print(f"\n{'='*50}")
        print(f"Running test case: {case_name}")
        print(f"Number of stocks in test case: {len(test_case['stocks'])}")
        print(f"First stock dimensions: {test_case['stocks'][0]}")
        print(f"Last stock dimensions: {test_case['stocks'][-1]}")
        print(f"Number of products: {len(test_case['products'])}")
        print(f"Products details: {test_case['products']}")

        observation, info = env.reset(
            options={
                "stocks": test_case["stocks"],
                "products": test_case["products"]
            }
        )

        # Test policies
        policies = {
            "Greedy": GreedyPolicy(),
            "Random": RandomPolicy(),
            # "Custom": Policy2210xxx(),
        }

        for policy_name, policy in policies.items():
            print(f"\nTesting policy: {policy_name}")
            ep = 0

            while ep < NUM_EPISODES:
                print(f"Start Episode {ep + 1}, Info: {info}")
                terminated, truncated = False, False

                while not (terminated or truncated):
                    action = policy.get_action(observation, info)
                    observation, reward, terminated, truncated, info = env.step(action)
                    print(f"Step Info: {info}")

                print(f"End Episode {ep + 1}, Final Info: {info}")
                ep += 1

            results.append({
                "test_case": case_name,
                "policy": policy_name,
                "total_reward": reward,  
                "average_filled_ratio": info.get("filled_ratio", 0),  
            })

    env.close()

    with open("policy_comparison_results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["test_case", "policy", "total_reward", "average_filled_ratio"])
        writer.writeheader()
        writer.writerows(results)

    print("\nSummary of Results:")
    for result in results:
        print(
            f"Test Case: {result['test_case']}, Policy: {result['policy']}, "
            f"Total Reward: {result['total_reward']}, Average Filled Ratio: {result['average_filled_ratio']:.2f}"
        )
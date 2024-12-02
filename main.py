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
NUM_EPISODES = 1

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
            # "Greedy": GreedyPolicy(),
            # "Random": RandomPolicy(),
            "Custom": Policy2210xxx(),
        }

        for policy_name, policy in policies.items():
            print(f"\nTesting policy: {policy_name}")
            ep = 0

            while ep < NUM_EPISODES:
                observation, info = env.reset(
                    options={
                        "stocks": test_case["stocks"],
                        "products": test_case["products"]
                    }
                )
                print(f"\nStart Episode {ep + 1}")
                print(f"Initial Info:")
                print(f"- Filled ratio: {info['filled_ratio']*100:.1f}%")
                print(f"- Total stock area: {int(info['total_stock_area'])}")
                print(f"- Used product area: {int(info['used_product_area'])}")

                terminated, truncated = False, False

                while not (terminated or truncated):
                    action = policy.get_action(observation, info)
                    observation, reward, terminated, truncated, info = env.step(action)
                    print(f"Step Info: Filled ratio = {info['filled_ratio']*100:.2f}%")

                print(f"\nEnd Episode {ep + 1}")
                print(f"Final Info:")
                print(f"- Filled ratio: {info['filled_ratio']*100:.1f}%")
                print(f"- Total stock area: {int(info['total_stock_area'])}")
                print(f"- Used product area: {int(info['used_product_area'])}")
                
                ep += 1

            results.append({
                "test_case": case_name,
                "policy": policy_name,
                "filled_ratio": info['filled_ratio'],
            })

    env.close()

    with open("policy_comparison_results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["test_case", "policy", "filled_ratio"])
        writer.writeheader()
        writer.writerows(results)

    print("\nSummary of Results:")
    for result in results:
        print(
            f"Test Case: {result['test_case']}, Policy: {result['policy']}, "
            f"Filled Ratio: {result['filled_ratio']*100:.2f}%"
        )
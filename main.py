import gym_cutting_stock
import gymnasium as gym
from policy import GreedyPolicy, RandomPolicy
from student_submissions.s2210xxx.policy2210xxx import Policy2210xxx
import random
import time

# Create the environment
env = gym.make(
    "gym_cutting_stock/CuttingStock-v0",
    render_mode="human",  # Comment this line to disable rendering
)
NUM_EPISODES = 100

if __name__ == "__main__":
    # Reset the environment
    # observation, info = env.reset(seed=42)

    # # Test GreedyPolicy
    # gd_policy = GreedyPolicy()
    # ep = 0
    # while ep < NUM_EPISODES:
    #     action = gd_policy.get_action(observation, info)
    #     observation, reward, terminated, truncated, info = env.step(action)

    #     if terminated or truncated:
    #         observation, info = env.reset(seed=ep)
    #         print(info)
    #         ep += 1

    # # Reset the environment
    # observation, info = env.reset(seed=42)

    # # Test RandomPolicy
    # rd_policy = RandomPolicy()
    # ep = 0
    # while ep < NUM_EPISODES:
    #     action = rd_policy.get_action(observation, info)
    #     observation, reward, terminated, truncated, info = env.step(action)

    #     if terminated or truncated:
    #         observation, info = env.reset(seed=ep)
    #         print(info)
    #         ep += 1

    # Uncomment the following code to test your policy
    # Reset the environment
    observation, info = env.reset(seed=42)
    # Modify observation to a specific case

    # num_products = 5
    # observation["products"] = [
    #     {"size": [1, 1], "quantity": 2},
    #     {"size": [2, 2], "quantity": 2},
    #     {"size": [3, 3], "quantity": 1},
    # ]

    print("Products: ", observation["products"])
    policy2210xxx = Policy2210xxx()
    list_products = observation["products"]
    sumA = 0
    for prod in list_products:
        sumA += prod["quantity"]
    print("Sum: ", sumA)
    start_time = time.perf_counter()
    for _ in range(300):
        action = policy2210xxx.get_action(observation, info)
        # for prod in observation["products"]:
        #     if prod["size"] == action["size"] and prod["quantity"] > 0:
        #         prod["quantity"] -= 1
        #         break
        # observations = observation
        # print("Action: ", action)
        observation, reward, terminated, truncated, info = env.step(action)
        # observation = observations
        # all_zero = all(prod["quantity"] == 0 for prod in observation["products"])
        # if all_zero:
        #     terminated = True
        # print(action)
        # print("Terminated: ", terminated)
        # print("Truncated: ", truncated)
        if terminated:
            print("Cutting Succesfully !")
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            print(info)
            print(f"Elapsed time: {elapsed_time} seconds")
            input("Press Enter to continue...")
            break

        if terminated or truncated:
            observation, info = env.reset()

env.close()

# from scipy.optimize import milp
# from scipy.optimize import LinearConstraint
# import numpy as np

# c = np.array([1, -4]) 
# A = np.array([
#     [-10, 20],  
#     [5, 10],
#     [1,0]  
# ])
# b_u = np.array([22, 49, 5])
# b_l = np.full_like(b_u, -np.inf, dtype=float)
# constraints = LinearConstraint(A, b_l, b_u)
# integrality = np.ones_like(c)
# result = milp(c=c, constraints=constraints, integrality=integrality)

# # Display results
# if result.success:
#     print(f"Optimal value: {-result.fun}, x1: {result.x[0]}, x2: {result.x[1]}")
# else:
#     print("Optimization failed.")

# from scipy.optimize import linprog

# # Coefficients of the objective function (negated for minimization) # -7x1 - 2x2
# c = [-7, -2, 0, 0, 0]

# # Coefficients for constraints (left-hand side)
# A = [
#     [-1, 2, 1, 0, 0],   # -x1 + 2x2 + x3 = 4 
#     [5, 1, 0, 1, 0],   # 5x1 + x2 + x4 = 20
#     [2, 2, 0, 0, -1]    # 2x1 + 2x2 + - x5 = 7
# ]

# # Right-hand side values for the constraints
# b = [4, 20, 7]

# # Bounds for each variable (x1, x2, x3, x4 >= 0)
# x_bounds = [(0, None), (0, None), (0, None), (0, None), (0, None)]

# # Solve the problem
# result = linprog(c, A_ub=A, b_ub=b, bounds=x_bounds, method="highs")

# # Output the results
# if result.success:
#     print("Optimal value:", result.fun)  # Convert back to maximization
#     print("Optimal solution:", result.x)
# else:
#     print("No solution found.")

# from scipy.optimize import linprog

# # Coefficients of the objective function (negated for minimization) # -7x1 - 2x2
# c = [-2,-3]

# # Coefficients for constraints (left-hand side)
# A = [
#     [4, 12],   # -x1 + 2x2 + x3 = 4 
#     [10,4],   # 5x1 + x2 + x4 = 20
#     # 2x1 + 2x2 + - x5 = 7
# ]

# # Right-hand side values for the constraints
# b = [33, 35]

# # Bounds for each variable (x1, x2, x3, x4 >= 0)
# x_bounds = [(0, None), (0, None)]

# # Solve the problem
# result = linprog(c, A_ub=A, b_ub=b, bounds=x_bounds, method="highs")

# # Output the results
# if result.success:
#     print("Optimal value:", -result.fun)  # Convert back to maximization
#     print("Optimal solution:", result.x)
#     print("Dual variable: ", result.ineqlin['marginals'])
# else:
#     print("No solution found.")


# ###################

# # Coefficients of the objective function (negated for minimization) # -7x1 - 2x2
# c = [33,35]

# # Coefficients for constraints (left-hand side)
# A = [
#     [-4, -10],   # -x1 + 2x2 + x3 = 4 
#     [-12,-4],   # 5x1 + x2 + x4 = 20
#     # 2x1 + 2x2 + - x5 = 7
# ]

# # Right-hand side values for the constraints
# b = [-2, -3]

# # Bounds for each variable (x1, x2, x3, x4 >= 0)
# x_bounds = [(0, None), (0, None)]

# # Solve the problem
# result = linprog(c, A_ub=A, b_ub=b, bounds=x_bounds, method="highs")

# # Output the results
# if result.success:
#     print("Optimal value:", result.fun)  # Convert back to maximization
#     print("Optimal solution:", result.x)
#     print("Dual variable: ", result.ineqlin['marginals'])
# else:
#     print("No solution found.")
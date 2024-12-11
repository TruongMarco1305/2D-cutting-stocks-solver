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

    # print("Products: ", observation["products"])
    policy2210xxx = Policy2210xxx(policy_id=2)
    list_products = observation["products"]
    sumA = 0
    # for prod in list_products:
    #     sumA += prod["quantity"]
    # print("Sum: ", sumA)
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
        # print('Products: ', observation[])
        print('Action: ', action)
        # print("Observation: ", observation['products'])
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

# import numpy as np
# import scipy
# from scipy.optimize import milp, LinearConstraint, Bounds

# # Minimal data
# D = np.array([50., 51., 52.])
# S = np.array([20., 20., 20., 20., 20.])
# c = np.array([4455., 4455., 4455., 4455., 5304., 5304.])

# A = np.array([
#     [0., 0., 1., 10., 33., 6.],
#     [9., 6., 0., 0., 0., 0.],
#     [7., 7., 7., 3., 0., 0.]
# ])

# B = np.array([
#     [0., 0., 0., 0., 0., 0.],
#     [0., 0., 0., 0., 0., 0.],
#     [1., 1., 1., 1., 0., 0.],
#     [0., 0., 0., 0., 1., 1.],
#     [0., 0., 0., 0., 0., 0.]
# ])

# constraints = [
#     LinearConstraint(A, D, D),
#     LinearConstraint(B, -np.inf, S)
# ]

# # Create bounds using Bounds class
# x_bounds = Bounds(np.zeros(len(c)), np.ones(len(c)) * 1e20)

# integrality = [1] * len(c)

# result_milp = milp(
#     c=c,
#     constraints=constraints,
#     integrality=integrality,
#     bounds=x_bounds,
#     options={"presolve": False, "disp": True}
# )


# if result_milp.success:
#     print("Optimal solution found.")
#     print("Decision variables (pattern usages):", result_milp.x)
#     print("Minimum total cost (total area):", result_milp.fun)
# else:
#     print("Optimization failed.")
#     print("Status:", result_milp.status)
#     print("Message:", result_milp.message)

# import numpy as np
# from scipy.optimize import milp, LinearConstraint

# # Define your data based on the provided matrices
# D = np.array([50., 51., 52.])            # Demand vector
# S = np.array([20., 20., 20., 20., 20.]) # Stock vector
# c = np.array([4455., 4455., 4455., 4455., 5304., 5304.]) # Cost vector

# A = np.array([
#     [0., 0., 1., 10., 33., 6.],
#     [9., 6., 0., 0., 0., 0.],
#     [7., 7., 7., 3., 0., 0.]
# ])

# B = np.array([
#     [0., 0., 0., 0., 0., 0.],
#     [0., 0., 0., 0., 0., 0.],
#     [1., 1., 1., 1., 0., 0.],
#     [0., 0., 0., 0., 1., 1.],
#     [0., 0., 0., 0., 0., 0.]
# ])

# # Define constraints
# constraints = [
#     LinearConstraint(A, D, D),         # Equality constraints: A * x = D
#     LinearConstraint(B, -np.inf, S)    # Inequality constraints: B * x <= S
# ]

# # Define bounds for each variable (x >= 0)
# x_bounds = [(0, None) for _ in range(len(c))]

# # Define integrality: 1 signifies integer variables
# integrality = [1] * len(c)  # All variables are integers

# # Solve the MILP
# result_milp = milp(
#     c=c,
#     constraints=constraints,
#     integrality=integrality,
#     options={"presolve": True, "disp": True}
# )

# # Check and print results
# if result_milp.success:
#     print("Optimal solution found.")
#     print("Decision variables (pattern usages):", result_milp.x)
#     print("Minimum total cost (total area):", result_milp.fun)
# else:
#     print("Optimization failed.")
#     print("Status:", result_milp.status)
#     print("Message:", result_milp.message)

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
# from dataclasses import dataclass
# from typing import List, Optional, Tuple

# @dataclass
# class ItemClass:
#     id: int
#     length: float  # Always the longer side
#     width: float   # Always the shorter side
#     demand: int
#     rotatable: bool
#     original_id: Optional[int] = None  # Reference to original item class if rotated
#     rotated: bool = False

# @dataclass
# class BinClass:
#     id: int
#     length: float  # Always the longer side
#     width: float   # Always the shorter side
#     area: float
#     quantity_limit: int
#     quantity_used: int = 0  # Track the number of bins used

# @dataclass
# class ItemPlacement:
#     item_class_id: int
#     quantity: int
#     position: Tuple[float, float]  # (x, y) position in the strip

# @dataclass
# class Strip:
#     width: float
#     height: float
#     items: List[ItemPlacement]  # Items placed in the strip

# @dataclass
# class Bin:
#     id: int
#     bin_class_id: int
#     length: float
#     width: float
#     remaining_length: float
#     remaining_width: float
#     strips: List[Strip]

# def ensure_longer_side_as_length(item_or_bin):
#     """Ensure that the length is the longer side."""
#     if item_or_bin.length < item_or_bin.width:
#         item_or_bin.length, item_or_bin.width = item_or_bin.width, item_or_bin.length

# def create_rotated_item_classes(item_classes: List[ItemClass]) -> List[ItemClass]:
#     new_item_classes = []
#     for item in item_classes:
#         ensure_longer_side_as_length(item)
#         new_item_classes.append(item)
#         if item.rotatable and item.length != item.width:
#             rotated_item = ItemClass(
#                 id=len(new_item_classes) + 1,
#                 length=item.width,
#                 width=item.length,
#                 demand=item.demand,
#                 rotatable=False,  # Avoid rotating again
#                 original_id=item.id,
#                 rotated=True
#             )
#             ensure_longer_side_as_length(rotated_item)
#             new_item_classes.append(rotated_item)
#     return new_item_classes

# def sort_item_classes(item_classes: List[ItemClass]) -> List[ItemClass]:
#     return sorted(
#         item_classes,
#         key=lambda x: (-x.width, -x.length)
#     )

# def assign_bin_classes_to_items(
#     item_classes: List[ItemClass],
#     bin_classes: List[BinClass]
# ) -> dict:
#     b_i = {}  # Mapping from item_class_id to bin_class_id
#     for item in item_classes:
#         assigned_bin_class = None
#         for bin_class in sorted(bin_classes, key=lambda x: x.area):
#             ensure_longer_side_as_length(bin_class)
#             # Check if the bin can fit the entire demand in one bin
#             items_fit_length = bin_class.length // item.length
#             items_fit_width = bin_class.width // item.width
#             max_items_in_bin = int(items_fit_length * items_fit_width)
#             if max_items_in_bin >= item.demand:
#                 assigned_bin_class = bin_class
#                 break
#         if assigned_bin_class:
#             b_i[item.id] = assigned_bin_class.id
#         else:
#             # Assign the bin that can fit the largest number of items
#             max_items_overall = 0
#             best_bin_class = None
#             for bin_class in sorted(bin_classes, key=lambda x: x.area):
#                 items_fit_length = bin_class.length // item.length
#                 items_fit_width = bin_class.width // item.width
#                 max_items_in_bin = int(items_fit_length * items_fit_width)
#                 if max_items_in_bin > max_items_overall:
#                     max_items_overall = max_items_in_bin
#                     best_bin_class = bin_class
#             if best_bin_class:
#                 b_i[item.id] = best_bin_class.id
#             else:
#                 raise Exception(f"No bin can accommodate item class {item.id}")
#     return b_i

# def place_items(
#     item_classes: List[ItemClass],
#     bin_classes: List[BinClass],
#     b_i: dict
# ) -> List[Bin]:
#     bins = []
#     bin_counter = 0
#     item_demand = {item.id: item.demand for item in item_classes}

#     sorted_items = sort_item_classes(item_classes)

#     for item in sorted_items:
#         while item_demand[item.id] > 0:
#             bin_class_id = b_i[item.id]
#             bin_class = next(bc for bc in bin_classes if bc.id == bin_class_id)

#             # Open a new bin of this class if possible
#             if bin_class.quantity_used < bin_class.quantity_limit:
#                 bin_class.quantity_used += 1
#                 bin_counter += 1
#                 current_bin = Bin(
#                     id=bin_counter,
#                     bin_class_id=bin_class.id,
#                     length=bin_class.length,
#                     width=bin_class.width,
#                     remaining_length=bin_class.length,
#                     remaining_width=bin_class.width,
#                     strips=[]
#                 )
#                 bins.append(current_bin)
#             else:
#                 # Try to find another bin class
#                 alternative_bin_class = None
#                 for bc in sorted(bin_classes, key=lambda x: x.area):
#                     if bc.quantity_used < bc.quantity_limit:
#                         alternative_bin_class = bc
#                         break
#                 if alternative_bin_class:
#                     bin_class = alternative_bin_class
#                     b_i[item.id] = bin_class.id
#                     bin_class.quantity_used += 1
#                     bin_counter += 1
#                     current_bin = Bin(
#                         id=bin_counter,
#                         bin_class_id=bin_class.id,
#                         length=bin_class.length,
#                         width=bin_class.width,
#                         remaining_length=bin_class.length,
#                         remaining_width=bin_class.width,
#                         strips=[]
#                     )
#                     bins.append(current_bin)
#                 else:
#                     # No more bins available, but demand must be fulfilled
#                     raise Exception(f"Cannot fulfill demand for item class {item.id} due to bin quantity limits.")

#             # Place items in strips within the bin
#             while item_demand[item.id] > 0 and current_bin.remaining_length >= item.length:
#                 # Initialize a new strip
#                 strip_width = item.width
#                 strip_height = 0
#                 strip_items = []

#                 max_items_in_row = int(current_bin.remaining_width // item.width)
#                 max_rows_in_strip = int(current_bin.remaining_length // item.length)
#                 total_items_in_strip = max_items_in_row * max_rows_in_strip
#                 items_to_place = min(item_demand[item.id], total_items_in_strip)

#                 if items_to_place == 0:
#                     break  # Cannot place more items in this bin

#                 rows_needed = (items_to_place + max_items_in_row - 1) // max_items_in_row
#                 strip_height = rows_needed * item.length

#                 if strip_height > current_bin.remaining_length:
#                     break  # Cannot place strip in remaining length

#                 item_placement = ItemPlacement(
#                     item_class_id=item.id,
#                     quantity=items_to_place,
#                     position=(0, current_bin.length - current_bin.remaining_length)
#                 )
#                 strip = Strip(
#                     width=strip_width,
#                     height=strip_height,
#                     items=[item_placement]
#                 )
#                 current_bin.strips.append(strip)

#                 # Update bin and item demand
#                 current_bin.remaining_length -= strip_height
#                 item_demand[item.id] -= items_to_place

#                 # Fill the strip with smaller items if possible (greedy procedure)
#                 fill_strip_with_smaller_items(
#                     strip,
#                     item_classes,
#                     item_demand,
#                     current_bin
#                 )

#     return bins

# def fill_strip_with_smaller_items(
#     strip: Strip,
#     item_classes: List[ItemClass],
#     item_demand: dict,
#     current_bin: Bin
# ):
#     # Start from the next item class in sorted order
#     sorted_items = sort_item_classes(item_classes)
#     strip_remaining_width = current_bin.remaining_width - strip.width
#     for next_item in sorted_items:
#         if item_demand[next_item.id] > 0 and next_item.width <= strip_remaining_width:
#             max_items_in_row = int(strip_remaining_width // next_item.width)
#             max_rows_in_strip = int(strip.height // next_item.length)
#             total_items = max_items_in_row * max_rows_in_strip
#             items_to_place = min(item_demand[next_item.id], total_items)
#             if items_to_place > 0:
#                 item_placement = ItemPlacement(
#                     item_class_id=next_item.id,
#                     quantity=items_to_place,
#                     position=(strip.width, current_bin.length - current_bin.remaining_length)
#                 )
#                 strip.items.append(item_placement)
#                 item_demand[next_item.id] -= items_to_place
#                 strip.width += next_item.width * max_items_in_row
#                 strip_remaining_width -= next_item.width * max_items_in_row
#                 if strip_remaining_width <= 0:
#                     break

# def main():
#     # Example input data
#     item_classes = [
#         ItemClass(id=1, length=14, width=11, demand=50, rotatable=True),
#         ItemClass(id=2, length=2, width=18, demand=51, rotatable=True),
#         ItemClass(id=3, length=14, width=39, demand=52, rotatable=True),
#         # Add more item classes as needed
#     ]

#     bin_classes = [
#         BinClass(id=1, length=56, width=53, area=2968, quantity_limit=20),
#         BinClass(id=2, length=59, width=52, area=3068, quantity_limit=20),
#         BinClass(id=3, length=81, width=55, area=4455, quantity_limit=20),
#         BinClass(id=4, length=78, width=68, area=5304, quantity_limit=20),
#         BinClass(id=5, length=62, width=73, area=4526, quantity_limit=20),

#         # Add more bin classes as needed
#     ]

#     # Ensure length is always the longer side for bin classes
#     for bin_class in bin_classes:
#         ensure_longer_side_as_length(bin_class)

#     # Step 1: Create rotated item classes
#     all_item_classes = create_rotated_item_classes(item_classes)

#     # Step 2: Assign bin classes to item classes
#     b_i = assign_bin_classes_to_items(all_item_classes, bin_classes)

#     # Step 3: Place items into bins
#     bins = place_items(all_item_classes, bin_classes, b_i)

#     # Output the solution
#     for bin in bins:
#         print(f"Bin {bin.id} (Class {bin.bin_class_id}):")
#         for strip in bin.strips:
#             print(f"  Strip Width: {strip.width}, Height: {strip.height}")
#             for item in strip.items:
#                 print(f"    Item Class {item.item_class_id}, Quantity: {item.quantity}, Position: {item.position}")

# if __name__ == "__main__":
#     main()
# from scipy.optimize import linprog
# from scipy.optimize import milp, LinearConstraint
# import numpy as np

# D = [50, 51, 52]
# S = [20, 20, 20, 20, 20]
# c = [4455, 4455, 4455, 4455, 5304, 5304, 2968, 3068, 4455, 5304, 2968, 3068, 5304, 2968, 2968]
# A = [[ 0,  0,  1, 10, 33,  6,  5,  5,  5,  5,  0,  0,  0,  5,  5],
#  [ 9,  6,  0,  0,  0,  0,  5,  5,  4,  0,  5,  5,  1,  5,  5],
#  [ 7,  7,  7,  3,  0,  0,  4,  4,  6,  8,  5,  5,  9,  4,  4]]
# B = [[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1],
#  [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
#  [1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
#  [0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0],
#  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# # D = [ 3., 18., 15., 20.,  5.,  3., 14.,  9.,  6., 17., 19.,  1., 20., 14.,  1., 15.,  8., 10., 17.]
# # S = [1 for _ in range(0,31)]
# # c = [4550, 4590, 4760, 4784, 4785, 4150, 4731, 4836, 4896, 5002, 5040, 5076, 8742, 8281, 8550, 8640, 8645, 9114, 7056, 7980, 8613, 8712, 5084, 5130, 5133, 5162, 8217, 7800, 5640, 5208, 5320]
# # A = [[ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 0,  0,  0,  0,  0,  0,  2,  1,  0,  0,  0,  0,  0],
# #  [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 0,  0,  0,  0,  2,  0,  0,  0,  0,  8,  8,  0,  0],
# #  [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0, 0,  0,  0,  0,  0,  0,  0,  0,  0,  5,  4,  5,  0.],
# #  [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 0,  0,  0,  0,  0,  0,  0,  0, 17,  3,  0,  0,  0.],
# #  [ 1,  1,  3,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0.],
# #  [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 0,  0,  0,  0,  0,  2,  0,  1,  0,  0,  0,  0,  0.],
# #  [ 0,  0,  0,  0,  0,  2,  2,  2,  2,  2,  2,  2,  0,  0,  0,  0,  0,  0, 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0.],
# #  [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  2,  0,  0,  0,  0, 0,  0,  0,  0,  2,  2,  1,  1,  0,  0,  0,  0,  0.],
# #  [ 0,  0,  0,  1,  1,  0,  2,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0, 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0.],
# #  [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  2,  2,  2,  1, 2,  4,  0,  2,  0,  0,  0,  0,  1,  0,  0,  0,  0.],
# #  [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  4,  4,  4,  4,  2, 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0.],
# #  [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1, 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0.],
# #  [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 0,  0,  2,  6,  3,  3,  3,  3,  0,  0,  0,  0,  0.],
# #  [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  2, 4,  4,  4,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0.],
# #  [ 0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0.],
# #  [ 0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  0,  1, 11,  0,  0,  0,  0,  0, 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0.],
# #  [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  5,  3.],
# #  [ 3,  7,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0.],
# #  [ 3,  3,  3,  3,  2,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0.]]

# # B:  [[0, 0, 0, .., 0, 0, 0.]
# #  [0, 0, 0, .., 0, 0, 0.]
# #  [0, 0, 0, .., 0, 0, 0.]
# #  ...
# #  [0, 0, 0, .., 0, 0, 0.]
# #  [0, 0, 0, .., 1, 0, 0.]
# #  [0, 0, 0, .., 0, 0, 0.]]
# # B = [[0 for _ in range(0, 31)] for _ in range(0, 31)]
# # # temp = [71, 78, 77, 55, 39, 70, 19, 65, 57, 10, 15, 69, 62, 16, 82, 73, 38, 52, 50, 30, 24, 12, 63, 64, 5, 49, 91, 68, 90, 58, 54]
# # for i in range (0,31):
# #     B[i][i] = 1

# x_bounds = [(0,None) for _ in range(len(c))]
# # print(linprog(c,A_ub=B,b_ub=S,A_eq=A,b_eq=D,bounds=x_bounds,method='highs',integrality=1).x)
# constraints = [
#     LinearConstraint(A,D,D),
#     LinearConstraint(B, -np.inf, S)
# ]
# integrality = [1] * len(c)
# result_milp = milp(
#     c=c,
#     constraints=constraints,
#     integrality=integrality,
#     options={"presolve": True, "disp": True}
# )
# # Check and print results
# # if result_milp.success:
# #     print("Optimal solution found.")
# #     print("Decision variables (pattern usages):", result_milp.x)
# #     print("Minimum total cost (total area):", result_milp.fun)
# # else:
# #     print("Optimization failed.")
# #     print("Status:", result_milp.status)
# #     print("Message:", result_milp.message)
# print(np.int64(result_milp.x))
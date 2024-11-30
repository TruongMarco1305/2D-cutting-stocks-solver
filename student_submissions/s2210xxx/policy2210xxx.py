from policy import Policy
import numpy as np
import time
import copy

class Policy2210xxx(Policy):
    def __init__(self):
        self.stock_buckets = {}
        self.bucket_size = 10  # Define the size range for each bucket
        self.patterns = []
        self.isComputing = True
        self.optimal_result = []
        self.result_counter = -1

    def get_action(self, observation, info):
        if(self.isComputing):
            self.solve_cutting_stock_problem(observation,info)
            self.isComputing = False
            for data in self.patterns:
                stock_idx = data['stock_idx']
                items = data['items']
        
                if items:  # Check if 'items' is non-empty
                    for item_id, details in items.items():
                        size = (details['width'], details['height'])
                        positions = details['positions']
                        for position in positions:
                            self.optimal_result.append({
                                'stock_idx': stock_idx,
                                'size': size,
                                'position': position,
                            })
            # for res in self.optimal_result:
            #     print(res)
            self.result_counter += 1
            return {
                "stock_idx": self.optimal_result[self.result_counter]["stock_idx"],
                "size": self.optimal_result[self.result_counter]["size"],
                "position": self.optimal_result[self.result_counter]["position"]
            }
        else:
            self.result_counter += 1
            return {
                "stock_idx": self.optimal_result[self.result_counter]["stock_idx"],
                "size": self.optimal_result[self.result_counter]["size"],
                "position": self.optimal_result[self.result_counter]["position"]
            }

    def solve_cutting_stock_problem(self, observation, info):
        initial_stocks = copy.deepcopy(observation["stocks"])
        initial_prods = copy.deepcopy(observation["products"])
        prod_num = 0
        list_prods = []
        for prod in initial_prods:
            prod_info = {"width": prod["size"][0], "height": prod["size"][1], "quantity": prod["quantity"]}
            list_prods.append(prod_info)
            prod_num += prod["quantity"]

        list_stocks = []
        for stock_i in initial_stocks:
            stock_w, stock_h = self._get_stock_size_(stock_i)
            quantity = 1
            duplicated_stock_idx = -1
            for stock_idx,stock in enumerate(list_stocks):
                if stock_w == stock["width"] and stock_h == stock["height"]:
                    duplicated_stock_idx = stock_idx
                    quantity += 1
            if duplicated_stock_idx != -1:
                list_stocks[duplicated_stock_idx]["quantity"] = quantity
            else:
                stock_info = {"width": stock_w, "height": stock_h, "quantity": quantity}
                list_stocks.append(stock_info)

        # Pattern for all stocks
        # pattern = {'stock_idx': number, 'items': map[]}[]
        # map: (key-value) -> (prod_idx: {"quantity": number, "positions": number[][], "width": number, "height": number})
        
        # Initialize the pattern
        for stock_idx in range (len(list_stocks)):
            pattern_element = {'stock_idx': stock_idx, 'items': {}}
            self.patterns.append(pattern_element)
        # print(self.patterns)
        # prod_idx, best_stock_idx, best_prod_size, best_position = self.initial_heuristic(observation)
        # Sample input
        # prod_idx = 0
        # best_stock_idx = 0
        # best_prod_size = np.array([10, 10])
        # best_position = (0,0)
        clone_stocks = initial_stocks
        clone_prods = initial_prods
        stock_indices = list(range(len(clone_stocks)))
        for _ in range(prod_num):
            heuristic_result = self.lazy_init_heuristic(clone_prods, clone_stocks, stock_indices)
            prod_idx = heuristic_result["prod_idx"]
            best_stock_idx = heuristic_result["stock_idx"]
            # print(best_stock_idx)
            best_position = heuristic_result["position"]
            best_prod_size = heuristic_result["size"]
            print("prod_idx: ", prod_idx, "best_stock_idx: ", best_stock_idx)
            clone_stocks, clone_prods = self.fill_to_clone_stocks(clone_stocks, clone_prods, prod_idx, best_stock_idx, best_position, best_prod_size)
            if prod_idx in self.patterns[best_stock_idx]["items"]:
                self.patterns[best_stock_idx]["items"][prod_idx]["quantity"] += 1
                self.patterns[best_stock_idx]["items"][prod_idx]["positions"].append(best_position)
            else:
                position_list = [best_position]
                prod_w, prod_h = best_prod_size
                self.patterns[best_stock_idx]["items"][prod_idx] = {"quantity": 1, "positions": position_list, "width": prod_w, "height": prod_h }

    def fill_to_clone_stocks(self,clone_stocks, clone_prods, prod_idx, best_stock_idx, best_position, best_prod_size):
        x, y = best_position
        w, h = best_prod_size
        for i in range(x, x + w):
            for j in range(y, y + h):
                clone_stocks[best_stock_idx][i][j] = prod_idx
        return clone_stocks, clone_prods

    def lazy_init_heuristic(self, clone_prods, clone_stocks, stock_indices):
        best_stock_idx, best_position, best_prod_size = -1, None, [0, 0]
        if not hasattr(self, 'sorted_prods'):
            self.sorted_prods = sorted(clone_prods, key=lambda p: p["size"][0] * p["size"][1], reverse=True)
            # self.sorted_prods = sorted(list_prods, key=lambda p: (p["size"][0], p["size"][1]), reverse=True)
        if not hasattr(self, 'sorted_stocks'):
            self.sorted_stocks = sorted(enumerate(clone_stocks), key=lambda x: self._get_stock_size_(x[1])[0] * self._get_stock_size_(x[1])[1])
        clone_prods = self.sorted_prods
        sorted_stocks = self.sorted_stocks
        # Group stocks into buckets based on size ranges
        self._group_stocks_into_buckets(clone_stocks)
        
        for prod_idx,prod in enumerate(clone_prods):
            if prod["quantity"] > 0:
                prod_size = prod["size"]
                min_waste_percentage = float('inf')
                candidate_stocks = self._get_candidate_stocks(prod_size)
                
                for stock_idx, stock in candidate_stocks:
                    placed = False
                    position = self._find_position(stock, prod_size[0], prod_size[1])
                    if position:
                        stock_w, stock_h = self._get_stock_size_(stock)
                        stock_area = stock_w * stock_h
                        prod_area = prod_size[0] * prod_size[1]
                        waste_percentage = (stock_area - prod_area) / stock_area
                        if waste_percentage < min_waste_percentage:
                            min_waste_percentage = waste_percentage
                            best_stock_idx = stock_idx
                            best_position = position
                            best_prod_size = prod_size
                            # placed = True
                            # break
                if best_position and best_stock_idx != -1:
                    prod["quantity"] -= 1
                    return {"prod_idx": prod_idx, "stock_idx": best_stock_idx, "size": (best_prod_size[0], best_prod_size[1]), "position": best_position}
        return {"stock_idx": -1, "size": [0, 0], "position": None}

    def _group_stocks_into_buckets(self, stocks):
        self.stock_buckets = {}
        for idx, stock in enumerate(stocks):
            stock_w, stock_h = self._get_stock_size_(stock)
            bucket_key = (stock_w // self.bucket_size, stock_h // self.bucket_size)
            if bucket_key not in self.stock_buckets:
                self.stock_buckets[bucket_key] = []
            self.stock_buckets[bucket_key].append((idx, stock))

    def _get_candidate_stocks(self, prod_size):
        prod_w, prod_h = prod_size
        bucket_key = (prod_w // self.bucket_size, prod_h // self.bucket_size)
        candidate_stocks = []
        for key in self.stock_buckets:
            if key[0] >= bucket_key[0] and key[1] >= bucket_key[1]:
                candidate_stocks.extend(self.stock_buckets[key])
        return candidate_stocks

    def _find_position(self, stock, product_width, product_height):
        stock_width, stock_height = self._get_stock_size_(stock)

        for x in range(stock_width - product_width + 1):
            for y in range(stock_height - product_height + 1):
                if self._can_place_(stock, (x, y), (product_width, product_height)):
                    return (x, y)
        return None

    # def __init__(self):
    #     self.stock_buckets = {}
    #     self.bucket_size = 20  # Define the size range for each bucket

    # def get_action(self, observation, info):
    #     list_prods = observation["products"]
    #     best_stock_idx, best_position, best_prod_size = -1, None, [0, 0]
    #     if not hasattr(self, 'sorted_prods'):
    #         self.sorted_prods = sorted(list_prods, key=lambda p: p["size"][0] * p["size"][1], reverse=True)
    #         # self.sorted_prods = sorted(list_prods, key=lambda p: (p["size"][0], p["size"][1]), reverse=True)
    #     if not hasattr(self, 'sorted_stocks'):
    #         self.sorted_stocks = sorted(enumerate(observation["stocks"]), key=lambda x: self._get_stock_size_(x[1])[0] * self._get_stock_size_(x[1])[1])
    #     list_prods = self.sorted_prods
    #     sorted_stocks = self.sorted_stocks
    #     # Group stocks into buckets based on size ranges
    #     self._group_stocks_into_buckets(observation["stocks"])
        
    #     for prod in list_prods:
    #         if prod["quantity"] > 0:
    #             prod_size = prod["size"]
    #             min_waste_percentage = float('inf')
    #             candidate_stocks = self._get_candidate_stocks(prod_size)
                
    #             for stock_idx, stock in candidate_stocks:
    #                 placed = False
    #                 position = self._find_position(stock, prod_size[0], prod_size[1])
    #                 if position:
    #                     stock_w, stock_h = self._get_stock_size_(stock)
    #                     stock_area = stock_w * stock_h
    #                     prod_area = prod_size[0] * prod_size[1]
    #                     waste_percentage = (stock_area - prod_area) / stock_area
    #                     if waste_percentage < min_waste_percentage:
    #                         min_waste_percentage = waste_percentage
    #                         best_stock_idx = stock_idx
    #                         best_position = position
    #                         best_prod_size = prod_size
    #                         placed = True
    #                         break
    #             if best_position and best_stock_idx != -1:
    #                 return {"stock_idx": best_stock_idx, "size": (best_prod_size[0], best_prod_size[1]), "position": best_position}
    #     return {"stock_idx": -1, "size": [0, 0], "position": None}

    # def _group_stocks_into_buckets(self, stocks):
    #     self.stock_buckets = {}
    #     for idx, stock in enumerate(stocks):
    #         stock_w, stock_h = self._get_stock_size_(stock)
    #         bucket_key = (stock_w // self.bucket_size, stock_h // self.bucket_size)
    #         if bucket_key not in self.stock_buckets:
    #             self.stock_buckets[bucket_key] = []
    #         self.stock_buckets[bucket_key].append((idx, stock))

    # def _get_candidate_stocks(self, prod_size):
    #     prod_w, prod_h = prod_size
    #     bucket_key = (prod_w // self.bucket_size, prod_h // self.bucket_size)
    #     candidate_stocks = []
    #     for key in self.stock_buckets:
    #         if key[0] >= bucket_key[0] and key[1] >= bucket_key[1]:
    #             candidate_stocks.extend(self.stock_buckets[key])
    #     return candidate_stocks

    # def _find_position(self, stock, product_width, product_height):
    #     stock_width, stock_height = self._get_stock_size_(stock)

    #     for x in range(stock_width - product_width + 1):
    #         for y in range(stock_height - product_height + 1):
    #             if self._can_place_(stock, (x, y), (product_width, product_height)):
    #                 return (x, y)
    #     return None

    # def _place_product(self, stock, product_width, product_height, position):
    #     if position is None:
    #         return  # No valid position found, do nothing

    #     x, y = position
    #     stock_width, stock_height = self._get_stock_size_(stock)

    #     # Ensure the product is placed within the stock dimensions
    #     # if x + product_width > stock_width or y + product_height > stock_height:
    #     #     return

    #     for i in range(product_height):
    #         for j in range(product_width):
    #             stock[y + i][x + j] = 1  # Mark the stock as used

    # def _place_product(self, stock, product_width, product_height, position):
    #     if position is None:
    #         return  # No valid position found, do nothing

    #     x, y = position
    #     stock_width, stock_height = self._get_stock_size_(stock)

    #     # Ensure the product is placed within the stock dimensions
    #     # if x + product_width > stock_width or y + product_height > stock_height:
    #     #     return

    #     for i in range(product_height):
    #         for j in range(product_width):
    #             stock[y + i][x + j] = 1  # Mark the stock as used
    
    # Student code here
    # def get_action(self, observation, info):
    #     list_prods = observation["products"]
    #     list_stocks = observation["stocks"]
    #     list_prods = sorted(list_prods, key=lambda p: (p["size"][0], p["size"][1]), reverse=True)
    #     list_stocks = sorted(list_stocks, key=lambda p: p["size"][0] * p["size"][1])
        
    #     item_to_bin = {tuple(item.values()): assign_bin_class(item, bin_classes) for item in extended_item_classes}

    #     # Step 4: Iteratively insert items into bins
    #     bins = []
    #     for item in list_prods:
    #         while item["quantity"] > 0:
    #             # Initialize a new strip in a partially used or new bin
    #             bin_class = item_to_bin[tuple(item.values())]
    #             if not bin_class:
    #                 raise ValueError(f"No bin can accommodate item class: {item}")

    #             bin_used = None
    #             for b in bins:
    #                 if b["class"] == bin_class and sum(s["height"] for s in b["strips"]) + item["length"] <= bin_class["length"]:
    #                     bin_used = b
    #                     break

    #             if not bin_used:
    #                 bin_used = {"class": bin_class, "strips": []}
    #                 bins.append(bin_used)

    #             # Insert items into the strip
    #             strip = {"width": item["width"], "items": []}
    #             remaining_width = bin_class["width"]
    #             while remaining_width >= item["width"] and item["demand"] > 0:
    #                 strip["items"].append(item)
    #                 remaining_width -= item["width"]
    #                 item["demand"] -= 1

    #             bin_used["strips"].append(strip)

    #             # Fill remaining space with smaller-width items using a greedy approach
    #             for other_item in extended_item_classes:
    #                 if other_item["width"] < strip["width"] and other_item["demand"] > 0:
    #                     while remaining_width >= other_item["width"] and other_item["demand"] > 0:
    #                         strip["items"].append(other_item)
    #                         remaining_width -= other_item["width"]
    #                         other_item["demand"] -= 1
    #     return bins
        # return bins

          
    # def assign_bin_class(item, bin_classes):
    #     for stock in sorted(list_stocks, key=lambda x: x["size"][0] * x["size"][1]):  # Sort bins by minimum area
    #         if bin_class["width"] >= item["width"] and bin_class["length"] >= item["length"] * item["demand"]:
    #             return bin_class  # Fits the entire demand
    #     # Assign to a bin that fits the largest number of items
    #     for bin_class in sorted(bin_classes, key=lambda x: x["area"]):
    #         if bin_class["width"] >= item["width"] and bin_class["length"] >= item["length"]:
    #             return bin_class
    #     return None  # No suitable bin found

    # def get_action(self, observation, info):
    # #     """
    # #     Generate an initial feasible solution for MS2DCSP without rotation.

    # #     Parameters:
    # #         observation (dict): Contains "stocks" and "products".
    # #             - stocks (list): List of NumPy arrays representing stocks.
    # #             - products (list): List of products with size and quantity information.

    # #     Returns:
    # #         list: Updated stocks showing the cutting plan.
    # #     """
    #     products = observation["products"]
    #     stocks = observation["stocks"]

    #     # Step 1: Sort products by non-increasing widths, breaking ties with non-increasing heights
    #     products = sorted(products, key=lambda p: (-p["size"][0], -p["size"][1]))

    #     placements = []  # Store placement details

    #     # Step 2: Iteratively insert products into stocks
    #     for product_idx, product in enumerate(products):
    #         product_width, product_height, product_quantity = product["size"][0], product["size"][1], product["quantity"]
    #         while product_quantity > 0:
    #             # Try to find a stock where the product can be placed
    #             placed = False
    #             for stock_idx, stock in enumerate(stocks):
    #                 stock_height, stock_width = stock.shape
    #                 for i in range(stock_height - product_height + 1):
    #                     for j in range(stock_width - product_width + 1):
    #                         if self.can_place_product(stock, product_width, product_height, i, j):
    #                             # Place the product and record placement details
    #                             placement = self.place_product(
    #                                 stock=stock,
    #                                 stock_idx=stock_idx,  # Pass `stock_idx` as an integer
    #                                 product_index=product_idx,
    #                                 product_width=product_width,
    #                                 product_height=product_height,
    #                                 start_row=i,
    #                                 start_col=j,
    #                             )                                
    #                             placements.append(placement)
    #                             product_quantity -= 1
    #                             product["quantity"] -= 1
    #                             placed = True
    #                             break
    #                     if placed:
    #                         break
    #                 if placed:
    #                     break

    #             # If no stock can fit the product
    #             if not placed:
    #                 print(f"Warning: Cannot fit product {product} in any stock.")
    #                 break

    #     return placement

    # def can_place_product(self, stock, product_width, product_height, start_row, start_col):
    #     for i in range(start_row, start_row + product_height):
    #         for j in range(start_col, start_col + product_width):
    #             if stock[i, j] != -1:  # Position must be empty
    #                 return False
    #     return True

    # def place_product(self, stock, stock_idx, product_index, product_width, product_height, start_row, start_col):
    #     for i in range(start_row, start_row + product_height):
    #         for j in range(start_col, start_col + product_width):
    #             stock[i][j] = product_index

    #     return {
    #         "stock_idx": stock_idx,
    #         "size": (product_width, product_height),
    #         "position": (start_col, start_row),
    #     }
    # You can add more functions if needed

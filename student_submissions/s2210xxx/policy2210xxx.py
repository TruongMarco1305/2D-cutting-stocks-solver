from policy import Policy
import numpy as np


class Policy2210xxx(Policy):
    def __init__(self):
        pass

    def get_action(self, observation, info):
        list_prods = observation["products"]
        best_stock_idx, best_position, best_prod_size = -1, None, [0, 0]
        list_prods = sorted(list_prods, key=lambda p: p["size"][0] * p["size"][1], reverse=True)
        # list_prods = sorted(list_prods, key=lambda p: (p["size"][0], p["size"][1]), reverse=True)
        sorted_stocks = sorted(enumerate(observation["stocks"]), key=lambda x: self._get_stock_size_(x[1])[0] * self._get_stock_size_(x[1])[1])
        sum = 0
        for prod in list_prods:
            if prod["quantity"] > 0:
                prod_size = prod["size"]
                min_waste_percentage = float('inf')
                for stock_idx, stock in sorted_stocks:
                    place = False
                    stock_w, stock_h = self._get_stock_size_(stock)
                    prod_w, prod_h = prod_size
                    if stock_w < prod_w or stock_h < prod_h:
                        continue
                    for x in range(stock_w - prod_w + 1):
                        for y in range(stock_h - prod_h + 1):
                            if self._can_place_(stock, (x, y), prod_size):
                                stock_area = stock_w * stock_h
                                prod_area = prod_w * prod_h
                                waste_percentage = (stock_area - prod_area) / stock_area
                                if waste_percentage < min_waste_percentage:
                                    min_waste_percentage = waste_percentage
                                    best_stock_idx = stock_idx
                                    best_position = (x, y)
                                    best_prod_size = prod_size
                                place = True
                                break
                        if place is True:
                            break
                if best_position is not None:
                    break

        return {"stock_idx": best_stock_idx, "size": best_prod_size, "position": best_position}

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

    def can_place_product(self, stock, product_width, product_height, start_row, start_col):
        for i in range(start_row, start_row + product_height):
            for j in range(start_col, start_col + product_width):
                if stock[i, j] != -1:  # Position must be empty
                    return False
        return True

    def place_product(self, stock, stock_idx, product_index, product_width, product_height, start_row, start_col):
        for i in range(start_row, start_row + product_height):
            for j in range(start_col, start_col + product_width):
                stock[i][j] = product_index

        return {
            "stock_idx": stock_idx,
            "size": (product_width, product_height),
            "position": (start_col, start_row),
        }
    # You can add more functions if needed

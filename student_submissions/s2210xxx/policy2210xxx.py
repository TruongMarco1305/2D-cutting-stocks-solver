from policy import Policy


class Policy2210xxx(Policy):
    def __init__(self):
        pass

    def get_action(self, observation, info):
        list_prods = observation["products"]
        best_stock_idx, best_position, best_prod_size = -1, None, [0, 0]
        list_prods = sorted(list_prods, key=lambda p: p["size"][0] * p["size"][1], reverse=True)
        for prod in list_prods:
            if prod["quantity"] > 0:
                prod_size = prod["size"]
                min_waste_percentage = float('inf')
                for stock_idx, stock in enumerate(observation["stocks"]):
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
                if best_position is not None:
                    break

        return {"stock_idx": best_stock_idx, "size": best_prod_size, "position": best_position}

    # Student code here
    # You can add more functions if needed

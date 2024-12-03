from policy import Policy
import numpy as np
from scipy.optimize import linprog
import time
import copy

class Policy2210xxx(Policy):
    def __init__(self):
        self.stock_buckets = {}
        self.bucket_size = 10  # Define the size range for each bucket
        self.initial_patterns = []
        self.isComputing = True
        self.result_counter = -1
        self.optimal_result = []
        self.indices_prods = []
        self.indices_stocks = []

    
    def get_action(self, observation, info):
        # print("Initial first stock: ",self._get_stock_size_(observation["stocks"][0]))
        if(self.isComputing):
            self.solve_cutting_stock_problem(observation,info)
            # for pattern in self.initial_patterns:
            #     print(pattern)
            self.isComputing = False
            for data in self.initial_patterns:
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
            self.result_counter += 1
            # print({
            #     "stock_idx": self.optimal_result[self.result_counter]["stock_idx"],
            #     "size": self.optimal_result[self.result_counter]["size"],
            #     "position": self.optimal_result[self.result_counter]["position"]
            # })
            return {
                "stock_idx": self.optimal_result[self.result_counter]["stock_idx"],
                "size": self.optimal_result[self.result_counter]["size"],
                "position": self.optimal_result[self.result_counter]["position"]
            }
        else:
            self.result_counter += 1
            # print({
            #     "stock_idx": self.optimal_result[self.result_counter]["stock_idx"],
            #     "size": self.optimal_result[self.result_counter]["size"],
            #     "position": self.optimal_result[self.result_counter]["position"]
            # })
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
            duplicated_stock_idx = -1
            for stock_idx,stock in enumerate(list_stocks):
                if stock_w == stock["width"] and stock_h == stock["height"]:
                    duplicated_stock_idx = stock_idx
            if duplicated_stock_idx != -1:
                list_stocks[duplicated_stock_idx]["quantity"] += 1
            else:
                stock_info = {"width": stock_w, "height": stock_h, "quantity": 1}
                list_stocks.append(stock_info)
        # Pattern for all stocks
        # pattern = {'stock_idx': number, 'items': map[]}[]
        # map: (key-value) -> (prod_idx: {"quantity": number, "positions": number[][], "width": number, "height": number})
        
        # Initialize the pattern
        for stock_idx, stock in enumerate(initial_stocks):
            stock_w, stock_h = self._get_stock_size_(stock)
            stock_type = -1
            for s_idx,s in enumerate(list_stocks):
                if s["width"] == stock_w and s["height"] == stock_h:
                    stock_type = s_idx
                    break
            pattern_element = {'key': '_' + str(stock_type) + '_','stock_idx': stock_idx, 'stock_type': stock_type, 'width': stock_w,'height': stock_h,'items': {}}
            self.initial_patterns.append(pattern_element)

        clone_stocks = initial_stocks
        clone_prods = initial_prods
        if len(self.indices_prods) == 0 and len(self.indices_stocks) == 0:
            self.indices_prods, self.indices_stocks = list(range(len(clone_prods))), list(range(len(clone_stocks)))
        for _ in range(prod_num):
            heuristic_result = self.lazy_init_heuristic(clone_prods, clone_stocks, self.indices_prods, self.indices_stocks)
            prod_idx = heuristic_result["prod_idx"]
            best_stock_idx = heuristic_result["stock_idx"]
            best_position = heuristic_result["position"]
            best_prod_size = heuristic_result["size"]
            # print("prod_idx: ", prod_idx, "best_stock_idx: ", best_stock_idx, "position: ", best_position, "prod_size: ", best_prod_size)
            clone_stocks, clone_prods = self.fill_to_clone_stocks(clone_stocks, clone_prods, prod_idx, best_stock_idx, best_position, best_prod_size)
            if prod_idx in self.initial_patterns[best_stock_idx]["items"]:
                self.initial_patterns[best_stock_idx]["items"][prod_idx]["quantity"] += 1
                self.initial_patterns[best_stock_idx]["items"][prod_idx]["positions"].append(best_position)
                self.initial_patterns[best_stock_idx]["key"]+=str(prod_idx) + '_'
            else:
                position_list = [best_position]
                prod_w, prod_h = best_prod_size
                self.initial_patterns[best_stock_idx]["items"][prod_idx] = {"quantity": 1, "positions": position_list, "width": prod_w, "height": prod_h }
                self.initial_patterns[best_stock_idx]["key"]+=str(prod_idx) + '_'
        
        # Simplex method init
        x = np.array([])

        D = np.array([])
        for prod in list_prods:
            D=np.append(D,prod["quantity"])
        D = D.flatten()
        # print('D: ',D)

        S = np.array([])
        for stock in list_stocks:
            S=np.append(S,stock["quantity"])
        S = S.flatten()
        # print('S: ',S)

        # self.initial_patterns.append({'key': '_83_0_', 'stock_idx': 84, 'stock_type': 83, 'width': np.int64(51), 'height': np.int64(50), 'items': {0: {'quantity': 1, 'positions': [(0, 0)], 'width': np.int64(41), 'height': np.int64(45)}}})
        unique_patterns = []
        keys = []
        c = np.array([])
        for pattern in self.initial_patterns:
            if pattern["items"] == {}: continue   
            if pattern["key"] not in keys:
                keys.append(pattern["key"])
                unique_pattern = {"stock_type": pattern["stock_type"], "items": pattern["items"]}
                unique_patterns.append(unique_pattern)
                area = pattern['width'] * pattern['height']
                # print(unique_pattern)
                c = np.append(c,area)
        c = c.flatten()
        # print('c: ', c)
     
        A = np.zeros(shape=(len(list_prods),len(unique_patterns))) # 11 row - 28 col
        for pattern_idx, pattern in enumerate(unique_patterns):
            for prod_idx, value in pattern['items'].items():
                # print(prod_index, ' ', value['quantity'])
                A[prod_idx][pattern_idx] = value['quantity']
        # print('A: ', A)

        B = np.zeros(shape=(len(list_stocks),len(unique_patterns))) # 97 row - 28 col
        for pattern_idx, pattern in enumerate(unique_patterns):
            B[pattern["stock_type"]][pattern_idx] = 1
        # print('B: ', B)

        #### Simplex method
        # print((np.concatenate((A,B),axis=0)).shape)

        x_bounds = [(0,None) for _ in range(len(unique_patterns))]
        result_simplex = linprog(c,A_ub=B,b_ub=S,A_eq=A,b_eq=D,bounds=x_bounds,method='highs',integrality=1)
        x = result_simplex.x
        dual_prods = result_simplex.eqlin['marginals']
        dual_stocks = result_simplex.ineqlin['marginals']
        # print(x)
        # print(dual_prods)
        # print(dual_stocks)
        # print(result_simplex)

        # 2 vector Dual_variable (về item + về loại stock) 
        # Mỗi loại stock, truyền vô cái Long làm
        # => Trả về [số loại stock] pattern + profit tương ứng
        # Cầm đống pattern mới kiếm tính reduce cost
        # Âm -> Có pattern mới vào RMP -> Quay lại step 1
        # Dương -> Giải MILP để cho ra kết quả nguyên -> Siuuuuuuuuuuuuuu


    def fill_to_clone_stocks(self,clone_stocks, clone_prods, prod_idx, best_stock_idx, best_position, best_prod_size):
        x, y = best_position
        w, h = best_prod_size
        for i in range(x, x + w):
            for j in range(y, y + h):
                clone_stocks[best_stock_idx][i][j] = prod_idx
        return clone_stocks, clone_prods

    def lazy_init_heuristic(self, clone_prods, clone_stocks, indices_prods, indices_stocks):
        best_stock_idx, best_position, best_prod_size = -1, None, [0, 0]
        if not hasattr(self, 'sorted_prods'):
            self.sorted_prods = sorted(clone_prods, key=lambda p: p["size"][0] * p["size"][1], reverse=True)
            self.indices_prods = sorted(self.indices_prods, key=lambda i: clone_prods[i]["size"][0] * clone_prods[i]["size"][1], reverse=True)
            # self.sorted_prods = sorted(list_prods, key=lambda p: (p["size"][0], p["size"][1]), reverse=True)
        if not hasattr(self, 'sorted_stocks'):
            self.sorted_stocks = sorted(enumerate(clone_stocks), key=lambda x: self._get_stock_size_(x[1])[0] * self._get_stock_size_(x[1])[1])

        clone_prods = self.sorted_prods
        sorted_stocks = self.sorted_stocks
        # print("Sorted first stock: ",self._get_stock_size_(sorted_stocks[0][1]))
        # Group stocks into buckets based on size ranges
        self._group_stocks_into_buckets(clone_stocks)
        # print(clone_prods)
        
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
                            placed = True
                            break
                if best_position and best_stock_idx != -1:
                    prod["quantity"] -= 1
                    # print({"prod_idx": self.indices_prods[prod_idx], "stock_idx": best_stock_idx, "size": (best_prod_size[0], best_prod_size[1]), "position": best_position})
                    # print(prod_idx)
                    return {"prod_idx": self.indices_prods[prod_idx], "stock_idx": best_stock_idx, "size": (best_prod_size[0], best_prod_size[1]), "position": best_position}
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
    # You can add more functions if needed

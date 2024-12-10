import numpy as np
from scipy.optimize import linprog
import copy
import itertools


from policy import Policy


class Policy2210xxx(Policy):
    # def __init__(self):
    #     pass

    # def get_action(self, observation, info):
    #     list_prods = observation["products"]
    #     best_stock_idx, best_position, best_prod_size = -1, None, [0, 0]
    #     list_prods = sorted(list_prods, key=lambda p: p["size"][0] * p["size"][1], reverse=True)
    #     for prod in list_prods:
    #         if prod["quantity"] > 0:
    #             prod_size = prod["size"]
    #             min_waste_percentage = float('inf')
    #             for stock_idx, stock in enumerate(observation["stocks"]):
    #                 stock_w, stock_h = self._get_stock_size_(stock)
    #                 prod_w, prod_h = prod_size
    #                 if stock_w < prod_w or stock_h < prod_h:
    #                     continue
    #                 for x in range(stock_w - prod_w + 1):
    #                     for y in range(stock_h - prod_h + 1):
    #                         if self._can_place_(stock, (x, y), prod_size):
    #                             stock_area = stock_w * stock_h
    #                             prod_area = prod_w * prod_h
    #                             waste_percentage = (stock_area - prod_area) / stock_area
    #                             if waste_percentage < min_waste_percentage:
    #                                 min_waste_percentage = waste_percentage
    #                                 best_stock_idx = stock_idx
    #                                 best_position = (x, y)
    #                                 best_prod_size = prod_size
    #             if best_position is not None:
    #                 break

    #     return {"stock_idx": best_stock_idx, "size": best_prod_size, "position": best_position}

    # Student code here
    # You can add more functions if needed

        def __init__(self):
            self.stock_buckets = {}
            self.bucket_size = 10  # Define the size range for each bucket
            self.optimal_patterns = []
            self.isComputing = True
            self.drawing_counter = -1
            self.drawing_data = []
            self.indices_prods = []
            self.list_stocks = []
            self.list_products = []

        def get_action(self, observation, info):
            if(self.isComputing):
                self.solve_cutting_stock_problem(observation,info)
                self.isComputing = False
                for data in self.optimal_patterns:
                    if data['quantity'] == 0: continue
                    for _ in range(data['quantity']):
                        stock_type = data['stock_type']
                        stock_idx = self.list_stocks[stock_type]['stock_index'][0]
                        self.list_stocks[stock_type]['stock_index'].pop(0)
                        items = data['items']
                        if items:
                            for item_id, details in items.items():
                                size = (details['width'], details['height'])
                                positions = details['positions']
                                for position in positions:
                                    self.drawing_data.append({
                                        'stock_idx': stock_idx,
                                        'size': size,
                                        'position': position,
                                    })
                self.drawing_counter += 1
                return {
                    "stock_idx": self.drawing_data[self.drawing_counter]["stock_idx"],
                    "size": self.drawing_data[self.drawing_counter]["size"],
                    "position": self.drawing_data[self.drawing_counter]["position"]
                }
            else:
                self.drawing_counter += 1
                return {
                    "stock_idx": self.drawing_data[self.drawing_counter]["stock_idx"],
                    "size": self.drawing_data[self.drawing_counter]["size"],
                    "position": self.drawing_data[self.drawing_counter]["position"]
                }

        def solve_cutting_stock_problem(self, observation, info):
            initial_stocks = copy.deepcopy(observation["stocks"])
            initial_prods = copy.deepcopy(observation["products"])
            prod_num = 0
            for prod_idx,prod in enumerate(initial_prods):
                prod_info = {"width": prod["size"][0], "height": prod["size"][1], "quantity": prod["quantity"]}
                self.list_products.append(prod_info)
                prod_num += prod["quantity"]

            for stock_i_idx,stock_i in enumerate(initial_stocks):
                stock_w, stock_h = self._get_stock_size_(stock_i)
                duplicated_stock_idx = -1
                for stock_idx,stock in enumerate(self.list_stocks):
                    if stock_w == stock["width"] and stock_h == stock["height"]:
                        duplicated_stock_idx = stock_idx
                        break
                if duplicated_stock_idx != -1:
                    self.list_stocks[duplicated_stock_idx]["quantity"] += 1
                    self.list_stocks[duplicated_stock_idx]["stock_index"].append(stock_i_idx)
                else:
                    stock_info = {"width": stock_w, "height": stock_h, "quantity": 1, "stock_index": [stock_i_idx]}
                    self.list_stocks.append(stock_info)

            # Pattern for all stocks
            # pattern = {'stock_idx': number, 'items': map[]}[]
            # map: (key-value) -> (prod_idx: {"quantity": number, "positions": number[][], "width": number, "height": number})
            
            # Initialize the pattern
            initial_patterns = []
            for stock_idx, stock in enumerate(initial_stocks):
                stock_w, stock_h = self._get_stock_size_(stock)
                stock_type = -1
                for s_idx,s in enumerate(self.list_stocks):
                    if s["width"] == stock_w and s["height"] == stock_h:
                        stock_type = s_idx
                        break
                pattern_element = {'key': '_' + str(stock_type) + '_','stock_idx': stock_idx, 'stock_type': stock_type, 'width': stock_w,'height': stock_h,'items': {}}
                initial_patterns.append(pattern_element)

            clone_stocks = initial_stocks
            clone_prods = initial_prods
            if len(self.indices_prods) == 0:
                self.indices_prods = list(range(len(clone_prods)))
            for _ in range(prod_num):
                heuristic_result = self.lazy_init_heuristic(clone_prods, clone_stocks, self.indices_prods)
                prod_idx = heuristic_result["prod_idx"]
                best_stock_idx = heuristic_result["stock_idx"]
                best_position = heuristic_result["position"]
                best_prod_size = heuristic_result["size"]
                # print("prod_idx: ", prod_idx, "best_stock_idx: ", best_stock_idx, "position: ", best_position, "prod_size: ", best_prod_size)
                clone_stocks, clone_prods = self.fill_to_clone_stocks(clone_stocks, clone_prods, prod_idx, best_stock_idx, best_position, best_prod_size)
                if prod_idx in initial_patterns[best_stock_idx]["items"]:
                    initial_patterns[best_stock_idx]["items"][prod_idx]["quantity"] += 1
                    initial_patterns[best_stock_idx]["items"][prod_idx]["positions"].append(best_position)
                    initial_patterns[best_stock_idx]["key"]+=str(prod_idx) + '_'
                else:
                    position_list = [best_position]
                    prod_w, prod_h = best_prod_size
                    initial_patterns[best_stock_idx]["items"][prod_idx] = {"quantity": 1, "positions": position_list, "width": prod_w, "height": prod_h }
                    initial_patterns[best_stock_idx]["key"]+=str(prod_idx) + '_'
            
            # Simplex method init
            D = np.array([])
            for prod in self.list_products:
                D=np.append(D,prod["quantity"])
            D = D.flatten()
            # print('D: ',D)

            S = np.array([])
            for stock in self.list_stocks:
                S=np.append(S,stock["quantity"])
            S = S.flatten()
            # print('S: ',S)

            # self.initial_patterns.append({'key': '_83_0_', 'stock_idx': 84, 'stock_type': 83, 'width': np.int64(51), 'height': np.int64(50), 'items': {0: {'quantity': 1, 'positions': [(0, 0)], 'width': np.int64(41), 'height': np.int64(45)}}})
            keys = []
            c = np.array([])
            for pattern in initial_patterns:
                if pattern["items"] == {}: continue   
                if pattern["key"] not in keys:
                    keys.append(pattern["key"])
                    unique_pattern = {"quantity": 0, "stock_type": pattern["stock_type"], "items": pattern["items"]}
                    self.optimal_patterns.append(unique_pattern)
                    area = pattern['width'] * pattern['height']
                    # print(unique_pattern)
                    c = np.append(c,area)
            c = c.flatten()
            # print('c: ', c)
        
            A = np.zeros(shape=(len(self.list_products),len(self.optimal_patterns))) # 11 row - 28 col
            for pattern_idx, pattern in enumerate(self.optimal_patterns):
                for prod_idx, value in pattern['items'].items():
                    # print(prod_index, ' ', value['quantity'])
                    A[prod_idx][pattern_idx] = value['quantity']
            # print('A: ', A)

            B = np.zeros(shape=(len(self.list_stocks),len(self.optimal_patterns))) # 97 row - 28 col
            for pattern_idx, pattern in enumerate(self.optimal_patterns):
                B[pattern["stock_type"]][pattern_idx] = 1
            # print('B: ', B)

            #### Simplex method
            # print((np.concatenate((A,B),axis=0)).shape)

            x_bounds = [(0,None) for _ in range(len(self.optimal_patterns))]
            result_simplex = linprog(c,A_ub=B,b_ub=S,A_eq=A,b_eq=D,bounds=x_bounds,method='highs',integrality=1)
            x = result_simplex.x
            x = np.int64(x)
            # print(x)
            dual_prods = result_simplex.eqlin['marginals']
            dual_stocks = result_simplex.ineqlin['marginals']
            for i in range(len(x)):
                self.optimal_patterns[i]['quantity'] = x[i]
                # self.optimal_patterns[i]['quantity'] = 1

            # 2 vector Dual_variable (về item + về loại stock) 
            # Mỗi loại stock, truyền vô cái Long làm 
            # => Trả về [số loại stock] pattern + profit tương ứng
            # Cầm đống pattern mới kiếm tính reduce cost
            reduce_costs = []
            for pattern_idx,pattern in enumerate(self.optimal_patterns):            
                # print(np.dot(A[:,pattern_idx],dual_prods.transpose()))
                reduce_cost = c[pattern_idx] - (np.dot(A[:,pattern_idx],dual_prods.transpose())  + dual_stocks[pattern['stock_type']])
                reduce_costs.append(reduce_cost)

        #     for i in range (len(reduce_costs)):
        #         if reduce_costs[i] < 0:
        #             # Bo vo RMP
        #             # Giai lai simplex
        #             print(reduce_costs[i])
            
        #     # result_simplex_milp = linprog(c,A_ub=B,b_ub=S,A_eq=A,b_eq=D,bounds=x_bounds,method='highs', integrality=1)
        #     # print(reduce_costs)
        #     # Âm -> Có pattern mới vào RMP -> Quay lại step 1
        #     # Dương -> Giải MILP để cho ra kết quả nguyên -> Siuuuuuuuuuuuuuu
        
        def fill_to_clone_stocks(self,clone_stocks, clone_prods, prod_idx, best_stock_idx, best_position, best_prod_size):
            x, y = best_position
            w, h = best_prod_size
            for i in range(x, x + w):
                for j in range(y, y + h):
                    clone_stocks[best_stock_idx][i][j] = prod_idx
            return clone_stocks, clone_prods

        def lazy_init_heuristic(self, clone_prods, clone_stocks, indices_prods):
            best_stock_idx, best_position, best_prod_size = -1, None, [0, 0]
            if not hasattr(self, 'sorted_prods'):
                self.sorted_prods = sorted(clone_prods, key=lambda p: p["size"][0] * p["size"][1], reverse=True)
                self.indices_prods = sorted(self.indices_prods, key=lambda i: clone_prods[i]["size"][0] * clone_prods[i]["size"][1], reverse=True)
                # self.sorted_prods = sorted(self.list_products, key=lambda p: (p["size"][0], p["size"][1]), reverse=True)
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
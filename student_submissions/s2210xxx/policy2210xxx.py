from policy import Policy
import numpy as np
from scipy.optimize import linprog
from copy import deepcopy
import itertools

class Policy2210xxx(Policy):    
    def __init__(self):
        self.optimal_patterns = []
        self.isComputing = True
        self.drawing_counter = -1
        self.drawing_data = []
        self.indices_prods = []
        self.indices_stocks = []
        self.list_stocks = []
        self.list_products = []

    def get_action(self, observation, info):
        if(self.isComputing):
            self.init_heuristic(observation,info)
            self.isComputing = False
            self.drawing_patterns()
            self.drawing_counter += 1
            dual_prods = [10,8] # dual_prods for generate pattern
            pattern = self.generate_pattern(dual_prods, 0) # generate pattern for stock type 0
            print("Pattern: ", pattern)
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
        
    def init_heuristic(self, observation, info):
        # Student code here
        initial_stocks = deepcopy(observation["stocks"])
        initial_prods = deepcopy(observation["products"])
        # prod_num = 0

        for prod_idx,prod in enumerate(initial_prods):
            prod_info = {'id': str(prod_idx),"width": prod["size"][0], "height": prod["size"][1], "quantity": prod["quantity"]}
            self.list_products.append(prod_info)
            # prod_num += prod["quantity"]
            prod_info = {'id': str(prod_idx) + '_rotated',"width": prod["size"][1], "height": prod["size"][0], "quantity": prod["quantity"]}
            self.list_products.append(prod_info)
        self.list_products.sort(key=lambda x: (-x['height'], -x['width']))

        for stock_i_idx,stock_i in enumerate(initial_stocks):
            stock_w, stock_h = self._get_stock_size_(stock_i)
            duplicated_stock_idx = -1
            for stock_idx,stock in enumerate(self.list_stocks):
                if min(stock_w,stock_h) == stock["width"] and max(stock_h,stock_w) == stock["length"]:
                    duplicated_stock_idx = stock_idx
                    break
            if duplicated_stock_idx != -1:
                self.list_stocks[duplicated_stock_idx]["quantity"] += 1
                self.list_stocks[duplicated_stock_idx]["stock_index"].append(stock_i_idx)
            else:
                stock_info = {'id': stock_i_idx,"width": min(stock_w,stock_h), "length": max(stock_h,stock_w), "quantity": 1, "stock_index": [stock_i_idx], 'used': 0, 'rotated': stock_h > stock_w }
                self.list_stocks.append(stock_info)
        self.list_stocks.sort(key=lambda x:x['width'] * x['length'])

        initial_patterns = []
        bin_counter = 0
        item_demand = {item['id']: item['quantity'] for item in self.list_products}

        for item in self.list_products:
            while item_demand[item['id']] > 0:
                # bin_class_id = b_i[item['id']]
                bin_class_id = self.choose_appropriate_stock_type_for_prod(self.list_stocks,item)
                bin_class = next(bc for bc in self.list_stocks if bc['id'] == bin_class_id)
    
                # Open a new bin of this class if possible
                bin_counter += 1
                # print('bin_class: ',bin_class)
                current_bin = {'id': bin_counter, 'bin_class_id': bin_class['id'], 'length': bin_class['length'], 'width': bin_class['width'], 'remaining_length': bin_class['length'], 'remaining_width': bin_class['width'], 'strips': []}
                initial_patterns.append(current_bin)

                while item_demand[item['id']] > 0 and current_bin['remaining_width'] >= item['height']:
                    # print(item['id'],': ',item_demand[item['id']])
                    # Initialize a new strip
                    strip_width = item['height']
                    strip_length = 0
                    strip_items = []

                    items_to_place = min(item_demand[item['id']],int(current_bin['length'] // item['width']))

                    if items_to_place == 0:
                        break  # Cannot place more items in this bin

                    # rows_needed = (items_to_place + max_items_in_row - 1) // max_items_in_row
                    strip_length = items_to_place * item['width']

                    if strip_width > current_bin['remaining_width']:
                        break  # Cannot place strip in remaining length

                    item_placement = {'item_class_id': item['id'], 'width': item['width'], 'height': item['height'],'quantity': items_to_place}
                    strip = {'length': strip_length, 'width': strip_width, 'items': [item_placement]}

                    # Update bin and item demand
                    current_bin['remaining_width'] -= strip_width
                    item_demand[item['id']] -= items_to_place
                    if('_rotated' in item['id']):
                        item_demand[item['id'].replace('_rotated','')] -= items_to_place
                    else:
                        item_demand[item['id'] + '_rotated'] -= items_to_place
                    # print(item['id'],': ',item_demand[item['id']])
                    # print(item['id'].replace('_rotated',''),': ',item_demand[item['id'].replace('_rotated','')])
                    # Fill the strip with smaller items if possible (greedy procedure)
                    
                    strip_remaining_length = current_bin['length'] - strip['length']
                    if strip_remaining_length > 0:
                        for next_item in self.list_products:
                            if item_demand[next_item['id']] > 0 and next_item['width'] <= strip_remaining_length and next_item['height'] <= strip_width:
                                items_to_place = min(item_demand[next_item['id']],int(strip_remaining_length // next_item['width']))
                                if(items_to_place > 0):
                                    item_placement = {'item_class_id': next_item['id'], 'width': next_item['width'], 'height': next_item['height'],'quantity': items_to_place}
                                    strip['items'].append(item_placement)
                                    item_demand[next_item['id']] -= items_to_place
                                    if('_rotated' in next_item['id']):
                                        item_demand[next_item['id'].replace('_rotated','')] -= items_to_place
                                    else:
                                        item_demand[next_item['id'] + '_rotated'] -= items_to_place
                                    strip['length'] += items_to_place * next_item['width']
                                    strip_remaining_length -= items_to_place * next_item['width']
                                    if strip_remaining_length <= 0:
                                        break
                    current_bin['strips'].append(strip)
                
                while current_bin['remaining_width'] > 0:
                    canPlaceMore = False
                    for sub_item in self.list_products:
                        if item_demand[sub_item['id']] > 0 and current_bin['remaining_width'] >= sub_item['height']:
                            canPlaceMore = True

                            strip_width = sub_item['height']
                            strip_length = 0
                            strip_items = []

                            items_to_place = min(item_demand[sub_item['id']],int(current_bin['length'] // sub_item['width']))

                            if items_to_place == 0:
                                break  # Cannot place more items in this bin

                            # rows_needed = (items_to_place + max_items_in_row - 1) // max_items_in_row
                            strip_length = items_to_place * sub_item['width']

                            if strip_width > current_bin['remaining_width']:
                                break  # Cannot place strip in remaining length

                            # item_placement = ItemPlacement(
                            #     item_class_id=item.id,
                            #     quantity=items_to_place,
                            #     position=(0, current_bin.length - current_bin.remaining_length)
                            # )
                            item_placement = {'item_class_id': sub_item['id'], 'width': sub_item['width'], 'height': sub_item['height'],'quantity': items_to_place}
                            # strip = Strip(
                            #     width=strip_width,
                            #     height=strip_height,
                            #     items=[item_placement]
                            # )
                            strip = {'length': strip_length, 'width': strip_width, 'items': [item_placement]}

                            # Update bin and item demand
                            current_bin['remaining_width'] -= strip_width
                            item_demand[sub_item['id']] -= items_to_place
                            if('_rotated' in sub_item['id']):
                                item_demand[sub_item['id'].replace('_rotated','')] -= items_to_place
                            else:
                                item_demand[sub_item['id'] + '_rotated'] -= items_to_place
                            
                            strip_remaining_length = current_bin['length'] - strip['length']
                            if strip_remaining_length > 0:
                                for next_item in self.list_products:
                                    if item_demand[next_item['id']] > 0 and next_item['width'] <= strip_remaining_length and next_item['height'] <= strip_width:
                                        items_to_place = min(item_demand[next_item['id']],int(strip_remaining_length // next_item['width']))
                                        if(items_to_place > 0):
                                            item_placement = {'item_class_id': next_item['id'],'width': next_item['width'], 'height': next_item['height'], 'quantity': items_to_place}
                                            strip['items'].append(item_placement)
                                            item_demand[next_item['id']] -= items_to_place
                                            if('_rotated' in next_item['id']):
                                                item_demand[next_item['id'].replace('_rotated','')] -= items_to_place
                                            else:
                                                item_demand[next_item['id'] + '_rotated'] -= items_to_place
                                            strip['length'] += items_to_place * next_item['width']
                                            strip_remaining_length -= items_to_place * next_item['width']
                                            if strip_remaining_length <= 0:
                                                break
                            current_bin['strips'].append(strip)
                    if canPlaceMore == False: break

        self.optimal_patterns = initial_patterns

        # for pattern in self.optimal_patterns:
        #     print(pattern)

    def choose_appropriate_stock_type_for_prod(self,list_stocks,item):
        max_items_in_bin = 0
        assigned_bin_class = None
        for bin_class in list_stocks:
            if bin_class['used'] < bin_class['quantity']:
                max_items = int((bin_class['width'] // item['height']) * (bin_class['length'] // item['width']))
                if max_items >= item['quantity']:
                    assigned_bin_class = bin_class
                    break
                elif max_items > max_items_in_bin:
                    max_items_in_bin = max_items
                    assigned_bin_class = bin_class
        if assigned_bin_class:
            # b_i[item['id']] = assigned_bin_class['id']
            assigned_bin_class['used'] += 1
            return assigned_bin_class['id']
        else:
            raise Exception(f"No available bin can accommodate item class {item['id']}")

    def get_stock_idx_to_draw(self,stock_type):
        for stock in self.list_stocks:
            if stock['id'] == stock_type:
                stock_idx = stock['stock_index'][0]
                stock['stock_index'].pop(0)
                rotated = stock['rotated']
                break
        return stock_idx, rotated

    def drawing_patterns(self):
        for data in self.optimal_patterns:
            stock_type = data['bin_class_id']
            stock_idx, rotated = self.get_stock_idx_to_draw(stock_type)
            # if(stock_idx == 2):
            #     stock_idx = 72
            # elif stock_idx == 7:
            #     stock_idx = 77
            # elif stock_idx == 0:
            #     stock_idx = 70
            x,y = 0,0
            if rotated:
                for strip in data['strips']:
                    for item in strip['items']:
                        for _ in range(item['quantity']):
                            size = (item['height'],item['width'])
                            position = (x,y)
                            y += item['width']
                            self.drawing_data.append({
                                'stock_idx': stock_idx,
                                'size': size,
                                'position': position,
                            })
                    x += strip['width']
                    y = 0
            else:
                for strip in data['strips']:
                    for item in strip['items']:
                        for _ in range (item['quantity']):
                            size = (item['width'],item['height'])
                            position = (x,y)
                            x += item['width']
                            self.drawing_data.append({
                                'stock_idx': stock_idx,
                                'size': size,
                                'position': position,
                            })
                    y += strip['width']
                    x = 0
    # You can add more functions if needed
    def generate_pattern(self, dual_prods, stock_type):
        #Initialize
        result = []
        stock_w = self.list_stocks[stock_type]['length']
        stock_h = self.list_stocks[stock_type]['width']
        product_widths = np.array([prod['width'] for prod in self.list_products])
        product_heights = np.array([prod['height'] for prod in self.list_products])
        # cut horizontal strips
        for i in range(len(product_heights)):
            if product_widths[i] > stock_w or product_heights[i] > stock_h:
                continue
            profit = np.zeros(stock_w + 1)
            itemCount = np.zeros((stock_w + 1, len(self.list_products)))
            for j in range(1, len(dual_prods)*2 + 1):
                p = dual_prods[int(j / 2) - 1]
                w = product_widths[j-1]
                if w > product_widths[i]:
                    continue
                for s in range(stock_w, 0, -1):
                    for d in range(1, min(self.list_products[j-1]["quantity"], stock_w // product_widths[j-1]) + 1):
                        if (s - (d * w) >= 0):
                            # if ((profit[int(s - (d * w))] + d * p) >= profit[s]):
                            profit[s] = profit[int(s - (d * w))] + d * p
                            itemCount[s][j-1] = d
                        else: 
                            break
            maxUse = 1000000000
            for j in range(len(dual_prods) * 2):
                if itemCount[stock_w][j] > 0:
                    maxUse = min(maxUse, self.list_products[j]["quantity"] // itemCount[stock_w][j])
            result.append({"strip": int(product_heights[i]), "profit": int(profit[stock_w]), "itemCount": itemCount[stock_w].astype(int), "maxUse": int(maxUse)})
        result = np.array(result)
        small_result = []
        prod_clone = deepcopy(self.list_products)
        for prod in prod_clone:
            if '_rotated' in prod['id']:
                prod['id'] = int(prod['id'].replace('_rotated', '')) * 2 + 1
            else:
                prod['id'] = int(prod['id']) * 2
        prod_clone.sort(key=lambda x: dual_prods[int(x['id'] / 2)], reverse=True)
        for strips in result:
            strips['profit'] = int(strips['profit'])
            strips['strip'] = int(strips['strip'])
            strips['maxUse'] = int(strips['maxUse'])
            for i in range(len(strips["itemCount"])):
                small_profit = 0
                small_l = 0
                array_cal = np.zeros(len(strips["itemCount"]), dtype=int)
                array_cal[i] = int(strips["itemCount"][i])
                temp_profit = array_cal[i] * dual_prods[int(i / 2)]
                if sum(array_cal) == 0:
                    continue
                small_result.append({"strip": int(strips["strip"]), "profit": int(temp_profit), "itemCount": array_cal.copy()})
                if prod_clone[i]["height"] > strips["strip"] or prod_clone[i]["width"] > strips["strip"]:
                    continue
                small_profit = array_cal[i] * dual_prods[int(i / 2)]
                small_l = product_widths[i] * array_cal[i]
                if small_l == stock_w:
                    small_result.append({"strip": int(strips["strip"]), "profit": int(small_profit), "itemCount": array_cal})
                    continue
                for j in range(len(prod_clone)):
                    if prod_clone[j]["height"] > stock_h or prod_clone[j]["width"] > stock_w:
                        continue
                    if prod_clone[j]["id"] == i:
                        continue
                    else:
                        for k in range(1, prod_clone[j]["quantity"] + 1):
                            if (small_l + product_widths[prod_clone[j]["id"]] <= stock_w):
                                array_cal[prod_clone[j]["id"]] += 1
                                small_profit += dual_prods[int(prod_clone[j]["id"] / 2)]
                                small_l += product_widths[j]
                            else:
                                continue
                small_result.append({"strip": int(strips["strip"]), "profit": int(small_profit), "itemCount": array_cal})
        prod_heights = [prod['height'] for prod in self.list_products]
        def find_combinations(heights, target, partial=[], start=0):
            if sum(partial) == target:
                combinations.append(tuple(partial))
            if sum(partial) >= target:
                return
            for i in range(start, len(heights)):
                find_combinations(heights, target, partial + [heights[i]], i)

        combinations = []
        find_combinations(prod_heights, stock_h)
        all_combinations = [tuple(map(int, combination)) for combination in combinations]
        final_combination = []
        seen = set()
        for combination in all_combinations:
            sorted_combination = tuple(sorted(combination))
            if sorted_combination not in seen:
                seen.add(sorted_combination)
                final_combination.append(combination)
        max_profit = 0
        max_result = []
        for combination in final_combination:
            profit_check = 0
            strip_list = combination
            strip_list = np.array(strip_list)
            strip_list = strip_list.tolist()
            strip_list.sort()
            small_result.sort(key=lambda x: (x["strip"], -x["profit"]))
            item_quantity = np.zeros(int(len(self.list_products)/2))
            for i in range(len(item_quantity)):
                item_quantity[i] = self.list_products[i*2]["quantity"]
            result_stock2 = []
            for strip_len in strip_list:
                matching_strips = [s for s in small_result if s['strip'] == strip_len]
                matching_strips.sort(key=lambda x: x['profit'], reverse=True)
                for strip in matching_strips:
                    can_use_strip = all(strip['itemCount'][idx] <= item_quantity[int(idx/2)] for idx in range(len(strip['itemCount'])))
                    if can_use_strip:
                        for idx in range(len(strip['itemCount'])):
                            item_quantity[int(idx/2)] -= strip['itemCount'][idx]
                        result_stock2.append(strip)
                        break
                    else:
                        continue
            for strip in result_stock2:
                profit_check += strip['profit']
            if profit_check > max_profit:
                print("Profit check: ", profit_check)
                max_profit = profit_check
                max_result = result_stock2
        result_stock = result_stock2
        print("Max profit: ", max_profit)
        return tuple(max_result)
        

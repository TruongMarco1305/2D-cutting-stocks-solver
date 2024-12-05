# import numpy as np

# def create_stock_with_boundaries(width, length, pattern="empty"):
#     """
#     Tạo stock với ranh giới rõ ràng cho random policy:
#     -2: Vùng ngoài stock (để random policy tính width/height)
#     -1: Vùng trong stock (có thể đặt)
#      0: Vùng bị chặn (không thể đặt)
#     """
#     # Tạo stock với padding cố định
#     padded_width, padded_length = width + 4, length + 4
#     data = np.full((padded_width, padded_length), -2, dtype=int)
    
#     # Vùng trong là -1 (có thể đặt)
#     data[2:width+2, 2:length+2] = -1
    
#     if pattern == "checkerboard":
#         for i in range(2, width+2, 2):
#             for j in range(2, length+2, 2):
#                 if i < width+2 and j < length+2:
#                     data[i, j] = 0
#     elif pattern == "random_holes":
#         num_holes = (width * length) // 25
#         for _ in range(num_holes):
#             x = np.random.randint(2, width+1)
#             y = np.random.randint(2, length+1)
#             hole_size = min(2, min(width+2-x, length+2-y))
#             data[x:x+hole_size, y:y+hole_size] = 0
    
#     return {
#         "width": padded_width,
#         "length": padded_length,
#         "data": data
#     }

# test_cases = {
#     # "case_1_all_different_sizes": {
#     #     "description": "100 stock với kích thước khác nhau",
#     #     "stocks": tuple([
#     #         create_stock_with_boundaries(10+i//2, 10+i//2, "empty") 
#     #         for i in range(100)
#     #     ]),
#     #     "products": [
#     #         {"size": np.array([2, 2]), "quantity": 500},
#     #         {"size": np.array([3, 3]), "quantity": 400},
#     #         {"size": np.array([4, 4]), "quantity": 300},
#     #     ],
#     # },

#     # "case_2_random_sizes": {
#     #     "description": "100 stock với kích thước ngẫu nhiên",
#     #     "stocks": tuple([
#     #         create_stock_with_boundaries(
#     #             np.random.randint(15, 40), 
#     #             np.random.randint(15, 40), 
#     #             "empty"
#     #         ) for _ in range(100)
#     #     ]),
#     #     "products": [
#     #         {"size": np.array([5, 5]), "quantity": 600},
#     #         {"size": np.array([8, 3]), "quantity": 400},
#     #         {"size": np.array([3, 8]), "quantity": 400},
#     #     ],
#     # },

#     # "case_3_same_size_different_products": {
#     #     "description": "100 stock cùng kích thước, nhiều loại sản phẩm",
#     #     "stocks": tuple([
#     #         create_stock_with_boundaries(30, 30, "empty") 
#     #         for _ in range(100)
#     #     ]),
#     #     "products": [
#     #         {"size": np.array([2, 2]), "quantity": 1000},
#     #         {"size": np.array([3, 3]), "quantity": 800},
#     #         {"size": np.array([5, 5]), "quantity": 500},
#     #         {"size": np.array([7, 7]), "quantity": 300},
#     #     ],
#     # },

#     # "case_4_product_larger_than_stock": {
#     #     "description": "100 stock, một số sản phẩm lớn hơn stock",
#     #     "stocks": tuple(
#     #         [create_stock_with_boundaries(10, 10, "empty") for _ in range(50)] +
#     #         [create_stock_with_boundaries(15, 15, "empty") for _ in range(50)]
#     #     ),
#     #     "products": [
#     #         {"size": np.array([8, 8]), "quantity": 100},
#     #         {"size": np.array([5, 5]), "quantity": 200},
#     #         {"size": np.array([12, 12]), "quantity": 30},
#     #         {"size": np.array([20, 20]), "quantity": 10},
#     #     ],
#     # },

#     # "case_5_exact_fit": {
#     #     "description": "100 stock, sản phẩm vừa khít",
#     #     "stocks": tuple(
#     #         [create_stock_with_boundaries(10, 10, "empty") for _ in range(50)] +
#     #         [create_stock_with_boundaries(20, 20, "empty") for _ in range(50)]
#     #     ),
#     #     "products": [
#     #         {"size": np.array([10, 10]), "quantity": 50},
#     #         {"size": np.array([20, 20]), "quantity": 50},
#     #         {"size": np.array([5, 5]), "quantity": 200},
#     #         {"size": np.array([4, 4]), "quantity": 250},
#     #     ],
#     # },

#     # "case_6_fragmented_stocks": {
#     #     "description": "100 stock với pattern checkerboard",
#     #     "stocks": tuple([
#     #         create_stock_with_boundaries(20, 20, "checkerboard") 
#     #         for _ in range(100)
#     #     ]),
#     #     "products": [
#     #         {"size": np.array([2, 2]), "quantity": 300},
#     #         {"size": np.array([3, 3]), "quantity": 200},
#     #         {"size": np.array([5, 5]), "quantity": 150},
#     #         {"size": np.array([8, 8]), "quantity": 100},
#     #     ],
#     # },

#     # "case_7_mixed_patterns": {
#     #     "description": "100 stock với nhiều pattern",
#     #     "stocks": tuple(
#     #         [create_stock_with_boundaries(30, 30, "empty") for _ in range(34)] +
#     #         [create_stock_with_boundaries(30, 30, "checkerboard") for _ in range(33)] +
#     #         [create_stock_with_boundaries(30, 30, "random_holes") for _ in range(33)]
#     #     ),
#     #     "products": [
#     #         {"size": np.array([2, 2]), "quantity": 800},
#     #         {"size": np.array([3, 3]), "quantity": 600},
#     #         {"size": np.array([4, 4]), "quantity": 400},
#     #         {"size": np.array([5, 5]), "quantity": 300},
#     #     ],
#     # },

#     # "case_8_large_products": {
#     #     "description": "100 stock, sản phẩm lớn",
#     #     "stocks": tuple([
#     #         create_stock_with_boundaries(30, 30, "empty") 
#     #         for _ in range(100)
#     #     ]),
#     #     "products": [
#     #         {"size": np.array([25, 25]), "quantity": 20},
#     #         {"size": np.array([20, 20]), "quantity": 30},
#     #         {"size": np.array([15, 15]), "quantity": 50},
#     #     ],
#     # },

#     # "case_9_progressive_difficulty": {
#     #     "description": "100 stock với độ khó tăng dần",
#     #     "stocks": tuple(
#     #         [create_stock_with_boundaries(20, 20, "empty") for _ in range(25)] +
#     #         [create_stock_with_boundaries(20, 20, "checkerboard") for _ in range(25)] +
#     #         [create_stock_with_boundaries(20, 20, "random_holes") for _ in range(25)] +
#     #         [create_stock_with_boundaries(15, 15, "empty") for _ in range(25)]
#     #     ),
#     #     "products": [
#     #         {"size": np.array([2, 2]), "quantity": 1200},
#     #         {"size": np.array([3, 3]), "quantity": 900},
#     #         {"size": np.array([4, 4]), "quantity": 600},
#     #         {"size": np.array([5, 5]), "quantity": 400},
#     #         {"size": np.array([6, 6]), "quantity": 300},
#     #     ],
#     # }, 
#     # "case_10_single_stock_type": {
#     #     "description": "100 stock cùng loại (30x30), tổng 500 sản phẩm",
#     #     "stocks": tuple([
#     #         create_stock_with_boundaries(80, 80, "empty") 
#     #         for _ in range(100)
#     #     ]),
#     #     "products": [
#     #         # Sản phẩm nhỏ (4 sản phẩm/stock)
#     #         {"size": np.array([10, 10]), "quantity": 20},   # Dễ đặt, nhiều cơ hội
#     #         # Sản phẩm vừa (2-3 sản phẩm/stock)
#     #         {"size": np.array([15, 15]), "quantity": 20},   
#     #         {"size": np.array([25, 25]), "quantity": 20},
#     #         # # Sản phẩm lớn (1 sản phẩm/stock)
#     #         {"size": np.array([50, 50]), "quantity": 20},  
#     #     ],
#     # }, 
#     # "case_11_single_stock_type": {
#     #     "description": "5 loại stock",
#     #     "stocks": tuple([create_stock_with_boundaries(50, 70, "empty") for _ in range(30)] 
#     #                     +
#     #         [create_stock_with_boundaries(65, 45, "empty") for _ in range(20)] +
#     #         [create_stock_with_boundaries(60, 40, "empty") for _ in range(20)]+
#     #         [create_stock_with_boundaries(30, 60, "empty") for _ in range(15)]+
#     #         [create_stock_with_boundaries(30, 50, "empty") for _ in range(15)]
#     #         ),
#     #     "products": [
#     #         # Sản phẩm nhỏ (4 sản phẩm/stock)
#     #         {"size": np.array([30, 20]), "quantity": 12},   # Dễ đặt, nhiều cơ hội
#     #         # Sản phẩm vừa (2-3 sản phẩm/stock)
#     #         {"size": np.array([25, 15]), "quantity": 10},   
#     #         {"size": np.array([20, 10]), "quantity": 18},   
#     #         {"size": np.array([15, 12]), "quantity": 15},
#     #         # # Sản phẩm lớn (1 sản phẩm/stock)
#     #         {"size": np.array([10, 10]), "quantity": 18}, 
#     #          {"size": np.array([5, 7]), "quantity": 20}, 
#     #          {"size": np.array([5, 7]), "quantity": 20}, 
#     #         {"size": np.array([40, 25]), "quantity": 17}, 
#     #          {"size": np.array([40, 50]), "quantity": 14}, 
#     #     ],
#     # }, 
#     "case_12_single_stock_type": {
#     "description": "3 loại stock",
#     "stocks": tuple(
#         [create_stock_with_boundaries(50, 70, "empty") for _ in range(40)] +
#         [create_stock_with_boundaries(60, 30, "empty") for _ in range(30)] +
#         [create_stock_with_boundaries(20, 80, "empty") for _ in range(30)]
#     ),
#     "products": [
#         # Nhóm sản phẩm nhỏ (4-6 sản phẩm/stock)
#         {"size": np.array([10, 20]), "quantity": 20},  # Phù hợp với tất cả các loại stock
#         {"size": np.array([15, 30]), "quantity": 15},  # Phù hợp với Stock 1 và Stock 2
#         {"size": np.array([20, 40]), "quantity": 10},  # Phù hợp với Stock 1 và Stock 3
        
#         # Nhóm sản phẩm trung bình (2-3 sản phẩm/stock)
#         {"size": np.array([30, 50]), "quantity": 12},  # Phù hợp với Stock 1
#         {"size": np.array([25, 30]), "quantity": 10},  # Phù hợp với Stock 2 và Stock 1
        
#         # Nhóm sản phẩm lớn (1-2 sản phẩm/stock)
#         {"size": np.array([40, 60]), "quantity": 8},   # Phù hợp với Stock 1
#         {"size": np.array([10, 70]), "quantity": 10},  # Phù hợp với Stock 3
#         {"size": np.array([15, 80]), "quantity": 6},   # Phù hợp với Stock 3
#     ],
# }
# }

# def validate_test_cases(test_cases):
#     """Kiểm tra tính hợp lệ của test cases với random policy"""
#     for case_name, case in test_cases.items():
#         stocks = case["stocks"]
#         products = case["products"]
        
#         # Kiểm tra số lượng stock
#         assert len(stocks) == 100, f"Case {case_name}: Cần đúng 100 stock"
        
#         # Kiểm tra định dạng và giá trị của mỗi stock
#         for i, stock in enumerate(stocks):
#             assert isinstance(stock, dict), f"Case {case_name}, Stock {i}: Phải là dictionary"
#             assert "data" in stock, f"Case {case_name}, Stock {i}: Thiếu key 'data'"
#             data = stock["data"]
#             assert isinstance(data, np.ndarray), f"Case {case_name}, Stock {i}: Data phải là numpy array"
#             assert -2 in data, f"Case {case_name}, Stock {i}: Phải có vùng ngoài (-2)"
#             assert -1 in data, f"Case {case_name}, Stock {i}: Phải có vùng trống (-1)"
            
#             # Kiểm tra vùng có thể đặt
#             placeable_area = np.any(data != -2, axis=1).sum()
#             assert placeable_area > 0, f"Case {case_name}, Stock {i}: Phải có vùng có thể đặt"
            
#         # Kiểm tra products
#         for product in products:
#             assert "size" in product, f"Case {case_name}: Product phải có size"
#             assert "quantity" in product, f"Case {case_name}: Product phải có quantity"
#             assert isinstance(product["size"], np.ndarray), f"Case {case_name}: Product size phải là numpy array"
            
#             # Kiểm tra kích thước sản phẩm
#             for stock in stocks:
#                 stock_width = stock["width"]
#                 stock_length = stock["length"]
#                 if product["size"][0] <= stock_width and product["size"][1] <= stock_length:
#                     break
#             else:
#                 print(f"Warning: Case {case_name} có sản phẩm size {product['size']} không thể đặt vào bất kỳ stock nào")

# # Chạy validation
# validate_test_cases(test_cases)
import numpy as np

def create_stock_with_boundaries(width, length, pattern="empty"):
    """
    Tạo stock với ranh giới rõ ràng
    width, length: kích thước thực của stock (không tính padding)
    """
    data = np.full((100, 100), -2, dtype=int)
    data[2:width+2, 2:length+2] = -1
    return {
        "width": 100,
        "length": 100,
        "data": data
    }

test_cases = {
    "case_single_stock_type": {
        "description": "100 stock cùng loại",
        "stocks": tuple(
            [create_stock_with_boundaries(90, 70, "empty") for _ in range(100)]
        ),
        "products": [
            # Products nhỏ
            {"size": np.array([20, 15]), "quantity": 20},
            {"size": np.array([25, 20]), "quantity": 18},
            {"size": np.array([30, 25]), "quantity": 15},
            # Products vừa
            {"size": np.array([40, 30]), "quantity": 12},
            {"size": np.array([45, 35]), "quantity": 10},
            # Products lớn
            {"size": np.array([50, 40]), "quantity": 8},
            {"size": np.array([60, 45]), "quantity": 5},
        ],
    },

    "case_three_stock_types": {
        "description": "3 loại stock khác nhau",
        "stocks": tuple(
            # Stock nhỏ: 60x45
            [create_stock_with_boundaries(60, 45, "empty") for _ in range(34)] +
            # Stock vừa: 75x60
            [create_stock_with_boundaries(75, 60, "empty") for _ in range(33)] +
            # Stock lớn: 90x80
            [create_stock_with_boundaries(90, 80, "empty") for _ in range(33)]
        ),
        "products": [
            # Products phù hợp với stock nhỏ
            {"size": np.array([20, 15]), "quantity": 20},
            {"size": np.array([30, 25]), "quantity": 15},
            {"size": np.array([40, 30]), "quantity": 12},
            # Products phù hợp với stock vừa
            {"size": np.array([45, 40]), "quantity": 10},
            {"size": np.array([50, 45]), "quantity": 8},
            # Products chỉ phù hợp với stock lớn
            {"size": np.array([70, 50]), "quantity": 6},
            {"size": np.array([80, 60]), "quantity": 4},
        ],
    },

    "case_five_stock_types": {
        "description": "5 loại stock khác nhau",
        "stocks": tuple(
            # Stock type 1: 40x50
            [create_stock_with_boundaries(40, 50, "empty") for _ in range(20)] +
            # Stock type 2: 55x45
            [create_stock_with_boundaries(55, 45, "empty") for _ in range(20)] +
            # Stock type 3: 70x60
            [create_stock_with_boundaries(70, 60, "empty") for _ in range(20)] +
            # Stock type 4: 80x65
            [create_stock_with_boundaries(80, 65, "empty") for _ in range(20)] +
            # Stock type 5: 95x75
            [create_stock_with_boundaries(95, 75, "empty") for _ in range(20)]
        ),
        "products": [
            # Products phù hợp với stock nhỏ nhất
            {"size": np.array([20, 15]), "quantity": 20},
            {"size": np.array([25, 20]), "quantity": 18},
            # Products phù hợp với stock vừa
            {"size": np.array([35, 30]), "quantity": 15},
            {"size": np.array([40, 35]), "quantity": 12},
            {"size": np.array([45, 40]), "quantity": 10},
            # Products phù hợp với stock lớn
            {"size": np.array([50, 45]), "quantity": 8},
            {"size": np.array([60, 50]), "quantity": 6},
            # Products chỉ phù hợp với stock lớn nhất
            {"size": np.array([70, 55]), "quantity": 4},
            {"size": np.array([85, 65]), "quantity": 3},
        ],
    },
}

def validate_test_cases(test_cases):
    for case_name, case in test_cases.items():
        stocks = case["stocks"]
        products = case["products"]
        
        # Kiểm tra số lượng stock
        assert len(stocks) == 100, f"Case {case_name}: Cần đúng 100 stock"
        
        # Kiểm tra kích thước stock và product
        for i, stock in enumerate(stocks):
            data = stock["data"]
            usable_area = (data == -1)
            stock_width = np.sum(np.any(usable_area, axis=1))
            stock_height = np.sum(np.any(usable_area, axis=0))
            
            assert stock_width >= 40 and stock_width <= 100, \
                f"Case {case_name}, Stock {i}: Width phải từ 40-100, hiện tại là {stock_width}"
            assert stock_height >= 40 and stock_height <= 100, \
                f"Case {case_name}, Stock {i}: Height phải từ 40-100, hiện tại là {stock_height}"

        # Kiểm tra số lượng và kích thước của products
        for prod_idx, product in enumerate(products):
            assert product["quantity"] <= 20, \
                f"Case {case_name}, Product {prod_idx}: Số lượng không được vượt quá 20"
            
            # Kiểm tra kích thước product phải nhỏ hơn hoặc bằng ít nhất một stock
            prod_width, prod_height = product["size"]
            valid_size = False
            
            for stock in stocks:
                data = stock["data"]
                usable_area = (data == -1)
                stock_width = np.sum(np.any(usable_area, axis=1))
                stock_height = np.sum(np.any(usable_area, axis=0))
                
                if prod_width <= stock_width and prod_height <= stock_height:
                    valid_size = True
                    break
                    
            assert valid_size, \
                f"Case {case_name}, Product {prod_idx}: Size {product['size']} lớn hơn mọi stock"

# Chạy validation
validate_test_cases(test_cases)



import numpy as np

def create_stock_with_boundaries(width, length, pattern="empty"):
    """
    Tạo stock với ranh giới rõ ràng cho random policy:
    -2: Vùng ngoài stock (để random policy tính width/height)
    -1: Vùng trong stock (có thể đặt)
     0: Vùng bị chặn (không thể đặt)
    """
    # Tạo stock với padding cố định
    padded_width, padded_length = width + 4, length + 4
    data = np.full((padded_width, padded_length), -2, dtype=int)
    
    # Vùng trong là -1 (có thể đặt)
    data[2:width+2, 2:length+2] = -1
    
    if pattern == "checkerboard":
        for i in range(2, width+2, 2):
            for j in range(2, length+2, 2):
                if i < width+2 and j < length+2:
                    data[i, j] = 0
    elif pattern == "random_holes":
        num_holes = (width * length) // 25
        for _ in range(num_holes):
            x = np.random.randint(2, width+1)
            y = np.random.randint(2, length+1)
            hole_size = min(2, min(width+2-x, length+2-y))
            data[x:x+hole_size, y:y+hole_size] = 0
    
    return {
        "width": padded_width,
        "length": padded_length,
        "data": data
    }

test_cases = {
    "case_1_all_different_sizes": {
        "description": "100 stock với kích thước khác nhau",
        "stocks": tuple([
            create_stock_with_boundaries(10+i//2, 10+i//2, "empty") 
            for i in range(100)
        ]),
        "products": [
            {"size": np.array([2, 2]), "quantity": 500},
            {"size": np.array([3, 3]), "quantity": 400},
            {"size": np.array([4, 4]), "quantity": 300},
        ],
    },

    "case_2_random_sizes": {
        "description": "100 stock với kích thước ngẫu nhiên",
        "stocks": tuple([
            create_stock_with_boundaries(
                np.random.randint(15, 40), 
                np.random.randint(15, 40), 
                "empty"
            ) for _ in range(100)
        ]),
        "products": [
            {"size": np.array([5, 5]), "quantity": 600},
            {"size": np.array([8, 3]), "quantity": 400},
            {"size": np.array([3, 8]), "quantity": 400},
        ],
    },

    "case_3_same_size_different_products": {
        "description": "100 stock cùng kích thước, nhiều loại sản phẩm",
        "stocks": tuple([
            create_stock_with_boundaries(30, 30, "empty") 
            for _ in range(100)
        ]),
        "products": [
            {"size": np.array([2, 2]), "quantity": 1000},
            {"size": np.array([3, 3]), "quantity": 800},
            {"size": np.array([5, 5]), "quantity": 500},
            {"size": np.array([7, 7]), "quantity": 300},
        ],
    },

    "case_4_product_larger_than_stock": {
        "description": "100 stock, một số sản phẩm lớn hơn stock",
        "stocks": tuple(
            [create_stock_with_boundaries(10, 10, "empty") for _ in range(50)] +
            [create_stock_with_boundaries(15, 15, "empty") for _ in range(50)]
        ),
        "products": [
            {"size": np.array([8, 8]), "quantity": 100},
            {"size": np.array([5, 5]), "quantity": 200},
            {"size": np.array([12, 12]), "quantity": 30},
            {"size": np.array([20, 20]), "quantity": 10},
        ],
    },

    "case_5_exact_fit": {
        "description": "100 stock, sản phẩm vừa khít",
        "stocks": tuple(
            [create_stock_with_boundaries(10, 10, "empty") for _ in range(50)] +
            [create_stock_with_boundaries(20, 20, "empty") for _ in range(50)]
        ),
        "products": [
            {"size": np.array([10, 10]), "quantity": 50},
            {"size": np.array([20, 20]), "quantity": 50},
            {"size": np.array([5, 5]), "quantity": 200},
            {"size": np.array([4, 4]), "quantity": 250},
        ],
    },

    "case_6_fragmented_stocks": {
        "description": "100 stock với pattern checkerboard",
        "stocks": tuple([
            create_stock_with_boundaries(20, 20, "checkerboard") 
            for _ in range(100)
        ]),
        "products": [
            {"size": np.array([2, 2]), "quantity": 300},
            {"size": np.array([3, 3]), "quantity": 200},
            {"size": np.array([5, 5]), "quantity": 150},
            {"size": np.array([8, 8]), "quantity": 100},
        ],
    },

    "case_7_mixed_patterns": {
        "description": "100 stock với nhiều pattern",
        "stocks": tuple(
            [create_stock_with_boundaries(30, 30, "empty") for _ in range(34)] +
            [create_stock_with_boundaries(30, 30, "checkerboard") for _ in range(33)] +
            [create_stock_with_boundaries(30, 30, "random_holes") for _ in range(33)]
        ),
        "products": [
            {"size": np.array([2, 2]), "quantity": 800},
            {"size": np.array([3, 3]), "quantity": 600},
            {"size": np.array([4, 4]), "quantity": 400},
            {"size": np.array([5, 5]), "quantity": 300},
        ],
    },

    "case_8_large_products": {
        "description": "100 stock, sản phẩm lớn",
        "stocks": tuple([
            create_stock_with_boundaries(30, 30, "empty") 
            for _ in range(100)
        ]),
        "products": [
            {"size": np.array([25, 25]), "quantity": 20},
            {"size": np.array([20, 20]), "quantity": 30},
            {"size": np.array([15, 15]), "quantity": 50},
        ],
    },

    "case_9_progressive_difficulty": {
        "description": "100 stock với độ khó tăng dần",
        "stocks": tuple(
            [create_stock_with_boundaries(20, 20, "empty") for _ in range(25)] +
            [create_stock_with_boundaries(20, 20, "checkerboard") for _ in range(25)] +
            [create_stock_with_boundaries(20, 20, "random_holes") for _ in range(25)] +
            [create_stock_with_boundaries(15, 15, "empty") for _ in range(25)]
        ),
        "products": [
            {"size": np.array([2, 2]), "quantity": 1200},
            {"size": np.array([3, 3]), "quantity": 900},
            {"size": np.array([4, 4]), "quantity": 600},
            {"size": np.array([5, 5]), "quantity": 400},
            {"size": np.array([6, 6]), "quantity": 300},
        ],
    }
}

def validate_test_cases(test_cases):
    """Kiểm tra tính hợp lệ của test cases với random policy"""
    for case_name, case in test_cases.items():
        stocks = case["stocks"]
        products = case["products"]
        
        # Kiểm tra số lượng stock
        assert len(stocks) == 100, f"Case {case_name}: Cần đúng 100 stock"
        
        # Kiểm tra định dạng và giá trị của mỗi stock
        for i, stock in enumerate(stocks):
            assert isinstance(stock, dict), f"Case {case_name}, Stock {i}: Phải là dictionary"
            assert "data" in stock, f"Case {case_name}, Stock {i}: Thiếu key 'data'"
            data = stock["data"]
            assert isinstance(data, np.ndarray), f"Case {case_name}, Stock {i}: Data phải là numpy array"
            assert -2 in data, f"Case {case_name}, Stock {i}: Phải có vùng ngoài (-2)"
            assert -1 in data, f"Case {case_name}, Stock {i}: Phải có vùng trống (-1)"
            
            # Kiểm tra vùng có thể đặt
            placeable_area = np.any(data != -2, axis=1).sum()
            assert placeable_area > 0, f"Case {case_name}, Stock {i}: Phải có vùng có thể đặt"
            
        # Kiểm tra products
        for product in products:
            assert "size" in product, f"Case {case_name}: Product phải có size"
            assert "quantity" in product, f"Case {case_name}: Product phải có quantity"
            assert isinstance(product["size"], np.ndarray), f"Case {case_name}: Product size phải là numpy array"
            
            # Kiểm tra kích thước sản phẩm
            for stock in stocks:
                stock_width = stock["width"]
                stock_length = stock["length"]
                if product["size"][0] <= stock_width and product["size"][1] <= stock_length:
                    break
            else:
                print(f"Warning: Case {case_name} có sản phẩm size {product['size']} không thể đặt vào bất kỳ stock nào")

# Chạy validation
validate_test_cases(test_cases)


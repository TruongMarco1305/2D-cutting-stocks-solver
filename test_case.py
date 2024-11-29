import numpy as np

test_cases = {
    "case_1_fully_empty": {
        "stocks": [{"width": 10, "length": 10} for _ in range(100)],
        "products": [
            {"size": np.array([3, 3]), "quantity": 10},  # Sản phẩm nhỏ
            {"size": np.array([5, 5]), "quantity": 5},   # Sản phẩm vừa
        ],
    },
    "case_2_partial_filled": {
        "stocks": [
            {
                "width": 10,
                "length": 10,
                "data": [
                    [-1, -1, -1, -1, -1, 0, 0, -2, -2, -2],
                    [-1, -1, -1, -1, -1, 0, 0, -2, -2, -2],
                    [-1, -1, -1, -1, -1, 1, 1, -2, -2, -2],
                    [-1, -1, -1, -1, -1, 1, 1, -2, -2, -2],
                    [-1, -1, -1, -1, -1, -1, -1, -2, -2, -2],
                ],
            }
            for _ in range(50)
        ],
        "products": [
            {"size": np.array([2, 2]), "quantity": 10},  # Sản phẩm rất nhỏ
            {"size": np.array([4, 4]), "quantity": 8},   # Sản phẩm lớn
        ],
    },
    "case_3_non_rectangular": {
        "stocks": [
            {
                "width": 8,
                "length": 12,
                "data": [
                    [-1, -1, -1, -2, -2, -2, -2, -2],
                    [-1, -1, -1, -2, -2, -2, -2, -2],
                    [-1, -1, -1, -2, -2, -2, -2, -2],
                    [-1, -1, -1, -1, -1, -1, -2, -2],
                    [-1, -1, -1, -1, -1, -1, -2, -2],
                ],
            }
        ],
        "products": [
            {"size": np.array([2, 3]), "quantity": 15},  # Sản phẩm dạng chữ nhật
            {"size": np.array([1, 5]), "quantity": 10},  # Sản phẩm dạng dài
        ],
    },
    "case_4_large_products": {
        "stocks": [{"width": 50, "length": 50} for _ in range(20)],
        "products": [
            {"size": np.array([45, 45]), "quantity": 10},  # Sản phẩm chiếm gần hết diện tích
            {"size": np.array([20, 20]), "quantity": 5},   # Sản phẩm vừa
        ],
    },
    "case_5_sparse_products": {
        "stocks": [{"width": 30, "length": 30} for _ in range(10)],
        "products": [
            {"size": np.array([5, 5]), "quantity": 2},     # Số lượng nhỏ
            {"size": np.array([10, 10]), "quantity": 1},   # Sản phẩm lớn hơn
        ],
    },
    "case_6_mixed_random": {
        "stocks": [{"width": 20, "length": 20} for _ in range(100)],
        "products": [
            {"size": np.array([3, 3]), "quantity": 30},
            {"size": np.array([7, 5]), "quantity": 20},
            {"size": np.array([10, 10]), "quantity": 15},
        ],
    },
}
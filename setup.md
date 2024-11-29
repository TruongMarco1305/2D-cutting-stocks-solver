
git clone git@github.com:martinakaduc/gym-cutting-stock.git

# sau đó vào file cutting_stock_copy.py copy toàn bộ nội dung trong file này và paste vào file gym-cutting-stock/gym_cutting_stock/envs/cutting_stock.py

python3 -m venv venv

# on mac ó
source venv/bin/activate 

# on windows ( không chắc lắm :))) 
venv\Scripts\activate


cd gym-cutting-stock


pip install -e .


cd ..

pip install gymnasium


pip install numpy


pip install matplotlib


pip install pygame



python main.py

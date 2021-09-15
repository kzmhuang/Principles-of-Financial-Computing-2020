Language: Python 3.6.4

packages:
numpy

How to execute:
python3 hw3.py S X H T r s n k

The inputs as below:
 (1) S (spot price), (2) X (strike price), (3) H (barrier price), (4) T (years), (5) r (risk-free interest rate), (6) s (volatility), (7) n (number of periods), and (8) k (number of simulation paths)

The output will be:
<puts price> <standard error> <delta>



Example:
python3 hw3.py 100 100 110 1 0.05 0.30 250 10000

output:
5.4523 0.0800 -0.0086
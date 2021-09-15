Language: Python 3.6.4

How to execute:
python3 hw2.py

Input variables are in input.txt
Format of input.txt:
S (stock price)
X (strike price)
r (continuously compounded annual interest rate in percentage, including the percent sign "%")
s (annual volatility in percentage, including the percent sign "%")
T (time to maturity in days, which of course is also an exercise date)
E (set of early exercise dates from now)
m (number of periods per day for the tree)

example:
input.txt:
100
110
3%
30%
60
[10, 20, 30, 40, 50]
5

The program will output:
put price of Bermuda option: 11.2486
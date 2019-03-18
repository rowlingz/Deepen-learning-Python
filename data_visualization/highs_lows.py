# -*- coding:utf-8 -*-

import csv
import matplotlib.pyplot as plt
from datetime import datetime


filename = "sitka_weather_2014.csv"
filename_1 = "death_valley_2014.csv"
with open(filename_1) as f:
    reader = csv.reader(f)
    header_row = next(reader)
    # print(header_row)

    # for index, column_header in enumerate(header_row):
    #     print(index, column_header)

    dates, highs, lows = [], [], []
    for row in reader:
        try:
            current_date = datetime.strptime(row[0], "%Y-%m-%d")
            high = int(row[1])
            low = int(row[3])
        except ValueError:
            print(current_date, 'missing data')
        else:
            dates.append(current_date)
            highs.append(int(row[1]))
            lows.append(int(row[3]))

    print(highs)

fig = plt.figure(dpi=128, figsize=(10, 6))
plt.plot(dates, highs, c='red')
plt.plot(dates, lows, c='blue')

# fill_between()方法填充两条线之间区域
plt.fill_between(dates, highs, lows, facecolor='blue', alpha=0.1)
plt.title("Daily high and low temperatures - 2014", fontsize=24)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.xlabel("", fontsize=14)
fig.autofmt_xdate()
plt.ylabel("Temperature(F)", fontsize=14)

plt.show()

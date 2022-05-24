import csv
from datetime import datetime

from matplotlib import pyplot as plt

filename = 'data/death_valley_2018_simple.csv'
with open(filename) as file:
    reader = csv.reader(file)
    header_row = next(reader)

    dates, highs, lows = [], [], []
    for row in reader:
        try:
            high = int(row[4])
            low = int(row[5])
            date = datetime.strptime(row[2], '%Y-%m-%d')
        except ValueError:
            print(f"Missing data for {date}")
        else:
            highs.append(high)
            lows.append(low)
            dates.append(date)

    plt.style.use('seaborn')
    fig, ax = plt.subplots()
    ax.plot(dates, highs, c='red', alpha=0.5)
    ax.plot(dates, lows, c='blue', alpha=0.5)
    plt.fill_between(dates, highs, lows, facecolor='blue', alpha=0.2)

    plt.title("Daily high and low temperatures - 2018\nDeath Value, CA", fontsize=20)
    plt.xlabel("", fontsize=16)
    fig.autofmt_xdate()
    plt.ylabel("Temperature(F)", fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=16)

    plt.show()

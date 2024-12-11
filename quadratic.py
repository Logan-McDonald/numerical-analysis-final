import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime

def feedCSVData(file):
    data_frame = pd.read_csv(file)
    
    # Extract dates from the CSV file
    dates = data_frame["date_of_interest"].tolist()
    
    # Convert string dates to datetime objects
    dates = [datetime.strptime(date, '%m/%d/%Y') for date in dates]
    
    case_count = data_frame["CASE_COUNT"].tolist()
    
    return dates, case_count

def quadratic_spline(dates, case_count):
    # Convert dates to numeric format for interpolation
    numeric_dates = mdates.date2num(dates)

    # Initialize arrays for quadratic spline parameters
    a = []
    b = []
    c = []
    z = [0]  # Start with z0 = 0 as per boundary condition

    # Compute z values using recurrence relation
    for i in range(len(case_count) - 1):
        h = numeric_dates[i + 1] - numeric_dates[i]
        delta = (case_count[i + 1] - case_count[i]) / h
        z_next = -z[i] + 2 * delta
        z.append(z_next)

    # Compute quadratic coefficients for each interval
    for i in range(len(case_count) - 1):
        h = numeric_dates[i + 1] - numeric_dates[i]
        a_i = (z[i + 1] - z[i]) / (2 * h)
        b_i = z[i]
        c_i = case_count[i]
        a.append(a_i)
        b.append(b_i)
        c.append(c_i)

    # Generate dense points for smooth plotting
    dense_dates = []
    dense_case_count = []

    for i in range(len(case_count) - 1):
        h = numeric_dates[i + 1] - numeric_dates[i]
        x_vals = np.linspace(numeric_dates[i], numeric_dates[i + 1], 100)
        y_vals = (
            a[i] * (x_vals - numeric_dates[i]) ** 2 +
            b[i] * (x_vals - numeric_dates[i]) +
            c[i]
        )
        dense_dates.extend(x_vals)
        dense_case_count.extend(y_vals)

    # Plot the results
    plt.figure(figsize=(12, 6))
    plt.plot(mdates.num2date(dense_dates), dense_case_count, label='Quadratic Spline Interpolation', color='blue')
    plt.scatter(dates, case_count, color='red', label='Original Data', zorder=5)

    plt.title('Quadratic Spline Interpolation')
    plt.xlabel('Date')
    plt.ylabel('Case Count')
    plt.grid(alpha=0.5)
    plt.legend()

    # Format x-axis to show dates properly
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.gcf().autofmt_xdate()  # Rotate and align the tick labels

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    file = "COVID-19_Daily_Counts_of_Cases__Hospitalizations__and_Deaths.csv"
    dates, case_count = feedCSVData(file)
    
    quadratic_spline(dates, case_count)

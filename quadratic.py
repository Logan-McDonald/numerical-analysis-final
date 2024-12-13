import pandas
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime

def feedCSVData(file):
    data_frame = pandas.read_csv(file)
    
    # Extract dates and case counts
    dates = data_frame["date_of_interest"].tolist()
    case_count = data_frame["CASE_COUNT"].tolist()
    
    # Convert string dates to datetime objects
    dates = [datetime.strptime(date, '%m/%d/%Y') for date in dates]
    
    return dates, case_count

def quadratic_spline_segment(dates, case_count):
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

    return dense_dates, dense_case_count

def quadratic_spline(file, reset_date, step, step2):
    
    dates, case_count = feedCSVData(file)
    plt.figure(figsize=(12, 6))
    plt.scatter(dates, case_count, color='green', label='Original Data', zorder=5)
    
    # Split the data into two segments: before and after the reset date
    reset_date = datetime.strptime(reset_date, '%Y-%m-%d')
    split_index = next(i for i, date in enumerate(dates) if date >= reset_date)
    
    # Interpolate each segment separately
    dense_dates_before, dense_case_count_before = quadratic_spline_segment(dates[:split_index:step], case_count[:split_index:step])
    dense_dates_after, dense_case_count_after = quadratic_spline_segment(dates[split_index::step], case_count[split_index::step])
    # Combine the results
    dense_dates = dense_dates_before + dense_dates_after
    dense_case_count = dense_case_count_before + dense_case_count_after
    plt.plot(mdates.num2date(dense_dates), dense_case_count, label=f'Quadratic Spline Interpolation of {100/step}% of the data', color='blue')
    
    dense_case_count2 = None
    if step2 != None:
        # Interpolate each segment separately
        dense_dates_before, dense_case_count_before = quadratic_spline_segment(dates[:split_index:step2], case_count[:split_index:step2])
        dense_dates_after, dense_case_count_after = quadratic_spline_segment(dates[split_index::step2], case_count[split_index::step2])
        # Combine the results
        dense_dates2 = dense_dates_before + dense_dates_after
        dense_case_count2 = dense_case_count_before + dense_case_count_after
        plt.plot(mdates.num2date(dense_dates2), dense_case_count2, label=f'Quadratic Spline Interpolation of {100/step2}% of the data', color='red')

    plt.title('Quadratic Spline Interpolation with Reset')
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
    
    return dense_case_count, dense_case_count2
    
def MSE(actual_list, predicted_list, step, step2):
    step = 100/step
    step2 = 100/step2
    mse = 0
    for x, x_hat in zip(actual_list[::int(step)], predicted_list[::int(step2)]):
        mse += (x - x_hat)**2
    final_mse = (1/(len(actual_list)-1)) * mse
    
    return np.sqrt(final_mse)

if __name__ == "__main__":
    file = "COVID-19_Daily_Counts_of_Cases__Hospitalizations__and_Deaths.csv"
    reset_date = "2022-01-28"
    type_graph = input("What type of graph would you like to produce? (C for compartative or S for single): ").lower()
    
    if type_graph == "s":
        step = int(input("What percentage of the data would you like to see? (100, 50, 25, or 10): "))
        step = int(100/step)
        step2 = None
        
        actual_list, predicted_list = quadratic_spline(file, reset_date, step, step2)
    elif type_graph == "c":
        step = int(input("What percentage of the data would you like to see for the first line? (100, 50, 25, or 10): "))
        step = int(100/step)
        
        step2 = int(input("What percentage of the data would you like to see for the second line? (100, 50, 25, or 10): "))
        step2 = int(100/step2)
        
        actual_list, predicted_list = quadratic_spline(file, reset_date, step, step2)
        print(f'Mean squared error between {int(100/step)}% and {int(100/step2)}% of data = {MSE(actual_list, predicted_list, step, step2):.2f}')
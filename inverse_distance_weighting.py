import pandas as pd # type: ignore
import matplotlib.pyplot as plt # type: ignore
import numpy as np # type: ignore
import matplotlib.dates as mdates # type: ignore
from datetime import datetime

def feedCSVData(file, step=1):
    data_frame = pd.read_csv(file)
    
    # Extract dates and case counts
    all_dates = data_frame["date_of_interest"].tolist()
    all_case_count = data_frame["CASE_COUNT"].tolist()
    
    # Select data points based on step
    dates = all_dates[::step]
    case_count = all_case_count[::step]
    
    # Convert string dates to datetime objects
    dates = [datetime.strptime(date, '%m/%d/%Y') for date in dates]
    return dates, case_count

def inverse_distance_weighting(dates, case_count, num_points=100):
    date_nums = mdates.date2num(dates)
    
    x_interp = np.linspace(min(date_nums), max(date_nums), num_points)
    y_interp = []

    for x in x_interp:
        distances = np.abs(date_nums - x)
        weights = 1 / (distances + 1e-6)  # Do NOT divide by zero, so add a small epsilon to avoid that here
        
        y_value = np.sum(weights * case_count) / np.sum(weights)
        y_interp.append(y_value)

    x_interp_dates = mdates.num2date(x_interp)
    return x_interp_dates, y_interp

def plot_idw_comparison(file, step1, step2=None, num_points=100):
    full_dates, full_case_count = feedCSVData(file, step=1)

    plt.figure(figsize=(12, 6))
    plt.scatter(full_dates, full_case_count, color='green', label='Original Points')

    dates1, case_count1 = feedCSVData(file, step=step1)
    x_interp1, y_interp1 = inverse_distance_weighting(dates1, case_count1, num_points=num_points)
    plt.plot(x_interp1, y_interp1, label=f'IDW Interpolation {int(100/step1)}% of data', color='blue')

    y_interp2 = None
    if step2 is not None:
        dates2, case_count2 = feedCSVData(file, step=step2)
        x_interp2, y_interp2 = inverse_distance_weighting(dates2, case_count2, num_points=num_points)
        plt.plot(x_interp2, y_interp2, label=f'IDW Interpolation {int(100/step2)}% of data', color='red')

    plt.title('Inverse Distance Weighting Interpolation')
    plt.xlabel('Dates')
    plt.ylabel('Case Count')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.gcf().autofmt_xdate()
    plt.grid(alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()

    return y_interp1, y_interp2

def calculate_rmse(y_actual, y_predicted):
    y_predicted_resampled = np.interp(
        np.linspace(0, 1, len(y_actual)),
        np.linspace(0, 1, len(y_predicted)),
        y_predicted
    )

    mse = np.mean((np.array(y_actual) - np.array(y_predicted_resampled)) ** 2)
    return np.sqrt(mse)

if __name__ == "__main__":
    file = "COVID-19_Daily_Counts_of_Cases__Hospitalizations__and_Deaths.csv"
    type_graph = input("What type of graph would you like to produce? (C for comparative or S for single): ").lower()

    if type_graph == "s":
        step = int(input("What percentage of the data would you like to see? (100, 50, 25, or 10): "))
        step = int(100 / step)
        y_interp1, _ = plot_idw_comparison(file, step1=step)
    elif type_graph == "c":
        step1 = int(input("What percentage of the data would you like to see for the first line? (100, 50, 25, or 10): "))
        step1 = int(100 / step1)

        step2 = int(input("What percentage of the data would you like to see for the second line? (100, 50, 25, or 10): "))
        step2 = int(100 / step2)

        y_interp1, y_interp2 = plot_idw_comparison(file, step1=step1, step2=step2)

        if y_interp2 is not None:
            rmse = calculate_rmse(y_interp1, y_interp2)
            print(f"Root Mean Squared Error (RMSE) between {int(100/step1)}% and {int(100/step2)}% of data: {rmse:.4f}")

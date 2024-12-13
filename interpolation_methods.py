import pandas
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime, timedelta

def feedCSVData(file, step):
    data_frame = pandas.read_csv(file)
    
    # Extract dates and case counts
    all_dates = data_frame["date_of_interest"].tolist()
    all_case_count = data_frame["CASE_COUNT"].tolist()
    
    # Select data points based on step
    dates = all_dates[::step]
    case_count = all_case_count[::step]
    
    # Convert string dates to datetime objects
    dates = [datetime.strptime(date, '%m/%d/%Y') for date in dates]
    
    return dates, case_count
    
def piecewise(file, step, step2=None):
    
    def eq(dates, case_count):

        x_interp = []
        y_interp = []

        # Perform linear interpolation for each segment
        for i in range(len(dates)-1):
            x1, y1 = dates[i], case_count[i]
            x2, y2 = dates[i+1], case_count[i+1]
            
            # Generate x values for this segment
            x_segment = np.linspace(0, 1, 100)  # Normalized interpolation
            x_segment = [x1 + (x2 - x1) * t for t in x_segment]
            y_segment = y1 + ((y2-y1)/(mdates.date2num(x2)-mdates.date2num(x1))) * (mdates.date2num(x_segment)-mdates.date2num(x1))
            
            # Append to the overall lists
            x_interp.extend(x_segment)
            y_interp.extend(y_segment)

        return x_interp, y_interp
    
    # In case of user didnt choose 100% for one of the steps, plot data properly.
    full_dates, full_casecount = feedCSVData(file, 1)
    plt.figure(figsize=(12, 6))
    plt.scatter(full_dates, full_casecount, color='green', label='Original Points')
    
    dates, case_count = feedCSVData(file, step)
    x_interp, y_interp = eq(dates, case_count)
    plt.plot(x_interp, y_interp, label=f'Piecewise Linear Interpolation {int(100/step)}% of data', color='blue')
    
    y_interp2 = None
    if step2 != None:
        dates2, case_count2 = feedCSVData(file, step2)
        x_interp2, y_interp2 = eq(dates2, case_count2)
        plt.plot(x_interp2, y_interp2, label=f'Piecewise Linear Interpolation {int(100/step2)}% of data', color='red')
    
    plt.title(f'Piecewise Linear Interpolation of Covid Cases')
    plt.xlabel('Dates')
    plt.ylabel('Case Count')
    
    # Format x-axis to show dates properly
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.gcf().autofmt_xdate()  # Rotate and align the tick labels
    
    plt.grid(alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    return y_interp, y_interp2
    
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
    type_graph = input("What type of graph would you like to produce? (C for compartative or S for single): ").lower()
    
    if type_graph == "s":
        step = int(input("What percentage of the data would you like to see? (100, 50, 25, or 10): "))
        step = int(100/step)
        step2 = None
        
        y_interp, y_interp2 = piecewise(file, step, step2)
    elif type_graph == "c":
        step = int(input("What percentage of the data would you like to see for the first line? (100, 50, 25, or 10): "))
        step = int(100/step)
        
        step2 = int(input("What percentage of the data would you like to see for the second line? (100, 50, 25, or 10): "))
        step2 = int(100/step2)
        
        y_interp, y_interp2 = piecewise(file, step, step2)
        print(f'Mean squared error between {int(100/step)}% and {int(100/step2)}% of data = {MSE(y_interp, y_interp2, step, step2):.2f}')
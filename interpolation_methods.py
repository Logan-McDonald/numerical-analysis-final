import pandas
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime, timedelta

def feedCSVData(file, step=1):
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
    
def piecewise(file, step=None):
    
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
    
    dates, case_count = feedCSVData(file)
    x_interp, y_interp = eq(dates, case_count)

    plt.figure(figsize=(12, 6))
    plt.plot(x_interp, y_interp, label='Piecewise Linear Interpolation 100 percent of data', color='blue')
    
    # If a set is step, graph will plot extra line with step
    if step != None:
        dates_step, case_count_step = feedCSVData(file, step=step)
        x_interp_step, y_interp_step = eq(dates_step, case_count_step)
        plt.plot(x_interp_step, y_interp_step, label=f'Piecewise Linear Interpolation {100/step} percent of data', color='red')
    
    plt.scatter(dates, case_count, color='green', label='Original Points')
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
    
if __name__ == "__main__":
    file = "COVID-19_Daily_Counts_of_Cases__Hospitalizations__and_Deaths.csv"
    piecewise(file)
    # piecewise(file, step=2)
    # piecewise(file, step=4)
    # piecewise(file, step=10)
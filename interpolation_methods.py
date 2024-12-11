import pandas
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime, timedelta

def feedCSVData(file):
    data_frame = pandas.read_csv(file)
    
    # Extract dates from the CSV file
    dates = data_frame["date_of_interest"].tolist()
    
    # Convert string dates to datetime objects
    dates = [datetime.strptime(date, '%m/%d/%Y') for date in dates]
    
    case_count = data_frame["CASE_COUNT"].tolist()
    
    return dates, case_count
    
def piecewise(dates, case_count):
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

    plt.figure(figsize=(12, 6))
    plt.plot(x_interp, y_interp, label='Piecewise Linear Interpolation', color='blue')
    plt.scatter(dates, case_count, color='red', label='Original Points')
    
    plt.title('Piecewise Linear Interpolation of Covid Cases Per Day')
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
    dates, case_count = feedCSVData(file)
    
    piecewise(dates, case_count)
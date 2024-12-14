# Project Presentation Video Link
https://youtu.be/-bBg-KrC7_w

# Project Contributions
All group memebers contributed about evenly on all the code across the files:

## Piecewise Linear Interpolation
Contained in "linear_interpolation.py"

We started off our project by implementing linear interpolation on the dataset. We figured that since it was among the easier algorithms to implement, that it would be a good start.

Our code follows similar format across all files, we have a feedCSVData method that will take the data from the CSV file and feed it into arrays that we pass into our calculation methods. For linear interpolation we feed it into the piecewise method that takes in the lists, calculates the x and y points for the interpolation graphs and then plots them using matplotlib.

We added options to also feed a percentage of data into the code, 100, 50, 25, and 10 percent. This is paired with an option to plot two lines for any of those options.

On top of all of this, we have a method to calculate the root MSE for comparison between data percentages.

## Piecewise Quadratic Interpolation
Contained in "quadratic.py"

Just like the linear interpolation, this code has the feedCSVData method, the calculation method, the root MSE calculation method, and the option to generate multiple different graphs. However, in this code, the plotting functionality is seperated into a different method called quadratic_spline, while the calculations are held in quadratic_spline_segment.

## Inverse Distance Weighting
Contained in "inverse_distance_weighting.py"

Again, like the other files in our codebase, it is very similar, most notably similar to quadratic.py's implementation where the matplotlib graphing and calculcation methods are seperate.

# Running The Code
Since all of our code is held in python scripts, all that is required to run them is having the latest version of python, and running the following commands depending on the file you want to run:
```
python quadratic.py
python linear_interpolation.py 
python inverse_distance_weighting.py  
```
**IMPORTANT NOTE** When running the code in an ssh shell, the matplotlib graphs will not display, the only way they will is if you run it in an IDE. (We used VSCode)
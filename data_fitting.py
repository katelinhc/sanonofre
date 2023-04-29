import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, num2date
from scipy.optimize import curve_fit, OptimizeWarning

AXIS_LABELS= dict(
    heart_rate = 'Heart Rate (bpm)',
    hrv = 'Heart Rate Variabiliity'
)

class DataFitting:
    # Data fitting based on https://github.com/roywright/NOAA_data/blob/master/asheville.ipynb
    def __init__(self, df: pd.DataFrame, data_type: str) -> None:
        self.df = df
        self.data_type = data_type
        self.days = 10
        
        
    def fit_data(self):
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'], utc=True)
        min_time =self. df.timestamp.apply(date2num).min()
        x = [date2num(t) for t in self.df.timestamp]
        p, _ = curve_fit(
            self.sine, x, self.df.value, 
            p0 = [20, 2*np.pi / self.days, 0, 50, min_time]
        )
        T = (2*np.pi / p[1])
        print(f'The best-fit sine function has a period of {T} days.')
        
        self.plot_fit(x, p, T)
        
        

    def sine(self, x, a, b, c, d, min_time):    
        x_ = x - min_time 
        return a * np.sin(b * (x_ - c)) + d
    
    
    def plot_fit(self, x, p, T):
        dt = [num2date(t) for t in x]
        plt.plot(
            dt, self.sine(x, *p), 
            lw = 3, c = 'black', zorder = 9001
        )

        # Plot the data again
        self.df.set_index('timestamp').value.plot(
            marker = 'o', markersize = 1, lw = 0,
            alpha = .1, legend = False    
        )

        # Display the sine formula
        plt.text(
            dt[0], 0, 
            '$y \;=\; %.1f\,\sin(2\pi/%.2f\cdot(x %s %.2f)) + %.1f$' 
            % (p[0], T, '-' if p[2] > 0 else '+', abs(p[2]), p[3])
        )

        plt.xlabel('')
        plt.ylabel(f'{AXIS_LABELS[self.data_type]}')
        plt.show()
                    
# to do: residual analysis with day/night time residuals
            
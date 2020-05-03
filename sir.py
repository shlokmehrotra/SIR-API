from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
import time
import numpy as np
from census import Census
import matplotlib.pyplot as plt
from us import states
from scipy import integrate, optimize
browser = webdriver.Safari()
browser.get("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv")
time.sleep(2) #adjust this based on how often you wanna webscrape tings.
countydata = (browser.find_element_by_xpath("/html/body/pre").text).split('\n')
#temp params
countyname = "Contra Costa"
statename = "California"
from census import Census
from us import states
#print(countydata[:10])
plotdata = []
for data in countydata:
	#print(data.split(','))
	data = data.split(',')
	date = data[0]
	county = data[1]
	state = data[2]
	fips = data[3]
	cases = data[4]
	deaths = data[5]
	if(county == countyname and statename == state):
		print(data)
		print("date:",data[0])
		print("county: ", data[1])
		print("cases: ", data[4])
		plotdata.append(int(data[4])) #cases data being appended
print("ya so like wtf")
print(plotdata)

xdata = np.arange(1, len(plotdata)+1)
ydata = np.array(plotdata)
def sir_model(y, x, beta, gamma):
    S = -beta * y[0] * y[1] / N
    R = gamma * y[1]
    I = -(S + R)
    return S, I, R

def fit_odeint(x, beta, gamma):
    return integrate.odeint(sir_model, (S0, I0, R0), x, args=(beta, gamma))[:,1]

N = 1.0
I0 = ydata[0]
S0 = N - I0
R0 = 0.0

popt, pcov = optimize.curve_fit(fit_odeint, xdata, ydata)
fitted = fit_odeint(xdata, *popt)

title = "SIR model in " + countyname + ", " + statename
plt.title(title)
plt.plot(xdata, ydata, 'o')
plt.plot(xdata, fitted)
plt.show()




#prenkish example below
'''
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Total population, N.
N = 1000
# Initial number of infected and recovered individuals, I0 and R0.
I0, R0 = 1, 0
# Everyone else, S0, is susceptible to infection initially.
S0 = N - I0 - R0
# Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
beta, gamma = 0.2, 1./10 
# A grid of time points (in days)
t = np.linspace(0, 160, 160)

# The SIR model differential equations.
def deriv(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

# Initial conditions vector
y0 = S0, I0, R0
# Integrate the SIR equations over the time grid, t.
ret = odeint(deriv, y0, t, args=(N, beta, gamma))
S, I, R = ret.T

# Plot the data on three separate curves for S(t), I(t) and R(t)
fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, axis_bgcolor='#dddddd', axisbelow=True)
ax.plot(t, S/1000, 'b', alpha=0.5, lw=2, label='Susceptible')
ax.plot(t, I/1000, 'r', alpha=0.5, lw=2, label='Infected')
ax.plot(t, R/1000, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
ax.set_xlabel('Time /days')
ax.set_ylabel('Number (1000s)')
ax.set_ylim(0,1.2)
ax.yaxis.set_tick_params(length=0)
ax.xaxis.set_tick_params(length=0)
ax.grid(b=True, which='major', c='w', lw=2, ls='-')
legend = ax.legend()
legend.get_frame().set_alpha(0.5)
for spine in ('top', 'right', 'bottom', 'left'):
    ax.spines[spine].set_visible(False)
plt.show()
'''
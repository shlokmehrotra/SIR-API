from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
import time
from scipy.optimize import minimize
from scipy import integrate
import pylab as pl
import numpy as np
from census import Census
import matplotlib.pyplot as plt
from us import states
from scipy import integrate, optimize
import csv
browser = webdriver.Safari()
browser.get("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv")
time.sleep(2) #adjust this based on how often you wanna webscrape tings.
countydata = (browser.find_element_by_xpath("/html/body/pre").text).split('\n')[1:]#because the first entry is the format ting. 
#temp params
'''
countyname = "New York City"
statename = "New York"
population = 8399000 #for normalization of coounty population 
'''
R0val = 1
from census import Census
from us import states
restricted = [("Unknown", "Arizona")]

def uniqueCounties():
    counties = []
    for data in countydata:
        data = data.split(',')
        if((data[1], data[2]) not in counties and (data[1], data[2]) not in restricted):
            counties.append((data[1], data[2]))
    return counties

counties = uniqueCounties()
print(len(counties))

def CalcR0(countyname, statename):

    plotdata = []
    for data in countydata:
        data = data.split(',')
        date = data[0]  
        county = data[1]
        state = data[2]
        fips = data[3]
        cases = data[4]
        deaths = data[5]
        if(county == countyname and statename == state):
            #print(data)
            #print("date:",data[0])
            #print("county: ", data[1])
            #print("cases: ", data[4])
            plotdata.append(int(data[4])) #cases data being appended -> infected 
    #print("ya so like wtf")
    #print(plotdata)
    ydata = plotdata
    xdata = np.arange(1, len(plotdata)+1)

    def funcFit(sirparams, time, beta, nu, k):
        s = sirparams[0]
        i = sirparams[1]
        r = sirparams[2]

        res = np.zeros((3))
        res[0] = - beta * s * i
        res[1] = beta * s * i - nu * i
        res[2] = nu * i
        #print("R0", nu/beta)
        global R0val
        R0val = nu/beta
        return res

    def leastSquares(model, xdata, ydata, n):
        #least squares fit type beat.
        time_total = xdata

        data_record = ydata

        k = 1.0/sum(data_record)

        I0 = data_record[0]*k
        S0 = 1 - I0
        R0 = 0 
        N0 = [S0,I0,R0]

        param_init = [0.75, 0.75]
        param_init.append(k)

        param = minimize(sse(model, N0, time_total, k, data_record, n), param_init, method="nelder-mead").x 
        Nt = integrate.odeint(model, N0, time_total, args=tuple(param))
        #print(Nt)
        Nt = np.divide(Nt, k)

        #print(Nt[:,1])
        return Nt[:,1]

    def sse(model, N0, time_total, k, data_record, n):
        #Sum of squares ting.
        def result(x):
            Nt = integrate.odeint(model, N0, time_total[:n], args=tuple(x))
            INt = [row[1] for row in Nt]
            INt = np.divide(INt, k)
            difference = data_record[:n] - INt

            diff = np.dot(difference, difference)
            return diff
        return result

    result = leastSquares(funcFit, xdata, ydata, 60)
    pl.clf()
    pl.title(str(countyname + "," + statename))
    pl.xlabel("Days since infection")
    pl.ylabel("Population infected")
    pl.plot(xdata, ydata, "o")
    pl.plot(xdata, result)
    filename = "images/" + "".join(countyname.split(' ')) + "_" + "".join(statename.split(' ')) + ".png"
    print(filename)
    pl.savefig(str(filename))
    return result

data = [["County", "State", "R0"]]

for county in counties:
    print(county[0], county[1])
    try:
        print(CalcR0(county[0], county[1]))
        data.append([county[0], county[1], R0val])
    except:
        print("UMM YEAAA", county[0], county[1])   

#CalcR0("Unknown", "Arizona")
with open('R0vals.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)


#pl.show()
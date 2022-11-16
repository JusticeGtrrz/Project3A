'''
This web service extends the Alphavantage api by creating a visualization module, 
converting json query results retuned from the api into charts and other graphics. 

This is where you should add your code to function query the api
'''
import requests
from datetime import datetime
from datetime import date
import pygal
from flask import request

#Helper function for converting date


def convert_date(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d').date()

def StockFunc():
    global StepData
    global symbol
    global time_series
    global URL
    StepData = ''
    symbol = request.form['symbol']
    time_series = request.form['time_series']
    Function = ['function=TIME_SERIES_INTRADAY','function=TIME_SERIES_DAILY_ADJUSTED','function=TIME_SERIES_WEEKLY','function=TIME_SERIES_MONTHLY']
    DictSeries =['Time Series (60min)', 'Time Series (Daily)', 'Weekly Time Series', 'Monthly Time Series']
    if int(time_series)-1 == 0:
        URL = 'https://www.alphavantage.co/query?'+ Function[int(time_series)-1] +'interval=60min'+ '&symbol=' + symbol +'&apikey=7CKUYMD19R6Q9LKW'
    else:
        URL = 'https://www.alphavantage.co/query?'+ Function[int(time_series)-1] + '&symbol=' + symbol +'&apikey=7CKUYMD19R6Q9LKW'
    DataDic = requests.get(URL)
    data = DataDic.json()
    StepData = data[DictSeries[int(time_series)-1]]
    print(URL)
    PopChart()

def PopChart():
    global chartvar
    global StepData
    global symbol
    global time_series
    global Close 
    global Date 
    global High
    global Low 
    global Open
    global chart_type
    global start_date
    global end_date
    global chart
    chart_type = request.form['chart_type']
    chart = None
    Close =[]
    Date =[]
    High = []
    Low =[]
    Open =[]
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    Index = list(StepData).index(start_date)
    Index2 = list(StepData).index(end_date)
    if Index > Index2:
        Value = list(StepData.values())[Index2]
        while Index2-1 < Index:
            Value = list(StepData.values())[Index2]
            Date.append(str(list(StepData.keys())[Index2]))
            Open.append(int(float(Value.get('1. open'))))
            High.append(int(float(Value.get('2. high'))))
            Low.append(int(float(Value.get('3. low'))))
            Close.append(int(float(Value.get('4. close'))))
            Index2 = Index2 + 1
        Date.reverse()
        Open.reverse()
        High.reverse()
        Low.reverse()
        Close.reverse()
    if int(chart_type) == 0:
        chart = pygal.Bar(spacing=100, fill=True, x_label_rotation=40)
        chart.title = ('Stock Data for '+ symbol + ': ' + start_date +' to ' + end_date)
        chart.x_labels =('Red', 'Blue', 'Green', 'Yellow')
        chart.x_labels = Date
        chart.add('Open', Open)
        chart.add('High', Close)
        chart.add('Low', Low)
        chart.add('close', Close)
    else:
        chart = pygal.Line(spacing=100, fill=False, x_label_rotation=40)
        chart.title = ('Stock Data for '+ symbol + ': ' + start_date +' to ' + end_date)
        chart.x_labels =('Red', 'Blue', 'Green', 'Yellow')
        chart.x_labels = Date
        chart.add('Open', Open)
        chart.add('High', Close)
        chart.add('Low', Low)
        chart.add('close', Close)
        chartvar = chart.render_data_uri()
        return chartvar
    
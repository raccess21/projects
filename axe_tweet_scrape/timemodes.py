from datetime import datetime as dt
from dateutil.relativedelta import relativedelta

#returns 1 day change in time        
def daily():
    return relativedelta(days=1)

#returns 1 month change in time        
def monthly():
    return relativedelta(months=1)

#returns 1 year change in time    
def yearly():
    return relativedelta(years=1)
    
    
#check if date falls within specified date range
#lower limit inclusive, upper limit exclusive
def in_interval(date, st_date, end_date) -> bool:
    try:
        if date >= st_date and date < end_date:
            return True
    except:
        ...
    return False

#standard date info input function, no fail infinite loop
#either user input or call value standardisation        
def input_date(name="the", tithi=' '):
    while True:
        try:
            return dt.strptime(tithi, '%Y/%m/%d')
        except ValueError:
            tithi = input(f"Enter {name} date in yyyy/mm/dd format: ")


#input period value(day/month/year) for x-axis of graph        
def input_period(period = 'l'):
    period_modes = {'d': daily, 'm': monthly, 'y': yearly}
    while True:
        try:
            return period_modes[period]
        except KeyError:
            print("Type (d or m or y) case insensitive..")
            period = input("Select period (daily/monthly/yearly): ").strip()[0].lower()
            
        

#generate list of date values for x-axis of graph
#from startdate to enddate with specified periods day, month or year    
def tperiod(startdate='', enddate='') -> list:
    if not startdate:
        startdate = input_date("start")#, "1212/01/01")
        enddate = input_date("end")#, "1215/12/01")
    if enddate <= startdate:
       print("End date should be greater than start date") 
       tperiod()
    fname = input_period()
    
    dates = []
    while startdate < enddate:
        dates.append(startdate)
        startdate += fname()
    dates.append(enddate)
    return dates


#serialse datetime object to string format   
def datetime_encoder(tithi):
    return tithi.isoformat()

#string format date time value to datetime object
def datetime_decoder(tithi):
    return dt.fromisoformat(tithi)  
   

#!------------!!-----------!!___________!!--------------!!---------------!#   
def main():
    ...
    
if __name__ == "__main__":
    main()

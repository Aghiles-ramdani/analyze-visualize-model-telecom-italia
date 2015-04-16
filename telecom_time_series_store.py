import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import math


# loop over days and store a total call in, call out, sms in, and sms out
# value for each day in December 2013

# range of days
prng = pd.period_range('12/1/2013', '12/31/2013', freq='D')
# common beginning of all daily data files:
pre = "sms-call-internet-mi-"

# dataframe to hold values
colnames = ['Call_in', 'Call_out']
activity = pd.DataFrame(columns=colnames, index=prng).fillna(0.0)

# column names for the reader
colnames = [
    'square_id', 'time_interval', 'country_code','SMS_in',
    'SMS_out', 'Call_in','Call_out', 'Internet_traffic'
    ]
used = ['Call_in','Call_out']

# loop over days
for day in prng:
	# get daily data
	filename = pre + str(day) + ".txt"
	reader = pd.read_csv('data/' + filename, 
		sep='\t', chunksize=1000, names=colnames, usecols=used)

	# loop over chunks of the data
	count = 0
	for chunk in reader:
	    # get sums for unique square ids within chunk
	    sums = chunk.sum()
	    count += len(chunk)
	    if math.isnan(sums['Call_in']):
	    	sums['Call_in'] = 0
	    if math.isnan(sums['Call_out']):
	    	sums['Call_out'] = 0
	    activity.ix[day]['Call_in'] += float(sums['Call_in'])
	    activity.ix[day]['Call_out'] += float(sums['Call_out'])

	# divide by total rows in the reader to get the average daily
	# activity
	activity.ix[day]['Call_in'] = activity.ix[day]['Call_in']/count
	activity.ix[day]['Call_out'] = activity.ix[day]['Call_out']/count

print activity.tail()

# save time series data
activity.to_csv('daily_calls_in_out.csv')
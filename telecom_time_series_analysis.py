import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import seaborn as sns
import numpy as np

# import daily Call in and Call out time series
columns = ['per', 'Call_in', 'Call_out']
df = pd.read_csv('daily_calls_in_out.csv', header=1, names=columns)

# set the dataframe index as daily periods
index = pd.PeriodIndex(df.per, freq='D')
df = df.set_index(index)
del df['per']

# Plot the Calls in/out time series
df.plot()
plt.ylabel('Activity')
plt.draw()
plt.savefig('ts_calls_in_out_plot.png')

# Model Calls In 

# RMSE for evaluating models:
def rmse(predictions, targets):
	return np.sqrt(((predictions-targets)**2).mean())

# list of models
models = ["ARMA(1,0)", "ARMA(2,0)", "ARMA(3,0)", "ARMA(2,1)"]
errors = []

# visualize fit
plt.figure()
plt.plot(df.index.values, df['Call_in'].values)

# with ARMA(.,0)
for i in range(1,4):
	tsa = sm.tsa
	arma_mod = tsa.ARMA(df['Call_in'].values, order=(i,0))
	arma_res = arma_mod.fit(trend='c')
	arma_pred = arma_res.predict()
	plt.plot(df.index.values, arma_pred, linestyle = '--', label=models[i-1])
	errors.append(rmse(arma_pred, df['Call_in'].values))

# with ARMA(2,1)
tsa = sm.tsa
arma_mod = tsa.ARMA(df['Call_in'].values, order=(2,1))
arma_res = arma_mod.fit(trend='nc')
arma_pred = arma_res.predict()
plt.plot(df.index.values, arma_pred, linestyle = '--', label=models[3])
errors.append(rmse(arma_pred, df['Call_in'].values))

# insert model legend and save model comparison plot
plt.legend()
plt.draw()
plt.savefig('model_comparison.png')

# plot and save barplot for model errors
error_df = pd.DataFrame(zip(models, errors), columns=['model','RMSE'])
plt.figure()
sns.factorplot("model", y="RMSE", data=error_df, kind="bar")
plt.draw()
plt.savefig('model_errors.png')

plt.show()

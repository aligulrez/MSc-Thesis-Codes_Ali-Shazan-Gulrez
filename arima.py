# the code for the ARIMA model for forecasting 
from pandas import read_csv
from pandas import datetime
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sys import argv

gn_data = read_csv(argv[1],header=None)
X = gn_data.values
class_file = open(argv[2],'r')

points = []
for line in class_file:
    points.append(int(line)-2)
start = 0
train = 5 #number of points for training
test = 1 # days for testing, this day is just after the training days 
history = []
for i in range(start,start+train):
    for val in (X[points[i]]):
        history.append(val)
test_v = []
for val in (X[points[int(argv[3])]]):
	test_v.append(val)

predictions = []
step = 15  # forecast range or forecasting period
for t in range(len(test_v)):
	model = ARIMA(history, order=(5,1,0)) # order of ARIMA (p,d,q)
	model_fit = model.fit(disp=0)
	output = model_fit.forecast()
	yhat = output[0]
	predictions.append(yhat)
	obs = test_v[t]
        if(t%step == 0):
	    history.append(obs)
        else:
            history.append(yhat)
	#print('predicted=%f, expected=%f' % (yhat, obs))
error = mean_squared_error(test_v, predictions)
error_mae = mean_absolute_error(test_v, predictions)
#rmse = math.sqrt(rmse_bird/len(ghi_bird))
print('Test MSE: %.3f' % error)
print('Test MAE: %.3f' % error_mae)
#Save
predict = open(argv[4],'w')
for value in predictions:
	predict.write(str(value))
	predict.write(",")
predict.close()
# plot
pyplot.plot(test_v)
pyplot.plot(predictions, color='red')
pyplot.show()


	
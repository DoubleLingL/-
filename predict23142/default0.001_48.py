# LSTM for international airline passengers problem with regression framing
# encoding: utf-8

#按半个小时分段统计  每天48个流量数据

import numpy
import pandas as pd
import matplotlib.pyplot as plt
from pandas import read_csv
import math
import time,datetime
from keras.models import Sequential
from keras.layers import Dense,Dropout,Activation
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.optimizers import SGD,Adam


# convert an array of values into a dataset matrix
def create_dataset( dataset, look_back ):
    dataX, dataY = [], []
    for i in range(len(dataset) - look_back):  # -1
        a = dataset[i:(i + look_back), 0]
        dataX.append(a)
        dataY.append(dataset[i + look_back, 0])
    return numpy.array(dataX), numpy.array(dataY)


# fix random seed for reproducibility
numpy.random.seed(7)
# load the dataset
dataframe = read_csv('/media/hll/amuse/gy/predict23142/flow48/inflow0525.csv',header=0)

print(dataframe)
dataset = dataframe.values
dataset = dataset.astype('float32')
print(dataset)
print(len(dataset))
# normalize the dataset
scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(dataset)
# split into train and test sets
train_size = int(len(dataset) * 0.90)
test_size = int(len(dataset) * 0.80)
numpy.savetxt('normalize.txt',dataset)
print('train_size:',train_size)
print('test_size:',test_size)
test_size = len(dataset) - test_size
print('test_size:',test_size)
train, test = dataset[0:train_size, :], dataset[test_size:len(dataset), :]
numpy.savetxt('normalizetrain.txt',train)
numpy.savetxt('normalizetest.txt',test)
#print('train:',train)
#print('test:',test)
print('lentrain:',len(train))
print('lentest:',len(test))
# reshape into X=t and Y=t+1
look_back = 48  # 1

trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)

print('lentrainX:',len(trainX))
print('lentrainY:',len(trainY))
#print(trainX[0])
print('lentestX:',len(testX))
print('lentestY:',len(testY))

trainX = numpy.reshape(trainX, (trainX.shape[0], trainX.shape[1], 1))
testX = numpy.reshape(testX, (testX.shape[0], testX.shape[1], 1))
print(trainX.shape, testX.shape)
# create and fit the LSTM network
model = Sequential()
# model.add(LSTM(4, input_shape=(1, look_back)))
model.add(LSTM(20, input_shape=(look_back, 1),return_sequences=True))
#model.add(Dropout(0.2))
model.add(LSTM(20,return_sequences=False))
#model.add(Dropout(0.2))
#model.add(LSTM(10,return_sequences=False))
model.add(Dense(1,activation='tanh'))
#adam=Adam(lr=0.05,beta_1=0.9, beta_2=0.999, epsilon=1e-08)
#sgd = SGD(lr=learning_rate, decay=learning_rate/nb_epoch, momentum=0.9, nesterov=True)
#decay 使学习速率在每次更新时衰减，即随着迭代 逐渐减小学习速率
#lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08
#model.compile(loss='mean_squared_error', optimizer='adam')
#epochs = 2
#learning_rate = 0.1
#decay_rate = learning_rate / epochs
#momentum = 0.8
#adam=Adam(lr=learning_rate,beta_1=0.9, beta_2=0.999,decay=0.02, epsilon=1e-08)
#sgd = SGD(lr=learning_rate, momentum=momentum, decay=decay_rate, nesterov=False)
#model.compile(loss='binary_crossentropy', optimizer=sgd, metrics=['accuracy'])
model.compile(loss='mean_squared_error', optimizer='adam')
start_time = time.clock()
starttime=datetime.datetime.now()
model.fit(trainX, trainY, epochs=2400, batch_size=16, verbose=2)
# make predictions
trainPredict = model.predict(trainX)
print(len(trainPredict))
testPredict = model.predict(testX)

b=[]
c=[]
b = testY
c = testPredict[:, 0]
def presicion(accu,b,c):
    presicion = 0
    for i in range(len(c)):
        if abs((b[i] - c[i])) < accu:
            presicion = presicion + 1
            #print( scaler.inverse_transform(b[i])- scaler.inverse_transform(c[i]))
    print('presicion,accu:',presicion,accu)
    print(format(float(presicion)/float(758),'.6f'))
presicion(0.1,b,c)
presicion(0.05,b,c)
presicion(0.025,b,c)
presicion(0.02,b,c)

# invert predictions
trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform([trainY])
testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform([testY])
# calculate root mean squared error
testSccore = math.sqrt(mean_squared_error(b, c))

print('Test Score: %.6f RM2SE' % (testSccore))
trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:, 0]))
print('Train Score: %.2f RMSE' % (trainScore))
testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:, 0]))
print('Test Score: %.2f RMSE' % (testScore))

#save1=pd.DataFrame.from_dict(testY[0],testPredict[:, 0])
save = pd.DataFrame({'real':testY[0],'predict':testPredict[:, 0]})
save.to_csv('/media/hll/amuse/gy/predict23142/flow48/inflowpre.csv',index=False,sep=',')
end_time = time.clock()
endtime=datetime.datetime.now()
print("running clock time is:%s seconds"%(end_time-start_time))
print("running now time is:%s seconds"%(endtime-starttime))
print('end')
#print(testPredict)
# shift train predictions for plotting
trainPredictPlot = numpy.empty_like(dataset)
trainPredictPlot[:, :] = numpy.nan
trainPredictPlot[look_back:len(trainPredict) + look_back, :] = trainPredict

# shift test predictions for plotting
testPredictPlot = numpy.empty_like(dataset)
testPredictPlot[:, :] = numpy.nan
#testPredictPlot[len(trainPredict)+(look_back*2)+1:len(dataset)-1, :] = testPredict
testPredictPlot[250:len(dataset), :] = testPredict

testPredictPlot1 = numpy.empty_like(dataset)
testPredictPlot1[:, :] = numpy.nan
#testPredictPlot[len(trainPredict)+(look_back*2)+1:len(dataset)-1, :] = testPredict
testPredictPlot1[960:len(dataset), :] = testPredict[710:]

datasetplot = numpy.empty_like(dataset)
datasetplot[:, :] = numpy.nan
plt.subplot(3,2,1)
dataset1=scaler.inverse_transform(dataset)
datasetplot[960:len(dataset),:]=dataset1[960:]
plt.plot(datasetplot,label='925true',color='red',marker="o")
plt.plot(testPredictPlot1,label='925pre',color='blue',marker="*")
plt.legend()

datasetplot2 = numpy.empty_like(dataset)
datasetplot2[:, :] = numpy.nan
plt.subplot(3,2,2)
dataset2=scaler.inverse_transform(dataset)
datasetplot2[912:960,:]=dataset2[912:960]
testPredictPlot2 = numpy.empty_like(dataset)
testPredictPlot2[:, :] = numpy.nan
testPredictPlot2[912:960, :] = testPredict[662:710]
plt.plot(datasetplot2,label='924true',color='red',marker="o")
plt.plot(testPredictPlot2,label='924pre',color='blue',marker="*")
plt.legend()

datasetplot4 = numpy.empty_like(dataset)
datasetplot4[:, :] = numpy.nan
plt.subplot(3,2,3)
dataset4=scaler.inverse_transform(dataset)
datasetplot4[864:912,:]=dataset4[864:912]
testPredictPlot4 = numpy.empty_like(dataset)
testPredictPlot4[:, :] = numpy.nan
testPredictPlot4[864:912, :] = testPredict[614:662]
plt.plot(datasetplot4,label='923true',color='red',marker="o")
plt.plot(testPredictPlot4,label='923pre',color='blue',marker="*")
plt.legend()

datasetplot5 = numpy.empty_like(dataset)
datasetplot5[:, :] = numpy.nan
plt.subplot(3,2,4)
dataset5=scaler.inverse_transform(dataset)
datasetplot5[816:864,:]=dataset5[816:864]
testPredictPlot5 = numpy.empty_like(dataset)
testPredictPlot5[:, :] = numpy.nan
testPredictPlot5[816:864, :] = testPredict[566:614]
plt.plot(datasetplot5,label='922true',color='red',marker="o")
plt.plot(testPredictPlot5,label='922pre',color='blue',marker="*")
plt.legend()

datasetplot3 = numpy.empty_like(dataset)
datasetplot3[:, :] = numpy.nan
plt.subplot(3,2,5)
dataset1=scaler.inverse_transform(dataset)
datasetplot3[768:816,:]=dataset1[768:816]
testPredictPlot3 = numpy.empty_like(dataset)
testPredictPlot3[:, :] = numpy.nan
testPredictPlot3[768:816, :] = testPredict[518:566]
plt.plot(datasetplot3,label='921true',color='red',marker="o")
plt.plot(testPredictPlot3,label='921pre',color='blue',marker="*")
plt.legend()
# plot baseline and predictions

plt.subplot(3,2,6)
plt.plot(scaler.inverse_transform(dataset),label='true')
# plt.plot(dataset)
plt.plot(trainPredictPlot,label='train')
plt.plot(testPredictPlot,label='predict')
plt.legend()
plt.suptitle('2LSTM_2400_16_0.001')
plt.show()

'''
datasetplot2 = numpy.empty_like(dataset)
datasetplot2[:, :] = numpy.nan
dataset2=scaler.inverse_transform(dataset)
datasetplot2[912:960,:]=dataset2[912:960]
testPredictPlot2 = numpy.empty_like(dataset)
testPredictPlot2[:, :] = numpy.nan
testPredictPlot2[912:960, :] = testPredict[662:710]
'''
plt.figure()
plt.plot(datasetplot2,label='true',color='red',marker="o")
plt.plot(testPredictPlot2,label='pre',color='blue',marker="*")
plt.title('2LSTM_2400_16_0.001  9.24')
plt.legend()
plt.show()

plt.figure()
plt.plot(datasetplot,label='true',color='red',marker="o")
plt.plot(testPredictPlot1,label='pre',color='blue',marker="*")
plt.title('2LSTM_2400_16_0.001  9.25')
plt.legend()
plt.show()
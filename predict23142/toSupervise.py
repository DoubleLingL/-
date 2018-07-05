#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Huang lingling
#转化为监督学习问题
from pandas import DataFrame
from pandas import concat
from pandas import read_csv
from math import sqrt
from matplotlib import pyplot
from sklearn import preprocessing
import numpy
from numpy import concatenate
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense,LSTM,Dropout
from keras.optimizers import SGD

def series_to_supervised(data,n_in=1,n_out=1,dropnan=True):
    n_vars=1 if type(data) is list else data.shape[1]
    df=DataFrame(data)
    cols,names=list(),list()
    #input sequence (t-n,....t-1)
    for i in range(n_in,0,-1):
        cols.append(df.shift(i))
        names+=[('var%d(t-%d)' %(j+1,i)) for j in range(n_vars)]
    #forecast sequence (t,t+1,....t+n)
    for i in range(0,n_out):
        cols.append(df.shift(-i))
        if i==0:
            names += [('var%d(t)' % (j + 1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j + 1, i)) for j in range(n_vars)]

    #put it all together
    agg=concat(cols,axis=1)
    agg.columns=names
    #drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)

    return agg

#load dataset
path='/media/hll/amuse/gy/predict23142/flow/flow_1.csv'
dataset=read_csv(path,header=0,index_col=0)
values=dataset.values
print('values:',values)
'''
#整数编码，针对字符型及混合类型编码
# 风向 为字符型 values[:,4]
encoder=preprocessing.LabelEncoder()
values[:,4]=encoder.fit_transform(values[:,4])
#print('values1[:,4]',values[:,4])
'''
#确定所有的数据为float
values=values.astype('float32')
#归一化
scaler=preprocessing.MinMaxScaler(feature_range=(0,1))
scaled=scaler.fit_transform(values)
#print('scaled',scaled[0:5])
#frame as supervised learning
reframed=series_to_supervised(scaled,1,1)
print(reframed.head(5))
#除去不想预测的列，也就是只预测 PM2.5 'pollution'这一列
reframed.drop(reframed.columns[[12,13,14,15,16,17,18,19,20,21]],axis=1,inplace=True)
print(reframed.head(5))

#根据所有因素(pollution','dew','temp','press','wind_dir','wind_spd','snow','rain')
# 来预测下一个pm2.5值

############################################
#将数据集分为训练集和测试集,LSTM的输入输出
############################################
values=reframed.values
n_train_hours = 18*24
train = values[:n_train_hours,:]
test = values[n_train_hours:,:]

#split into input an outputs
train_x,train_y = train[:,:-1],train[:,-1]
test_x,test_y = test[:,:-1],test[:,-1]

#reshpe input to be 3D [samples,timesteps,features]
train_x = train_x.reshape((train_x.shape[0],1,train_x.shape[1]))
test_x = test_x.reshape(test_x.shape[0],1,test_x.shape[1])
print(train_x.shape,train_y.shape,test_x.shape,test_y.shape)
print(train_x.shape[1],train_x.shape[2])
############################################
#拟合LSTM模型
#输入层：8个神经元,隐藏层：50个神经元，输出层：1个神经元
#使用平均绝对误差损失函数（MAE）
#epoch=50,batch_size=72
############################################
#design network
model = Sequential()
model.add(LSTM(50,input_shape=(train_x.shape[1],train_x.shape[2]),return_sequences=False))
#model.add(Dropout(0.2))
#model.add(LSTM(20,return_sequences=False))
model.add(Dense(1))
#model.compile(loss='mae',optimizer='adam')
sgd=SGD(lr=0.01,decay=1e-6,momentum=0.9,nesterov=True)
model.compile(loss='mse',optimizer='sgd',metrics=['accuracy'])
#fit network
history=model.fit(train_x,train_y,epochs=300,batch_size=72,validation_data=(test_x,test_y),verbose=2,shuffle=False)
#plot history
pyplot.plot(history.history['loss'],label='train')
pyplot.plot(history.history['val_loss'],label='test')

pyplot.legend()
pyplot.show()
score=model.evaluate(test_x,test_y)
print('test score',score[0])
print('test accuary',score[1])
#history.loss_plot('epoch')
# make a prediction
ypre = model.predict(test_x)
test_x = test_x.reshape((test_x.shape[0],test_x.shape[2]))
print(test_x.shape,test_y.shape)
#invert scaling for forecast
#计算误差之前要先把预测数据转换成同一单位



#测试集
inv_ypre=concatenate((ypre,test_x[:,1:]),axis=1)
inv_ypre=scaler.inverse_transform(inv_ypre)
inv_ypre=inv_ypre[:,0]
#invert scaling for actual
inv_y=scaler.inverse_transform(test_x)
print('inv_ypre',inv_ypre)

inv_y=inv_y[:,0]
print('inv_y',inv_y)
#calculate RMSE 均方根误差
rmse=sqrt(mean_squared_error(inv_y,inv_ypre))
print('Test RMSE:%.3f' %rmse)

#画图
datasetp=dataset['seqGridInFlow'].values
#print('datasetp',datasetp)
'''
trainPplot=numpy.empty_like(datasetp)
trainPplot[:,:]=numpy.nan
trainPplot[1:len(inv_trainypre)+1,:]=inv_trainypre

testPplot=numpy.empty_like(datasetp)
#testPplot[:,:]=numpy.nan
testPplot[len(train_x)+3,len(datasetp)-1,:]=inv_ypre
'''
pyplot.figure()
pyplot.plot(datasetp)
xdata=range(len(datasetp)-len(inv_ypre),len(datasetp))
pyplot.plot(xdata,inv_ypre)
pyplot.title('seqGridInFlow',y=1,loc='right')

pyplot .show()
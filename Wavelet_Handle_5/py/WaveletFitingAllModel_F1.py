import pandas as pd
import numpy as np
import pywt
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.externals import joblib
from sklearn.model_selection import KFold, train_test_split, GridSearchCV
from sklearn import metrics
import xgboost as xgb
from sklearn.feature_selection import SelectFromModel
import AllModelWaveletTransformByDOW

print "loading dataset .............." 
handledataset = pd.read_csv(u'/home/haven/Tianchi_power/Tianchi_power__boxhandle15_DayOfWeek.csv')

print "transform date to datetime .............."
handledataset.record_date = pd.to_datetime(handledataset.record_date)

print "select train1 dataset ............."
train1 = handledataset[(handledataset.record_date>=pd.to_datetime('2015-01-01')+pd.to_timedelta(7*66, unit='D')) & (handledataset.record_date<(pd.to_datetime('2015-01-01')+pd.to_timedelta(7*78, unit='D')))]
train1_MeanStdSum = train1.groupby(['user_id'])['power_consumption'].agg({'power_mean':np.mean, 'power_std':np.std, 'power_sum':np.sum}).reset_index()
train1_MeanStdSum['power_rate'] = train1_MeanStdSum.power_sum / train1_MeanStdSum.power_sum.sum()
train1_DOW_MeanStdSum = train1.groupby(['user_id','day_of_week'])['power_consumption'].agg({'DOW_power_mean':np.mean, 'DOW_power_std':np.std, 'DOW_power_sum':np.sum}).reset_index()
train1_DOW_MeanStdSum.groupby('day_of_week')['DOW_power_sum'].agg({'DOW_allsum':sum}).reset_index()
train1_DOW_MeanStdSumAllsum = train1_DOW_MeanStdSum.merge(train1_DOW_MeanStdSum.groupby('day_of_week')['DOW_power_sum'].agg({'DOW_allsum':sum}).reset_index(), on='day_of_week', how='left', copy=True)
train1_DOW_MeanStdSumAllsum['DOW_power_rate'] = train1_DOW_MeanStdSumAllsum.DOW_power_sum / train1_DOW_MeanStdSumAllsum.DOW_allsum
train1_mergeDataset = pd.merge(train1_DOW_MeanStdSumAllsum, train1_MeanStdSum, on='user_id', how='left')

train1_dayofweek_dataset = AllModelWaveletTransformByDOW.waveletTransform(train1)
train1_dayofweek_dataset.drop('level_2', axis=1,inplace=True)

train1_mergeDataset_add = pd.merge(train1_mergeDataset,train1_dayofweek_dataset,on=['user_id', 'day_of_week'], how='left')
#train1_mergeDataset_add = train1_mergeDataset
#train1_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum', 'DOW_power_mean', 'DOW_power_std', 'DOW_powaer_rate', 'power_mean', 'power_std', 'power_rate'], axis=1,inplace=True)
#train1_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum', 'DOW_power_mean', 'DOW_powaer_rate', 'power_mean', 'power_rate'], axis=1,inplace=True)
#train1_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum'], axis=1,inplace=True)
train1_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum', 'DOW_power_rate', 'power_rate'], axis=1,inplace=True)
train1_Y = handledataset[(handledataset.record_date>=(pd.to_datetime('2015-01-01') + pd.to_timedelta(7*78, unit='D'))) & (handledataset.record_date<(pd.to_datetime('2015-01-01') + pd.to_timedelta(7*79, unit='D')))]
final_train1 = pd.merge(train1_mergeDataset_add,train1_Y,on=['user_id', 'day_of_week'], how='left')



print "select train2 dataset ............."
train2 = handledataset[(handledataset.record_date>=pd.to_datetime('2015-01-01')+pd.to_timedelta(7*67, unit='D')) & (handledataset.record_date<(pd.to_datetime('2015-01-01')+pd.to_timedelta(7*79, unit='D')))]
train2_MeanStdSum = train2.groupby(['user_id'])['power_consumption'].agg({'power_mean':np.mean, 'power_std':np.std, 'power_sum':np.sum}).reset_index()
train2_MeanStdSum['power_rate'] = train2_MeanStdSum.power_sum / train2_MeanStdSum.power_sum.sum()
train2_DOW_MeanStdSum = train2.groupby(['user_id','day_of_week'])['power_consumption'].agg({'DOW_power_mean':np.mean, 'DOW_power_std':np.std, 'DOW_power_sum':np.sum}).reset_index()
train2_DOW_MeanStdSum.groupby('day_of_week')['DOW_power_sum'].agg({'DOW_allsum':sum}).reset_index()
train2_DOW_MeanStdSumAllsum = train2_DOW_MeanStdSum.merge(train2_DOW_MeanStdSum.groupby('day_of_week')['DOW_power_sum'].agg({'DOW_allsum':sum}).reset_index(), on='day_of_week', how='left', copy=True)
train2_DOW_MeanStdSumAllsum['DOW_power_rate'] = train2_DOW_MeanStdSumAllsum.DOW_power_sum / train2_DOW_MeanStdSumAllsum.DOW_allsum
train2_mergeDataset = pd.merge(train2_DOW_MeanStdSumAllsum, train2_MeanStdSum, on='user_id', how='left')

train2_dayofweek_dataset = AllModelWaveletTransformByDOW.waveletTransform(train2)
train2_dayofweek_dataset.drop('level_2', axis=1,inplace=True)

train2_mergeDataset_add = pd.merge(train2_mergeDataset, train2_dayofweek_dataset, on=['user_id', 'day_of_week'], how='left')
#train2_mergeDataset_add = train2_mergeDataset
#train2_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum', 'DOW_power_mean', 'DOW_power_std', 'DOW_powaer_rate', 'power_mean', 'power_std', 'power_rate'], axis=1,inplace=True)
#train2_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum', 'DOW_power_mean', 'DOW_powaer_rate', 'power_mean', 'power_rate'], axis=1,inplace=True)
#train2_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum'], axis=1,inplace=True)
train2_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum', 'DOW_power_rate', 'power_rate'], axis=1,inplace=True)

train2_Y = handledataset[(handledataset.record_date>=(pd.to_datetime('2015-01-01') + pd.to_timedelta(7*79, unit='D'))) & (handledataset.record_date<(pd.to_datetime('2015-01-01') + pd.to_timedelta(7*80, unit='D')))]

final_train2 = pd.merge(train2_mergeDataset_add,train2_Y,on=['user_id', 'day_of_week'], how='left')




print "select train3 dataset ............."
train3 = handledataset[(handledataset.record_date>=pd.to_datetime('2015-01-01')+pd.to_timedelta(7*68, unit='D')) & (handledataset.record_date<(pd.to_datetime('2015-01-01')+pd.to_timedelta(7*80, unit='D')))]
train3_MeanStdSum = train3.groupby(['user_id'])['power_consumption'].agg({'power_mean':np.mean, 'power_std':np.std, 'power_sum':np.sum}).reset_index()
train3_MeanStdSum['power_rate'] = train3_MeanStdSum.power_sum / train3_MeanStdSum.power_sum.sum()
train3_DOW_MeanStdSum = train3.groupby(['user_id','day_of_week'])['power_consumption'].agg({'DOW_power_mean':np.mean, 'DOW_power_std':np.std, 'DOW_power_sum':np.sum}).reset_index()
train3_DOW_MeanStdSum.groupby('day_of_week')['DOW_power_sum'].agg({'DOW_allsum':sum}).reset_index()
train3_DOW_MeanStdSumAllsum = train3_DOW_MeanStdSum.merge(train3_DOW_MeanStdSum.groupby('day_of_week')['DOW_power_sum'].agg({'DOW_allsum':sum}).reset_index(), on='day_of_week', how='left', copy=True)
train3_DOW_MeanStdSumAllsum['DOW_power_rate'] = train3_DOW_MeanStdSumAllsum.DOW_power_sum / train3_DOW_MeanStdSumAllsum.DOW_allsum
train3_mergeDataset = pd.merge(train3_DOW_MeanStdSumAllsum, train3_MeanStdSum, on='user_id', how='left')

train3_dayofweek_dataset = AllModelWaveletTransformByDOW.waveletTransform(train3)
train3_dayofweek_dataset.drop('level_2', axis=1,inplace=True)

train3_mergeDataset_add = pd.merge(train3_mergeDataset,train3_dayofweek_dataset,on=['user_id', 'day_of_week'], how='left')
#train3_mergeDataset_add = train3_mergeDataset
#train3_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum', 'DOW_power_mean', 'DOW_power_std', 'DOW_powaer_rate', 'power_mean', 'power_std', 'power_rate'], axis=1,inplace=True)
#train3_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum', 'DOW_power_mean', 'DOW_powaer_rate', 'power_mean', 'power_rate'], axis=1,inplace=True)
#train3_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum'], axis=1,inplace=True)
train3_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum', 'DOW_power_rate', 'power_rate'], axis=1,inplace=True)

train3_Y = handledataset[(handledataset.record_date>=(pd.to_datetime('2015-01-01') + pd.to_timedelta(7*80, unit='D'))) & (handledataset.record_date<(pd.to_datetime('2015-01-01') + pd.to_timedelta(7*81, unit='D')))]

final_train3 = pd.merge(train3_mergeDataset_add,train3_Y,on=['user_id', 'day_of_week'], how='left')




print "select train4 dataset ............."
train4 = handledataset[(handledataset.record_date>=pd.to_datetime('2015-01-01')+pd.to_timedelta(7*69, unit='D')) & (handledataset.record_date<(pd.to_datetime('2015-01-01')+pd.to_timedelta(7*81, unit='D')))]
train4_MeanStdSum = train4.groupby(['user_id'])['power_consumption'].agg({'power_mean':np.mean, 'power_std':np.std, 'power_sum':np.sum}).reset_index()
train4_MeanStdSum['power_rate'] = train4_MeanStdSum.power_sum / train4_MeanStdSum.power_sum.sum()
train4_DOW_MeanStdSum = train4.groupby(['user_id','day_of_week'])['power_consumption'].agg({'DOW_power_mean':np.mean, 'DOW_power_std':np.std, 'DOW_power_sum':np.sum}).reset_index()
train4_DOW_MeanStdSum.groupby('day_of_week')['DOW_power_sum'].agg({'DOW_allsum':sum}).reset_index()
train4_DOW_MeanStdSumAllsum = train4_DOW_MeanStdSum.merge(train4_DOW_MeanStdSum.groupby('day_of_week')['DOW_power_sum'].agg({'DOW_allsum':sum}).reset_index(), on='day_of_week', how='left', copy=True)
train4_DOW_MeanStdSumAllsum['DOW_power_rate'] = train4_DOW_MeanStdSumAllsum.DOW_power_sum / train4_DOW_MeanStdSumAllsum.DOW_allsum
train4_mergeDataset = pd.merge(train4_DOW_MeanStdSumAllsum, train4_MeanStdSum, on='user_id', how='left')

train4_dayofweek_dataset = AllModelWaveletTransformByDOW.waveletTransform(train4)
train4_dayofweek_dataset.drop('level_2', axis=1,inplace=True)

train4_mergeDataset_add = pd.merge(train4_mergeDataset,train4_dayofweek_dataset,on=['user_id', 'day_of_week'], how='left')
#train4_mergeDataset_add = train4_mergeDataset
#train4_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum', 'DOW_power_mean', 'DOW_power_std', 'DOW_powaer_rate', 'power_mean', 'power_std', 'power_rate'], axis=1,inplace=True)
#train4_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum', 'DOW_power_mean', 'DOW_powaer_rate', 'power_mean', 'power_rate'], axis=1,inplace=True)
#train4_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum'], axis=1,inplace=True)
train4_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum', 'DOW_power_rate', 'power_rate'], axis=1,inplace=True)

train4_Y = handledataset[(handledataset.record_date>=(pd.to_datetime('2015-01-01') + pd.to_timedelta(7*81, unit='D'))) & (handledataset.record_date<(pd.to_datetime('2015-01-01') + pd.to_timedelta(7*82, unit='D')))]

final_train4 = pd.merge(train4_mergeDataset_add,train4_Y,on=['user_id', 'day_of_week'], how='left')


print "select train5 dataset ............."
train5 = handledataset[(handledataset.record_date>=pd.to_datetime('2015-01-01')+pd.to_timedelta(7*65, unit='D')) & (handledataset.record_date<(pd.to_datetime('2015-01-01')+pd.to_timedelta(7*77, unit='D')))]
train5_MeanStdSum = train5.groupby(['user_id'])['power_consumption'].agg({'power_mean':np.mean, 'power_std':np.std, 'power_sum':np.sum}).reset_index()
train5_MeanStdSum['power_rate'] = train5_MeanStdSum.power_sum / train5_MeanStdSum.power_sum.sum()
train5_DOW_MeanStdSum = train5.groupby(['user_id','day_of_week'])['power_consumption'].agg({'DOW_power_mean':np.mean, 'DOW_power_std':np.std, 'DOW_power_sum':np.sum}).reset_index()
train5_DOW_MeanStdSum.groupby('day_of_week')['DOW_power_sum'].agg({'DOW_allsum':sum}).reset_index()
train5_DOW_MeanStdSumAllsum = train5_DOW_MeanStdSum.merge(train5_DOW_MeanStdSum.groupby('day_of_week')['DOW_power_sum'].agg({'DOW_allsum':sum}).reset_index(), on='day_of_week', how='left', copy=True)
train5_DOW_MeanStdSumAllsum['DOW_power_rate'] = train5_DOW_MeanStdSumAllsum.DOW_power_sum / train5_DOW_MeanStdSumAllsum.DOW_allsum
train5_mergeDataset = pd.merge(train5_DOW_MeanStdSumAllsum, train5_MeanStdSum, on='user_id', how='left')

train5_dayofweek_dataset = AllModelWaveletTransformByDOW.waveletTransform(train5)
train5_dayofweek_dataset.drop('level_2', axis=1,inplace=True)

train5_mergeDataset_add = pd.merge(train5_mergeDataset,train5_dayofweek_dataset,on=['user_id', 'day_of_week'], how='left')
#train1_mergeDataset_add = train1_mergeDataset
#train1_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum', 'DOW_power_mean', 'DOW_power_std', 'DOW_powaer_rate', 'power_mean', 'power_std', 'power_rate'], axis=1,inplace=True)
#train1_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum', 'DOW_power_mean', 'DOW_powaer_rate', 'power_mean', 'power_rate'], axis=1,inplace=True)
#train1_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum'], axis=1,inplace=True)
train5_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum', 'DOW_power_rate', 'power_rate'], axis=1,inplace=True)
train5_Y = handledataset[(handledataset.record_date>=(pd.to_datetime('2015-01-01') + pd.to_timedelta(7*77, unit='D'))) & (handledataset.record_date<(pd.to_datetime('2015-01-01') + pd.to_timedelta(7*78, unit='D')))]
final_train5 = pd.merge(train5_mergeDataset_add,train5_Y,on=['user_id', 'day_of_week'], how='left')


print "select train6 dataset ............."
train6 = handledataset[(handledataset.record_date>=pd.to_datetime('2015-01-01')+pd.to_timedelta(7*64, unit='D')) & (handledataset.record_date<(pd.to_datetime('2015-01-01')+pd.to_timedelta(7*76, unit='D')))]
train6_MeanStdSum = train6.groupby(['user_id'])['power_consumption'].agg({'power_mean':np.mean, 'power_std':np.std, 'power_sum':np.sum}).reset_index()
train6_MeanStdSum['power_rate'] = train6_MeanStdSum.power_sum / train6_MeanStdSum.power_sum.sum()
train6_DOW_MeanStdSum = train6.groupby(['user_id','day_of_week'])['power_consumption'].agg({'DOW_power_mean':np.mean, 'DOW_power_std':np.std, 'DOW_power_sum':np.sum}).reset_index()
train6_DOW_MeanStdSum.groupby('day_of_week')['DOW_power_sum'].agg({'DOW_allsum':sum}).reset_index()
train6_DOW_MeanStdSumAllsum = train6_DOW_MeanStdSum.merge(train6_DOW_MeanStdSum.groupby('day_of_week')['DOW_power_sum'].agg({'DOW_allsum':sum}).reset_index(), on='day_of_week', how='left', copy=True)
train6_DOW_MeanStdSumAllsum['DOW_power_rate'] = train6_DOW_MeanStdSumAllsum.DOW_power_sum / train6_DOW_MeanStdSumAllsum.DOW_allsum
train6_mergeDataset = pd.merge(train6_DOW_MeanStdSumAllsum, train6_MeanStdSum, on='user_id', how='left')

train6_dayofweek_dataset = AllModelWaveletTransformByDOW.waveletTransform(train6)
train6_dayofweek_dataset.drop('level_2', axis=1,inplace=True)

train6_mergeDataset_add = pd.merge(train6_mergeDataset,train6_dayofweek_dataset,on=['user_id', 'day_of_week'], how='left')
#train1_mergeDataset_add = train1_mergeDataset
#train1_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum', 'DOW_power_mean', 'DOW_power_std', 'DOW_powaer_rate', 'power_mean', 'power_std', 'power_rate'], axis=1,inplace=True)
#train1_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum', 'DOW_power_mean', 'DOW_powaer_rate', 'power_mean', 'power_rate'], axis=1,inplace=True)
#train1_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum'], axis=1,inplace=True)
train6_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum', 'DOW_power_rate', 'power_rate'], axis=1,inplace=True)
train6_Y = handledataset[(handledataset.record_date>=(pd.to_datetime('2015-01-01') + pd.to_timedelta(7*76, unit='D'))) & (handledataset.record_date<(pd.to_datetime('2015-01-01') + pd.to_timedelta(7*77, unit='D')))]
final_train6 = pd.merge(train6_mergeDataset_add,train6_Y,on=['user_id', 'day_of_week'], how='left')


print "select train7 dataset ............."
train7 = handledataset[(handledataset.record_date>=pd.to_datetime('2015-01-01')+pd.to_timedelta(7*63, unit='D')) & (handledataset.record_date<(pd.to_datetime('2015-01-01')+pd.to_timedelta(7*75, unit='D')))]
train7_MeanStdSum = train7.groupby(['user_id'])['power_consumption'].agg({'power_mean':np.mean, 'power_std':np.std, 'power_sum':np.sum}).reset_index()
train7_MeanStdSum['power_rate'] = train7_MeanStdSum.power_sum / train7_MeanStdSum.power_sum.sum()
train7_DOW_MeanStdSum = train7.groupby(['user_id','day_of_week'])['power_consumption'].agg({'DOW_power_mean':np.mean, 'DOW_power_std':np.std, 'DOW_power_sum':np.sum}).reset_index()
train7_DOW_MeanStdSum.groupby('day_of_week')['DOW_power_sum'].agg({'DOW_allsum':sum}).reset_index()
train7_DOW_MeanStdSumAllsum = train7_DOW_MeanStdSum.merge(train7_DOW_MeanStdSum.groupby('day_of_week')['DOW_power_sum'].agg({'DOW_allsum':sum}).reset_index(), on='day_of_week', how='left', copy=True)
train7_DOW_MeanStdSumAllsum['DOW_power_rate'] = train7_DOW_MeanStdSumAllsum.DOW_power_sum / train7_DOW_MeanStdSumAllsum.DOW_allsum
train7_mergeDataset = pd.merge(train7_DOW_MeanStdSumAllsum, train7_MeanStdSum, on='user_id', how='left')

train7_dayofweek_dataset = AllModelWaveletTransformByDOW.waveletTransform(train7)
train7_dayofweek_dataset.drop('level_2', axis=1,inplace=True)

train7_mergeDataset_add = pd.merge(train7_mergeDataset,train7_dayofweek_dataset,on=['user_id', 'day_of_week'], how='left')
#train1_mergeDataset_add = train1_mergeDataset
#train1_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum', 'DOW_power_mean', 'DOW_power_std', 'DOW_powaer_rate', 'power_mean', 'power_std', 'power_rate'], axis=1,inplace=True)
#train1_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum', 'DOW_power_mean', 'DOW_powaer_rate', 'power_mean', 'power_rate'], axis=1,inplace=True)
#train1_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum'], axis=1,inplace=True)
train7_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum', 'DOW_power_rate', 'power_rate'], axis=1,inplace=True)
train7_Y = handledataset[(handledataset.record_date>=(pd.to_datetime('2015-01-01') + pd.to_timedelta(7*75, unit='D'))) & (handledataset.record_date<(pd.to_datetime('2015-01-01') + pd.to_timedelta(7*76, unit='D')))]
final_train7 = pd.merge(train7_mergeDataset_add,train7_Y,on=['user_id', 'day_of_week'], how='left')

print "select train8 dataset ............."
train8 = handledataset[(handledataset.record_date>=pd.to_datetime('2015-01-01')+pd.to_timedelta(7*62, unit='D')) & (handledataset.record_date<(pd.to_datetime('2015-01-01')+pd.to_timedelta(7*74, unit='D')))]
train8_MeanStdSum = train8.groupby(['user_id'])['power_consumption'].agg({'power_mean':np.mean, 'power_std':np.std, 'power_sum':np.sum}).reset_index()
train8_MeanStdSum['power_rate'] = train8_MeanStdSum.power_sum / train8_MeanStdSum.power_sum.sum()
train8_DOW_MeanStdSum = train8.groupby(['user_id','day_of_week'])['power_consumption'].agg({'DOW_power_mean':np.mean, 'DOW_power_std':np.std, 'DOW_power_sum':np.sum}).reset_index()
train8_DOW_MeanStdSum.groupby('day_of_week')['DOW_power_sum'].agg({'DOW_allsum':sum}).reset_index()
train8_DOW_MeanStdSumAllsum = train8_DOW_MeanStdSum.merge(train8_DOW_MeanStdSum.groupby('day_of_week')['DOW_power_sum'].agg({'DOW_allsum':sum}).reset_index(), on='day_of_week', how='left', copy=True)
train8_DOW_MeanStdSumAllsum['DOW_power_rate'] = train8_DOW_MeanStdSumAllsum.DOW_power_sum / train8_DOW_MeanStdSumAllsum.DOW_allsum
train8_mergeDataset = pd.merge(train8_DOW_MeanStdSumAllsum, train8_MeanStdSum, on='user_id', how='left')

train8_dayofweek_dataset = AllModelWaveletTransformByDOW.waveletTransform(train8)
train8_dayofweek_dataset.drop('level_2', axis=1,inplace=True)

train8_mergeDataset_add = pd.merge(train8_mergeDataset,train8_dayofweek_dataset,on=['user_id', 'day_of_week'], how='left')
#train1_mergeDataset_add = train1_mergeDataset
#train1_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum', 'DOW_power_mean', 'DOW_power_std', 'DOW_powaer_rate', 'power_mean', 'power_std', 'power_rate'], axis=1,inplace=True)
#train1_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum', 'DOW_power_mean', 'DOW_powaer_rate', 'power_mean', 'power_rate'], axis=1,inplace=True)
#train1_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum'], axis=1,inplace=True)
train8_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum', 'DOW_power_rate', 'power_rate'], axis=1,inplace=True)
train8_Y = handledataset[(handledataset.record_date>=(pd.to_datetime('2015-01-01') + pd.to_timedelta(7*74, unit='D'))) & (handledataset.record_date<(pd.to_datetime('2015-01-01') + pd.to_timedelta(7*75, unit='D')))]
final_train8 = pd.merge(train8_mergeDataset_add,train8_Y,on=['user_id', 'day_of_week'], how='left')


print "select train9 dataset ............."
train9 = handledataset[(handledataset.record_date>=pd.to_datetime('2015-01-01')+pd.to_timedelta(7*61, unit='D')) & (handledataset.record_date<(pd.to_datetime('2015-01-01')+pd.to_timedelta(7*73, unit='D')))]
train9_MeanStdSum = train9.groupby(['user_id'])['power_consumption'].agg({'power_mean':np.mean, 'power_std':np.std, 'power_sum':np.sum}).reset_index()
train9_MeanStdSum['power_rate'] = train9_MeanStdSum.power_sum / train9_MeanStdSum.power_sum.sum()
train9_DOW_MeanStdSum = train9.groupby(['user_id','day_of_week'])['power_consumption'].agg({'DOW_power_mean':np.mean, 'DOW_power_std':np.std, 'DOW_power_sum':np.sum}).reset_index()
train9_DOW_MeanStdSum.groupby('day_of_week')['DOW_power_sum'].agg({'DOW_allsum':sum}).reset_index()
train9_DOW_MeanStdSumAllsum = train9_DOW_MeanStdSum.merge(train9_DOW_MeanStdSum.groupby('day_of_week')['DOW_power_sum'].agg({'DOW_allsum':sum}).reset_index(), on='day_of_week', how='left', copy=True)
train9_DOW_MeanStdSumAllsum['DOW_power_rate'] = train9_DOW_MeanStdSumAllsum.DOW_power_sum / train9_DOW_MeanStdSumAllsum.DOW_allsum
train9_mergeDataset = pd.merge(train9_DOW_MeanStdSumAllsum, train9_MeanStdSum, on='user_id', how='left')

train9_dayofweek_dataset = AllModelWaveletTransformByDOW.waveletTransform(train9)
train9_dayofweek_dataset.drop('level_2', axis=1,inplace=True)

train9_mergeDataset_add = pd.merge(train9_mergeDataset,train9_dayofweek_dataset,on=['user_id', 'day_of_week'], how='left')
#train1_mergeDataset_add = train1_mergeDataset
#train1_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum', 'DOW_power_mean', 'DOW_power_std', 'DOW_powaer_rate', 'power_mean', 'power_std', 'power_rate'], axis=1,inplace=True)
#train1_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum', 'DOW_power_mean', 'DOW_powaer_rate', 'power_mean', 'power_rate'], axis=1,inplace=True)
#train1_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum'], axis=1,inplace=True)
train9_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum', 'DOW_power_rate', 'power_rate'], axis=1,inplace=True)
train9_Y = handledataset[(handledataset.record_date>=(pd.to_datetime('2015-01-01') + pd.to_timedelta(7*73, unit='D'))) & (handledataset.record_date<(pd.to_datetime('2015-01-01') + pd.to_timedelta(7*74, unit='D')))]
final_train9 = pd.merge(train9_mergeDataset_add,train9_Y,on=['user_id', 'day_of_week'], how='left')


print "select train10 dataset ............."
train10 = handledataset[(handledataset.record_date>=pd.to_datetime('2015-01-01')+pd.to_timedelta(7*60, unit='D')) & (handledataset.record_date<(pd.to_datetime('2015-01-01')+pd.to_timedelta(7*72, unit='D')))]
train10_MeanStdSum = train10.groupby(['user_id'])['power_consumption'].agg({'power_mean':np.mean, 'power_std':np.std, 'power_sum':np.sum}).reset_index()
train10_MeanStdSum['power_rate'] = train10_MeanStdSum.power_sum / train10_MeanStdSum.power_sum.sum()
train10_DOW_MeanStdSum = train10.groupby(['user_id','day_of_week'])['power_consumption'].agg({'DOW_power_mean':np.mean, 'DOW_power_std':np.std, 'DOW_power_sum':np.sum}).reset_index()
train10_DOW_MeanStdSum.groupby('day_of_week')['DOW_power_sum'].agg({'DOW_allsum':sum}).reset_index()
train10_DOW_MeanStdSumAllsum = train10_DOW_MeanStdSum.merge(train10_DOW_MeanStdSum.groupby('day_of_week')['DOW_power_sum'].agg({'DOW_allsum':sum}).reset_index(), on='day_of_week', how='left', copy=True)
train10_DOW_MeanStdSumAllsum['DOW_power_rate'] = train10_DOW_MeanStdSumAllsum.DOW_power_sum / train10_DOW_MeanStdSumAllsum.DOW_allsum
train10_mergeDataset = pd.merge(train10_DOW_MeanStdSumAllsum, train10_MeanStdSum, on='user_id', how='left')

train10_dayofweek_dataset = AllModelWaveletTransformByDOW.waveletTransform(train10)
train10_dayofweek_dataset.drop('level_2', axis=1,inplace=True)

train10_mergeDataset_add = pd.merge(train10_mergeDataset,train10_dayofweek_dataset,on=['user_id', 'day_of_week'], how='left')
#train1_mergeDataset_add = train1_mergeDataset
#train1_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum', 'DOW_power_mean', 'DOW_power_std', 'DOW_powaer_rate', 'power_mean', 'power_std', 'power_rate'], axis=1,inplace=True)
#train1_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum', 'DOW_power_mean', 'DOW_powaer_rate', 'power_mean', 'power_rate'], axis=1,inplace=True)
#train1_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum'], axis=1,inplace=True)
train10_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum', 'DOW_power_rate', 'power_rate'], axis=1,inplace=True)
train10_Y = handledataset[(handledataset.record_date>=(pd.to_datetime('2015-01-01') + pd.to_timedelta(7*72, unit='D'))) & (handledataset.record_date<(pd.to_datetime('2015-01-01') + pd.to_timedelta(7*73, unit='D')))]
final_train10 = pd.merge(train10_mergeDataset_add,train10_Y,on=['user_id', 'day_of_week'], how='left')


print "select test dataset ............."
test = handledataset[(handledataset.record_date>=pd.to_datetime('2015-01-01')+pd.to_timedelta(7*70, unit='D')) & (handledataset.record_date<(pd.to_datetime('2015-01-01')+pd.to_timedelta(7*82, unit='D')))]
test_MeanStdSum = train4.groupby(['user_id'])['power_consumption'].agg({'power_mean':np.mean, 'power_std':np.std, 'power_sum':np.sum}).reset_index()
test_MeanStdSum['power_rate'] = test_MeanStdSum.power_sum / test_MeanStdSum.power_sum.sum()
test_DOW_MeanStdSum = test.groupby(['user_id','day_of_week'])['power_consumption'].agg({'DOW_power_mean':np.mean, 'DOW_power_std':np.std, 'DOW_power_sum':np.sum}).reset_index()
test_DOW_MeanStdSum.groupby('day_of_week')['DOW_power_sum'].agg({'DOW_allsum':sum}).reset_index()
test_DOW_MeanStdSumAllsum = test_DOW_MeanStdSum.merge(test_DOW_MeanStdSum.groupby('day_of_week')['DOW_power_sum'].agg({'DOW_allsum':sum}).reset_index(), on='day_of_week', how='left', copy=True)
test_DOW_MeanStdSumAllsum['DOW_power_rate'] = test_DOW_MeanStdSumAllsum.DOW_power_sum / test_DOW_MeanStdSumAllsum.DOW_allsum
test_mergeDataset = pd.merge(test_DOW_MeanStdSumAllsum, test_MeanStdSum, on='user_id', how='left')

test_dayofweek_dataset = AllModelWaveletTransformByDOW.waveletTransform(test)
test_dayofweek_dataset.drop('level_2', axis=1,inplace=True)

test_mergeDataset_add = pd.merge(test_mergeDataset,test_dayofweek_dataset,on=['user_id', 'day_of_week'], how='left')
#test_mergeDataset_add = test_mergeDataset
#test_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum', 'DOW_power_mean', 'DOW_power_std', 'DOW_powaer_rate', 'power_mean', 'power_std', 'power_rate'], axis=1,inplace=True)
#test_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum', 'DOW_power_mean', 'DOW_powaer_rate', 'power_mean', 'power_rate'], axis=1,inplace=True)
#test_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum'], axis=1,inplace=True)
test_mergeDataset_add.drop(['DOW_power_sum', 'DOW_allsum', 'power_sum', 'DOW_power_rate', 'power_rate'], axis=1,inplace=True)

test_Y = handledataset[(handledataset.record_date>=(pd.to_datetime('2015-01-01') + pd.to_timedelta(7*82, unit='D'))) & (handledataset.record_date<(pd.to_datetime('2015-01-01') + pd.to_timedelta(7*83, unit='D')))]

final_test = pd.merge(test_mergeDataset_add,test_Y,on=['user_id', 'day_of_week'], how='left')





print "make all train dataset ........."
#train = pd.concat([final_train1, final_train2, final_train3, final_train4], axis=0, ignore_index=True)
train1_matrix = final_train1.drop(['user_id', 'day_of_week', 'record_date'], axis=1).as_matrix()
train2_matrix = final_train2.drop(['user_id', 'day_of_week', 'record_date'], axis=1).as_matrix()
train3_matrix = final_train3.drop(['user_id', 'day_of_week', 'record_date'], axis=1).as_matrix()
train4_matrix = final_train4.drop(['user_id', 'day_of_week', 'record_date'], axis=1).as_matrix()
train5_matrix = final_train5.drop(['user_id', 'day_of_week', 'record_date'], axis=1).as_matrix()
train6_matrix = final_train6.drop(['user_id', 'day_of_week', 'record_date'], axis=1).as_matrix()
train7_matrix = final_train7.drop(['user_id', 'day_of_week', 'record_date'], axis=1).as_matrix()
train8_matrix = final_train8.drop(['user_id', 'day_of_week', 'record_date'], axis=1).as_matrix()
train9_matrix = final_train9.drop(['user_id', 'day_of_week', 'record_date'], axis=1).as_matrix()
train10_matrix = final_train10.drop(['user_id', 'day_of_week', 'record_date'], axis=1).as_matrix()
#final_train_matrix = train.drop(['user_id', 'day_of_week', 'record_date'], axis=1).as_matrix()
final_train_matrix = np.row_stack((train1_matrix, train2_matrix, train3_matrix, train4_matrix, train5_matrix, train6_matrix, train7_matrix, train8_matrix, train9_matrix, train10_matrix))
train_X = final_train_matrix[:,:-1]
train_Y = final_train_matrix[:,-1]

print "make test datset"
final_test_matrix = final_test.drop(['user_id', 'day_of_week', 'record_date'], axis=1).as_matrix()
test_matrix_X = final_test_matrix[:,:-1]
test_matrix_Y = final_test_matrix[:,-1]



print("hyper-parameter optimization...................")
xgb_model = xgb.XGBRegressor()
params = {'max_depth':[2,3,4,5,6], 'learning_rate':[0.05,0.1,0.15], 'n_estimators':[50,100,150,200], 'max_delta_step':[1] ,
          'objective':['reg:linear', 'reg:gamma','reg:tweedie',]}
# , 'colsample_bytree':[1], 'colsample_bylevel':[1], 'reg_alpha':[0], 'reg_lambda':[1], 'scale_pos_weight':[1], 'base_score':[0.5], 'seed':[0], 'missing':[None],'nthread':[-1], 'gamma':[0], 'min_child_weight':[1], , 'subsample':[0.5,0.8,1]
gridsearchcvRegression = GridSearchCV(xgb_model, params, iid=True,scoring=None, n_jobs=1, refit=True, verbose=2, return_train_score=True)

print "optimization fitting ..............."
gridsearchcvRegression.fit(train_X,train_Y)

print "/n"
print "Best Score : ",gridsearchcvRegression.best_score_
print "Best Params : ",gridsearchcvRegression.best_params_

print "predict fiting............."
xgb_model = xgb.XGBRegressor(n_estimators=gridsearchcvRegression.best_params_['n_estimators'],max_depth=gridsearchcvRegression.best_params_['max_depth'],objective=gridsearchcvRegression.best_params_['objective'], max_delta_step=1, learning_rate=gridsearchcvRegression.best_params_['learning_rate'],silent=False)
xgb_model.fit(train_X, train_Y)

input_flag = raw_input("Do you want to save the model by train? Input[y/n]:")
if input_flag == 'y':
	joblib.dump(xgb_model, "../model/F1_xgb_model.m")
print "predict ............"
predict_Y = xgb_model.predict(test_matrix_X)
predict_Y = np.round(predict_Y).astype(int)

print "MSE = ",metrics.mean_squared_error(test_matrix_Y, predict_Y)

summ =0
for i in range(len(test_matrix_Y)):
    if (predict_Y[i]+test_matrix_Y[i]) == 0:
        continue
    summ+=abs((predict_Y[i]-test_matrix_Y[i])/(predict_Y[i]+test_matrix_Y[i]))
meansum = summ/len(test_matrix_Y)
print "MeanSum = ",meansum

print "corrcoef = ",np.corrcoef(predict_Y, test_matrix_Y)


print "create next datasets ..........."
train1_matrix_X = train1_matrix[:,:-1]
train1_predict_Y = xgb_model.predict(train1_matrix_X)
train1_Y['power_consumption'] = train1_predict_Y
train1AndPredictY = pd.concat([train1, train1_Y], axis=0, ignore_index=True)
train1AndPredictY.to_csv(u'../F1_Result/train1AndPredictY.csv', header=True, index=False)

train2_matrix_X = train2_matrix[:,:-1]
train2_predict_Y = xgb_model.predict(train2_matrix_X)
train2_Y['power_consumption'] = train2_predict_Y
train2AndPredictY = pd.concat([train2, train2_Y], axis=0, ignore_index=True)
train2AndPredictY.to_csv(u'../F1_Result/train2AndPredictY.csv', header=True, index=False)

train3_matrix_X = train3_matrix[:,:-1]
train3_predict_Y = xgb_model.predict(train3_matrix_X)
train3_Y['power_consumption'] = train3_predict_Y
train3AndPredictY = pd.concat([train3, train3_Y], axis=0, ignore_index=True)
train3AndPredictY.to_csv(u'../F1_Result/train3AndPredictY.csv', header=True, index=False)

train4_matrix_X = train4_matrix[:,:-1]
train4_predict_Y = xgb_model.predict(train4_matrix_X)
train4_Y['power_consumption'] = train4_predict_Y
train4AndPredictY = pd.concat([train4, train4_Y], axis=0, ignore_index=True)
train4AndPredictY.to_csv(u'../F1_Result/train4AndPredictY.csv', header=True, index=False)

train5_matrix_X = train5_matrix[:,:-1]
train5_predict_Y = xgb_model.predict(train5_matrix_X)
train5_Y['power_consumption'] = train5_predict_Y
train5AndPredictY = pd.concat([train5, train5_Y], axis=0, ignore_index=True)
train5AndPredictY.to_csv(u'../F1_Result/train5AndPredictY.csv', header=True, index=False)

train6_matrix_X = train6_matrix[:,:-1]
train6_predict_Y = xgb_model.predict(train6_matrix_X)
train6_Y['power_consumption'] = train6_predict_Y
train6AndPredictY = pd.concat([train6, train6_Y], axis=0, ignore_index=True)
train6AndPredictY.to_csv(u'../F1_Result/train6AndPredictY.csv', header=True, index=False)

train7_matrix_X = train7_matrix[:,:-1]
train7_predict_Y = xgb_model.predict(train7_matrix_X)
train7_Y['power_consumption'] = train7_predict_Y
train7AndPredictY = pd.concat([train7, train7_Y], axis=0, ignore_index=True)
train7AndPredictY.to_csv(u'../F1_Result/train7AndPredictY.csv', header=True, index=False)

train8_matrix_X = train8_matrix[:,:-1]
train8_predict_Y = xgb_model.predict(train8_matrix_X)
train8_Y['power_consumption'] = train8_predict_Y
train8AndPredictY = pd.concat([train8, train8_Y], axis=0, ignore_index=True)
train8AndPredictY.to_csv(u'../F1_Result/train8AndPredictY.csv', header=True, index=False)

train9_matrix_X = train9_matrix[:,:-1]
train9_predict_Y = xgb_model.predict(train9_matrix_X)
train9_Y['power_consumption'] = train9_predict_Y
train9AndPredictY = pd.concat([train9, train9_Y], axis=0, ignore_index=True)
train9AndPredictY.to_csv(u'../F1_Result/train9AndPredictY.csv', header=True, index=False)

train10_matrix_X = train10_matrix[:,:-1]
train10_predict_Y = xgb_model.predict(train10_matrix_X)
train10_Y['power_consumption'] = train10_predict_Y
train10AndPredictY = pd.concat([train10, train10_Y], axis=0, ignore_index=True)
train10AndPredictY.to_csv(u'../F1_Result/train10AndPredictY.csv', header=True, index=False)

test_Y['power_consumption'] = predict_Y
testAndPredictY = pd.concat([test, test_Y], axis=0, ignore_index=True)
testAndPredictY.to_csv(u'../F1_Result/testAndPredictY.csv', header=True, index=False)

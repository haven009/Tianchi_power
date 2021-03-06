import pandas as pd
import numpy as np
import pywt

def waveletTransform(dataset):
	print "loading dataset .............." 
	def test(group):
		group.reset_index(inplace=True, drop=True)
		waveletGroup = pywt.wavedec(group.power_consumption, 'db2', 'zero')
		wavelet_std_mean_list = list()
		wavelet_std_mean_list.extend([np.std(waveletGroup[0]),np.mean(waveletGroup[0])])
		wavelet_std_mean_list.extend([np.std(waveletGroup[1]),np.mean(waveletGroup[1])])
		wavelet_std_mean_list.extend([np.std(waveletGroup[2]),np.mean(waveletGroup[2])])
		newgroup = pd.DataFrame([wavelet_std_mean_list], columns=['DOW_cA_std', 'DOW_cA_mean', 'DOW_cD2_std', 'DOW_cD2_mean', 'DOW_cD1_std', 'DOW_cD1_mean'])
		return newgroup
	groupbydataset = dataset.groupby(['user_id', 'day_of_week']).apply(test).reset_index()
	return groupbydataset

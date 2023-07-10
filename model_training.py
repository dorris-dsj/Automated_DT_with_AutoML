import autogluon.tabular.predictor
from autogluon.tabular import TabularDataset, TabularPredictor
#from autogluon.core.utils.utils import setup_outputdir
from multilabelpredictor import MultilabelPredictor

#training time
train_data=TabularDataset('datatest_3.csv')
train_data=train_data.head(20)

#train_data.rename(columns={"0":"queue1","1":"queue2","2":"queue3","3":"queue4","4":"latency1","5":"latency2"})
train_data.columns=['queue1','queue2','queue3','queue4','latency1','latency2']
#'','','','','',''
#print(train_data)
#print(train_data.columns)

labels=['latency1','latency2']
#

problem_types=['regression','regression']
save_path='agModels_predict'

time_limit = 5

multi_predictor=MultilabelPredictor(labels=labels,problem_types=problem_types,path=save_path)
multi_predictor.fit(train_data,time_limit=time_limit)

test_data=TabularDataset('datatest_3.csv')
test_data=test_data.sample(20,random_state=1)
test_data.columns=['queue1','queue2','queue3','queue4','latency1','latency2']
test_data_nolab=test_data.drop(columns=labels)
test_data_nolab.head()
# print(test_data_nolab)

multi_predictor=MultilabelPredictor.load(save_path)
predictions=multi_predictor.predict(test_data)
print("Predictions:\n",predictions)

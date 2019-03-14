import pandas as pd
import numpy as np
import warnings
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from scipy import stats

# import dill
import numpy as np
from sklearn import datasets, preprocessing
warnings.filterwarnings('ignore')
import gc, sys
gc.enable()

class Data:
    def __init__(self,predict_rest):
        '''

        :param predict_rest: 需要增加的冗余数据
        '''
        self.input = []  # dict
        self.input_rest = predict_rest  # dataframe
        # self.data_processed =''
        self.sologroupid = '406abb5bce236b'
        self.duegroupid = '92c7b5e8f9ee5e'
        self.squadgroupid = 'b36d4018a110ab'
        self.matchid = 'aeb375fc57110c'
        self.column = ['Id', 'groupId', 'matchId', 'assists', 'boosts', 'damageDealt', 'DBNOs',
                       'headshotKills', 'heals', 'killPlace', 'killPoints', 'kills',
                       'killStreaks', 'longestKill', 'matchDuration', 'matchType', 'maxPlace',
                       'numGroups', 'rankPoints', 'revives', 'rideDistance', 'roadKills',
                       'swimDistance', 'teamKills', 'vehicleDestroys', 'walkDistance',
                       'weaponsAcquired', 'winPoints']

    def fillInf(self,df, val):  # 删除inf值
        '''

        :param df: 输入的dataframe
        :param val: 需要将inf替换的值
        :return:
        '''
        numcols = df.select_dtypes(include='number').columns
        cols = numcols[numcols != 'winPlacePerc']
        df[df == np.Inf] = np.NaN
        df[df == np.NINF] = np.NaN
        for c in cols: df[c].fillna(val, inplace=True)

    def feature_engineering(self,inputdata):
        '''

        :param inputdata: 输入的dataframe
        :return: processeddata(numpy.ndarry), feature_names
        '''
        is_train = False
        print("processing test")
        df = inputdata
        df.dropna(inplace=True)
        df['totalDistance'] = df['rideDistance'] + df["walkDistance"] + df["swimDistance"]
        match = df.groupby('matchId')
        df['killPlacePerc'] = match['kills'].rank(pct=True).values
        df['walkDistancePerc'] = match['walkDistance'].rank(pct=True).values

        df['_totalDistance'] = df['rideDistance'] + df['walkDistance'] + df['swimDistance']
        df['zombi'] = ((df['_totalDistance'] == 0) | (df['kills'] == 0)
                       | (df['weaponsAcquired'] == 0)
                       | (df['matchType'].str.contains('solo'))).astype(int)
        df['cheater'] = ((df['kills'] / df['_totalDistance'] >= 1)
                         | (df['kills'] > 30) | (df['roadKills'] > 10)).astype(int)
        pd.concat([df['zombi'].value_counts(), df['cheater'].value_counts()], axis=1).T
        df['_healthAndBoosts'] = df['heals'] + df['boosts']
        df['_killDamage'] = df['kills'] * 100 + df['damageDealt']
        # all_data['_headshotKillRate'] = all_data['headshotKills'] / all_data['kills']
        df['_killPlaceOverMaxPlace'] = df['killPlace'] / df['maxPlace']
        df['_killsOverWalkDistance'] = df['kills'] / df['walkDistance']
        # all_data['_killsOverDistance'] = all_data['kills'] / all_data['_totalDistance']
        df['_walkDistancePerSec'] = df['walkDistance'] / df['matchDuration']
        # suicide: solo and teamKills > 0
        # all_data['_suicide'] = ((all_data['players'] == 1) & (all_data['teamKills'] > 0)).astype(int)
        self.fillInf(df, 0)
        mapper = lambda x: 'solo' if ('solo' in x) else 'duo' if ('duo' in x) or ('crash' in x) else 'squad'
        # mapper = lambda x: 'solo' if ('solo' in x) else 'team'
        df['matchType'] = df['matchType'].map(mapper)
        df['matchType'] = df['matchType'].map(mapper)
        # 设置哑变量
        a = pd.get_dummies(df['matchType'], prefix='matchType')
        df = pd.concat([df, a], axis=1)
        df.drop(['headshotKills', 'teamKills', 'roadKills', 'vehicleDestroys'], axis=1, inplace=True)
        df.drop(['rideDistance', 'swimDistance', 'matchDuration'], axis=1, inplace=True)
        df.drop(['rankPoints', 'killPoints', 'winPoints'], axis=1, inplace=True)
        df.drop(['matchType'], axis=1, inplace=True)
        del a, match
        gc.collect()
        print("remove some columns")
        target = 'winPlacePerc'
        features = list(df.columns)
        features.remove("Id")
        features.remove("matchId")
        features.remove("groupId")

        y = None

        print("get target")
        if is_train:
            y = np.array(df.groupby(['matchId', 'groupId'])[target].agg('mean'), dtype=np.float64)
            features.remove(target)

        print("get group mean feature")
        agg = df.groupby(['matchId', 'groupId'])[features].agg('mean')
        agg_rank = agg.groupby('matchId')[features].rank(pct=True).reset_index()

        if is_train:
            df_out = agg.reset_index()[['matchId', 'groupId']]
        else:
            df_out = df[['matchId', 'groupId']]

        df_out = df_out.merge(agg.reset_index(), suffixes=["", ""], how='left', on=['matchId', 'groupId'])
        df_out = df_out.merge(agg_rank, suffixes=["_mean", "_mean_rank"], how='left', on=['matchId', 'groupId'])
        del agg, agg_rank
        gc.collect()
        print("get group max feature")
        agg = df.groupby(['matchId', 'groupId'])[features].agg('max')
        agg_rank = agg.groupby('matchId')[features].rank(pct=True).reset_index()
        df_out = df_out.merge(agg.reset_index(), suffixes=["", ""], how='left', on=['matchId', 'groupId'])
        df_out = df_out.merge(agg_rank, suffixes=["_max", "_max_rank"], how='left', on=['matchId', 'groupId'])
        del agg, agg_rank
        gc.collect()
        print("get group min feature")
        agg = df.groupby(['matchId', 'groupId'])[features].agg('min')
        agg_rank = agg.groupby('matchId')[features].rank(pct=True).reset_index()
        df_out = df_out.merge(agg.reset_index(), suffixes=["", ""], how='left', on=['matchId', 'groupId'])
        df_out = df_out.merge(agg_rank, suffixes=["_min", "_min_rank"], how='left', on=['matchId', 'groupId'])
        del agg, agg_rank
        gc.collect()
        print("get group size feature")
        agg = df.groupby(['matchId', 'groupId']).size().reset_index(name='group_size')
        df_out = df_out.merge(agg, how='left', on=['matchId', 'groupId'])

        print("get match mean feature")
        agg = df.groupby(['matchId'])[features].agg('mean').reset_index()
        df_out = df_out.merge(agg, suffixes=["", "_match_mean"], how='left', on=['matchId'])
        del agg
        gc.collect()
        print("get match size feature")
        agg = df.groupby(['matchId']).size().reset_index(name='match_size')
        df_out = df_out.merge(agg, how='left', on=['matchId'])
        gc.collect()
        df_out.drop(["matchId", "groupId"], axis=1, inplace=True)

        X = np.array(df_out, dtype=np.float64)

        feature_names = list(df_out.columns)

        del df, df_out, agg
        gc.collect()
        return X, y, feature_names
class Data_process(Data):
    def __init__(self,predict_rest):
        super().__init__(predict_rest)
        data_processed = np.array([])
        pred_test = np.array([])
        winprec = 0
        self.df_input_converge = [] # 'dataframe'
    # 数据预处理
    def preprocess(self,input):
        '''
        :return:converged testdata
        '''
        #将数据改为和需测试一样
        # predictdatalist = ['id']
        # predictdatalist.append(self.matchid)

        for (key, value) in input.items():
            try:
                input[key] = float(input[key])
            except:
                e=''

        input['matchId'] = self.matchid
        input['Id'] = 'test'
        try:
            if (input['matchType_select'] == 'solo'):
                del input['matchType_select']
                # predictdatalist.append(self.sologroupid)
                input['matchType'] = 'solo'
                input['groupId'] = self.sologroupid
            elif (input['matchType_select'] == 'duo'):
                # predictdatalist.append(self.duegroupid)
                del input['matchType_select']
                # predictdatalist.append(self.sologroupid)
                input['matchType'] = 'duo'
                input['groupId'] = self.duegroupid
            else:
                # predictdatalist.append(self.squedgroupid)
                del input['matchType_select']
                # predictdatalist.append(self.sologroupid)
                input['matchType'] = 'squad'
                input['groupId'] = self.squadgroupid
        except:
            e=''

        predictdatalist =[]
        for (key, value) in input.items():
            predictdatalist.append(key)
        #将数据整合
        df_input = pd.DataFrame(input,index=[0])
        df_input.columns = predictdatalist
        df_input = df_input[self.column]
        print(df_input.tail())
        self.df_input_converge = pd.concat([self.input_rest,df_input],ignore_index=False)
        self.df_input_converge.to_csv("static/res/model/temp_converge.csv",index=False)
        self.df_input_converge = pd.read_csv("static/res/model/temp_converge.csv")
        self.data_processed,_,_ =self.feature_engineering(self.df_input_converge)
        # print(len(self.data_processed))
        return self.data_processed
        # print("x和y的和为：%d"%(self.x+self.y))

    #数据处理
    def process(self,model):
        '''

        :param model: the training model
        :return:the player winperc
        '''
        self.pred_test = model.predict(self.data_processed, num_iteration=model.best_iteration)
        # print(len(self.pred_test))
        self.winprec = self.pred_test.tolist().pop()
        return  self.winprec

    def postprocess(self):
        '''

        :return: fix error winpredict percent
        '''
        print("fix winPlacePerc")
        for i in range(len(self.df_input_converge)):
            winPlacePerc = self.pred_test[i]
            maxPlace = int(self.df_input_converge.iloc[i]['maxPlace'])
            if maxPlace == 0:
                winPlacePerc = 0.0
            elif maxPlace == 1:
                winPlacePerc = 1.0
            else:
                gap = 1.0 / (maxPlace - 1)
                winPlacePerc = round(winPlacePerc / gap) * gap
            if winPlacePerc < 0: winPlacePerc = 0.0
            if winPlacePerc > 1: winPlacePerc = 1.0
            self.pred_test[i] = winPlacePerc
        self.winprec = self.pred_test.tolist().pop()
        return self.winprec
    def getwinprec(self):
        return self.winprec
    def getinputconverge(self):
        return self.df_input_converge
class Data_advice(Data_process):
    advice_list = ['assists', 'boosts', 'damageDealt', 'DBNOs',
                   'headshotKills', 'heals', 'killPlace', 'killPoints', 'kills',
                   'killStreaks', 'longestKill', 'matchDuration', 'maxPlace',
                   'numGroups', 'rankPoints', 'revives', 'rideDistance', 'roadKills',
                   'swimDistance', 'teamKills', 'vehicleDestroys', 'walkDistance',
                   'weaponsAcquired', 'winPoints']
    def __init__(self,predict_rest):
        super().__init__(predict_rest)
        advice = ''

    def giveadvice(self,model,inputconverge):
        '''

        :param model: train model
        :param inputconverge: all test and rest train dataframe
        :return:
        '''
        winpreclist_add = []
        winpreclist_reduce = []
        advicelist = Data_advice.advice_list
        # add
        newdf = inputconverge
        for item in advicelist:
            # 预测
            tempdf = newdf.iloc[[len(newdf)-1]]
            tempdf[item] = tempdf[item] + tempdf[item]/10
            # tempdf.to_csv('temp.csv')
            # newtempdf = pd.concat([newdf, tempdf], ignore_index=False)
            # newtempdf.to_csv('newtemp.csv')
            self.preprocess(tempdf)
            self.process(model)
            newData_predict = self.postprocess()

            #append
            winpreclist_add.append(newData_predict)
        #max_add
        addmax = max(winpreclist_add)
        addmax_index = winpreclist_add.index(addmax)
        #reduce
        for item in advicelist:
            # 预测
            tempdf = newdf.iloc[[len(newdf)-1]]
            tempdf[item] = tempdf[item] - tempdf[item]/10
            if(tempdf[item].values<0):
                tempdf[item] = 0
            self.preprocess(tempdf)
            self.process(model)
            newData_predict = self.postprocess()

            # append
            winpreclist_reduce.append(newData_predict)
        #max_reduce
        reducemax = max(winpreclist_reduce)
        reducemax_index = winpreclist_reduce.index(addmax)
        if(addmax>reducemax):
            self.advice = '增加'+ advicelist[addmax_index]
        else:
            self.advice = '减少'+ advicelist[reducemax_index]
        return self.advice
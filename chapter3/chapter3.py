# 테크닉 21. 데이터를 읽어 들이고 확인하기

import pandas as pd
from dateutil.relativedelta import relativedelta
from pandas.core.indexes.base import InvalidIndexError
import matplotlib.pyplot as plt


uselog= pd.read_csv('use_log.csv')
# print(len(uselog))
# print(uselog.head())


customer = pd.read_csv('customer_master.csv')
# print(len(uselog))
# print(customer.head())

class_master = pd.read_csv('class_master.csv')
# print(len(class_master))
# print(class_master.head())

campaign_master = pd.read_csv('campaign_master.csv')
# print(len(campaign_master))
# print(campaign_master.head())


# 테크닉 22. 고객 데이터 가공하기

customer_join = pd.merge(customer, class_master, on="class", how="left")
customer_join = pd.merge(customer_join, campaign_master, on="campaign_id", how="left")
# print(customer_join.head())

# 결측치 확인하기
# print(len(customer))
# print(len(customer_join))


# 테크닉 23. 고객 데이터 집계
# print(customer_join.groupby("class_name").count()["customer_id"])

# print(customer_join.groupby("campaign_name").count()["customer_id"])

# print(customer_join.groupby("gender").count()["customer_id"])

# print(customer_join.groupby("is_deleted").count()["customer_id"])

# 2018/4/1~2019/3/31 가입인원 
customer_join["start_date"] = pd.to_datetime(customer_join["start_date"])
customer_start = customer_join.loc[customer_join["start_date"] > pd.to_datetime("20180401")]
# print(len(customer_join))


# 최신 고객 데이터 집계
customer_join["end_date"] = pd.to_datetime(customer_join["end_date"])
customer_newer = customer_join.loc[(customer_join["end_date"] >= pd.to_datetime("20190331")) | (customer_join["end_date"].isna())]
# print(len(customer_newer))
# print(customer_newer["end_date"].unique())

# 회원 구분, 캠페인 구분, 성별로 전체 파악
# print(customer_newer.groupby("class_name").count()["customer_id"])
# print()
# print(customer_newer.groupby("campaign_name").count()["customer_id"])
# print()
# print(customer_newer.groupby("gender").count()["customer_id"])



# 테크닉 25
uselog['usedate'] = pd.to_datetime(uselog['usedate'])
uselog['연월'] = uselog['usedate'].dt.strftime('%Y%m')

# 년월 컬럼 만들기
uselog_months = uselog.groupby(["연월","customer_id"],as_index=False).count()

# 년월 별 아이디별 갯수
uselog_months.rename(columns={"log_id":"count"},inplace=True)
del uselog_months["usedate"]
uselog_months.head()

uselog_customer = uselog_months.groupby("customer_id").agg(['mean','median','max','min'])["count"]
uselog_customer = uselog_customer.reset_index(drop=False)
uselog_customer.head()

# 26

uselog['weekday'] = uselog['usedate'].dt.weekday
uselog_weekday = uselog.groupby(['customer_id', '연월','weekday'],
                               as_index=False).count()[['customer_id','연월','weekday','log_id']]
uselog_weekday.rename(columns={"log_id":"count"}, inplace=True)
# 동일 요일 방문 횟수 
# 0 월요일 6 일요일
                                                        
uselog_weekday.head()

uselog_weekday = uselog_weekday.groupby("customer_id", as_index=False).max()[["customer_id","count"]]
# 고객 아이디별로 묶어서 특정 요일에 가장 많이 이용한 최대값 구하기 
uselog_weekday["routine_flg"] = 0
uselog_weekday["routine_flg"] = uselog_weekday["routine_flg"].where(uselog_weekday["count"]<4,1)
# 특정요일 방문 횟수가 4 이상인 고객은 1을 표시 아니면 0 표시 

uselog_weekday.head()


# 27

customer_join = pd.merge(customer_join, uselog_customer, on="customer_id", how="left")
# uselog_weekday의 'customer_id'와 'routine_flg'만 추출해 결합 
customer_join = pd.merge(customer_join, uselog_weekday[["customer_id", "routine_flg"]], on="customer_id", how="left")
customer_join.head()



#28 회원기간
customer_join.head()

customer_join['calc_date'] = customer_join['end_date']
customer_join['calc_date'] = customer_join["calc_date"].fillna(pd.to_datetime("20190430"))
customer_join['membership_period']=0

for i in range(len(customer_join)):
    delta = relativedelta(customer_join['calc_date'].iloc[i], customer_join['start_date'].iloc[i])
    customer_join['membership_period'].iloc[i] = delta.years*12 + delta.months 
    
# print(customer_join.head())


# 테크닉 29. 고객 행동 각종 통계량 파악
# print(customer_join[["mean", "median", "max", "min"]].describe())

# routine_flg 집계
# print(customer_join.groupby("routine_flg").count()["customer_id"])

# routine_flg
# 0     779
# 1    3413       >>> 정기적 사용자 많음

# 회원 기간 분포
# %%
plt.hist(customer_join["membership_period"])
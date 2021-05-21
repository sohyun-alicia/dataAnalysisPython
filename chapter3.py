# 테크닉 21. 데이터를 읽어 들이고 확인하기

import pandas as pd
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
print(customer_newer.groupby("class_name").count()["customer_id"])
print()
print(customer_newer.groupby("campaign_name").count()["customer_id"])
print()
print(customer_newer.groupby("gender").count()["customer_id"])

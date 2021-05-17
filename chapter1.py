import pandas as pd
import matplotlib.pyplot as plt

# 세로 방향(행 방향) 결합
transaction_1 = pd.read_csv('transaction_1.csv')
transaction_2 = pd.read_csv('transaction_2.csv')
transaction = pd.concat([transaction_1, transaction_2], ignore_index=True)
# print(transaction.head())

# print(len(transaction_1))
# print(len(transaction_2))
# print(len(transaction))


# 세로 방향(행 방향) 결합
transaction_detail_1 = pd.read_csv('transaction_detail_1.csv')
transaction_detail_2 = pd.read_csv('transaction_detail_2.csv')
transaction_detail = pd.concat([transaction_detail_1, transaction_detail_2], ignore_index=True)

# print(transaction_detail.head())


#  매출 데이터끼리 결합(조인)
join_data = pd.merge(transaction_detail, transaction[["transaction_id", "payment_date", "customer_id"]], on="transaction_id", how="left")

# print(join_data.head())



#  마스터 데이터 결합
customer_master = pd.read_csv("customer_master.csv")
item_master = pd.read_csv("item_master.csv")
join_data = pd.merge(join_data, customer_master, on="customer_id", how="left")
join_data = pd.merge(join_data, item_master, on="item_id", how="left")
join_data.head()


# 필요한 데이터 컬럼 만들기
join_data["price"] = join_data["quantity"] * join_data["item_price"]
# print(join_data[["quantity", "item_price", "price"]].head())


# 데이터 검산
# print(join_data["price"].sum())
# print(transaction["price"].sum())

# print(join_data["price"].sum() == transaction["price"].sum())



# 각종 통계량 파악
# 결손치 개수 출력
# print(join_data.isnull().sum())
# 각종 통계량 출력(개수count, 평균mean, 표준편차std, ...)
# print(join_data.describe())



# 테크닉 8: 월별 데이터 집계
# 칼럼마다 데이터형 확인
# print(join_data.dtypes)

join_data["payment_date"] = pd.to_datetime(join_data["payment_date"])   # datetime형으로 변환
join_data["payment_month"] = join_data["payment_date"].dt.strftime("%Y%m")  # 연월 단위로 작성
# print(join_data[["payment_date", "payment_month"]].head())

# 집계
print(join_data.groupby("payment_month").sum()["price"])
 

#  테크닉 9: 월별, 상품별 데이터 집계
join_data.groupby(["payment_month", "item_name"]).sum()[["price", "quantity"]]

pd.pivot_table(join_data, index = "item_name", columns="payment_month", values=["price", "quantity"], aggfunc="sum")


# 테크닉 10: 상품별 매출 추이 가시화
graph_data = pd.pivot_table(join_data, index="payment_month", columns="item_name", values="price", aggfunc="sum")
# print(graph_data.head())


#%%
plt.plot(list(graph_data.index), graph_data["PC-A"], label="PC-A")
plt.plot(list(graph_data.index), graph_data["PC-B"], label="PC-B")
plt.plot(list(graph_data.index), graph_data["PC-C"], label="PC-C")
plt.plot(list(graph_data.index), graph_data["PC-D"], label="PC-D")
plt.plot(list(graph_data.index), graph_data["PC-E"], label="PC-E")
plt.legend()
plt.show()
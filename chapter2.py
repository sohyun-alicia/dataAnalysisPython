import pandas as pd



# 11. 데이터 읽기
uriage_data = pd.read_csv("uriage.csv")
# print(uriage_data.head())

kokyaku_data = pd.read_excel("kokyaku_daicho.xlsx")
# print(kokyaku_data.head())


# 12. 데이터 오류 확인
# print(uriage_data["item_name"].head())

# print(uriage_data["item_price"].head())


# 13. 데이터에 오류가 있는 상태로 집계
uriage_data["purchase_date"] = pd.to_datetime(uriage_data["purchase_date"])
uriage_data["purchase_month"] = uriage_data["purchase_date"].dt.strftime("%Y%n")
res = uriage_data.pivot_table(index="purchase_month", columns="item_name", aggfunc="size", fill_value=0)
# print(res)


# 14. 상품명 오류 수정
# 상품명의 유니크 수 확인(매출 이력 item_name의 중복 제외 데이터 건수)
# print(len(pd.unique(uriage_data.item_name)))

# 오류 수정
uriage_data["item_name"] = uriage_data["item_name"].str.upper()
uriage_data["item_name"] = uriage_data["item_name"].str.replace("  ", "")
uriage_data["item_name"] = uriage_data["item_name"].str.replace(" ", "")
# print(uriage_data.sort_values(by=["item_name"], ascending=True))


# 상품명 수정 결과 검증
# print(len(pd.unique(uriage_data["item_name"])))
# print(pd.unique(uriage_data["item_name"]))


# 15. 금액의 결측치 수정
# print(uriage_data.isnull().any(axis=0))



# 결손치 수정
flg_is_null = uriage_data["item_price"].isnull()                # item_price 중 결측치가 있는 곳 조사

#  앞서 생성한 flg_is_null이용, 결측치가 있는 상품명 리스트 작성
for trg in list(uriage_data.loc[flg_is_null, "item_name"].unique()):
    # loc함수는 조건에 일치하는 데이터 추출
    # item_name은 조건과 일치하는 데이터 중 어떤 칼럼을 가져올지 지정
    price = uriage_data.loc[(~flg_is_null) & (uriage_data["item_name"] == trg), "item_price"].max()
    uriage_data["item_price"].loc[(flg_is_null) & (uriage_data["item_name"]==trg)] = price
# print(uriage_data.head())

# 결측치 체크 결과(수정후)
# print(uriage_data.isnull().any(axis=0))


# 각 상품의 금액이 정상적으로 수정됐는지 확인
# for trg in list(uriage_data["item_name"].sort_values().unique()):
    # 반목문에서 상품에 설정된 최대 금액과 최소 금액을 출력
    
    # print(trg + "의 최고가 : " + str(uriage_data.loc[uriage_data["item_name"]==trg]
    # ["item_price"].max()) + "의 최저가 : " + str(uriage_data.loc[uriage_data
    # ["item_name"] == trg]["item_price"].min(skipna=False)))
    # min(skipna=False)에서 skipna는 NaN의 무시 여부 설정
    # False -> NaN이 존재할 경우 최솟값이 NaN으로 표시됨



# 테크닉16. 고객 이름의 오류 수정
# 고객 정보의 고객 이름
# print(kokyaku_data["고객이름"].head())

# 매출 이력의 고객 이름
# print(uriage_data["customer_name"].head())

# 고객 정보의 고객 이름 공백 제거
kokyaku_data["고객이름"] = kokyaku_data["고객이름"].str.replace("  ", "")
kokyaku_data["고객이름"] = kokyaku_data["고객이름"].str.replace(" ", "")
# print(kokyaku_data["고객이름"].head())

# 테크닉17. 날짜 오류 수정
# '숫자'로 읽히는 데이터(오류) 확인
flg_is_serial = kokyaku_data["등록일"].astype("str").str.isdigit()
# print(flg_is_serial)
# print(flg_is_serial.sum())


# 숫자로 등록된 부분 수정
# to_timedelta 함수로 숫자 > 날짜로 변환
fromSerial = pd.to_timedelta(kokyaku_data.loc[flg_is_serial, "등록일"].astype("float"), unit = "D") + pd.to_datetime("1900/01/01")
# print(fromSerial)


# 날짜로 변환된 데이터도 서식 통일하기
# 슬래시로 구분된 서식을 하이픈으로 구분된 서식으로 통일
fromString = pd.to_datetime(kokyaku_data.loc[~flg_is_serial, "등록일"])
print(fromString)

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def main():
    df = pd.read_excel(
        io='HolyGrailWorp.xlsx',
    sheet_name = '2022'
    )

    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(df[['WPA']])

    df['Value'] = scaled * 400

    with pd.ExcelWriter("HolyGrailWorp2.xlsx") as writer:
        df.to_excel(writer, sheet_name="2022", index=False)

main()

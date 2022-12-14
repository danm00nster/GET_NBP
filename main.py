import requests
import json
from requests.exceptions import HTTPError
import pandas as pd
import sqlalchemy
def get_data_range_of_currency(currency, start_date,end_date):
    try:
        url= f'http://api.nbp.pl/api/' \
             f'exchangerates/rates/a/' \
             f'{currency}/' \
             f'{start_date}/' \
             f'{end_date}' \
             f'?format=json'
        response = requests.get(url)
        #print(url)
    except HTTPError as http_error:
        print(f'HTTP error: {http_error}')
    except Exception as e:
        print(f'Other exception: {e}')
    else:
        if response.status_code == 200:
            return json.dumps(response.json(), indent=4, sort_keys=True)

def get_data_range_of_GOLD(start_date,end_date):
    try:
        url= f'http://api.nbp.pl/api/' \
             f'cenyzlota/' \
             f'{start_date}/' \
             f'{end_date}' \
             f'?format=json'
        response = requests.get(url)
        #print(url)
    except HTTPError as http_error:
        print(f'HTTP error: {http_error}')
    except Exception as e:
        print(f'Other exception: {e}')
    else:
        if response.status_code == 200:
            return json.dumps(response.json(), indent=4, sort_keys=True)

if __name__ == '__main__':
    dfCurrency = pd.DataFrame(columns=['effectiveDate', 'mid', 'no','code'])
    dfGOLD=pd.DataFrame(columns=['data','cena'])
    currencySET = ['USD','GBP','EUR','CHF']
    DataSET=[['2018-01-01','2018-12-31'],
             ['2019-01-01','2019-12-31'],
             ['2020-01-01','2020-12-31'],
             ['2021-01-01','2021-12-31'],
             ['2022-01-01','2022-12-12']]
    print(DataSET)
    for start, end in DataSET:
        print('dekodowanie' , start, end, 'GOLD')
        jsonGOLD=json.loads(get_data_range_of_GOLD(start, end))
        for dGOLD in jsonGOLD:
            dictGOLD=dict(dGOLD)
            tmpGOLD=pd.DataFrame.from_dict(dictGOLD,orient='index')
            tmpGOLD=tmpGOLD.transpose()
            dfGOLD=pd.concat([dfGOLD,tmpGOLD])
    for currency in currencySET:
        for start, end in DataSET:
            jsonNBP=json.loads(get_data_range_of_currency(currency, start, end))
            print("dekodowanie", start, end,currency)
            Rrates=((jsonNBP['rates']))

            for RatesDict in Rrates:
                dRatesDict=dict(RatesDict)
                tmpdf=pd.DataFrame.from_dict(dRatesDict, orient='index')
                tmpdf=tmpdf.transpose()
                tmpdf['mid']=tmpdf['mid'].astype(float)
                tmpdf['code']=currency
                dfCurrency= pd.concat([dfCurrency, tmpdf])

    dfGOLD=dfGOLD[['data','cena']]
    print(dfGOLD)
    dfGOLD.to_csv("gold.csv", encoding="utf-8")
    dfCurrency.to_csv("currency.csv", encoding="utf-8")
    print("done")
    # dzia??a po????czenie do bazy
    engine=sqlalchemy.create_engine('mssql+pymssql://adminuser:TjmnhdMySQL1!@pwserver2.database.windows.net:'
                                    '1433/PWdatabase')
    # dzia??a - zapis do bazy
    dfGOLD.to_sql('GOLD', index=False, if_exists='append', con=engine)
    dfCurrency.to_sql('Currency', index=False, if_exists='append', con=engine)

    # print(dfCurrency.head(5))
    # print(dfCurrency.describe())
    # print("------")
    # print(dfCurrency['mid'].dtypes)
    # print(dfCurrency)
    # print(dfGOLD)

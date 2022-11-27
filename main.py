


import requests
import json
from requests.exceptions import HTTPError
import pandas as pd

def get_rates_of_currency(currency, rates_number):
    try:
        url = f'http://api.nbp.pl/api/' \
              f'exchangerates/rates/a/' \
              f'{currency}/' \
              f'last/{rates_number}/' \
              f'?format=json'
        response = requests.get(url)
    except HTTPError as http_error:
        print(f'HTTP error: {http_error}')
    except Exception as e:
        print(f'Other exception: {e}')
    else:
        if response.status_code == 200:
            return json.dumps(response.json(), indent=4, sort_keys=True)

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
    DataSET=[['2018-01-01','2018-12-31'],['2019-01-01','2019-12-31'],['2020-01-01','2020-12-31'],['2021-01-01','2021-12-31']]
    print(DataSET)
    arates_number = 3

    for start, end in DataSET:
        print('dekodowanie' , start, end, 'GOLD')
        jsonGOLD=json.loads(get_data_range_of_GOLD(start, end))
        for dGOLD in jsonGOLD:
            dictGOLD=dict(dGOLD)
            #print(dictGOLD)
            tmpGOLD=pd.DataFrame.from_dict(dictGOLD,orient='index')
            tmpGOLD=tmpGOLD.transpose()
            dfGOLD=pd.concat([dfGOLD,tmpGOLD])

        for currency in currencySET:
            jsonNBP=json.loads(get_data_range_of_currency(currency, start, end))
            #df=pd.DataFrame(data(jsonNBP, columns=['code'])
            #dfa=pd.read_json(get_data_range_of_currency(currency,start,end))
            #dfa=pd.read_json(get_rates_of_currency(currency,arates_number),orient='records')
            print("dekodowanie", start, end,currency)
            Rrates=((jsonNBP['rates']))
            #print(type(Rrates))
            #print(Rrates[iDex])
            #print(dfCurrency.describe())

            for RatesDict in Rrates:
                dRatesDict=dict(RatesDict)
                # cDate=dRatesDict['effectiveDate']
                # cRate=RatesDict['mid']
                tmpdf=pd.DataFrame.from_dict(dRatesDict, orient='index')
                tmpdf=tmpdf.transpose()
                tmpdf['mid']=tmpdf['mid'].astype(float)
                tmpdf['code']=currency
                dfCurrency= pd.concat([dfCurrency, tmpdf])

        #print(tmpdf)
        #print(cDate,currency, cRate)
        # print(tmpdf)
        #print(dfCurrency)
        #print(type(dfCurrency))


    print("done")
    print(dfCurrency.head(5))
    print(dfCurrency.describe())
    print("------")
    print(dfCurrency['mid'].dtypes)
    print(dfCurrency)
    print(dfGOLD)
    # print(dfa.columns)
    # print(dfa.code)
    # print(dfa.rates)
    # print(type(dfa.code))
    #dfa.describe()
    #print("Head")
    #dfa.head()
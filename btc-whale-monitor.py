import pandas as pd
import time
import datetime

days = 5 #change the number to check the transactions in the last X days
start_date = datetime.datetime.now() - datetime.timedelta(days)

#connect to data from xlsx
dftr = pd.read_excel(r'BTC-wallet-tracker1.xlsx')

#list of transactions
latest_trans = []

# appending the transactions to the list

for i in range(len(dftr)):
    wallet_id = dftr.iloc[i]['Address']
    transactions_url = 'https://blockchain.info/rawaddr/' + wallet_id
    df = pd.read_json(transactions_url)
    trans = df['txs']
    d = []
    for i in trans:
        res = int(i['result'])/100000000
        bal = int(i['balance'])/100000000
        timev = i['time']
        timef = (pd.to_datetime(timev, unit='s'))
        obj = {'Result':res,'Balance':bal,'Time':timef}
        d.append(obj)
    tradelist = pd.DataFrame(d)
    for i in range(len(tradelist)):
        timee = tradelist.iloc[i]['Time']
        if timee > start_date:
            res = tradelist.iloc[i]['Result']
            bal = tradelist.iloc[i]['Balance']
            obj = {'Wallet':wallet_id,'Result':res,'Balance':bal,'Time':timee}
            latest_trans.append(obj)
    time.sleep(10)
    
    #time.sleep not to be blocked by blockchain.info

# list of all latest transactions
watchlist = pd.DataFrame(latest_trans)

# number of transactions
print('number of transactions: ', len(watchlist))


# Final btc bought - sold result
finalres = 0.0
for i in range(len(watchlist)):
    finalres += watchlist.iloc[i]['Result']

print('Final btc bought - sold result: ', len(finalres))




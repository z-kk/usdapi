import requests
import json

def getUSDRate():

	url = 'https://www.gaitameonline.com/rateaj/getrate'
	res = requests.get(url).json()

	for row in res['quotes']:

		# 米ドルのみを抽出
		if (row['currencyPairCode'] == 'USDJPY'):
			bid = float(row['bid'])
			ask = float(row['ask'])
			print("bid: {}, ask: {}".format(bid, ask))
			return (bid + ask) / 2

if __name__ == '__main__':

	# 米ドルレートを取得
	rate = getUSDRate()
	print(rate)

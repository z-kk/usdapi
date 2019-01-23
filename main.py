import os
import requests
import json
import time
import datetime

confFile = 'conf.json'
dataFile = 'data.json'

def getUSDRate():
	""" 米ドルの為替レートを取得
	return:
		int 買値と売値の平均値
	"""

	url = "https://www.gaitameonline.com/rateaj/getrate"
	res = requests.get(url).json()

	for row in res['quotes']:

		# 米ドルのみを抽出
		if (row['currencyPairCode'] == "USDJPY"):
			bid = float(row['bid'])
			ask = float(row['ask'])

			return (bid + ask) / 2

def getDataFromJson(fileName):
	""" JSONファイルから過去のデータを取得
	params:
		fileName JSONファイル名
	return:
		dict 過去のデータ
	"""

	if (os.path.exists(fileName)):
		with open(fileName, 'r') as f:
			jdata = json.load(f)
	else:
		jdata = {"data": []}

	return jdata

def checkRate(jdata, rate):
	""" 取得したデータを評価する
	params:
		jdata 過去のデータ
		rate  現在の為替レート
	"""

if __name__ == '__main__':

	# 過去のデータを取得
	jdata = getDataFromJson(dataFile)

	while 1:
		# 米ドルレートを取得
		rate = getUSDRate()

		# 取得したデータを過去のデータに追加
		jdata['data'].append({"when": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "rate": round(rate, 3)})

		# 全データを書き込む
		with open(dataFile, 'w') as f:
			json.dump(jdata, f)

		time.sleep(60)

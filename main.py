import requests
import time
import datetime
import jsonUtils
from slack_bot import Slack

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

def checkRate(jdata, rate):
	""" 取得したデータを評価する
	params:
		jdata 過去のデータ
		rate  現在の為替レート
	"""

	slack = Slack(SLACK_API)

	isOverSellRate = False
	isUnderBuyRate = False

	for row in jdata['data']:
		if (row['rate'] > SELL_RATE):
			isOverSellRate = True
			isUnderBuyRate = False

			if (row['rate'] > MAX_RATE):
				isOverSellRate = False

		elif (row['rate'] < BUY_RATE):
			isOverSellRate = False
			isUnderBuyRate = True

			if (row['rate'] < MIN_RATE):
				isUnderBuyRate = False

		if (row['rate'] < ALERT_RATE):
			isOverSellRate = False

	rateMessage = "為替レートが設定値[{}円]を"
	if (isOverSellRate):
		if (rate > MAX_RATE):
			slack.post_message_to_channel("general", rateMessage.format(str(MAX_RATE)) + "超えました")
			print("max rate")
			jdata.update({"data": []})
		elif (rate < ALERT_RATE):
			slack.post_message_to_channel("general", rateMessage.format(str(ALERT_RATE)) + "下回りました")
			print("alert")
		elif (rate < BUY_RATE):
			slack.post_message_to_channel("general", rateMessage.format(str(BUY_RATE)) + "下回りました")
			print("buy")
	elif (isUnderBuyRate):
		if (rate < MIN_RATE):
			slack.post_message_to_channel("general", rateMessage.format(str(MIN_RATE)) + "下回りました")
			print("min rate")
			jdata.update({"data": []})
		elif (rate > SELL_RATE):
			slack.post_message_to_channel("general", rateMessage.format(str(SELL_RATE)) + "超えました")
			print("sell")

	return jdata

def initialize():
	""" 初期設定
	return:
		dict confData
	"""

	confData = jsonUtils.readJsonFile(confFile)

	if ("MAX_RATE" not in confData):
		MAX_RATE = input("MaxRate: ")
		confData.update({"MAX_RATE": MAX_RATE})
	if ("MIN_RATE" not in confData):
		MIN_RATE = input("MinRate: ")
		confData.update({"MIN_RATE": MIN_RATE})
	if ("BUY_RATE" not in confData):
		BUY_RATE = input("BuyRate: ")
		confData.update({"BUY_RATE": BUY_RATE})
	if ("SELL_RATE" not in confData):
		SELL_RATE = input("SellRate: ")
		confData.update({"SELL_RATE": SELL_RATE})
	if ("ALERT_RATE" not in confData):
		ALERT_RATE = input("AlertRate: ")
		confData.update({"ALERT_RATE": ALERT_RATE})
	if ("SLEEP_TIME" not in confData):
		SLEEP_TIME = input("取得間隔[s]: ")
		confData.update({"SLEEP_TIME": SLEEP_TIME})
	if ("SLACK_API" not in confData):
		SLACK_API = input("slack api: ")
		confData.update({"SLACK_API": SLACK_API})

	jsonUtils.writeJsonFile(confFile, confData)

	return confData

if __name__ == '__main__':
	""" main """

	confData = initialize()

	MAX_RATE = float(confData['MAX_RATE'])
	MIN_RATE = float(confData['MIN_RATE'])
	BUY_RATE = float(confData['BUY_RATE'])
	SELL_RATE = float(confData['SELL_RATE'])
	ALERT_RATE = float(confData['ALERT_RATE'])
	SLEEP_TIME = int(confData['SLEEP_TIME'])
	SLACK_API = confData['SLACK_API']

	# 過去のデータを取得
	jdata = jsonUtils.readJsonFile(dataFile)
	if (jdata == {}):
		jdata = {"data": []}

	while 1:
		# 米ドルレートを取得
		rate = getUSDRate()

		# レートを分析
		checkRate(jdata, rate)

		# 取得したデータを過去のデータに追加
		jdata['data'].append({"when": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "rate": round(rate, 3)})

		# 全データを書き込む
		jsonUtils.writeJsonFile(dataFile, jdata)

		time.sleep(SLEEP_TIME)

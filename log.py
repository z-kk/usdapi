import datetime
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

import jsonUtils

JPY = 0
USD = 1
DEFAULT_MARGIN = 15
jsonFile = "log.json"
dataFile = "data.json"
fp = FontProperties(fname="C:\Windows\Fonts\msgothic.ttc", size=12)

def buyUSD():
	""" 米ドル購入処理 """

	jprice, uprice, rate, margin = getPriceRate()

	if (jprice == 0):
		jprice = uprice * (rate + margin / 100)
	else:
		uprice = jprice / (rate + margin / 100)

	jprice = -jprice

	logData = jsonUtils.readJsonFile(jsonFile)
	if (logData == {}):
		logData = {"data": []}
	logData['data'].append({"when": datetime.date.today().strftime('%Y-%m-%d'), "jprice": round(jprice, 2), "uprice": round(uprice, 2), "rate": round(rate, 2), "margin": margin})

	jsonUtils.writeJsonFile(jsonFile, logData)

	return 0

def buyJPY():
	""" 日本円購入処理 """

	jprice, uprice, rate, margin = getPriceRate()

	if (jprice == 0):
		jprice = uprice * (rate - margin / 100)
	else:
		uprice = jprice / (rate - margin / 100)

	uprice = -uprice

	logData = jsonUtils.readJsonFile(jsonFile)
	if (logData == {}):
		logData = {"data": []}
	logData['data'].append({"when": datetime.date.today().strftime('%Y-%m-%d'), "jprice": round(jprice, 2), "uprice": round(uprice, 2), "rate": round(rate, 2), "margin": margin})

	jsonUtils.writeJsonFile(jsonFile, logData)

	return 0

def showLog():
	""" 購入履歴を表示 """

	logData = jsonUtils.readJsonFile(jsonFile)
	if (logData == {}):
		return 404

	jprice = 0
	uprice = 0

	for row in logData['data']:
		jprice += row['jprice']
		uprice += row['uprice']
		print(row)

	print("日本円収支: {}".format(round(jprice, 2)))
	print("米ドル収支: {}".format(round(uprice, 2)))

	if (jprice < 0):
		rate = - jprice / uprice
		print("現レート: {}".format(round(rate, 2)))
		print("取引時最低レート条件; {}".format(round(rate + DEFAULT_MARGIN / 100, 2)))

	return 0

def printGraph():
	""" 為替レートグラフを出力 """

	jdata = jsonUtils.readJsonFile(dataFile)
	if (jdata == {}):
		return 404

	x = []
	y = []
	for row in jdata['data']:
		x.append(datetime.datetime.strptime(row['when'], "%Y-%m-%d %H:%M:%S"))
		y.append(row['rate'])

	plt.switch_backend("agg")
	plt.plot(x, y, label="rate")
	plt.xlabel("when")
	plt.ylabel("rate")
	plt.title("為替レート", fontproperties=fp)
	plt.legend()

	plt.savefig("data.png")

	return 0

def getPriceRate():
	""" 取引額とレートを取得
	params:
		yod		JPY or USD
	return:
		jprice	取引額[円]
		uprice	取引額[$]
		rate	為替レート[円/$]
		margin	為替手数料[銭]
	"""

	# 取引額を取得
	while 1:
		upstr = input("取引額[$]: ")
		try:
			uprice = float(upstr)
			jprice = 0
			break
		except:
			uprice = 0
		jpstr = input("取引額[円]: ")
		try:
			uprice = 0
			jprice = float(jpstr)
			break
		except:
			jprice = 0

	while 1:
		rateStr = input("為替レート[円/$]: ")
		try:
			rate = float(rateStr)
			break
		except:
			rate = 0

	while 1:
		margStr = input("為替手数料[銭]: ")
		if (margStr == ""):
			margin = DEFAULT_MARGIN
			break
		try:
			margin = int(margStr)
			break
		except:
			margin = 0

	return jprice, uprice, rate, margin

if __name__ == '__main__':
	""" main """

	while 1:
		print()
		print("何をしますか?")
		print("1. 米ドル購入(日本円売却)の登録")
		print("2. 米ドル売却(日本円購入)の登録")
		print("3. 履歴を表示")

		whatToDo = input("> ")

		if (whatToDo == "1"):
			buyUSD()
		elif (whatToDo == "2"):
			buyJPY()
		elif (whatToDo == "3"):
			showLog()
		else:
			printGraph()
			break

	# 終了
	print("return 0")

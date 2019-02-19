import sys

import jsonUtils

DataFile = "data.json"

def qsort(li):
	""" クイックソート
	params:
		li	ソート対象のリスト
	return:
		li	ソートしたリスト
	"""

	if (len(li) < 2):
		return li

	pivot = li[0]

	slist = [x for x in li[1:] if (x['when'] < pivot['when'])]
	llist = [x for x in li[1:] if (x['when'] >= pivot['when'])]

	return qsort(slist) + [pivot] + qsort(llist)

if __name__ == '__main__':
	""" main """

	sys.setrecursionlimit(1000000)

	jdata = jsonUtils.readJsonFile(DataFile)
	if (jdata == {}):
		exit

	jdata['data'] = qsort(jdata['data'])

	jsonUtils.writeJsonFile(DataFile, jdata)
	print("return 0")

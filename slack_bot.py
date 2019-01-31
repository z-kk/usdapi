from slacker import Slacker

slackToken = "hogeToken"

class Slack(object):

	__slacker = None

	def __init__(self, token):
		self.__slacker = Slacker(token)

	def get_channel_list(self):
		""" Slackチーム内のチャンネルID, チャンネル名を取得
		return:
			dict list チャンネルの辞書リスト
		"""

		raw_data = self.__slacker.chennels.list().body

		result = []
		for data in raw_data['channels']:
			result.append(dict(channel_id=data['id'], channel_name=data['name']))

		return result

	def post_message_to_channel(self, channel, message):
		""" Slackのチャンネルにメッセージを投稿する
		params:
			channel チャンネル名
			message 投稿するメッセージ
		"""

		channel_name = "#" + channel
		self.__slacker.chat.post_message(channel_name, message)

if __name__ == '__main__':

	slack = Slack(slackToken)
	slack.post_message_to_channel("random", "hogemessage")

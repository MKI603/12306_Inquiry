# coding: utf8
"""

Usage:
	mytrain.py  <from> <to> <date>

Example：
	mytrain.py 杭州 上海 2018-08-22
	mytrain.py 西藏 济南 2018-08-22

"""
from prettytable import PrettyTable
from colorama import init, Fore
from docopt import docopt
import requests
from stations import stations

init()

class AllTrains(object):
	def __init__(self, trains_list, op_list={}):
		self.headers = '车次 出发站 到达站 出发时间 到达时间 历时 商务特等座 一等 二等 高级软卧 软卧 动卧 硬卧 软座 硬座 无座 其他'.split()
		self.trains_list = trains_list.json()['data']['result']
		self.op_list = op_list
		self.map = trains_list.json()['data']['map']

	@property
	def a_train(self):
		for one in self.trains_list:
			seat = str(one).split('|')

			for i in range(len(seat)):  # 判读是不是空值，是的话转换成--
				if seat[i] == '':
					seat[i] = '--'
				else:
					seat[i] = seat[i]

			message = [
					'\n'.join([Fore.YELLOW + seat[3] + Fore.RESET]),  # 车次s
					'\n'.join([Fore.GREEN + self.map[seat[6]][0:] + Fore.RESET]),  # 出发站
					'\n'.join([Fore.RED + self.map[seat[7]][0:] + Fore.RESET]),  # 到达站
					seat[8],  # 出发时间
					seat[9],  # 到达时间
					seat[10], # 历时
					seat[32], # 商务特等座
					seat[31], # 一等座
					seat[30], # 二等座
					seat[21], # 高级软卧
					seat[23], # 软卧
					seat[33], # 动卧
					seat[28], # 硬卧
					seat[24], # 软座
					seat[28], # 硬卧 
					seat[26], # 无座
					seat[22], # 其他

			]
			yield message


	def show(self):
		pt = PrettyTable()
		pt._set_field_names(self.headers)
		for raw in self.a_train:    # 添加每一列火车的信息
			pt.add_row(raw)
		print(pt)



def main():
	argument = docopt(__doc__)       # 获取用户输入
	from_station = stations.get(argument['<from>'])
	to_station = stations.get(argument['<to>'])        
	date = argument['<date>']
	url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(date, from_station, to_station)
	r = requests.get(url, verify = False)   # 发请求
	AllTrains(r).show()



if __name__ == '__main__':
	main()















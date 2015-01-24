# -*- coding:utf-8 -*-
from statslistmanager import *
def main():
	statsManager = StatsListManager()
	statsManager.get_id_from_json()
	statsManager.get_meta_from_json()
	statsManager.get_stats_from_json()
if __name__ == '__main__':
	main()
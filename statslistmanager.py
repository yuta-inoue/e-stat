import os.path
from statslist import *
import exportjson as ejson
#import exportcsv as ecsv

class StatsListManager:
	def __init__(self,workspace_path=None,lang='J'):
		self.workspace_path = './' if workspace_path is None else './' if os.path.isdir(workspace_path) is False else workspace_path
		if self.workspace_path[len(self.workspace_path)-1]!='/':
			self.workspace_path += '/'
		self.lang = lang
		self.statsList = StatsList(self.lang)
	def get_id_from_json(self,file_name=None):
		if file_name is None:
			json_file = open(self.workspace_path+'id.json','r')
		else:
			json_file = open(self.workspace_path+file_name,'r')
		raw_datas = json.load(json_file)
		dir_path = self.gen_dir('statsIdList')
		for raw_data in raw_datas:
			ids = self.statsList.get_stats_list_ids(raw_data['search_kind'],
				kw=None if 'kw' not in raw_data else raw_data['kw'],
				code=None if 'code' not in raw_data else raw_data['code'],
				field=None if 'field' not in raw_data else raw_data['field'],
				open_years=None if 'open_years' not in raw_data else raw_data['open_years'],
				survey_years=None if 'survey_years' not in raw_data else raw_data['survey_years'])
			file_path = dir_path + raw_data['kw'] + '.json'
			if ids['result']['status']=='0':
				ejson.export_json_dict(ids['stats_list'],file_path)

	def get_meta_from_json(self,file_name=None):
		if file_name is None:
			json_file = open(self.workspace_path+'meta.json','r')
		else:
			json_file = open(self.workspace_path+file_name,'r')
		raw_datas = json.load(json_file)
		dir_path = self.gen_dir('metaInfo')
		for raw_data in raw_datas:
			if raw_data['statistical_table_code'] is None:
				continue
			metas = self.statsList.get_meta_info(raw_data['statistical_table_code'])
			file_path = dir_path + raw_data['statistical_table_code'] + '.json'
			if metas['result']['status']=='0':
				ejson.export_json_dict(metas['class_obj_list'],file_path)

	def get_stats_from_json(self,file_name=None):
		if file_name is None:
			json_file = open(self.workspace_path+'stat.json','r')
		else:
			json_file = open(self.workspace_path+file_name,'r')
		raw_datas = json.load(json_file)
		dir_path = self.gen_dir('statsData')
		for raw_data in raw_datas:
			if raw_data['statistical_table_code'] is None:
				continue
			stats = self.statsList.get_stats_data(raw_data['statistical_table_code'],0)
			file_path = dir_path + raw_data['statistical_table_code'] + '.json'
			if stats['result']['status']=='0':
				ejson.export_json_dict(stats['value_list'],file_path)
	def gen_dir(self,dir_name):
		dir_path = self.workspace_path+dir_name
		if dir_path[len(dir_path)-1]!='/':
			dir_path += '/'
		if (os.path.exists(dir_path) and os.path.isdir(dir_path)) is False:
			os.mkdir(dir_path)
		return dir_path
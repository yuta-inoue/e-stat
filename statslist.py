# -*- coding:utf-8 -*-
import urllib2
import urllib
import json

from bs4 import BeautifulSoup

class StatsList:
  BASE_URL = "http://api.e-stat.go.jp/rest/1.0/app/"
  def __init__(self,lang='J'):
    u"""
    全API共通のパラメータを設定する(同じ階層に存在するclient.jsonからappIdを読み込む)
    """
    json_file = open('client.json','r')
    self.client = json.load(json_file)
    json_file.close()
    self.lang = lang
  def get_stats_list_ids(self,search_kind,kw=None,code=None,field=None,open_years=None,survey_years=None):
    u"""
    統計表の一覧を取得する関数
    @param search_kind
    @return {'result','statsList'}  
    """
    app_id = self.client['appId']
    if kw is not None:
      kw = urllib.quote(kw.decode('utf-8').encode('utf-8'))
    url = '%sgetStatsList?appId=%s&lang=%s' % (self.BASE_URL,app_id,self.lang) + self.gen_params_id(search_kind,kw,code,field,open_years,survey_years).decode('utf-8')
    req = urllib2.Request(url.encode('utf-8'))
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page,'xml')
    result_xml = soup.find('RESULT')
    result = {"status":result_xml.find('STATUS').text,"date":result_xml.find('DATE').text}
    data_list = soup.find('DATALIST_INF')
    num = data_list.find('NUMBER').text
    stats_xml_list = data_list.findAll('LIST_INF')
    stats_list = []
    for stats in stats_xml_list:
      row = {}
      row["statistical_table_code"] = stats.get('id').encode('utf-8')
      stat_name = stats.find('STAT_NAME')
      if stat_name is not None:
        row["stat_name"] = {"code":stat_name.get('code').encode('utf-8'),"text":stat_name.text.encode('utf-8')}
      gov_org = stats.find('GOV_ORG')
      if gov_org is not None:
        row["gov_org"] = {"code":gov_org.get('code').encode('utf-8'),"text":gov_org.text.encode('utf-8')}
      statistics_name = stats.find('STATISTICS_NAME')
      if statistics_name is not None:
        row["statistics_name"] = {"text":statistics_name.text.encode('utf-8')}
      title = stats.find('TITLE')
      if title is not None:
        row["title"] = {"code":'' if title.get('no') is None else title.get('no').encode('utf-8'),"text":title.text.encode('utf-8')}
      cycle = stats.find('CYCLE')
      if cycle is not None:
        row["cycle"] = {"text":cycle.text.encode('utf-8')}
      survey_date = stats.find('SURVEY_DATE')
      if survey_date is not None:
        row["survey_date"] = {"text":survey_date.text.encode('utf-8')}
      open_date = stats.find('OPEN_DATE')
      if open_date is not None:
        row["open_date"] = {"text":open_date.text.encode('utf-8')}
      small_area = stats.find('SMALL_AREA')
      if small_area is not None:
        row["small_area"] = {"text":small_area.text.encode('utf-8')}
      stats_list.append(row)
    return {'result':result,'stats_list':stats_list}

  def get_meta_info(self,stats_data_id):
    u"""
    統計表IDをもとにメタ情報のリストを返す関数
    """
    app_id = self.client['appId']
    url = '%sgetMetaInfo?appId=%s&lang=%s' % (self.BASE_URL,app_id,self.lang) + self.gen_params_meta(stats_data_id)
    req = urllib2.Request(url)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page,'xml')
    result_xml = soup.find('RESULT')
    result = {"status":result_xml.find('STATUS').text,"date":result_xml.find('DATE').text}
    data_list = soup.find('METADATA_INF')
    table_inf = data_list.find('TABLE_INF')
    class_obj_tags = data_list.find('CLASS_INF').findAll('CLASS_OBJ')
    class_obj_list = {}

    for class_obj in class_obj_tags:
      class_obj_id = class_obj.get('id').encode('utf-8')
      class_obj_name = class_obj.get('name').encode('utf-8')
      class_obj_item = {
        'id':class_obj_id,
        'name':class_obj_name,
        'objects':{}
      }
      class_tags = class_obj.findAll('CLASS')
      for class_tag in class_tags:
        class_item = {
          'code':class_tag.get('code').encode('utf-8'),
          'name':class_tag.get('name').encode('utf-8'),
          'level':class_tag.get('level').encode('utf-8'),
          'unit': '' if class_tag.get('unit') is None else class_tag.get('unit').encode('utf-8')
        }
        class_obj_item['objects'][class_item['code']] = class_item
      class_obj_list[class_obj_id] = class_obj_item
    return {'result':result,'class_obj_list':class_obj_list}
  def get_stats_data(self,stats_data_id,start_position,value_list=None):
    u"""
    統計表IDをもとに統計情報を取得する
    """
    app_id = self.client['appId']
    url = '%sgetStatsData?limit=10000&appId=%s&lang=%s&metaGetFlg=N&cntGetFlg=N' % (self.BASE_URL,app_id,self.lang) + self.gen_params_meta(stats_data_id)
    if start_position > 0:
      url += ('&startPosition=%d' % start_position)
    req = urllib2.Request(url)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page,'xml')
    result_xml = soup.find('RESULT')
    result = {"status":result_xml.find('STATUS').text,"date":result_xml.find('DATE').text}
    data_list = soup.find('STATISTICAL_DATA')
    table_inf = data_list.find('TABLE_INF')
    value_tags = data_list.find('DATA_INF').findAll('VALUE')
    if value_list is None:
      value_list = []
    for value in value_tags:
      value_item = {
        'tab':'' if value.get('tab') is None else value.get('tab').encode('utf-8'),
        'cat01':'' if value.get('cat01') is None else value.get('cat01').encode('utf-8'),
        'cat02':'' if value.get('cat02') is None else value.get('cat02').encode('utf-8'),
        'cat03':'' if value.get('cat03') is None else value.get('cat03').encode('utf-8'),
        'area':'' if value.get('area') is None else value.get('area').encode('utf-8'),
        'time':'' if value.get('time') is None else value.get('time').encode('utf-8'),
        'unit':'' if value.get('unit') is None else value.get('unit').encode('utf-8'),
        'value':value.text.encode('utf-8')
      }
      value_list.append(value_item)

    next_tag = table_inf.findAll('NEXT_KEY')
    if next_tag:
      if next_tag[0].text:
        self.get_stats_data(stats_data_id,int(next_tag[0].text),value_list)
    return {'result':result,'value_list':value_list}
  def gen_params_meta(self,stats_data_id):
    u"""
    メタ情報を取得する際のURLパラメータを生成      
    """
    params = '&statsDataId=%s' % stats_data_id
    return params
  def gen_params_id(self,search_kind,kw,code,field,open_years,survey_years):
    u"""
    統計表IDを取得する際のURLパラメータを生成
    """
    params = '&searchKind=%s' % search_kind
    params += '' if kw is None else '&searchWord=%s' % kw.decode('utf-8').encode('utf-8')
    params += '' if code is None else '&statsCode=%s' % code.encode('utf-8')
    params += '' if field is None else '&statsField=%s' % field.encode('utf-8')
    params += '' if open_years is None else '&openYears=%s' % open_years.encode('utf-8')
    params += '' if survey_years is None else '&surveyYears=%s' % survey_years.encode('utf-8')
    return params
  def gen_params_stats(self,stats_data_id):
    u"""
    統計情報を取得する際のURLパラメータを生成      
    """
    params = '&statsDataId=%s' % stats_data_id
    return params
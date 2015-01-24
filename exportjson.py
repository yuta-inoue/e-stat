import json
import sys
import codecs
sys.stdin = codecs.getreader("utf-8")(sys.stdin)
sys.stdout = codecs.getwriter("utf-8")(sys.stdout)
def export_json_dict(objects,path):
	f = codecs.open(path,'w','utf-8')
	json.dump(objects,f,ensure_ascii=False,indent=4)
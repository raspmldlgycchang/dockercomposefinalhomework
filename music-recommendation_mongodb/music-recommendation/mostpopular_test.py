import os
import json

base_path = os.getcwd()+'/recom_data/results/json_dir/'

def make_answers_Dir():
	for i in range(10):
		readpath = 'recom_data/results/results.json'
		filepath = base_path+'users'+str(i)+'/results.json'
		dirname = os.path.dirname(filepath)
		if not os.path.exists(dirname):
			os.makedirs(dirname)
		os.system('python3 split_data.py run data/train.json')
		os.system('python3 most_popular.py run --train_fname=recom_data/orig/train.json --question_fname=recom_data/questions/val.json')
		with open(readpath, "r") as fp:
			obj = json.load(fp)
			with open(filepath, "w") as f:
				f.write(json.dumps(obj))

if __name__=="__main__":
	make_answers_Dir()

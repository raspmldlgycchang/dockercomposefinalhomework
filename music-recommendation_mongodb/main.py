from typing import Optional

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel

import json
import pymongo
import os

app = FastAPI()

class Item(BaseModel):
	result:str
	cid:str

users = []
count = {}
result = {}

myclient = pymongo.MongoClient("mongodb://mongo-server:27017")
#myclient = pymongo.MongoClient("mongodb+srv://<Database username>:<Database password>@<요기 개인마다 다른것같아 생략>/<db이름>")
#mydb = myclient["test"]
#mycol = mydb["usertodays"]
mydb = myclient["mydatabase"]
mycol = mydb["customers"]

#print(myclient.list_database_names())

@app.get("/v2/customers/{cid}")
async def add_customers(cid:str):
	mycol.save({"cid":cid})
	if mycol.find({cid:cid})!=None:
		return {
				"result":"SUCCESS",
				"customerID": "{cid}"
		}
	else:
		return {
				"result":"FAILED",
				"message":"duplicate {cid}"
		}
@app.get("/v2/customers/{cid}/listened/{sid}")
async def add_users(cid:str, sid:str):
	if mycol.find({cid:cid,sid:sid})!=None:
		return {
				"result":"SUCCESS",
				"customerID": "{cid}",
				"studentID": "{sid}"
		}
	else:
		return {
				"result":"FAILED",
				"message":"duplicate {cid} {sid}"
		}
@app.post("/{result}/{cid}")
async def make_result(item:Item):
	dictionary = dict(item)
	dictionary['success'] = True
	return dictionary
@app.put("/v2/customers/{cid}")
async def add_users(cid:str) -> dict:
	mycol.save({"cid":cid})

	if mycol.find({cid:cid})!=None:
		return {
				"result":"SUCCESS"
		}
				
	else:
		return {
				"result":"FAILED",
				"message":{cid}
		}
@app.post("/v2/customers/")
async def update_users(cid:str):
	if mycol.find({cid:cid})!=None:
		pass
@app.get("/v2/post")
async def get_document():
	cur_path = os.getcwd()
	img_path = cur_path + '/public/img/IU.jpg'
	print("img_path and mycol[0].name is"+img_path==mycol[0].name)
	for i in range(mycol.find({})):
		html = '<html>'
		html += '<head><meta charset="utf-8">'
		html +='<body><p>'
		html += mycol[0].name
		html += '</p></body></head></html>'
	return html
@app.put("/users/")
async def add_users(name:str, username: str, password: str):
	mycol.save({"name":name, "username":username, "password":password})
	if mycol.find({username:username})!=None:
		result["result"] = "SUCCESS"
	else:
		result["result"] = "FAILED"
	return result
@app.get("/")
async def get_root():
	return "this is first web"
@app.get("/users/")
async def get_users():
	for i in mycol.find():
		#print(i)
		users.append({'username':i.get('username'), 'password':i.get('password')})
	return users
@app.delete("/users/")
async def delete_user(username: str):
	if mycol.find({username:username})!=None:
		mycol.remove({"username":username})
		result["result"] = "SUCCESS"
	else:
		result["result"] = "FAILED"
	return result

@app.get("/users/_count_")
async def count_users():
	size = 0
	for i in mycol.find({}):
		size += 1
	count["count"] = size
	return count

@app.put("/users/{userid}/recommendations/playlist/{songid}")
async def add_songs(userid:str,songid:str):
	with open('../music-recommendation/data/song_meta.json','r') as fp:
		obj = json.load(fp)
@app.get("/users/{userid}/recommendations")
async def get_playlist(userid:str):
	if mycol.find({userid:userid})==None:
		return {
			"result":"no customer"
		}
	else:
		with open("./music-recommendation/data/song_meta.json","r") as fp:
			obj = json.load(fp)
			result["result"]="FAILED"
			for i in range(len(obj)):
				if(obj[i]["id"]==songid):
					result["result"] = "SUCCESS"
			if results.get('result')=="FAILED":
				return 0
		userplaylist = []
		userplaylist.append(int(songid))
		userplaydict={songs:0 for songs in userplaylist}
		return {
				"userid":{userid},
				"songs":[
					{},
					{},
					{},
					{}
				]
		}
	
	return {
			"result":"FAILED"
	}
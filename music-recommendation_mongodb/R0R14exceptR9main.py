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
playlist = []
count = {}
result = {}
myclient = pymongo.MongoClient("mongodb://mongo-server:27017")
mydb = myclient["mydatabase"]
mycol = mydb["customers"]
songcol = mydb["songs"]

#R3
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
#R4
@app.put("/v2/customers/{cid}")
async def add_users(cid:str, name:str):
	if mycol.find({cid:cid})!=None:
		mycol.drop(mycol.find({cid:cid}))
		mycol.save({"cid":cid,"name":name}))
	else:
		return {
				"result":"FAILED",
				"message":"{cid} not found"
		}
	return {
		"result":"SUCCESS",
		"customer ID":"{cid}",
		"name":"{name}"
	}
#R6
@app.delete("/v2/customers/{cid}")
async def delete_users(cid:str):
	if mycol.find({cid:cid})!=None:
		mycol.remove({"cid":cid})
	else:
		return {
			"result":"FAILED",
			"message":"{cid} not found"
		}
	return {
			"result":"SUCCESS",
			"customer ID":"{cid}"
	}
#R7_1
@app.post("/v2/customers/{cid}/listened/{sid}")
async def add_songs(cid:str,sid:str):
	if mycol.find({cid:cid})!=None:
		length_ = 0
		playlist_private = []
		for i in range(len(mycol.find({cid:cid}))):
				length_+=1
		for i in range(length):
			playlist_private.append({mycol.find({cid:cid}).get('sid'))
		songcol.save({"sid":sid})
		mycol.drop(mycol.find({cid:cid}))
		mycol.save({"customer id":"{cid}","songs":playlist_private})
		return {
				"customerID": "{cid}",
				"songs":locals(playlist_private)
		}
	else:
		return {
				"result":"FAILED",
				"message":"duplicate {cid}"
		}
#R7_2
@app.get("/v2/customers/{cid}/listened")
async def get_lists(cid:str):
	if mycol.find({cid:cid})!=None:
		return mycol.find({cid:cid})
	else:
		return {
			"result":"FAILED",
			"message":"{cid} not found"
		}
#R7_3
@app.delete("/v2/customers/{cid}/listened/{sid}")
async def delete_songs(cid:str,sid:str):
	obj = json.dumps(sid)
	for i in range(mycol.find({cid:cid}).get('songs')):
		if i._isEqual(obj,i):
			mycol.find({cid:cid}).get('songs').remove(i)
			return mycol.find({cid:cid})
		else:
			pass
	return {
		"result":"FAILED"
	}
#R8
@app.get("/v2/songs/{sid}")
async def get_popular(sid:str):
	with open('../music-recommendation/data/song_meta.json', 'r') as fp:
		obj = json.load(fp)
	for i in range(len(obj)):
		j = i.get['song id']
		if i.get['song id'] == json.dumps(sid):
			playlist = []
			for k in range(j.get['artist id']):
				playlist.append(j.get['artist id'])
			return {
				"song_id":"{sid}",
				"album_id": i.get['album_id'],
				"artists": playlist
			}

#R5
@app.get("/v2/customers/{cid}")
async def get_users(cid:str):
	if mycol.find({cid:cid,name:name})!=None:
		return {
			"result":"SUCCESS",
			"customer ID":"{cid}",
			"name":"{name}"
		}
	elif mycol.find({cid:cid})!=None:
		return {
			"result":"SUCCESS",
			"customer ID":"{cid}"
		}
	else:
		return {
			"reuslt":"FAILED",
			"message:":"{cid} not found"
		}
#R12
@app.get("/v2/")
async def get_root():
	return "please insert song_meta.json file at host machine at this location: ./musie-recommendation/data/song_meta.json"

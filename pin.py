#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from flask import Flask,request,  Response, json
sys.path.append('pydal')
from pydal import DAL, Field
class JSONDateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        else:
            return json.JSONEncoder.default(self, obj)
        
def model():
    db = DAL('sqlite://pin.db',pool_size=1,folder='./',migrate=False)
    Pin=db.define_table('pin',Field('title'),Field('image'))
    return (db,Pin)

app = Flask(__name__, static_url_path='')    

@app.route('/')
def index():
    return app.send_static_file("index.html")

@app.route('/api/<tablename>',methods=['GET',"POST"])
@app.route('/api/<tablename>/<mid>',methods=["PUT","DELETE"])
def api(tablename,mid=None):
    db,Pin=model()
    if request.method=="GET":
        table = db[tablename]
        query = table.id>0
        rows = db(query).select().as_list()  
        return Response(json.dumps({'objects':rows},cls=JSONDateTimeEncoder), mimetype='application/json')
    elif request.method=="POST":
        data=request.json #request.get_data()
        id=db[tablename].insert(**data)
        db.commit()
        data[id]=id
        return Response(json.dumps(data,cls=JSONDateTimeEncoder), mimetype='application/json')
 
    elif request.method=="PUT":
        data=request.json #request.get_data()
        db(db[tablename]._id==int(mid)).update(**data)
        db.commit()
        data['id']=mid
        return Response(json.dumps(data,cls=JSONDateTimeEncoder), mimetype='application/json')
    
    elif request.method=="DELETE":
        db(db[tablename]._id==int(mid)).delete()
        db.commit()
        return Response(json.dumps({}))
     
            
app.debug = True

if __name__ == "__main__":
    app.run()
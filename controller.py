import os, os.path
import random
import string
import operator

import cherrypy

import json
from models import RedisDb


class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return open('views/index.html')

    @cherrypy.expose
    def about(self):
        return open('../index.html')


    #trending equity index data population API
    @cherrypy.expose
    def getindexapi(self):
        rdb=RedisDb('localhost','eqlist')
        conn=rdb.connect()
        res={'a':1,'b':2,'c':3}
        equityList=rdb.getequityListindex(conn)
        print(equityList)
        res=[]
        for item in equityList:
            fields=rdb.getequityHash(conn,item)
            fields={i.decode('ascii'):j.decode('ascii') for i,j in fields.items()}#converting binary to string key:value
            fields['HIGH']=float(fields['HIGH'])
            # fields={i.decode('ascii'):j.decode('ascii') for i,j in fields.items()}
            res.append(fields)

        sorted_res=sorted(res, key=operator.itemgetter("HIGH"))
        return json.dumps(sorted_res[-10:][::-1])


    # graph data population api
    @cherrypy.expose
    def getGraphDatAPI(self):
        rdb=RedisDb('localhost','eqlist')
        conn=rdb.connect()
        res={'a':1,'b':2,'c':3}
        equityList=rdb.getequityListindex(conn)
        print(equityList)
        res=[]
        for item in equityList:
            fields=rdb.getequityHash(conn,item)
            fields={i.decode('UTF-8'):j.decode('UTF-8') for i,j in fields.items()}#converting binary to string key:value
            fields['HIGH']=float(fields['HIGH'])
            # fields={i.decode('ascii'):j.decode('ascii') for i,j in fields.items()}
            res.append(fields)

        sorted_res=sorted(res, key=operator.itemgetter("HIGH"))[-4:]
        companies=[]
        datas=[]
        for i in sorted_res:
            data=[0]
            for value in ['OPEN', 'HIGH','LOW','CLOSE']:
                data.append(float(i[value]))
            datas.append(data)
            companies.append(i['SC_NAME'])
        result={"data":datas,"companies":companies}

        # result=json.loads(result)
        print(result['data'])

        return json.dumps(result)
    
    #search engine auto fill api
    @cherrypy.expose
    def getAutoFillData(self):
        rdb=RedisDb('localhost','eqlist')
        conn=rdb.connect()
        equityList=rdb.getequityListindex(conn)
        print(equityList)
        res=[]
        for item in equityList:
            fields=rdb.getequityHash(conn,item)
            fields={i.decode('UTF-8'):j.decode('UTF-8') for i,j in fields.items()}#converting binary to string key:value
            company=fields['SC_NAME']
            # fields={i.decode('ascii'):j.decode('ascii') for i,j in fields.items()}
            res.append(company)

        return json.dumps(res)
    

    #search engine api
    @cherrypy.expose
    def searchAPI(self,searchString):
        rdb=RedisDb('localhost','eqlist')
        conn=rdb.connect()
        searchString=searchString.strip()
        count=searchString.split()
        res=[]
        if len(count) > 0:
            searchString='_'.join(count)
            for i in count:
                searchString=i+'_'
                indexes=conn.lrange(searchString,0,-1)
                res+=indexes

        else:
            searchString+='_'
            indexes=conn.lrange(searchString,0,-1)
            res+=indexes
        res=[i.decode('ascii') for i in res]
        results=set(res)
        results=list(results)
        final_res=[]
        for item in results:
            fields=rdb.getequityHash(conn,item)
            fields={i.decode('ascii'):j.decode('ascii') for i,j in fields.items()}#converting binary to string key:value
            fields['HIGH']=float(fields['HIGH'])
            # fields={i.decode('ascii'):j.decode('ascii') for i,j in fields.items()}
            final_res.append(fields)
        return json.dumps(final_res)


import redis



class RedisDb(object):
	"""redis database model functions to set and get key,values"""
	def __init__(self, host,EQUITY_LIST_KEY):
		self.host = host
		self.EQUITY_LIST_KEY=EQUITY_LIST_KEY

	def connect(self):
		conn=redis.Redis(host=self.host)
		return conn 

	def getNewId(self,key,conn):
		if conn.setnx(key,1) == False:
			return conn.incr(key)
		else:
			return 1

	def setequityListindex(self,conn,value):
		key=self.EQUITY_LIST_KEY
		length=conn.lpush(key,value)
		index_values=conn.lrange(key, 0, -1)
		return length,index_values

	def getequityListindex(self,conn):
		key=self.EQUITY_LIST_KEY
		return conn.lrange(key, 0, -1)
	
	def deleteEquityList(self,conn):
		key=self.EQUITY_LIST_KEY
		conn.delete(key)

    #fields {code,name,start,stop,high,low,timestamp}
    #key is I=>(getId)
	def setequityHash(self,conn,key,fields={}):
		return conn.hmset(key, fields)

	def getequityHash(self,conn,key):
		return conn.hgetall(key)

	def setSearchListindex(self,conn,key,value):
		# key=self.EQUITY_LIST_KEY
		length=conn.lpush(key,value)
		# index_values=conn.lrange(key, 0, -1)
		return length




# rdb=RedisDb('localhost','eqlist')
# conn=rdb.connect()
# print(conn)
# index_key='id'

# fields=[{'code':123,'name':'xyz','start':123,'stop':222,'high':222,'low':124},
#         {'code':123,'name':'xyz','start':123,'stop':222,'high':222,'low':124},
#         {'code':123,'name':'xyz','start':123,'stop':222,'high':222,'low':124}]
# rdb.deleteEquityList(conn)
# for field in fields:
# 	value=rdb.getNewId(index_key,conn)
# 	print(value)
# 	rdb.setequityListindex(conn,value)
# 	rdb.setequityHash(conn,value,field)
# 	print(rdb.getequityHash(conn,value))

# print(rdb.getequityListindex(conn))


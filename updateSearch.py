import redis
from models import RedisDb


def updateSearchModel():
	rdb=RedisDb('localhost','eqlist')
	conn=rdb.connect()
	equityList=rdb.getequityListindex(conn)
	res=[]
	for item in equityList:
		fields=rdb.getequityHash(conn,item)
		fields={i.decode('UTF-8'):j.decode('UTF-8') for i,j in fields.items()}#converting binary to string key:value
		company_name=fields['SC_NAME']
		company_name= company_name.strip()
		count=company_name.split()
		if len(count) > 0:
			company_name='_'.join(count)
		for l in range(1,len(company_name)+1):
			prefix=company_name[0:l]
			prefix+='_'
			value=int(item)
			print(value)
			key=str(prefix)
			print(key)
			length=rdb.setSearchListindex(conn,key,value)
			# print(length)
			# conn.lpush(p, int(i))
			# print(prefix)
			
	print('updated search engine model')


if __name__=="__main__":
	updateSearchModel()




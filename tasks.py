import os

from selenium.webdriver import Firefox 
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

import wget
import time
import zipfile
import csv

from celery import Celery

app = Celery('tasks', broker='amqp://localhost')
app.config_from_object("celeryconfig")


from models import RedisDb




@app.task
def getBhavData():
	try:
		url="https://www.bseindia.com/markets/equity/EQReports/BhavCopyDebt.aspx?expandable=3&utm_campaign=website&utm_source=sendgrid.com&utm_medium=email"
		
		opts = Options()
		opts.set_headless()
		browser = Firefox(executable_path="/home/prajwal/project/cherryApp/geckodriver",options=opts)
		
		browser.get(url)
		
		#gets iframe element using xpath
		iframeElements = browser.find_elements_by_xpath('/html/body/form/div[3]/div/div[3]/div[2]/div/div[2]/div/div/table/tbody/tr/td/iframe')
		browser.switch_to.frame(iframeElements[0]) #switches to iframe element
		html_page = browser.page_source #gets page source of iframe

		soup = BeautifulSoup(html_page, 'html.parser')
		link=soup.find('a',attrs={'id': 'btnhylZip'},href=True)
		download_link=link['href'] 
		*_,file_name=download_link.split('/') #gets file name from download url link
		print(file_name)

		current_dir=os.getcwd()
		download_dir=os.path.join(current_dir,'bhavDownload') #path for download directory
		os.makedirs(download_dir, exist_ok=True) #creates dirctory if not exits
        
        #dowload file from link
		wget.download(download_link,out=download_dir)
		download_filename=os.path.join(download_dir,file_name)
		print(download_filename)

		#unzips downloaded file to download_dir and extracts csv file
		zip_ref = zipfile.ZipFile(download_filename, 'r')
		zip_ref.extractall(download_dir)
		zip_ref.close()

        #gets downloaded CSV File name 
		csv_filename,*_=file_name.split('_')
		csv_filename='.'.join((csv_filename,'CSV'))
		print(csv_filename)

		# files=os.listdir(download_dir)
		# print(files)
		try:
			csv_filepath=os.path.join(download_dir,csv_filename)
			print(csv_filepath)
			with open(csv_filepath, 'r') as csvFile:
				print('file opened')
				reader = csv.DictReader(csvFile)
				print(reader)
				rdb=RedisDb('localhost','eqlist')
				conn=rdb.connect()
				print(conn)
				index_key='id'
				rdb.deleteEquityList(conn)
				for row in reader:
					row=dict(row)
					field=dict([(i,row[i])for i in ['SC_CODE','SC_NAME','OPEN','CLOSE','LOW', 'HIGH'] ])
					field['HIGH']=float(field['HIGH'])
					field['LOW']=float(field['LOW'])
					value=rdb.getNewId(index_key,conn)
					print(value)
					rdb.setequityListindex(conn,value)
					rdb.setequityHash(conn,value,field)
					print(rdb.getequityHash(conn,value))
				print(rdb.getequityListindex(conn))
		except:
			print('failed to read csv')

		
		time.sleep( 5 )
		print('downloaded file deleting started')

		try:
			#deletes all files in download dir
			files=os.listdir(download_dir)
			for file in files:
				os.remove(os.path.join(download_dir,file))
		except OSError:
			pass

		browser.close() #closes browser
	except:
		print('faild to get data')

if __name__=="__main__":
	getBhavData()



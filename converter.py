#!/usr/bin/python

#Author : SimMan
#Date: 2016-03-24
#Github: simman

import sys  
reload(sys)  
sys.setdefaultencoding('utf8')   
import sqlite3
import time

DB_FILE_PATH = ''

def init():
	global DB_FILE_PATH
	
def converter():
	conn = sqlite3.connect(DB_FILE_PATH)
	
	sql = """
	select title,text,created,category,tags from typecho_contents c,
	 (select cid,group_concat(m.name) tags from typecho_metas m,typecho_relationships r where m.mid=r.mid and m.type='tag' group by cid ) t1,
	(select cid,m.name category from typecho_metas m,typecho_relationships r where m.mid=r.mid and m.type='category') t2
	where t1.cid=t2.cid and c.cid=t1.cid
	"""
	articles = fetchall(conn, sql)
	if len(articles) > 0:
		for e in range(len(articles)):
			title = articles[e][0]
			content = articles[e][1].replace('<!--markdown-->','')
			x = time.localtime(articles[e][2])
			create = time.strftime('%Y-%m-%d %H:%M:%S',x)
			category = articles[e][3]
			tags = articles[e][4]
			
			md_content = "title: %s\ncategories: %s\ntags: %s\ndate: %s\n---\n\n%s" % (title, category, tags, create, content)
			outmdfile(title, md_content.decode('utf-8'))

def outmdfile(title, content):
	filename = title + '.md'
	file = open(filename, 'w')
	file.write(content)
	file.close( )
	print('generate ' + filename + ' success')

def fetchall(conn, sql):
	if sql is not None and sql != '':
		cu = conn.cursor()
		cu.execute(sql)
		r = cu.fetchall()
		return r
	else:
		print('the [{}] is empty or equal None!'.format(sql)) 

def main():
	init()
	converter()

if __name__ == '__main__':
	main()

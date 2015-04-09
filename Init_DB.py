from DBConnector import DBConnector
import psycopg2
		
class Init_DB():
	
	connector = None
	
	def __init__(self):
		self.connector = DBConnector.get_connection()
		self.connector.conn.autocommit = True
		
	def init_db(self):
		self.create_table_metrics()
		
	def create_table_metrics(self):
		cursor = self.connector.conn.cursor()
		cursor.execute('drop table IF EXISTS metrics')
		
		cursor.execute("""Create table metrics(
			release text, 
			class_path text, 
			CBO int, 
			LCOM int);""")
			
		cursor.close()
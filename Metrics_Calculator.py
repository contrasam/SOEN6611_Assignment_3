import understand
import sys
import re
from LCOM import LCOM
from CBO import CBO
from Init_DB import Init_DB
from DBConnector import DBConnector


class Metrics_Calculator:

	def __init__(self):
		self.db_file_name = None
		self.release_version = None
		self.connector = DBConnector.get_connection()
		self.connector.conn.autocommit = True

		Init_DB().init_db()

	def measure(self):
		if len(sys.argv) < 3:
		    print("Please provide understand DB file name and release version")
		    return
		else:
		    self.db_file_name = sys.argv[1]
		    self.release_version = sys.argv[2]

		db = understand.open(self.db_file_name)

		lcom = LCOM()
		cbo = CBO()

		cursor = self.connector.conn.cursor()		
		
		ents_system_namespace = dict()
		ents_system_class = dict()

		cpp_class_regex = re.compile("[\w]+[.](cpp|cc)")

		for ent_file in db.lookup(cpp_class_regex, "File"):
			ents_namespace = ent_file.ents("Declare","Namespace")
			for ent_namespace in ents_namespace:
				self.get_ents_namespace(ents_system_namespace,ent_namespace)

			ents_global_class = ent_file.ents("Define", "Class Type, Abstract Class Type")
			for ent_global_class in ents_global_class:
				ents_system_class[ent_global_class.longname()] = ent_global_class

		self.get_ents_class(ents_system_class,ents_system_namespace)

		for ent_class_key, ent_class_val in ents_system_class.items():

			lcom_val = lcom.calculate_lcom(ent_class_val)
			cbo_val = cbo.calculate_cbo(ent_class_val,ents_system_class)

			cursor.execute("""
                insert into metrics values(%s, %s, %s, %s)
            """,(self.release_version.strip(), ent_class_key.strip(), cbo_val, lcom_val))
			
		cursor.close()

	def get_ents_namespace(self,ents_system_namespace,entity):
		ents_namespace = entity.ents("Declare","Namespace")
		ents_system_namespace[entity.name()] = entity
		
		if(len(ents_namespace)<=0):
			return	
		else:
			for ent_namespace in ents_namespace:
				self.get_ents_namespace(ents_system_namespace,ent_namespace)

	def get_ents_class(self,ents_system_class,ents_system_namespace):
		for ent_namespace_key, ent_namespace_val  in ents_system_namespace.items():
			ents_class = ent_namespace_val.ents("Define", "Class Type, Abstract Class Type")
			for ent_class in ents_class:
				ents_system_class[ent_class.longname()] = ent_class

metric_calc = Metrics_Calculator()
metric_calc.measure()
		

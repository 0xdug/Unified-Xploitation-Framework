__author__ = 'deadmanwalking'

"""
.. module:: DB_API_1
	:platform: Linux
	:synopsis: A module for DB API.

.. moduleauthor:: Arjun T.U <d3admanwalking2252@gmail.com>
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

# This class is the encapsulation class . The class which can be imported to get all the DB functionalities.


class inter:
	"""The super class """
	Base = declarative_base()

	def make_base(self):
		"""Makes the variable **Base global** and assigns it the value assigned above ( which is local)."""
		global Base
		Base = self.Base

	def __init__(self):
		"""The constructor for the inter class . Calls the *make_base()* function."""
		self.make_base()

	def create_obj(self):
		"""Creates an object of the **class DBinter** and returns it."""
		obj = self.DBinter()
		return obj

	# This is the section where all the classes for table creation are inserted.
	class myDB(Base):
		__tablename__ = "posts"

		id = Column(Integer, primary_key=True)
		title = Column(String)
		body = Column(String)
		payload = Column(String)

	class DBinter:
		"""This is the *class which interacts with the classes for table creation* above and provides the API's"""

		# Function tables can be optimised further and it will be.
		def tables(self, data_dict=None, db_name=None):
			"""This function creates a db object based on the data and db_name given and returns it.

			*data_dict -> dictionary with the column name as keys and data to be inserted as values
			*db_name   -> the name of the db to which it is to be inserted
			"""
			if data_dict is None or db_name is None:
				return None
			"""Using the keys and values,an *argument string of the format id="1",title="new_post",body="None",payload=0
			is created*.This newly created string is substituted for function argument . The db_name is also substituted.
			Both of this is done using the **eval()** function.
			"""
			key = list(data_dict.keys())
			i = 0
			argument_str = ""
			while i < len(data_dict):
				if i == 0:
					argument_str = argument_str + str(key[i]) + "=" + " \" " + str(data_dict[key[i]]) + " \" "
					i = i + 1
					continue
				argument_str = argument_str + "," + str(key[i]) + "=" + " \" " + str(data_dict[key[i]]) + " \" "
				i = i + 1
			post = eval("inter." + db_name + "(" + argument_str + ")")
			return post

		def __init__(self):
			"""Constuctor for the *class DBinter*.

			*self.engine        -> The link between the server and program.
			*self.session       -> session object created using the engine.
			*self.session.main  -> instantiating session.
			*self.Base          -> The reason why we made Base global

			**change the create_engine function argument as per your system**.

			*deadmanwalking -> postgreusername
			*keysersoze2252 -> postgrepassword
			*localhost      -> current machine
			*myDB           -> the database
			"""
			self.engine = create_engine("postgresql://deadmanwalking:keysersoze2252@localhost/myDB")
			self.session = sessionmaker(bind=self.engine)
			self.session_main = self.session()
			self.Base = Base

		def create_tables_all(self):
			"""*Creates all the tables* specified above"""
			self.Base.metadata.create_all(self.engine)

		def drop_tables_all(self):
			"""*Deletes all the tables* specified above"""
			self.session_main.close()
			self.Base.metadata.drop_all(bind=self.engine)

		def insert_data(self, data_dict, db_name):
			"""Actual **insertion** of data into the db.

			*data_dict -> the dictionary containing data.
			*db_name   -> the name of the db to which data is to be inserted.
			*obj       -> the db object returned by tables()

			*self.session_main.add(obj) -> adds the object
			*self.session_main.commit() -> commits the changes
			"""
			obj = self.tables(data_dict, db_name)
			if obj is None:
				print("Error :- No data provided")
				exit()
			self.session_main.add(obj)
			self.session_main.commit()

		def get_session(self):
			"""Returns the **session_main instance**."""
			return self.session_main

		# Further optimisations like commiting the changes only after adding all the objects can be done.
		def insert_data_file(self, file_path, db_name):
			"""Reads data from the *file specified and creates data_dict* , which is then passed to insert_data()
			*The first line of the file is the column names*.From 2nd line onwards the data is presented.
			The seperator used here is a **single whitespace**.

			*file_path -> path of the file.
			*key  -> list column names creates using the first line of file.
			*line -> single line in the file(seperator ->/n)
			*word -> single word in the line(seperator -> whitespace)
			*i    -> to see if its the first line or not

			The list key is used as the key for creation of data_dict
			"""
			key = []
			i = 0
			with open(file_path, 'r') as file:
				data_dict = {}
				for line in file:
					j = 0
					for word in line.split():
						if i == 0:
							key.append(word)
						else:
							data_dict[key[j]] = word
							j = j + 1
					i = i+1
					if data_dict != {}:
						self.insert_data(data_dict, db_name)


def test():
	"""Funtion intended for **testing the working of the API**.

	*inter_obj    -> inter class object.
	*db_inter_obj -> object of DB_inter class creates using inter_obj
	*fp           -> path of the file (here with respect to this file)
	*session      -> instance of session obtained using DB_inter_obj



	*db_inter_obj.create_tables_all()           -> creates all the tables in the DB
	*session.query(inter.myDB).all()            -> returns the list of all the myDB objects.
	*session.query(inter.myDB).all()[1]         -> returns the second object ( staring index -> 0)
	*session.query(inter.myDB).all()[1].payload -> returns the value at column payload for 2nd object
	*db_inter_obj.drop_tables_all()             -> deletes all the tables in the DB
	"""
	inter_obj = inter()
	db_inter_obj = inter_obj.create_obj()
	db_inter_obj.create_tables_all()
	fp = os.path.join(os.path.dirname(__file__), 'my_file')
	db_inter_obj.insert_data_file(fp, "myDB")
	session = db_inter_obj.get_session()
	print(session.query(inter.myDB).all()[1].payload)
	db_inter_obj.drop_tables_all()


test()

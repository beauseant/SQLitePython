#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys


class DataBase:

	_name	= 'docs.db'
	_con	= None
	_direct	= ''
	
	def __init__ ( self, direct ):

		self._direct = direct

		try:
		    self._con = lite.connect( self._name )
		    
		    cur = self._con.cursor()    
		    cur.execute('SELECT SQLITE_VERSION()')
		    
		    data = cur.fetchone()
		    
		    print "SQLite version: %s" % data                
		    
		except lite.Error, e:
		    
		    print "Error %s:" % e.args[0]
		    sys.exit(1)
		    
	    

	def __del__ ( self ):
		if self._con:
			self._con.close()


	def cargarDatos ( self ):
		with self._con:    
		    cur = self._con.cursor()    
		    cur.execute("CREATE VIRTUAL TABLE Documentos USING fts4 (Id INT, Name TEXT, Contenido TEXT)")
		

		

if __name__ == "__main__":

	db	= DataBase ('Documentos/')
	db.cargarDatos ()




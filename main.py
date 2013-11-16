#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
import os
import logging
import argparse
import time

class DataBase:

	_name	= 'docs.db'
	_con	= None
	_dir	= ''
	
	def __init__ ( self, direct ):

		self._dir = direct

		try:
		    self._con = lite.connect( self._name )

		    #Base de datos solo en memoria, no se guarda nada el terminar:
		    #self._con = lite.connect( :memory )
		    
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


		totales = []


		for base, dirs, files in os.walk( self._dir):
			logging.debug ( 'Cargando %s' % ( base ) )
			for fich in files:
				with self._con:    
					cur = self._con.cursor()
					with open(base + '/' + fich) as f:
						data = f.read()
						totales.append  ((fich, unicode (data, "utf-8")) )

		#Grabamos las cosas en una tabla de tipo fts4 que se supone se encuentra optimizida para buscar textos en ella:
		with self._con:    
			cur = self._con.cursor()    
			cur.execute("DROP TABLE IF EXISTS Documentos_fts4")
			cur.execute("CREATE VIRTUAL TABLE Documentos_fts4 USING fts4 (Name TEXT, Contenido TEXT)")
			cur = self._con.cursor()
			cur.executemany ("INSERT INTO Documentos_fts4 (Name, Contenido) VALUES (?,?)", totales  )
			self._con.commit()

		#Grabamos las cosas en una tabla normal que deberia dar unos resultados netamente inferiores a una tabla fts4 al buscar textos:
		with self._con:    
			cur = self._con.cursor()    
			cur.execute("DROP TABLE IF EXISTS Documentos")
			cur.execute("CREATE TABLE Documentos  (Name TEXT, Contenido TEXT)")
			cur = self._con.cursor()
			cur.executemany ("INSERT INTO Documentos (Name, Contenido) VALUES (?,?)", totales  )
			self._con.commit()



	def _lanzarConsulta ( self, consulta ):
		with self._con:    
			cur = self._con.cursor()    
			cur.execute( consulta )
			rows = cur.fetchall()
			return rows


	def buscarPalabra ( self, palabra,fts4 = 0 ):

		#¿Queremos hacer la busqueda en la tabla fts4 o en una tabla normal?

		if not (fts4):
			return self._lanzarConsulta ( "SELECT rowid, Name FROM " + 'Documentos' + " WHERE Contenido LIKE '%" + palabra + "%'" )
		else:
			return self._lanzarConsulta ( "SELECT rowid, Name FROM " + 'Documentos_fts4' + " WHERE Contenido MATCH '" + palabra + "'" )
		

		

if __name__ == "__main__":

	parser	= argparse.ArgumentParser ( description= '' )
	parser.add_argument('--d', action="store_true", help='imprimir informacion de debug')

	args	 =	parser.parse_args()

	if args.d:
		logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)



	db	= DataBase ('DocEjemplo/')

	t0 = time.time()
	db.cargarDatos ()
	t1 = time.time()
	print 'directorio cargado en %s secs' % (t1-t0)

	palabra = 'yesterday'

	t0 = time.time()
	r =  db.buscarPalabra (palabra, 1)
	t1 = time.time()
	total1 = t1-t0
	print 'Encontrada la palabra %s %s. Tiempo usando tablas fts4:  \t %s' % (palabra, r, total1 )

	t0 = time.time()
	r = db.buscarPalabra (palabra, 0)
	t1 = time.time()
	total2 = t1 -t0
	print 'Encontrada la palabra %s %s. Tiempo NO usando tablas fts4: \t %s' % (palabra, r, total2 )

	print 'tiemponormal / tiempofts4: %s' % (total2 / total1)







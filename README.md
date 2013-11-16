El objetivo de este programa es volcar un directorio que contiene ficheros en formato texto en una base de datos SQLite. La idea es comparar el uso de las tablas estándar de SQLite con el formato de tablas FTS4, optimizada para guardar texto.

Desde el programa prinicpal, main.py, se abre el directorio DocsEjemplo y procede a cargar ese directorio en un tabla FTS4 y en una tabla normal, una vez cargado se procede a comparar los tiempos. En todos los casos analizados las tablas FTS4 son superiores.


http://www.sqlite.org/fts3.html


Como usar el programa:

	python main.py --d

Salida típica:

SQLite version: 3.8.0.2
DEBUG:Cargando DocEjemplo/
directorio cargado en 1.7425160408 secs
Encontrada la palabra yesterday [(2, u'11.txt'), (3, u'pg1661.txt.1'), (4, u'pg135.txt'), (5, u'pg1661.txt')]. Tiempo usando tablas fts4:  	 0.0092658996582
Encontrada la palabra yesterday [(2, u'11.txt'), (3, u'pg1661.txt.1'), (4, u'pg135.txt'), (5, u'pg1661.txt')]. Tiempo NO usando tablas fts4: 	 0.0112941265106
tiemponormal / tiempofts4: 1.21889151914

Editando main.py se puede cambiar la palabra a buscar o el directorio que contiene los ficheros.




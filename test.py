import sqlite3

with sqlite3.connect("bd_btf.db") as conexion:
	try:
		sentencia = ''' create  table personajes
		(
		id integer primary key autoincrement,
		nombre text,
		apellido text,
		anio real
		)
		'''
		conexion.execute(sentencia)
		print("Se creo la tabla personajes")                       
	except sqlite3.OperationalError:
		print("La tabla personajes ya existe")

	#INSERT:

	try:
		conexion.execute("insert into personajes(nombre,apellido,anio) values (?,?,?)", ("Marty", "MacFly","1968"))
		conexion.execute("insert into personajes(nombre,apellido,anio) values (?,?,?)", ("Emmet", "Brown","1914")) 
		conexion.commit()# Actualiza los datos realmente en la tabla
	except:
		print("Error")

	#SELECT:
	cursor=conexion.execute("SELECT * FROM personajes")
	for fila in cursor:
		print(fila)

	#RECUPERAR UNA SOLA FILA:
	id = "1"
	sentencia = "SELECT * FROM personajes WHERE id=?"
	cursor=conexion.execute(sentencia,(id,))
	for fila in cursor:
		print(fila)

	#ACTUALIZAR DATOS EN RELACION A ID 1
	sentencia = "UPDATE personajes SET nombre = 'XX' WHERE id=?"
	cursor=conexion.execute(sentencia,(id,))
	filas=cursor.fetchall()
	for fila in filas:
		print(fila)

	#ELIMINAR DATOS EN RELACION A ID 1
	sentencia = "DELETE FROM personajes WHERE id=?"
	cursor=conexion.execute(sentencia,(id,))

	#SELECT:
	cursor=conexion.execute("SELECT * FROM personajes")
	for fila in cursor:
		print(fila)
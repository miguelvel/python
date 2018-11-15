#!/usr/bin/python
# -*- coding: utf-8 -*-

#Para ejecutar este script solo basta con ir a un terminal y ejecutar el comando python pedregal.py
#previamente debemos cambiar el usuario y password del servidor MySQL a conectarnos.
#Este script crea la base de datos 'python_pedregal', crea la tabla 'cajas_producidas', lee y valida los
#registros del archivo cajas.txt para depues insertarlos como registros en la tabla 'cajas_producidas'


# Importamos el modulo para trabajar con MySQL
import MySQLdb
# Importamos el modulo para trabajar con expresiones regulares
import re
 
# Conectar a la base de datos
# Tenemos que sustituir los valores por los correpondientes al servidor MySQL
db = MySQLdb.connect(host = "localhost",user = "root",passwd = "CLAVE")

# Creamos un objeto tipo cursor que sera el que nos permitira el acceso al servidor de base de datos.
cursor = db.cursor()

# Creamos la base de datos python_pedregal(puede ser otro nombre)
#cursor.execute ("DROP DATABASE IF EXISTS python_pedregal")
cursor.execute ("CREATE DATABASE python_pedregal")
# Usamos la base de datos creada(python_pedregal)
cursor.execute ("USE python_pedregal")
#cursor.execute ("DROP TABLE IF EXISTS cajas_producidas")
#creamos la tabla cajas_producidas mediante sql
cursor.execute ("""
                   CREATE TABLE cajas_producidas
                   (
                       id              int(11) NOT NULL AUTO_INCREMENT,
                       serial          VARCHAR(7) NOT NULL,
                       codigo          VARCHAR(2) NOT NULL,
                       especie         VARCHAR(50) NOT NULL,
                       variedad        VARCHAR(50) NOT NULL,
                       procedencia     VARCHAR(50) NOT NULL,
                       anio_produccion VARCHAR(50) NOT NULL,
                       PRIMARY KEY (`id`)
                   )
                """)

#abrimos el archivo caja.txt de donde se leeran y validaran los datos
file = open('cajas.txt')

#recorremos el archivo
for linea in file:
    #mediante expresiones regulares validamos la estructura del codigo segun especificaciones
    if re.match('[B]....[1,2][9,0,1][1,2].......', linea):
        # si la validacion es correcta guardamos en variables la estructura del codigo
        serial = linea[8:15]
        codigo = linea[3:5]
        especie = linea[7]
        if especie == '1':
            esp = "Uva"
        elif especie == '2':
            esp = "Palta"
        else:
            esp = ""

        variedad = linea[2]

        procedencia = linea[7]
        if procedencia == '1':
            proc = 'Ica'
        elif procedencia == '2':
            proc = 'Piura'
        else:
            proc = ""

        anio_produccion = linea[6]
        if anio_produccion == '9':
            anio = '2009'
        elif anio_produccion == '0':
            anio = '2010'
        elif anio_produccion == '1':
            anio = '2011'
        else:
            anio = ""

        #escribimos la sentencia sql que efectuara la insercion de registros en la tabla cajas_producidas
        sql = "INSERT INTO cajas_producidas (serial, codigo, especie, variedad, procedencia, anio_produccion) VALUES ('%s','%s','%s','%s','%s','%s')" % (serial,codigo,esp,variedad,proc,anio)
        #ejecutamos la consulta
        cursor.execute(sql)

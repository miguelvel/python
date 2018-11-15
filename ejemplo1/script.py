import xlrd
import datetime
path = 'D:\Proyecto SAP\PeruActiveSoLinesReportDetailed.xlsx'

workbook = xlrd.open_workbook(path)
worksheet = workbook.sheet_by_index(0)

# Change this depending on how many header rows are present
# Set to 0 if you want to include the header data.
offset = 1

#este script de ejemplo valida nuevos registros del excel y los registra en la BD Hana, obtiene registros de clientes, areas, branches y assignments

clientes = []
for i, row in enumerate(range(worksheet.nrows)):
    cod_cliente = worksheet.cell_value(i,6)
    nom_cliente = worksheet.cell_value(i,7)
    cliente = [cod_cliente,nom_cliente]
    if cliente not in clientes:
        clientes.append(cliente)

branches = []
for i, row in enumerate(range(worksheet.nrows)):
    cod_branch = worksheet.cell_value(i,0)
    nom_branch = worksheet.cell_value(i,1)
    branch = [cod_branch,nom_branch]
    if branch not in branches:
        branches.append(branch)

areas = []
for i, row in enumerate(range(worksheet.nrows)):
    cod_branch = worksheet.cell_value(i,0)
    cod_area = worksheet.cell_value(i,2)
    nom_area = worksheet.cell_value(i,3)
    so_status = worksheet.cell_value(i,4)
    area = [cod_branch,cod_area,nom_area,so_status]
    if area[3] == 'AUTHORIZED':
        if area not in areas:
            areas.append(area)    

assignments = []
for i, row in enumerate(range(worksheet.nrows)):
    cod_cliente = worksheet.cell_value(i,6)
    cod_cliente = worksheet.cell_value(i,6)
    cod_branch = worksheet.cell_value(i,0)
    cod_area = worksheet.cell_value(i,2)
    cod_assignment = worksheet.cell_value(i,8)
    nom_assignment = worksheet.cell_value(i,9)
    so_status = worksheet.cell_value(i,4)
    assignment = ['C'+cod_cliente,cod_branch,cod_area,cod_assignment,nom_assignment,so_status]
    if assignment[5] == 'AUTHORIZED':
        if assignment not in assignments:
            assignments.append(assignment)


print ('Total clientes: %s' % (len(clientes)))
print ('Total branches: %s' % (len(branches)))
print ('Total areas: %s' % (len(areas)))
print ('Total assignments: %s' % (len(assignments)))

#conectar a SAP HANA
import pyhdb

#credenciales sap hana bd
P_SERVER = 'X.X.X.X'
P_PORT ='XXXXX'
P_USER_SERVER = 'XXXXXX'
P_PASSWD_SERVER = 'XXXXX'
P_COMPANY = 'XXXXXX'

connection = pyhdb.connect(host=P_SERVER,port=P_PORT,user=P_USER_SERVER,password=P_PASSWD_SERVER)
cursor = connection.cursor()


###########################################################################
############################## BRANCH #####################################
###########################################################################

for branch in branches:
    cursor.execute("""SELECT CODBRANCH,NOMBRANCH FROM "%s"."MAESTROS_BRANCH" where CODBRANCH='%s' """ % (P_COMPANY,branch[0]))
    branch_actuales = cursor.fetchall()
    if len(branch_actuales) == 0:
         cursor.execute("""INSERT INTO "%s"."MAESTROS_BRANCH"(CODBRANCH,NOMBRANCH,ESTADO,FECHACREACION,FECHAEDICION,MAQUINACREACION,MAQUINAEDICION,USUARIOCREACION_ID,
                USUARIOEDICION_ID) VALUES(%s,'%s',1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,'127.0.0.1',null,null,null)""" % (P_COMPANY,branch[0],branch[1]))
         connection.commit()
         print("successfull branch")


###########################################################################
############################### AREA ######################################
###########################################################################

for area in areas:
    cursor.execute("""SELECT* FROM "%s"."MAESTROS_AREA" where CODAREA='%s' and CODBRANCH_ID='%s'""" % (P_COMPANY,area[1],area[0]))
    area_actuales = cursor.fetchall()
    if len(area_actuales) == 0:
        cursor.execute("""INSERT INTO "%s"."MAESTROS_AREA"(CODAREA,NOMAREA,ESTADO,FECHACREACION,FECHAEDICION,MAQUINACREACION,MAQUINAEDICION,CODBRANCH_ID,USUARIOCREACION_ID,
                USUARIOEDICION_ID) VALUES('%s','%s',1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,'127.0.0.1',null,'%s',null,null)""" % (P_COMPANY,area[1],area[2],area[0]))
        connection.commit()
        print("successfull area")


###########################################################################
######################## CLIENTES - EJECUTAR SP ###########################
###########################################################################

cursor.execute(""" call "%s".SP_CLIENTE_CARGA """ % (P_COMPANY))
connection.commit()
print("succesfull SP_CLIENTE_CARGA") 

###########################################################################
########################### ASSIGNMENT ####################################
###########################################################################


for assignment in assignments:
    cursor.execute("""SELECT CODCLIENTE FROM "%s"."MAESTROS_CLIENTE" WHERE CODCLIENTE='%s'"""% (P_COMPANY,assignment[0]))
    cliente_actuales = cursor.fetchall()
    if len(cliente_actuales) != 0:
        cursor.execute("""SELECT* FROM "%s"."MAESTROS_ASSIGNMENT" where CODASSIGNMENT='%s' and CODAREA_ID='%s' and CODBRANCH_ID=%s and CODCLIENTE_ID='%s'"""
                        % (P_COMPANY,assignment[3],assignment[2],assignment[1],assignment[0]))
        assignment_actuales = cursor.fetchall()
        
        if len(assignment_actuales) == 0:
            lista=[]
            hoy=datetime.datetime.now()   
            query = """INSERT INTO "%s"."MAESTROS_ASSIGNMENT" VALUES ("%s".MAESTROS_ASSIGNMENT_ID_SEQ.nextval,:1,:2,:3,:4,:5,:6,:7,:8, :9,:10,:11,:12)""" % (P_COMPANY,P_COMPANY)
            lista.append([str(assignment[3]),str(assignment[4]),1,hoy,hoy,None,None,str(assignment[2]),assignment[1],str(assignment[0]),1,1])
            cursor.executemany(query,lista)
            print ("guardado")
            connection.commit()
connection.close()

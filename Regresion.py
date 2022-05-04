import numpy as np
import matplotlib.pyplot as plt
import genetico



def crearBaseDatos(RangosEntradas,nE):#nE es el numero de entradas

    #Vamos a sacar las etiquetas de cada entrada
    #Para ello vamos a dividir el rango en el numero de etiquetas
    # Para que se solapen las etiquetas se aumentan un 10% por la izquierda y por la derecha

    #fig, ax = plt.subplots(len(RangosEntrada))
    

    BD=[0]*len(RangosEntradas) # Base de datos (BD)

    for i in range(len(RangosEntradas)):
        li=RangosEntradas[i][0] #cogemos el limite inferior
        ls=RangosEntradas[i][1]#cogemos el limite superior
        BD[i]=[None]*nE
        tamañoEtiqueta=(ls-li)/nE
        
        #Asignamos la primera etiqueta de la entrada a la base de datos
        BD[i][0]=[0]*3
        BD[i][0][0]=li
        BD[i][0][1]=li
        if(li+tamañoEtiqueta)>0:BD[i][0][2]=(li+tamañoEtiqueta)*1.05 #Los positivos los multiplico por 1.05 para que agranden
        else:BD[i][0][2]=(li+tamañoEtiqueta)*0.8 #Los positivos los multiplico por 0.9 para que agranden
        #ax[i].plot([BD[i][0][0],BD[i][0][1],BD[i][0][2]],[0,1,0])

        #Asignamos de la 2º etiqueta a la nE-1
        maxAnterior =li+tamañoEtiqueta

        for n in range(1,nE-1):
            BD[i][n]=[0]*3
            if(maxAnterior)>0:BD[i][n][0]=maxAnterior * 0.95 
            else:BD[i][n][0]=maxAnterior * 1.05 
            BD[i][n][1]=maxAnterior+(tamañoEtiqueta/2)
           
            if(maxAnterior+tamañoEtiqueta)>0: BD[i][n][2]=(maxAnterior+tamañoEtiqueta)*1.05
            else: BD[i][n][2]=(maxAnterior+tamañoEtiqueta)*0.95
            maxAnterior=maxAnterior+tamañoEtiqueta

            #ax[i].plot([BD[i][n][0],BD[i][n][1],BD[i][n][2]],[0,1,0])
            

        #Asignamos la ultima etiqueta
        BD[i][-1]=[0]*3
        if(maxAnterior>0): BD[i][-1][0]=maxAnterior*0.95
        else:BD[i][-1][0]=maxAnterior*1.05
        BD[i][-1][1]=ls
        BD[i][-1][2]=ls

        #ax[i].plot([BD[i][-1][0],BD[i][-1][1],BD[i][-1][2]],[0,1,0])
    plt.show()

    return BD

def crearBaseDatos2(RangosEntradas,nE):#Creamos la base de datos sin superposición entre etiquetas

    #Vamos a sacar las etiquetas de cada entrada
    #Para ello vamos a dividir el rango en el numero de etiquetas
    # de lo que le pertenece par aque queden solapadas

    #fig, ax = plt.subplots(len(RangosEntrada))
    

    BD=[0]*len(RangosEntradas) # Base de datos (BD)

    for i in range(len(RangosEntradas)):
        li=RangosEntradas[i][0] #cogemos el limite inferior
        ls=RangosEntradas[i][1]#cogemos el limite superior
        BD[i]=[None]*nE
        tamañoEtiqueta=(ls-li)/nE
        
        #Asignamos la primera etiqueta de la entrada a la base de datos
        BD[i][0]=[0]*3
        BD[i][0][0]=li
        BD[i][0][1]=li
        BD[i][0][2]=(li+tamañoEtiqueta)#*1.05
        #ax[i].plot([BD[i][0][0],BD[i][0][1],BD[i][0][2]],[0,1,0])

        #Asignamos de la 2º etiqueta a la nE-1
        maxAnterior =li+tamañoEtiqueta

        for n in range(1,nE-1):
            BD[i][n]=[0]*3
            BD[i][n][0]=maxAnterior #* 0.95 
            BD[i][n][1]=maxAnterior+(tamañoEtiqueta/2)
            BD[i][n][2]=(maxAnterior+tamañoEtiqueta)#*1.05 
            maxAnterior=maxAnterior+tamañoEtiqueta

            #ax[i].plot([BD[i][n][0],BD[i][n][1],BD[i][n][2]],[0,1,0])
            

        #Asignamos la ultima etiqueta
        BD[i][-1]=[0]*3
        BD[i][-1][0]=maxAnterior#*0.95
        BD[i][-1][1]=ls
        BD[i][-1][2]=ls

       # ax[i].plot([BD[i][-1][0],BD[i][-1][1],BD[i][-1][2]],[0,1,0])
    #plt.show()

    return BD

def calcularH(x1,x2,x3,ve):
    #fig, ax = plt.subplots()
    #ax.plot([x1,x2,x3],[0,1,0])
    
    if ve<x1: 
        #ax.scatter([ve],[0],color = "tab:red")
        return 0
    if(ve>x3): 
        #ax.scatter([ve],[0],color = "tab:red")
        return 0
    if(ve==x2): 
       # ax.scatter([ve],[0])
        return 1
    if ve<x2: 
       # ax.scatter([ve],[0],color = "tab:orange")
        return (ve-x1)/(x2-x1)
    else: 
        #ax.scatter([ve],[0],color = "tab:gray")
        return (ve-x3)/(x2-x3)

def leerFichero(nombreFich):
    lectura = open(nombreFich,"r")
    fichero=lectura.read().split("\n")
    fich =[]
    for i in range(10,len(fichero)):#Recorremos todo el fichero saltando las lineas de información
        linea = fichero[i].split(",")#Separamo todos los datos de cada linea
        fich.append(linea)
    
    lectura.close()
    return fich #Devolvemos una tabla con cada linea y cada dato separado

def mayorPertenencia(e1,e2,ve,y1,y2):#Devolvemos la "y" de la etiqueta a la cual el punto ve pertenece mas
    if calcularH(e1[0],e1[1],e1[2],ve) < calcularH(e2[0],e2[1],e2[2],ve):
        return y2
    else:
        return y1

def sacarReglas(fich,numMuestras,BD):

    BR=[]
    for i in range(len(fich)-1): #Miramos cada linea del fichero leido. La ultima linea esta vacia, por eso vamos hasta len-1
        r=[None]*numMuestras

        for j in range (numMuestras): #En cada linea miramos cada campo
            
            for y in range(len(BD[j])): #Miramos todas las figuras hasta encontrar una que contenga al campo j leido

                if min(BD[j][y])< float(fich[i][j])<= max(BD[j][y]):  #Buscamos si pertenece a la etiqueta
                    if(y<len(BD[j])-1 ):#Miramos que no sea la ultima etiqueta
                        if(min(BD[j][y+1])< float(fich[i][j])<= max(BD[j][y+1])):# Si tambien pertenece a la siguiente etiqueta
                            #Miramos a cual etiqueta pertenece mas el punto y le asignamos la etiqueta
                            r[j]=mayorPertenencia(BD[j][y],BD[j][y+1],float(fich[i][j]),y,y+1)   
                            break     
                    #Asignamos el punto a la etiqueta encontrada
                    r[j]=y
                    break
            
        BR.append(r)
    
    return BR

def sacarReglas2(fich,numMuestras,BD):#Sacamos las reglas sin tener en cuenta la superposición de etiquetas
    BR=[]
    for i in range(len(fich)-1): #Miramos cada linea del fichero leido. La ultima linea esta vacia, por eso vamos hasta len-1
        r=[None]*numMuestras

        for j in range (numMuestras): #En cada linea miramos cada campo
            
            for y in range(len(BD[j])): #Miramos todas las figuras hasta encontrar una que contenga al campo j leido

                if min(BD[j][y])< float(fich[i][j])<= max(BD[j][y]):  #Si encontramos la figura la guardamos y salimos del bucle de y
                    r[j]=y
                    break
            
        BR.append(r)
    
    return BR

def quitarReglasDuplicadas(BR):#Quitamos de la base de reglas las repetidas y que no tengan una salida valida
    BRsimplificada=[]
    for r in BR:
        repetido=False
        for j in BRsimplificada:
            if np.array_equal(r,j): #Si la regla esta duplicada nos salimos del bucle j y no la metemos
                repetido=True
                break

        if not repetido and r[-1]!=None: #Añadimos las reglas con salidas valida y que no esten repetidas
            BRsimplificada.append(r)

    
    return BRsimplificada

def quitarReglasContradictorias(BR,entrada,BD):
    #Como antes de este metodo se deberia quitar las reglas repetidas, vamos a tener en cuenta que no hay reglas repetidas
    BRaux=BR.copy()
    for i in range(1,len(BR)):
        if(BR[i][0]==BR[i-1][0] and BR[i][1]==BR[i-1][1] and BR[i][2]==BR[i-1][2] and BR[i][3]==BR[i-1][3] and BR[i][4]==BR[i-1][4]):
            matching1=[]
            matching2=[]
            for vE in entrada: #Recorremos cada linea del fichero test
                if len(vE)!= 1:#El ultimo campo lo lee vacio, para que no de error, colocamos el if
                    matching1.append(Regresion(BD,[BR[i-1]],vE))
                    matching2.append(Regresion(BD,[BR[i]],vE))

            if(sum(matching1)>sum(matching2)):#Nos quedamos con la regla con mayor matching
                BRaux.remove(BR[i])
            else:
                BRaux.remove(BR[i-1])

    return BRaux

def crearFicheroReglas(nE,BR,g,n):
    nombreFichero="ReglasRegresion "+str(nE)+" etiquetas "+g+str(n)

    np.savetxt(nombreFichero,BR,fmt="%s") #Crea el fichero con la base de reglas

    print("Fichero de reglas creado")

def leerFicheroReglas(nE,g,n):

    nombreFichero="ReglasRegresion "+str(nE)+" etiquetas "+g+str(n)
    

    lectura = open(nombreFichero,"r")
    fichero=lectura.read().split("\n")
    BRleida =[]
    for i in range(len(fichero)-1):#Recorremos todo el fichero
        linea = fichero[i].split(" ")#Separamo todos los datos de cada linea
        BRleida.append(linea)
    
    lectura.close()
    return BRleida 

def Regresion(BD,BR,vE):
    T=[]# operador de conjunción
    sumaHxPMV=float(0)

    for i in range(len(BR)):
        r=BR[i]
        h=[] #Es cada resultado de cada entrada de la regla
        

        for j in range(len(BR[0])-1):

             if None !=r[j]!="None"  :
                #Sacamos las coordenadas de cada triangulo
                x1=BD[j][int(r[j])][0]
                x2=BD[j][int(r[j])][1]
                x3=BD[j][int(r[j])][2]

                h.append(calcularH(x1,x2,x3,float(vE[j])))#ve es el valor de entrada
                #plt.show()
        
        T.append(min(h))

        #Al ser una figura simétrica, simplemente tenemos que buscar el punto central (xc)
        xc= BD[-1][int(r[-1])][1]
        sumaHxPMV+= min(h)*xc
    if(sum(T)==0): matching=0
    else: matching= sumaHxPMV/sum(T)

    return matching        

def errorCuadraticoMedio(entrada,matching):
    sumatorio=0.0
    for i in range(len(entrada)-1):
        sumatorio+=(float(entrada[i][-1])-matching[i])**2
    
    return (sumatorio/len(matching))


#main

#Rangos de los campos introducidos
RR=[-0.02081, 0.0177]
PR=[-0.00771, 0.0108]
CP=[-0.00601, 0.041]
CR=[-0.051, 0.051]
DRR=[-0.00151, 8.2E-4]
SA=[-0.00211, 0.0022]

RangosEntrada=[RR,PR,CP,CR,DRR,SA]

nE=5   #Número de etiquetas que utilizaremos (triangulos)
BD=crearBaseDatos(RangosEntrada,nE)

nombreFicheros="./DataSet/delta_ail-5-"
ECM=[None]*5
"""for nfichero in range(1,6):
#########################################                   Train                     ###############################
    nomb=nombreFicheros+str(nfichero)+"tra.dat"
    ficheroTrain=leerFichero(nomb)
    BRprimaria=sacarReglas(ficheroTrain,len(RangosEntrada),BD)
    BRs=quitarReglasDuplicadas(BRprimaria)
    BR=quitarReglasContradictorias(BRs,ficheroTrain,BD)
    crearFicheroReglas(nE,BR,"",nfichero)"""

"""for nE in range(5,6,2):
#########################################                   Train  genetico                   ###############################
    BD=crearBaseDatos(RangosEntrada,nE)
    nomb=nombreFicheros+str(1)+"tra.dat"
    ficheroTrain=leerFichero(nomb)
    BRprimaria=sacarReglas(ficheroTrain,len(RangosEntrada),BD)
    BRs=quitarReglasDuplicadas(BRprimaria)
    BR=quitarReglasContradictorias(BRs,ficheroTrain,BD)
    ######genetico
    print(f" Inicio genetico para {nE}-------------------------------")
    BR=genetico.genetico(BR,ficheroTrain,BD)
    crearFicheroReglas(nE,BR,"genetico",1)"""

for nfichero in range(1,6):
#########################################                   Test                     #################################
    nombt=nombreFicheros+str(nfichero)+"tra.dat"
    #BR=leerFicheroReglas(nE,"genetico",nfichero)
    BR=leerFicheroReglas(nE,"",nfichero)
    print(f"Fichero {nfichero}  nReglas: {len(BR)}")
    test=leerFichero(nombt)
    matching=[]
    for vE in test: #Recorremos cada linea del fichero test
       if len(vE)!= 1:#El ultimo campo lo lee vacio, para que no de error, colocamos el if
        matching.append(Regresion(BD,BR,vE))

    ECM[nfichero-1]=errorCuadraticoMedio(test,matching)

print(ECM)

print(f"Error medio: {sum(ECM)/len(ECM)}")
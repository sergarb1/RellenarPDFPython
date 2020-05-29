#!/usr/bin/python3
import csv
import os
from pdfrw import PdfWriter, PdfReader, IndirectPdfDict, PdfName, PdfDict,PdfObject

#Valores por defecto de rutas de entrada y salida de los PDF
INVOICE_TEMPLATE_PATH = '9_FP_GM_I_GS_AUTO.pdf'
INVOICE_OUTPUT_PATH = 'invoice.pdf'

#Anotaciones necesarias para manejar el formato PDF
ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'


'''
Funcion que recibe ruta del PDF a rellenar, ruta donde guardar el PDF rellenado,
diccionario de datos con el par clave (campo) y valor (dato a rellenar) y
lista de que campos deben ser tratados como checkbox
'''
def write_fillable_pdf(input_pdf_path, output_pdf_path, data_dict, camposCheckBox):

    
    template_pdf = PdfReader(input_pdf_path)
    #Necesario para que se vean cambios
    template_pdf.Root.AcroForm.update(PdfDict(NeedAppearances=PdfObject('true'))) 
    
    #Por cada pagina del PDF
    for page in template_pdf.pages:
        annotations = page[ANNOT_KEY]

        #Para cada anotacion de la pagina
        for annotation in annotations:
            if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                if annotation[ANNOT_FIELD_KEY]:
                    key = annotation[ANNOT_FIELD_KEY][1:-1]
                    if key in data_dict.keys():
                        
                        #HACK PARA LOS CHECK. Si es true, se marcan, sino no
                        if key in camposCheckBox:
                            if(data_dict[key]=='true'):
                                annotation.update(PdfDict(V='{}'.format(data_dict[key]),AS=PdfName('Yes')))
                            #Si no se pone nada, por defecto no se marcan    
                            continue

                       #Objeto necesario para que al rellenar se vean los campos
                        rct = annotation.Rect
                        hight = round(float(rct[3]) - float(rct[1]),2)
                        width =(round(float(rct[2]) - float(rct[0]),2))

                        xobj = PdfDict(
                        BBox = [0, 0, width, hight],
                        FormType = 1,
                        Resources = PdfDict(ProcSet = [PdfName.PDF, PdfName.Text]),
                        Subtype = PdfName.Form,
                        Type = PdfName.XObject
                        )
                        #assign a stream to it
                        xobj.stream = '''/Tx BMC
                        BT
                        /Helvetica 8.0 Tf
                        1.0 5.0 Td
                        0 g
                        (''' + data_dict[key] + ''') Tj
                        ET EMC'''

                        #Actualizamos la anotacion en el PDF
                        annotation.update(PdfDict(AP=PdfDict(N = xobj),V='{}'.format(data_dict[key])))
                        
    #Escribimos el PDF ya anotado al PATH de salida
    PdfWriter().write(output_pdf_path, template_pdf)



#LINEA DE EJECUCION PRINCIPAL (MAIN)

#Lista que contiene el nombre de los campos del PDF que deben tratarse
#como checkbox
camposCheckBox=["untitled6","untitled21","untitled22","untitled23","untitled24","untitled25"]

#Diccionario de datos que contiene la informacion que se usara para rellenar el dato.
#Algunos de estos datos se modifican dinamicamente bebiendo de fuentes CSV
data_dict = {
   'untitled1': '123456', #Codigo de centro
   'untitled5': 'CENTRO', #Nombre del centro
   'untitled6': "true", #Centro titularidad publica
   'untitled2': 'Narnia', #Localidad centro
   'untitled4': 'Narnia', #Provincia centro
   'untitled8': '123456', #Telefono Centro
   'untitled3': 'Calle falsa, 123', #Direccion Centro
   'untitled9': '00000', #Codigo Postal Centro
   'untitled10': 'NIA', #NIA Alumno
   'untitled11': 'Curso', #Curso Alumno
   'untitled12': 'Apellidos, Nombre', #Apellidos, Nombre - Alumnos
   'untitled15': 'Nombre ciclo formativo', #Titulo ciclo
   'untitled16': 'Superior', #Grado ciclo
   'untitled18': 'Punto 1.1', #Punto 1.1
   'untitled17': 'Punto 1.2', #Punto 1.2
   'untitled19': 'Punto 1.3', #Punto 1.3
   'untitled20': 'Punto 1.4', #Punto 1.4
   'untitled21': 'true', #Check Avanzado
   'untitled22': 'false', #Check Intermedio
   'untitled23': 'false', #Check Basico
   'untitled24': 'false', #Check No superado
   'untitled25': 'Punto 2.1', #Punto 2.1
   'untitled26': 'Punto 2.2', #Punto 2.2
   'untitled27': 'Punto 2.3', #Punto 2.3
   'untitled28': 'Punto 2.4', #Punto 2.4
   'untitled30': 'Ciudad', #Firma Ciudad de firma
   'untitled31': '28', #Firma dia
   'untitled32': 'Mayo' #Firma Mes
}


print("Comenzamos a procesar los PDFs")

#Abrimos el fichero CSV
with open('datosFake.csv', newline='\n') as csvfile:
    #Con el fichero abierto, configuramos el lector CSV 
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    #Para cada linea (una linea por alumno)
    for alumno in reader:
        #Modificamos el data_dic dinamicamente con los valores leidos del CSV

        data_dict["untitled10"]=alumno[3] # NIA del alumno
        data_dict["untitled12"]=alumno[1]+" "+alumno[0] # Apellidos,Nombre del alumno
        
        #Generamos un nombre de PDF de salida basado en nombre alumno y nia
        #Se guarda dentro de la carpeta "documentos"
        INVOICE_OUTPUT_PATH="documentos/"+alumno[1]+" "+alumno[0]+"-"+alumno[3]+".pdf"
        #Llamamos a la funcion que creara el PDF rellenado
        write_fillable_pdf(INVOICE_TEMPLATE_PATH, INVOICE_OUTPUT_PATH, data_dict,camposCheckBox)

# Indicamos que la ejecucion ha finalizado con exito
print("Ejecucion realizada con exito")
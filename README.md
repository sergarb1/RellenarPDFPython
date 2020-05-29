# RellenarPDF Python
Programa para facilitar el rellenado de PDFs en Python, usando biblioteca pdfrw. Ejemplo con documento GVA.

Este programa es un pequeño prototipo adaptable.

Algunas consideraciones

1) El programa funciona con Python 3

2) Es necesario instalar biblioteca "pdfrw" (pip3 install pdfrw)

3) El documento base utilizado en este ejemplo es el existente en http://www.ceice.gva.es/documents/162640733/169967001/9_FP_GM_I_GS_AUTO.pdf/466ef927-d703-4b69-bfd1-8e8e48d5a7f5

4) En este ejmplo se usan datos en formato CSV en el fichero "datosfake.csv". 
El programa toman los campos del fichero 0,1 (Nombre y apellidos) y 3 (NIA). 
El fichero "datosfake.csv" contiene datos falsos.

5) Se debe crear carpeta "documentos", donde se generarán los PDF rellenados.

6) Actualmente, para editar datos a mano que no se beban de una fuente CSV, se debe modificar dentro del fichero .py el diccionario llamado "data_dic".
El diccionario consta de un par clave con el nombre del campo y valor con el valor que se rellenara.

7) En el caso de los Checkbox, se deberá incluir el nombre del campo en la lista "camposCheckBox" y en "data_dic" indicar en esos campos "true" si quiere que se marque, "false" en caso contrario.



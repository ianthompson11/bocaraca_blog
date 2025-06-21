### 1. **Instalar Silk**

Abre tu terminal y corre:

`pip install django-silk`

### 2. **Modificaciones codigo**
Luego de la instalacion es necesario realizar las modificaciones en el codigo las cuales se detallan en el mismo codigo, para encontrarla solo busca con f3 **Profiling** en los archivos modificados que mencionare mas adelante, asi se encontraran los puntos exactos de modificacion ya que los mencione en el codigo con ese nombre. 
 Especificamente se modificaron el archivo views de blogapp , settings y url de blogproject

En cuanto al profiling es util colocar el codigo `@silk_profile()` en cada seccion del codigo donde se desee medir el rendimiento de una funcion o seccion de codigo especifica

### 3. **Pasos finales**
Antes de poder usar la funcion del profiling es necesario hacer dos cosas en el terminal:
`python manage.py migrate`
esta linea es para hacer la migracion de lo importante. 

### 4. **Opcional** ###
En caso de querer desactivar el modo debug, es necesario usar un comando. Esto es importante ya que no es recomendable usar esto de silk en produccion, es decir para los usuarios finales: 

`set DJANGO_DEBUG=false`


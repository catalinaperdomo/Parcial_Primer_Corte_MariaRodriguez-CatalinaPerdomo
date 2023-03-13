# Parcial_Primer_Corte_MariaRodriguez-CatalinaPerdomo


Lambda1

Usando zappa crear una función lambda que descargue la primera página de resultados del sitio Finca Raiz(https://www.fincaraiz.com.co) para la venta de casas en el sector de chapinero.
Esta lambda se debe ejecutar todos los lunes a las 9 am.
La página html se debe guardar en un bucket s3://landing-casas-xxx/yyyy-mm-dd.html

Lambda2

Al llegar la página web al bucket se debe disparar un segundo lambda que procese el archivo utilizando el paquete de python beatifulsoup y extraiga la información de cada casa.
Se debe crear un archivo CSV en s3://casas-final-xxx/yyyy-mm-dd.csv con la siguiente estructura de columnas:
FechaDescarga, Barrio, Valor, NumHabitaciones, NumBanos, mts2

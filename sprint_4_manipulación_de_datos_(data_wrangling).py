# -*- coding: utf-8 -*-
#Este es uno de los proyectos que realicé para el bootcamp de Tripleten.
#This is one of the projects I did for the Tripleten bootcamp.

"""Sprint 4: Manipulación de datos (Data Wrangling)

Automatically generated by Colab.

Original file is located at
    Google Colab

from google.colab import drive
drive.mount('/con**/**')

import pandas as pd
import matplotlib.pyplot as plt

insta_orders=pd.read_csv('/con**/drive/My **/instacart_orders.csv',sep=';')
products=pd.read_csv('/con**/drive/My **/products.csv',sep=';')
aisles=pd.read_csv('/con**/drive/My **/aisles.csv',sep=';')
departments=pd.read_csv('/con**/drive/My **/departments.csv',sep=';')
order_product=pd.read_csv('/con**/drive/My **/order_products.csv',sep=';')

# mostrar información del DataFrame
insta_orders.info()

# mostrar información del DataFrame
products.info()

# mostrar información del DataFrame
aisles.info()

# mostrar información del DataFrame
departments.info()

# mostrar información del DataFrame
order_product.info(show_counts = True)

"""Los archivos, a pesar de ser csv, tienen un formato diferente. En la primera lectura que hice, solo se mostró como una columna a pesar de que hay varias. Por lo que utilicé sep para separarlas.

Y lo último que pude notar es que por ejemplo, en el último DataFrame no se muestran los valores nulos, solo están el índice, columna, y el tipo de dato.


The files, despite being csv, have a different format. On the first read I did, it only showed as one column even though there are several. So I used sep to separate them.

And the last thing I could notice is that for example, in the last DataFrame the null values are not shown, there are only the index, column, and data type.

Plan de solución

*  Analizar si es seguro convertir datos
*  Utilizar métodos que me permitan verificar si hay valores duplicados (duplicated().sum(),drop_duplicates(), y luego reset_index ya que afecta a los indices)
*  Utilizar métodos que me permitan verificar si hay valores ausentes (isna(), y luego los rellenaré con la palabra "unknown")



Solution plan

* Analyse if it is safe to convert data
* Use methods that allow me to check for duplicate values (duplicated().sum(),drop_duplicates(), then reset_index as it affects the indexes)
* Use methods that allow me to check for missing values (isna(), and then fill in with the word ‘unknown’)
"""

# Revisar si hay pedidos duplicados
orders=insta_orders.duplicated().sum()
print(orders)
print()
print(insta_orders[insta_orders.duplicated()])

"""Hay 15 duplicados. Lo que tienen en comun son el dia de la semana en la que se hizo el pedido (3, que sería miércoles ya que la semana comienza en 0), y la hora (2).

There are 15 duplicates. What they have in common are the day of the week on which the order was placed (3, which would be Wednesday as the week starts at 0), and the time (2).
"""

print(insta_orders.query("order_dow == 3 and order_hour_of_day == 2"))

""" Este resultado sugiere que si bien existen valores duplicados en los que fue el miércoles a las 2, al filtrar usando esas variables nos indica que hay 121 filas, osea, 121 pedidos fueron realizados en ese momento. Eso lleva a pensar que los valores duplicados se deben a otros motivos, no necesariamente por haberse realizado el miércoles a las 2.

  This result suggests that while there are duplicate values where it was Wednesday at 2 o'clock, filtering using these variables indicates that there are 121 rows, i.e. 121 orders were placed at that time. This suggests that the duplicate values are due to other reasons, not necessarily because they were placed on Wednesday at 2 o'clock.
"""

# Eliminar los pedidos duplicados

orders1 = insta_orders.drop_duplicates().reset_index(drop=True)


print(orders1.duplicated().sum())

print(insta_orders)

#verificar si hay filas duplicadas
print(orders1.duplicated().sum())

#verificar únicamente si hay IDs duplicados de pedidos

print(insta_orders.duplicated('order_id').sum())

"""Al aplicar el método duplicated() en la fila de los IDs de pedidos si nos salen que hay duplicados, pero eso puede significar que probablemente el producto fue pedido más de 1 vez.

When applying the duplicated() method on the order IDs row we do get duplicates, but that may mean that the product was probably ordered more than 1 time.
"""

# Verificar si hay filas totalmente duplicadas
print(products.duplicated().sum())
print()
print(products[products.duplicated()])

# Revisar únicamente si hay ID de departamentos duplicados
print(products.duplicated('product_id').sum())

# Revisar únicamente si hay nombres duplicados de productos (convierte los
# nombres a letras mayúsculas para compararlos mejor)
products['product_name']= products['product_name'].fillna('')

col=products['product_name']
new=[]
for names in col:
    new_name= names.upper()
    new.append(new_name)
products['product_name']=new

col2=['product_id','product_name']

print(products[col2])
print()
print(products.duplicated('product_name').sum())

# Revisar si hay nombres duplicados de productos no faltantes
non_empty=products[products['product_name']!= '']
duplicate_count=non_empty['product_name'].duplicated().sum()
print(duplicate_count)

"""Descubrí que en este DataFrame, no hay valores duplicados. Si bien si tuvimos valores duplicados en el nombre de los productos los IDs de cada uno son diferentes.

I discovered that in this DataFrame, there are no duplicate values. Although we did have duplicate values in the name of the products, the IDs of each one are different.
"""

# Revisar si hay filas totalmente duplicadas
print(departments.duplicated().sum())

# Revisar únicamente si hay IDs duplicadas de productos

print(departments.duplicated('department_id').sum())

# Revisar si hay filas totalmente duplicadas
print(aisles.duplicated().sum())

#Revisar únicamente si hay IDs duplicadas de pasillos
print(aisles.duplicated('aisle_id').sum())

# Revisar si hay filas totalmente duplicadas
print(order_product.duplicated().sum())

# Vuelve a verificar si hay cualquier otro duplicado engañoso
print(order_product['order_id'].nunique())
print()
print(order_product['product_id'].nunique())
print()
print(order_product['add_to_cart_order'].nunique())
print()
print(order_product['reordered'].nunique())

#print()
#print(order_product['add_to_cart_order'].sample(10))

print(order_product['order_id'].duplicated().sum())
print()
print(order_product['product_id'].duplicated().sum())
print()
print(order_product['add_to_cart_order'].duplicated().sum())
print()
print(order_product['reordered'].duplicated().sum())

"""A primera vista no tenemos filas duplicadas, pero al revisar columna por columna, nos damos cuenta que sí. A pesar de eso, no podemos eliminarlos, ya que son valores que estamos analizando por separado. Puede ser que algo se haya pedido varias veces y por eso ciertos valores se repiten.

At first glance we do not have duplicate rows, but when reviewing column by column, we realize that we do. In spite of that, we cannot eliminate them, since they are values that we are analyzing separately. It may be that something has been requested several times and that is why certain values are repeated.
"""

# Encontrar los valores ausentes en la columna 'product_name'
are_empty=products[products['product_name']== '']
duplicates_count=are_empty['product_name'].duplicated().sum()
print(duplicates_count)

#  ¿Todos los nombres de productos ausentes están relacionados con el pasillo con ID 100?
print(products.query("product_name == '' and aisle_id ==100"))
print()
print(products.query("product_name == '' and aisle_id !=100"))

"""A través del filtrado con query, podemos ver que los nombres de productos que están vacios, si están relacionados al pasillo con ID 100.

Through query filtering, we can see that the empty product names are related to the aisle with ID 100.
"""

# ¿Todos los nombres de productos ausentes están relacionados con el departamento con ID 21?
print(products.query("product_name == '' and department_id !=21"))
print()
print(products.query("product_name == '' and department_id ==21"))

"""A través del filtrado con query, podemos ver que los nombres de productos que están vacios, si están relacionados al departamento con ID 21.

Through query filtering, we can see that the empty product names are related to the department with ID 21.
"""

# Usar las tablas department y aislar para revisar los datos del pasillo con ID
# 100 y el departamento con ID 21. print(products.query("product_name == '' and
# department_id ==21 and aisle_id ==100"))

both = products.merge(aisles,on='aisle_id', how='outer')
print(both.query("product_name == '' and department_id ==21 and aisle_id ==100"))

"""Después de combinar las tablas, pudimos ver que todos los valores de pasillo con ID 100 y el departamento con ID 21 dice "missing", osea, que están perdidos.

After combining the tables, we could see that all the values for the corridor with ID 100 and the department with ID 21 are missing.
"""

# Completar los nombres de productos ausentes con 'Unknown'
col4=products['product_name']

new_empty=[]

for names in col4:
    if names == '':
        new_empty_name='unknown'
        new_empty.append(new_empty_name)
    else:
        new_empty.append(names)


products['product_name']=new_empty
print(products['product_name'].isna())

"""Para uno de los ejercicios anteriores, tuve que reemplazar los valores ausentes para poder ejecutar el código. Ahora, he reemplazado los valores ausentes con la palabra "unknown".

For one of the previous exercises, I had to replace the missing values in order to execute the code. Now, I have replaced the missing values with the word “unknown”.
"""

# Encontrar los valores ausentes
print(insta_orders.isna().sum())

# ¿Hay algún valor ausente que no sea el primer pedido del cliente?
print(insta_orders.info())
print()
print(insta_orders.nunique())

# Encontrar los valores ausentes

print(order_product.isna().sum())
print()
print(order_product['add_to_cart_order'].isna())

# ¿Cuáles son los valores mínimos y máximos en esta columna?
print(order_product['add_to_cart_order'].min())
print()
print(order_product['add_to_cart_order'].max())

# Guardar todas las IDs de pedidos que tengan un valor ausente en
# 'add_to_cart_order'
non_value= order_product[order_product['add_to_cart_order'].isna()]

missing_order_ids = non_value['order_id'].unique()
print(non_value)

# ¿Todos los pedidos con valores ausentes tienen más de 64 productos?

# Primero identificamos los pedidos con valores ausentes
pedidos_con_ausentes = order_product[order_product['add_to_cart_order'].isna()]['order_id'].unique()

# Contamos cuántos productos hay en cada pedido
conteo_productos = order_product.groupby('order_id')['product_id'].count()

todos_mas_de_64 = True

# Verificamos cada pedido individualmente
for pedido in pedidos_con_ausentes:
    if pedido in conteo_productos.index:
        if conteo_productos[pedido] <= 64:
            todos_mas_de_64 = False
            break
    else:
        # Si el pedido no está en conteo_productos, consideramos que no cumple la condición
        todos_mas_de_64 = False
        break

print(f"¿Todos los pedidos con valores ausentes tienen más de 64 productos? {todos_mas_de_64}")

# Agrupar todos los pedidos con datos ausentes por su ID de pedido.
empty_val= order_product[order_product['add_to_cart_order'].isna()]
ordered_emtpy= empty_val.groupby('order_id').size()
print(ordered_emtpy)

# Contar el número de 'product_id' en cada pedido y revisa el valor mínimo del
# conteo.
counting = order_product.groupby('order_id')['product_id'].count()
print(counting.sort_values())

# Remplazar los valores ausentes en la columna 'add_to_cart? con 999 y convertir
# la columna al tipo entero.
order_product['add_to_cart_order']=order_product['add_to_cart_order'].fillna(999)
print(order_product.info())
order_product['add_to_cart_order'] = order_product['add_to_cart_order'].astype('int')
#print(order_product.isna().sum())
print()
print(order_product.info())

# Verificar que los valores en las columnas 'order_hour_of_day' y 'order_dow' en
# la tabla orders sean razonables (es decir, 'order_hour_of_day' oscile entre 0
# y 23 y 'order_dow' oscile entre 0 y 6).



# Valores únicos en order_hour_of_day
print("Valores únicos en 'order_hour_of_day':", sorted(insta_orders['order_hour_of_day'].unique()))
print(insta_orders['order_hour_of_day'].value_counts().sort_index())

# Valores únicos en order_dow
print("\nValores únicos en 'order_dow':", sorted(insta_orders['order_dow'].unique()))
print(insta_orders['order_dow'].value_counts().sort_index())

# Estadísticas generales
print("\nEstadísticas de 'order_hour_of_day':\n", insta_orders['order_hour_of_day'].describe())
print("\nEstadísticas de 'order_dow':\n", insta_orders['order_dow'].describe())

"""No hay ningun problema. El dia tiene 24 horas, y la semana 7 dias.

There is no problem. The day has 24 hours, and the week has 7 days.
"""

# Crear un gráfico que muestre el número de personas que hacen pedidos
# dependiendo de la hora del día.
people_hour = insta_orders.groupby('order_hour_of_day')['user_id'].count()
#print(people_hour)

people_hour.plot(x='order_hour_of_day',y='user_id',xlabel='Horas',ylabel='Nº Usuarios',title='Número de personas con pedidos según hora del día', kind='bar',color='pink', figsize=[4,4],rot=90)

#plt.xticks(rotation=0)  # You can adjust the degree of rotation (45, 90, etc.)

# Make sure the rotated labels don't get cut off
#plt.tight_layout()

plt.show()

"""Las horas en las que la gente hace más pedidos es entre las horas del mediodía, pero específicamente a las 10 am. También es interesante ver que la gente hace pedidos durante todo el día, incluso durante la madrugada.

The hours when people place the most orders is between the noon hours, but specifically at 10 am. It is also interesting to see that people place orders throughout the day, even during the early morning hours.
"""

#Crear un gráfico que muestre qué día de la semana la gente hace sus compras.
people_day = insta_orders.groupby('order_dow')['user_id'].count()
#print(people_day)

people_day.plot(x='order_dow',y='user_id',xlabel='Dias de la semana',ylabel='Nº Usuarios',title='Número de personas con pedidos según día de la semana', kind='bar',color='pink', figsize=[4,4],rot=90)
plt.show()

"""Los días con mayor compra son los domingos y lunes. Es interesante ver el nivel de compras de los viernes sea menora al del lunes.

The days with the most purchases are Sundays and Mondays. Interestingly, the level of purchases on Fridays is lower than on Mondays.
"""

# Crear un gráfico que muestre el tiempo que la gente espera hasta hacer su
# siguiente pedido.


people_buying_time = insta_orders.groupby('days_since_prior_order')['user_id'].count()

people_buying_time.plot(x='days_since_prior_order',y='user_id',xlabel='Tiempo de espera(días)',ylabel='Nº Usuarios',title='Cantidad de tiempo para realizar un pedido', kind='bar',color='pink')
plt.show()

min_days= people_buying_time.index.min()
max_days = people_buying_time.index.max()

print('Menor tiempo:',min_days)
print()
print('Mayor tiempo:',max_days)

"""* Podemos ver que mucha gente espera 30 dias para volver a realizar otro pedido.
* Los días entre pedidos que tienen 0, podrían significar que hay personas que realizan solamente una vez un pedido.
* Uno de los valores más altos es cada 7 días. Esto puede deberse a que las personas les puede gustar iniciar la semana con la alacena hecha y completa.

* We can see that many people wait 30 days to place another order.
* The days between orders that have 0 could mean that there are people who place only one order.
* One of the highest values is every 7 days. This may be because people may like to start the week with the cupboard done and complete.
"""

#¿Existe alguna diferencia entre las distribuciones 'order_hour_of_day' de los miércoles y los sábados?
# Trazar gráficos de barra de 'order_hour_of_day' para ambos días en la misma
# figura.



miercoles_orders = insta_orders[insta_orders['order_dow'] == 3]
sabados_orders = insta_orders[insta_orders['order_dow'] == 6]

wednesday_counts = miercoles_orders['order_hour_of_day'].value_counts().sort_index()
saturday_counts = sabados_orders['order_hour_of_day'].value_counts().sort_index()


insta_orders[insta_orders['order_dow'].isin([3, 6])].groupby(['order_hour_of_day', 'order_dow']).size().unstack().plot(kind='bar', figsize=(12,6), xlabel="Hora del día", ylabel="Número de pedidos",
          title="Distribución de pedidos por hora: Miércoles vs. Sábado", color=['blue', 'orange'])

plt.legend(["Miércoles", "Sábados"])
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()

"""Podemos ver que hay mas actividad de mañana que de noche y madrugada. Desde las 7 hasta las 10 de la mañana los miércoles son mayores a los sábados.

We can see that there is more activity in the morning than at night and in the early morning. From 7 a.m. to 10 a.m. Wednesdays are busier than Saturdays.
"""

# Graficar la distribución para el número de órdenes que hacen los clientes
# (es decir, cuántos clientes hicieron solo 1 pedido, cuántos hicieron 2,
# cuántos 3, y así sucesivamente...).


buying_per_client = insta_orders.groupby('user_id')['order_number'].max().value_counts().sort_index()
buying_per_client.plot(x='order_number',y='user_id',xlabel='Pedidos total por clientes',ylabel='Numero de clientes', title='Distribución de Pedidos por cliente',kind='bar',figsize=[10,6])
plt.show()

# ¿Cuáles son los 20 principales productos que se piden con más frecuencia
# (mostrar su identificación y nombre)?
top_products = order_product['product_id'].value_counts().head(20).reset_index()
top_products.columns = ['product_id', 'order_count']
top_products = top_products.merge(products[['product_id', 'product_name']], on='product_id', how='left')

print(top_products)

top_products.plot(kind='barh',x='product_name',y='order_count', xlabel='Productos',ylabel='Cantidad',title='Top 20 productos',legend=False, color='pink')
plt.show()

"""Podemos ver que la mayoría de los productos son orgánicos.

We can see that most of the products are organic.
"""

# ¿Cuántos artículos suelen comprar las personas en un pedido? ¿Cómo es la
# distribución?

items_per_order = order_product.groupby('order_id')['product_id'].count()

# Mostrar estadísticas generales
print(items_per_order.describe())

items_per_order.plot(kind='hist',x='product_id',y='order_id',xlabel='Número de productos en un pedido',ylabel='cantidad de pedidos',title='Distribución de artículos por pedido',color='pink')
plt.show()

"""La mayoria de los pedidos tienen pocos articulos. A partir de 40 articulos, los pedidos son casi nulos.

Most of the orders have few items. From 40 or more items, the orders are almost null.
"""

# ¿Cuáles son los 20 principales artículos que vuelven a pedirse con mayor
# frecuencia (mostrar sus nombres e IDs de los productos)?

top_reordered = order_product[order_product['reordered'] == 1]  # Filtrar reordenados
top_reordered = top_reordered['product_id'].value_counts().head(20).reset_index()
top_reordered.columns = ['product_id', 'reorder_count']

# Unir con el nombre del producto
top_reordered = top_reordered.merge(products[['product_id', 'product_name']], on='product_id', how='left')

print(top_reordered)

"""Los productos que se piden con mayor frecuencia corresponden a las frutas y verduras.
De esto podemos suponer que, la mayoria de usuarios quieren tener una alimentación y dieta saludables.

The most frequently ordered products are fruits and vegetables.
From this we can assume that the majority of users want to have a healthy food and diet.
"""

# Para cada producto, ¿cuál es la tasa de repetición del pedido (número de
# repeticiones de pedido/total de pedidos?

# Contar el número total de pedidos por producto
total_orders = order_product['product_id'].value_counts().reset_index()
total_orders.columns = ['product_id', 'total_orders']

# Contar cuántos de esos pedidos fueron reordenados
reordered_counts = order_product[order_product['reordered'] == 1]['product_id'].value_counts().reset_index()
reordered_counts.columns = ['product_id', 'reordered_orders']

# Unir ambos DataFrames
reorder_rate = total_orders.merge(reordered_counts, on='product_id', how='left')

# Calcular la tasa de repetición
reorder_rate['reordered_orders'] = reorder_rate['reordered_orders'].fillna(0)
reorder_rate['reorder_rate'] = reorder_rate['reordered_orders'] / reorder_rate['total_orders']

# Unir con los nombres de los productos
reorder_rate = reorder_rate.merge(products[['product_id', 'product_name']], on='product_id', how='left')

# Mostrar el resultado
print(reorder_rate[['product_id', 'product_name', 'reorder_rate']])

"""Podemos ver que por ejemplo, la tasa de repeticion de la banana es una de las mas altas. Es interesante ver que por ejemplo la carne no tiene tasa de repeticion. Tambien se puede ver que los productos organicos son pedidos reiteradas veces.

We can see that for example, the repetition rate of banana is one of the highest. It is interesting to see that for example meat has no repeat rate. We can also see that organic products are repeatedly ordered.
"""

#Para cada cliente, ¿qué proporción de los productos que pidió ya los había pedido?
# Calcular la tasa de repetición de pedido para cada usuario en lugar de para
# cada producto.

order_insta= insta_orders.merge(order_product,on='order_id')
#print(order_insta)

# Paso 2: Agrupar por usuario y calcular la proporción de productos reordenados
user_reorder_rates = order_insta.groupby('user_id').agg(
    total_products=('product_id', 'count'),
    reordered_products=('reordered', 'sum')
)

# Paso 3: Calcular la proporción
user_reorder_rates['reorder_rate'] = user_reorder_rates['reordered_products'] / user_reorder_rates['total_products']

# Mostrar los resultados
print(user_reorder_rates)

user_reorder_rates['reorder_rate'].plot(kind='hist',title='Distribución de Tasas de Repetición por Usuario',bins=20)
plt.show()

#¿Cuáles son los 20 principales artículos que la gente pone primero en sus carritos
# (mostrar las IDs de los productos, sus nombres, y el número de veces en que
# fueron el primer artículo en añadirse al carrito)?

# Paso 1: Filtrar solo los productos que fueron añadidos primero al carrito
first_items = order_product[order_product['add_to_cart_order'] == 1]

# Paso 2: Contar cuántas veces cada producto fue el primero en añadirse
first_item_counts = first_items.groupby('product_id').size().reset_index(name='count')

# Paso 3: Ordenar de mayor a menor según la frecuencia
first_item_counts = first_item_counts.sort_values('count', ascending=False)

# Paso 4: Unir con la tabla de productos para obtener los nombres
top_first_items = pd.merge(first_item_counts, products[['product_id', 'product_name']], on='product_id')

# Paso 5: Mostrar los 20 principales
top_20_first_items = top_first_items.head(20)
print(top_20_first_items)

"""# Conclusiones

Proyecto: Análisis de Pedidos en Instacart A lo largo de este proyecto, se realizó un análisis detallado de los datos de pedidos de la plataforma Instacart.

A continuación, se presentan los pasos realizados y las conclusiones clave:

1. Carga e Importación de Datos
Se importaron y exploraron los datasets relacionados con pedidos, productos, pasillos y departamentos.
Se verificó la estructura de los datos y se identificaron valores nulos en algunas columnas.
2. Limpieza y Preparación de los Datos
Se manejaron valores nulos en la columna days_since_prior_order, ya que estos correspondían a clientes que realizaban su primer pedido.
Se verificó que los valores en order_hour_of_day (0-23) y order_dow (0-6) fueran razonables.
Se comprobó que la variable add_to_cart_order tuviera un máximo de 64, lo que sugiere una posible restricción en el sistema de Instacart.
3. Análisis de Frecuencia de Pedidos
Se identificaron los 20 productos más pedidos, mostrando sus nombres e identificadores.
Se realizó un gráfico de barras para visualizar estos productos y sus respectivas cantidades.
4. Análisis de Reordenamiento de Productos
Se calcularon los productos más frecuentemente reordenados.
Se analizó la tasa de repetición de cada producto como la relación entre reordenamientos y pedidos totales.
5. Distribución de Artículos por Pedido
Se analizó la cantidad de artículos comprados por pedido y se generó una distribución visual.
Se concluyó que la mayoría de los pedidos contienen menos de 20 artículos.

Conclusiones Generales
* Tendencias de Pedido: La mayoría de los pedidos contienen pocos productos, con un límite máximo de 64 artículos.
* Productos más populares: Se identificaron los productos más vendidos y los más reordenados, lo que puede ayudar a optimizar la disponibilidad de inventario.
* Tasa de reordenamiento: Se determinó qué productos tienen mayor recurrencia en los pedidos, información útil para promociones y estrategias de marketing.
* Calidad de los datos: No se encontraron valores inconsistentes en variables clave como el día y la hora del pedido.



# Conclusions

Project: Instacart Order Analysis Throughout this project, a detailed analysis of order data from the Instacart platform was performed.

The steps performed and key findings are presented below:

Data Loading and Importing 1.
Datasets related to orders, products, aisles and departments were imported and explored.
The data structure was verified and null values were identified in some columns.
2. Data Cleaning and Preparation
Null values were handled in the days_since_prior_order column, since they corresponded to customers placing their first order.
The values in order_hour_of_day (0-23) and order_dow (0-6) were checked for reasonableness.
The add_to_cart_order variable was checked for a maximum of 64, suggesting a possible constraint in the Instacart system.
3. Order Frequency Analysis
The 20 most ordered products were identified, showing their names and identifiers.
A bar chart was made to visualize these products and their respective quantities.
4. Product Reorder Analysis
The most frequently reordered products were calculated.
The repetition rate of each product was analyzed as the ratio of reorders to total orders.
5. Distribution of Items per Order
The number of items purchased per order was analyzed and a visual distribution was generated.
It was concluded that most orders contain less than 20 items.

General Conclusions
* Ordering Trends: Most orders contain few products, with a maximum limit of 64 items.
* Most popular products: Best sellers and most reordered products were identified, which can help optimize inventory availability.
* Reorder rate: It was determined which products have the highest recurrence in orders, useful information for promotions and marketing strategies.
* Data quality: No inconsistent values were found in key variables such as day and time of order.
"""

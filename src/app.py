from utils import db_connect
engine = db_connect()

# your code here

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df_airbnb = pd.read_csv("https://raw.githubusercontent.com/4GeeksAcademy/data-preprocessing-project-tutorial/main/AB_NYC_2019.csv")

df_airbnb.sample(5)

# averiguando que columnas tienen valores nulos:
df_airbnb.isnull().sum()

# información del dataset:
df_airbnb.info()

# cambiar algunas variables de formato
df_airbnb=df_airbnb.astype({'name':'str','host_name':'str','neighbourhood_group':'category','neighbourhood':'category','room_type':'category'})
df_airbnb['last_review'] = pd.to_datetime(df_airbnb['last_review'], format="%Y/%m/%d")
df_airbnb.dtypes

round(df_airbnb.describe()) 

df_airbnb['id'].nunique()

df_airbnb.describe(include=['object','category','datetime64'])

# cantidad de Host 
print('Cantidad de hosts:', df_airbnb['host_id'].nunique())

print('Tipos de alojamientos')
df_airbnb['room_type'].value_counts(normalize=True)

df_airbnb['room_type'].unique()

df_airbnb['host_id'].value_counts(sort=True)[:10] # Top 10 host

df_airbnb.groupby('host_id')[['number_of_reviews','id']].agg({'id':pd.Series.nunique,'number_of_reviews':['sum','mean']}).sort_values(by=('id','nunique'),ascending=False)[0:10] # Top 10 host

df_hn=round(df_airbnb.groupby(['host_id','neighbourhood_group'])[['number_of_reviews','id','price']].agg({'id':pd.Series.nunique,'number_of_reviews':['sum','mean'],'price':'mean'}).sort_values(by=('id','nunique'),ascending=False))[0:10] # Top 10 host
df_hn

list(df_hn.reset_index()['host_id'])

df_hn_filt=df_airbnb[df_airbnb['host_id'].isin(list(df_hn.reset_index()['host_id']))]
df_hn_filt

pd.set_option('display.max_rows',110)
round(df_hn_filt.groupby(['host_id','neighbourhood_group','neighbourhood'])[['number_of_reviews','id','price']].agg({'id':pd.Series.nunique,'number_of_reviews':['sum','mean'],'price':'mean'}).sort_values(by=['host_id',('id','nunique')],ascending=False).dropna()) # Top 10 host

df_airbnb[['neighbourhood_group','neighbourhood']].value_counts(sort=True)[:10]

df_nei=df_airbnb.groupby(['neighbourhood_group','neighbourhood']).agg({'price':'mean'}).sort_values(by=['neighbourhood_group','price'],ascending=False).dropna()

df_nei.reset_index(inplace=True)

list(df_nei.neighbourhood_group.unique())

len(df_airbnb.neighbourhood.unique())

for barrio in list(df_nei.neighbourhood_group.unique()) :
    display(df_nei[df_nei['neighbourhood_group'] == barrio].head(5))

# mostrar las últimas 5 filas: 
for barrio in list(df_nei.neighbourhood_group.unique()) :
    display(df_nei[df_nei['neighbourhood_group'] == barrio].tail(5))

# podemos hacer una visualizacion eliminando los datos extremos.

#creamos a sub-dataframe con valores no extremos / menos que 500
sub_df=df_airbnb[df_airbnb.price < 500]
#using violinplot to showcase density and distribtuion of prices 
viz_2=sns.violinplot(data=sub_df, x='neighbourhood_group', y='price')
viz_2.set_title('Density and distribution of prices for each neighberhood_group')

# ahora aplicamos longitud y latitud 

# diagrama de dispersión
# usando para precios menores de 500
viz_4=sub_df.plot(kind='scatter', x='longitude', y='latitude', label='availability_365', c='price',
                  cmap=plt.get_cmap('jet'), colorbar=True, alpha=0.4, figsize=(10,8))
viz_4.legend()



















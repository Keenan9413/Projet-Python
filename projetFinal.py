import streamlit as st
from pymongo import MongoClient
import numpy as np
from faker import Faker
import pandas as pd
import matplotlib.pyplot as plt
import requests
import json

url= "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.6.2"
client= MongoClient(url)

df = pd.DataFrame(list(MongoClient()["F1"]["Circuit2020"].find()))
st.title('Pilotes :')
df2 = pd.DataFrame(list(MongoClient()["F1"]["Drivers2015"].find()))
st.dataframe(df2)

#Diagramme du nombre de pilote en fonction de la nationnalité 
pilotes = pd.DataFrame(list(MongoClient()["F1"]["pilotes"].find()))
marques = pd.DataFrame(list(MongoClient()["F1"]["constructors"].find()))
pilotes_par_marque = pilotes.groupby('nationality').count()['driverId']
plt.bar(pilotes_par_marque.index, pilotes_par_marque.values)
plt.xlabel('Nationnalité')
plt.ylabel('Nombre de pilotes')
st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot()

# Diagramme circulaire
pilotes = pd.DataFrame(list(MongoClient()["F1"]["pilotes"].find()))
marques = pd.DataFrame(list(MongoClient()["F1"]["constructors"].find()))

pilotes_par_nationalite = pilotes.groupby('nationality').count()['driverId']

plt.pie(pilotes_par_nationalite.values, labels=pilotes_par_nationalite.index, autopct='%1.1f%%')
plt.title('Répartition des pilotes par nationalité')
st.pyplot()


df3 = pd.DataFrame(list(MongoClient()["F1"]["constructors"].find()))
df4 = pd.DataFrame(list(MongoClient()["F1"]["Season"].find()))
df5= pd.DataFrame(list(MongoClient()["F1"]["Calendrier"].find()))


# Ajouter un bouton à la barre latérale
add_selectbox = st.sidebar.selectbox(
    "Grand Prix",
    df5.raceName)


df6=pd.DataFrame(list(MongoClient()["F1"]["Classements"].find()))
df7=pd.DataFrame(list(MongoClient()["F1"]["Classements2015"].find()))
df8=pd.DataFrame(list(MongoClient()["F1"]["Classements2016"].find()))
df9=pd.DataFrame(list(MongoClient()["F1"]["Classements2017"].find()))
df10=pd.DataFrame(list(MongoClient()["F1"]["Classements2018"].find()))
df11=pd.DataFrame(list(MongoClient()["F1"]["Classements2019"].find()))
df12=pd.DataFrame(list(MongoClient()["F1"]["Classements2020"].find()))
df13=pd.DataFrame(list(MongoClient()["F1"]["Classements2021"].find()))
df14=pd.DataFrame(list(MongoClient()["F1"]["Classements2022"].find()))
df15=pd.DataFrame(list(MongoClient()["F1"]["Drivers2015"].find()))
df16=pd.DataFrame(list(MongoClient()["F1"]["Constructor2020"].find()))
df17=pd.DataFrame(list(MongoClient()["F1"]["Qualification"].find()))

df15=pd.DataFrame(list(MongoClient()["F1"]["Drivers2015"].find()))

df11=pd.DataFrame(list(MongoClient()["F1"]["Classements2019"].find()))


st.title('Classement 2019')

#Faire un tableau à partir des données de l'API
url = "http://ergast.com/api/f1/2019/driverStandings.json"

response = requests.request("GET", url)
data = response.json()

# Extraire les données du classement des pilotes
driver_standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
driver_standings_data = []
for driver in driver_standings:
    driver_data = {
        'Position': driver['position'],
        'Nom': driver['Driver']['givenName'] + ' ' + driver['Driver']['familyName'],
        'Nationalité': driver['Driver']['nationality'],
        'Écurie': driver['Constructors'][0]['name'],
        'Points': driver['points'],
        'Victoires': driver['wins']
    }
    driver_standings_data.append(driver_data)

# Créer un dataframe pandas à partir des données du classement des pilotes
driver_standings_df = pd.DataFrame(driver_standings_data)

st.dataframe(driver_standings_df)


url = "http://ergast.com/api/f1/2019/driverStandings.json?limit=1000"
response = requests.request("GET", url)
data = response.json()
results = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

# Stocker le nombre de victoires par pilote
victoires_par_pilote = {}
for driver in results:
    pilote = driver['Driver']['givenName'] + ' ' + driver['Driver']['familyName']
    victoires = driver['wins']
    victoires_par_pilote[pilote] = victoires

# Créer un dataframe pandas à partir des données de victoire de chaque pilote
df_victoires = pd.DataFrame(victoires_par_pilote.items(), columns=['Pilote', 'Nombre de victoires'])

st.title('Diagramme')
# Créer un diagramme bâton
plt.bar(df_victoires['Pilote'], df_victoires['Nombre de victoires'])
plt.xticks(rotation=90)
plt.xlabel('Pilote')
plt.ylabel('Nombre de victoires')
plt.title('Nombre de victoires par pilote en 2019')
st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot()


# DataFrame crée pour que ca soit plus lisible 
victoires = [11, 4, 3, 2, 1]
pilotes = ['Hamilton', 'Bottas', 'Verstappen', 'Leclerc', 'Vettel']

#Diagramme bâton
plt.bar(pilotes, victoires)
plt.title('Nombre de victoires par joueur pour la saison 2019')
plt.xlabel('Nom des pilotes')
plt.ylabel('Nombre de victoires')
st.pyplot()


st.title('Resultat le plus récent')

# Afficher l'url sous forme de tableau 
url = "http://ergast.com/api/f1/current/last/results.json"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

data = response.json()
results = data['MRData']['RaceTable']['Races'][0]['Results']

# Créer un dataframe pandas à partir des données de résultats
df_results = pd.DataFrame(columns=['Pilote', 'Écurie', 'Position', 'Points'])
for driver in results:
    pilote = driver['Driver']['givenName'] + ' ' + driver['Driver']['familyName']
    ecurie = driver['Constructor']['name']
    position = driver['position']
    points = driver['points']
    df_results = df_results.append({'Pilote': pilote, 'Écurie': ecurie, 'Position': position, 'Points': points}, ignore_index=True)

# Afficher le dataframe sous forme de tableau
st.table(df_results)



st.title('Nombre de victoire des écuries en 2021')
# Extraire les données de la victoire de chaque écurie en 2021
url = "http://ergast.com/api/f1/2021/constructorStandings.json?limit=1000"
response = requests.request("GET", url)
data = response.json()
results = data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']

# Créer un dictionnaire pour stocker le nombre de victoires par écurie
victoires_par_ecurie = {}
for team in results:
    ecurie = team['Constructor']['name']
    victoires = int(team['wins'])
    victoires_par_ecurie[ecurie] = victoires

# Créer un dataframe pandas à partir des données de victoire par écurie
df_victoires = pd.DataFrame(victoires_par_ecurie.items(), columns=['Ecurie', 'Nombre de victoires'])

# Trier le dataframe par nombre de victoires décroissant
df_victoires = df_victoires.sort_values(by='Nombre de victoires', ascending=False)

# Créer un diagramme en camembert
fig, ax = plt.subplots()
ax.pie(df_victoires['Nombre de victoires'], labels=df_victoires['Ecurie'], autopct='%1.0f')
ax.set_title('Nombre de victoires par écurie en 2021')

# Afficher les chiffres dans le tableau
df_victoires['Nombre de victoires'] = df_victoires['Nombre de victoires'].astype(str)
labels = df_victoires['Ecurie'] + ' (' + df_victoires['Nombre de victoires'] + ')'
table = pd.DataFrame({'Ecurie': labels})
st.table(table)

# Afficher le diagramme en camembert dans Streamlit
st.pyplot(fig)






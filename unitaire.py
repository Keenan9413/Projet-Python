import unittest
import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
from unittest.mock import patch
from pymongo import MongoClient

# Test unitaire de df11(Clasement 2019)
class TestMongoDB(unittest.TestCase):
    def setUp(self):
        # Connexion à la base de données MongoDB
        url= "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.6.2"
        self.client= MongoClient(url)
    
    def test_get_data_from_mongodb(self):
        # Récupération des données de la collection Classements2019
        data = list(self.client["F1"]["Classements2019"].find())
        
        # Vérification que le dataframe est cohérent
        df = pd.DataFrame(data)
        self.assertGreater(len(df), 0)
        self.assertEqual(df.columns.tolist(), ['_id', 'position', 'points', 'wins', 'Driver', 'Constructors'])
        
    def tearDown(self):
        # Fermeture de la connexion à la base de données MongoDB
        self.client.close()

# Test unitaire pour le nombre de victoire par écuries 
class TestNombreVictoireEcuries(unittest.TestCase):
    def test_requete_api(self):
        # Test si la requête à l'API retourne un code 200
        url = "http://ergast.com/api/f1/2021/constructorStandings.json?limit=1000"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

    def test_victoires_par_ecurie(self):
        # Test si le dictionnaire contient les écuries avec leur nombre de victoires
        url = "http://ergast.com/api/f1/2021/constructorStandings.json?limit=1000"
        response = requests.get(url)
        data = response.json()
        results = data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']

        victoires_par_ecurie = {}
        for team in results:
            ecurie = team['Constructor']['name']
            victoires = int(team['wins'])
            victoires_par_ecurie[ecurie] = victoires

        expected = {'Mercedes': 15, 'Red Bull': 10, 'McLaren': 1, 'Ferrari': 0, 'Alpine': 0, 'AlphaTauri': 0, 'Aston Martin': 0, 'Williams': 0, 'Alfa Romeo': 0, 'Haas F1 Team': 0}
        self.assertDictEqual(victoires_par_ecurie, expected)

    def test_dataframe_victoires(self):
        # Test si le dataframe est correctement créé à partir des données de victoire de chaque écurie
        victoires_par_ecurie = {'Mercedes': 15, 'Red Bull': 10, 'McLaren': 1, 'Ferrari': 0, 'Alpine': 0, 'AlphaTauri': 0, 'Aston Martin': 0, 'Williams': 0, 'Alfa Romeo': 0, 'Haas F1 Team': 0}

        df_victoires = pd.DataFrame(victoires_par_ecurie.items(), columns=['Ecurie', 'Nombre de victoires'])

        expected = pd.DataFrame({'Ecurie': ['Mercedes', 'Red Bull', 'McLaren', 'Ferrari', 'Alpine', 'AlphaTauri', 'Aston Martin', 'Williams', 'Alfa Romeo', 'Haas F1 Team'],
                                 'Nombre de victoires': [15, 10, 1, 0, 0, 0, 0, 0, 0, 0]})
        pd.testing.assert_frame_equal(df_victoires, expected)

    def test_trier_dataframe(self):
        # Test si le dataframe est correctement trié par nombre de victoires décroissant
        df_victoires = pd.DataFrame({'Ecurie': ['Mercedes', 'Red Bull', 'McLaren', 'Ferrari', 'Alpine', 'AlphaTauri', 'Aston Martin', 'Williams', 'Alfa Romeo', 'Haas F1 Team'],
                                     'Nombre de victoires': [15, 10, 1, 0, 0, 0, 0, 0, 0, 0]})
        
if __name__ == '__main__':
     unittest.main()

     


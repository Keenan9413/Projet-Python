import unittest
import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
from unittest.mock import patch
from my_module import get_driver_standings_data
from pymongo import MongoClient

# Test unitaire de df16(Constructeur 2020)

url= "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.6.2"
client= MongoClient(url)

start_time = time.time()
df16=pd.DataFrame(list(MongoClient()["F1"]["Constructor2020"].find()))
end_time = time.time()

print(f"Temps d'exécution: {end_time - start_time} secondes.")


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

# Test unitaire pour le nombre de victoire par pilote
class TestF1(unittest.TestCase):

    def setUp(self):
        self.url = 'http://ergast.com/api/f1/2019/driverStandings.json?limit=1000'

    @patch('requests.request')
    def test_request(self, mock_request):
        mock_data = {
            'MRData': {
                'StandingsTable': {
                    'StandingsLists': [{
                        'DriverStandings': [{
                            'Driver': {'givenName': 'Lewis', 'familyName': 'Hamilton'},
                            'wins': '5'
                        }]
                    }]
                }
            }
        }
        mock_request.return_value.json.return_value = mock_data

        response = requests.request('GET', self.url)
        data = response.json()

        self.assertEqual(data, mock_data)

    def test_victoires_par_pilote(self):
        mock_data = {
            'MRData': {
                'StandingsTable': {
                    'StandingsLists': [{
                        'DriverStandings': [
                            {'Driver': {'givenName': 'Lewis', 'familyName': 'Hamilton'}, 'wins': '5'},
                            {'Driver': {'givenName': 'Valtteri', 'familyName': 'Bottas'}, 'wins': '2'}
                        ]
                    }]
                }
            }
        }
        expected_output = {'Lewis Hamilton': '5', 'Valtteri Bottas': '2'}

        victoires_par_pilote = {}
        results = mock_data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
        for driver in results:
            pilote = driver['Driver']['givenName'] + ' ' + driver['Driver']['familyName']
            victoires = driver['wins']
            victoires_par_pilote[pilote] = victoires

        self.assertEqual(victoires_par_pilote, expected_output)

    def test_df_victoires(self):
        victoires_par_pilote = {'Lewis Hamilton': '5', 'Valtteri Bottas': '2'}
        expected_output = pd.DataFrame({'Pilote': ['Lewis Hamilton', 'Valtteri Bottas'], 'Nombre de victoires': ['5', '2']})

        df_victoires = pd.DataFrame(victoires_par_pilote.items(), columns=['Pilote', 'Nombre de victoires'])

        pd.testing.assert_frame_equal(df_victoires, expected_output)

    @patch('matplotlib.pyplot.show')
    def test_plot(self, mock_show):
        df_victoires = pd.DataFrame({'Pilote': ['Lewis Hamilton', 'Valtteri Bottas'], 'Nombre de victoires': ['5', '2']})
        fig, ax = plt.subplots()
        ax.bar(df_victoires['Pilote'], df_victoires['Nombre de victoires'])
        ax.set_xticklabels(df_victoires['Pilote'], rotation=90)
        ax.set_xlabel('Pilote')
        ax.set_ylabel('Nombre de victoires')
        ax.set_title('Nombre de victoires par pilote en 2019')

        plot_output = plt.gcf()

        self.assertEqual(str(type(plot_output)), "<class 'matplotlib.figure.Figure'>")

if __name__ == '__main__':
    unittest.main()

# Test unitaire pour les résultats les plus récents
class TestF1Results(unittest.TestCase):

    @patch('requests.request')
    def test_get_results_data(self, mock_request):
        # Configuration de la réponse de l'API
        mock_response = {'MRData': {'RaceTable': {'Races': [{'Results': [{'Driver': {'givenName': 'Lewis', 'familyName': 'Hamilton'},
                                                                         'Constructor': {'name': 'Mercedes'},
                                                                         'position': '1',
                                                                         'points': '25'},
                                                                        {'Driver': {'givenName': 'Max', 'familyName': 'Verstappen'},
                                                                         'Constructor': {'name': 'Red Bull Racing'},
                                                                         'position': '2',
                                                                         'points': '18'}]}]}}}
        mock_request.return_value.json.return_value = mock_response

        # Appel de la fonction à tester
        from get_f1_results import get_results_data
        df_results = get_results_data()

        # Vérification que le dataframe contient les données attendues
        expected_columns = ['Pilote', 'Écurie', 'Position', 'Points']
        self.assertListEqual(list(df_results.columns), expected_columns)

        expected_data = {'Pilote': ['Lewis Hamilton', 'Max Verstappen'],
                         'Écurie': ['Mercedes', 'Red Bull Racing'],
                         'Position': ['1', '2'],
                         'Points': ['25', '18']}
        self.assertDictEqual(dict(df_results), expected_data)


if __name__ == '__main__':
    unittest.main()

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

     


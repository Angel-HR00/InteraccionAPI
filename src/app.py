import os
import pandas as pd
import seaborn as sns
from dotenv import load_dotenv

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# load the .env file variables
load_dotenv()

client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
artist_id = "7LVC96BEVGugTAp38AajV6"


#Connect to API
connect = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=connect)
                                                      

response = sp.artist_top_tracks("7LVC96BEVGugTAp38AajV6")

if response:
    tracks = response["tracks"]
    
    #Obtenemos los valores que queremos de cada variable si tenemos respuesta de la API
    tracks = [{k: (v/(1000*60))%60 if k == "duration_ms" else v for k, v in track.items() if k in ["name", "popularity", "duration_ms"]} for track in tracks]
    

#Creacion dataframe para mostrar los resultados
tracks_df = pd.DataFrame.from_records(tracks)
tracks_df.sort_values(["popularity"], inplace = True)

print(tracks_df.head(5))

scatter_plot = sns.scatterplot(data = tracks_df, x = "popularity", y = "duration_ms")
fig = scatter_plot.get_figure()
fig.savefig("scatter_plot.png")
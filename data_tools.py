import pandas as pd
import requests

def get_api_key() -> str:
	try:
		with open('api.key') as file:
			return file.read().strip()
	except FileNotFoundError:
		raise FileNotFoundError(f"Missing omdbapi key. Store it in file 'api.key'.")

def parse_float(n: str) -> float:
	try:
		return float(n)
	except ValueError as e:
		return float('nan')

def load(show: str) -> pd.DataFrame:
	try:
		return pd.read_csv(f'{show}_data.csv')
	except FileNotFoundError:
		return default(show, get_api_key())

def save(data: pd.DataFrame, show: str):
	data.to_csv(f'{show}_data.csv', index=False)

def default(show: str, api_key: str) -> pd.DataFrame:
	show_info = requests.get(f'http://www.omdbapi.com/?t={show}&apikey={api_key}').json()
	if show_info['Response'] == "False":
		raise Exception(f"OMDb does not list {show}.")
	id = show_info['imdbID']
	total_seasons = int(show_info['totalSeasons'])
	# title = show_info['Title']

	data = []
	for i in range(1, total_seasons+1):
		season_info = requests.get(f'http://www.omdbapi.com/?i={id}&Season={i}&apikey={api_key}').json()
		for episode in season_info['Episodes']:
			data.append([
				i,
				int(episode['Episode']),
				episode['Title'],
				parse_float(episode['imdbRating']),
				float('nan'),
			])
	return pd.DataFrame(data, columns=['season', 'episode', 'title', 'rating', 'date'])

#!/usr/bin/env python
import requests
import sys
import pandas as pd

if len(sys.argv) != 2:
	raise Exception("Must use as './script.py futurama'")
SHOW = sys.argv[1]

try:
	with open("apikey") as file:
		KEY = file.read().strip()
except FileNotFoundError:
	raise FileNotFoundError(f"Missing omdbapi key. Store it in file 'apikey'.")

def handle_nan(n):
	try:
		return float(n)
	except ValueError as e:
		return float('nan')

def from_api():
	show_info = requests.get(f"http://www.omdbapi.com/?t={SHOW}&apikey={KEY}").json()

	id = show_info['imdbID']
	total_seasons = int(show_info['totalSeasons'])

	def f(id, num_seasons, KEY):
		seasons = {}
		for i in range(1, num_seasons+1):
			temp = requests.get(f"http://www.omdbapi.com/?i={id}&Season={i}&apikey={KEY}").json()
			seasons[i] = {}
			for entry in temp['Episodes']:
				seasons[i][int(entry['Episode'])] = (entry['Title'], handle_nan(entry['imdbRating']))
		return seasons

	seasons = f(id, total_seasons, KEY)

	temp = []
	for i, s in seasons.items():
		for j, e in s.items():
			temp.append([i, j, *e])
	df = pd.DataFrame(temp, columns=["season", "episode", "title", "rating"])
	df.to_csv(f"{SHOW}_data.csv")
	return df

try:
	df = pd.read_csv(f"{SHOW}_data.csv")
except FileNotFoundError:
	df = from_api()

print(df)

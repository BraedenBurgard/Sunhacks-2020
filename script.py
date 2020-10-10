#!/usr/bin/env python
import requests
import sys
import pandas as pd

if len(sys.argv) != 3:
	raise Exception("need to pass in show name then key")

SHOW = sys.argv[1]
KEY  = sys.argv[2]


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
				seasons[i][int(entry['Episode'])] = (entry['Title'], float(entry['imdbRating']))
		return seasons

	seasons = f(id, total_seasons, KEY)

	temp = []
	k = 0
	for i, s in seasons.items():
		for j, e in s.items():
			temp.append([k, i, j, *e])
			k += 1
	df = pd.DataFrame(temp, columns=["id", "season", "episode", "title", "rating"])
	df.to_csv(f"{SHOW}_data.csv")
	return df

try:
	df = pd.read_csv(f"{SHOW}_data.csv")
except FileNotFoundError:
	df = from_api()
print(df)

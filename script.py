#!/usr/bin/env python
import pandas as pd
import numpy as np
import sys
from time import time as now
from data_tools import load, save, parse_float

def get_show() -> str:
	if len(sys.argv) != 2:
		raise Exception("Must use as './script.py show-name'\n\nFor example, './script.py futurama'")
	return sys.argv[1]

def recently_seen(data: pd.DataFrame) -> pd.Index:
	return data.nlargest(len(data)//5, columns=['date'])

def not_recently_seen(data: pd.DataFrame) -> pd.Index:
	return data.iloc[data.index.difference(recently_seen(data).index)]

def algorithm(ratings):
	z_scores = (ratings - ratings.mean()) / ratings.std()
	p = np.exp(z_scores)
	p /= p.sum()
	p = p.fillna(0)
	return p

def select_episode(show):
	data = load(show)
	ratings = not_recently_seen(data)['rating']
	p = algorithm(ratings)
	i = np.random.choice(len(p), p=p)
	entry = data.iloc[i]
	return i, entry['season'], entry['episode'], entry['title']

def rate_episode(show, i, rating):
	rating = parse_float(rating)
	if rating < 0 or rating > 10:
		raise ValueError('Ratings must be between 0 and 10')

	if not np.isnan(rating):
		data = load(show)
		data.loc[i, 'rating'] = (data.loc[i, 'rating'] + rating) / 2
		data.loc[i, 'date'] = now()
		save(data, show)

def __main__():
	show = get_show()
	i, season, episode, title = select_episode(show)
	print(f'Season {season}, Episode {episode}\n{title}')
	rating = input(f'Give this episode a rating (0-10) or Enter to skip\nRating: ')
	rate_episode(show, i, rating)

if __name__ == '__main__':
	__main__()

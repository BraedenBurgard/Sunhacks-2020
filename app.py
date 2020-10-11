from flask import Flask, request, render_template, url_for
import script

app = Flask(__name__, )

@app.route('/')
def main():
	return render_template('main.html')

def watch_another(show):
	return f"""
	<form action="/pick" method="get">
		<input type="hidden" name="show" value="{show}"/>
		<button type="submit">
			Watch another?
    	</button>
	</form>
	"""

@app.route('/rate/<show>/<episode>', methods=['POST'])
def rate(show=None, episode=None):
	rating = request.form['rating']
	script.rate_episode(show, int(episode), float(rating))
	return render_template('rated.html', show=show)

@app.route('/pick', methods=['GET'])
def run():
	show = request.args.get('show', '')
	try:
		i, season, episode, title = script.select_episode(show)
	except Exception as e:
		return render_template('error.html', show=show)
	return render_template('find.html', show=show, i=i,  season=season, episode=episode, title=title)

if __name__ == "__main__":
	app.run(host="127.0.0.1")


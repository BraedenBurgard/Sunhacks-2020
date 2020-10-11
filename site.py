from flask import Flask, request
import script
app = Flask(__name__)

@app.route('/')
def main():
    return """
		<form action="/futurama" method="get">
    		<button type="submit">get</button>
		</form>
    """

@app.route('/rate/<show>/<episode>', methods=['POST'])
def rate(show=None, episode=None):
	rating = request.form['rating']
	script.rate_episode(show, int(episode), float(rating))
	return f"{rating}, {episode}, {show}"

@app.route('/<show>', methods=['GET'])
def run(show=None):
	i, season, episode, title = script.select_episode(show)
	return f"""
	<h1>{title}</h1>
	<h2>Season {season} - Episode {episode}</h2>
	<form action="/rate/{show}/{i}" method="post">
    	<button type="button">
			Rate it?
    	</button>
    	<input type="number" id="rating" name="rating" min="1" max="10">
	</form>
	<form action="/{show}" method="get">
    	<button type="submit">
			Watch another?
    	</button>
	</form>
	"""

if __name__ == "__main__":
	app.run(host="127.0.0.1")

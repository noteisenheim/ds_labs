from flask import Flask, render_template
import redis
import random

app = Flask(__name__, template_folder='./www', static_folder='./www/media')
cache = redis.Redis(host='redis', port=6379)

images = [
   "https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Rhynchocyon_petersi_from_side.jpg/1200px-Rhynchocyon_petersi_from_side.jpg",
    "https://nationalzoo.si.edu/sites/default/files/animals/shortearedelephantshrew-001.jpg",
    "https://i.pinimg.com/originals/6e/15/b2/6e15b2afd2d5255001d605be7ba82b99.png",
    "https://static.boredpanda.com/blog/wp-content/uploads/2020/08/elephant-shrew-rediscovered-animal-lost-species-africa4-5f3d0768101bb__700.jpg"
    ]

def get_hit_count():
	retries = 5
	while True:
		try:
			return cache.incr('hits')
		except redis.exceptions.ConnectionError as exc:
			if retries == 0:
				raise exc
			retries -= 1
			time.sleep(0.5)


@app.route('/')
def index():
    url = random.choice(images)
    count = get_hit_count()
    return render_template('index.html', url=url, visit_count=count)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
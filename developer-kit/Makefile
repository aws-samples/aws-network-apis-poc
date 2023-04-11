build:
		docker build -t developer-kit .
run:
		docker run -d --name developer-kit -p 80:80 developer-kit
stop:
		docker stop developer-kit
		docker rm developer-kit
logs:
		docker logs developer-kit
exec:
		docker exec -it developer-kit bash
python:
		python app.py

clean:
		rm -rf __pycache__

install: get-reqs setup run

get-reqs:
	pip install -U -r requirements.txt

setup:
	python3 ./python/config.py	

run:
	python3 ./python/main.py
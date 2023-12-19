
install:
	pip3 install -r requirements.txt;
	sudo npm install -g concurrently;
	cd frontend && npm install;

start:
	unset HOST;
	concurrently "make run-flask" "make run-node"

run-flask:
	python3 query.py

run-node:
	cd frontend && npm start
BIN=backend/venv/bin/
BDIR=backend/
# run frontend vue server by make frontend
frontend:
	@echo "building vue app"; \
	npm install; \
	clear
	npm run serve
# run backend flask server by make backendS
backendS: 
	@echo "runnning backend" ;\
	python3 -m venv ${BDIR}venv 
	${BIN}pip install -r ${BDIR}req.txt
	${BIN}python -m textblob.download_corpora
	clear
	cd backend && venv/bin/python app.py
# make clean for removing venv and node modules from computer
clean:
	cd backend && rm -rf venv
	rm -rf node_modules	
	@echo done with cleaning

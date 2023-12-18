version = 0.0.1

install_dep:
	python3 -m pip install -r requirements.txt

docker_build:
	./docker/docker_build.sh version

streamlit:
	streamlit run main.py

webserver:
	export FLASK_APP=flask_app.py; flask run
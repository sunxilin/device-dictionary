install_dep:
	python3 -m pip install -r requirements.txt

streamlit:
	streamlit run main.py

webserver:
	export FLASK_APP=flask_app.py; flask run
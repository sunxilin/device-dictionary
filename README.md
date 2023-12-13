# device-info-retreiver
Streamlit based app intergrating Langchain for query device info based on model code purpose.<br>

The app is combining google search and openai model via api to effectively convert a user input(typically the model code of a device) into a carefully formatted results, in the case of sample code, device name and processor seperated by comma.<br>

First, don't forget to copy-paste your openai api key into the openaiapi.json file.<br>

Then, make sure to install all the dependencies.<br>

<code>python3 -m pip install -r requirements.txt</code>

When all set, just run:<br>

<code>streamlit run main.py</code><br>

Note: You can change the google search keywords or prompt template for openai model in app_qt.py.

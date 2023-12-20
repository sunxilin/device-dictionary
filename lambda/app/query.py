import os
import re
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from .google_search import search
from time import sleep
from bs4 import BeautifulSoup
import requests
from . import utils  # relative import

# Error log
pkg_path = utils.pkg_path
filename = re.findall("(.*).py", os.path.basename(__file__))


def googleSearch(query):
    """Return Google search results."""

    results = []

    results = search(
        query,
        num_results=15,
        lang="en",
        advanced=True,
    )

    return results


def queryToPrompt(keyword):
    results = googleSearch(keyword)
    prompt = []

    for result in results:
        try:
            prompt.append(
                f"Title: {result.title}\nSnippet: {result.description}")
        except Exception as e:
            utils.exceptionLog(
                pkg_path,
                filename,
                func_name=queryToPrompt.__name__,
                error=e,
                loop_item="nothing(not a loop)",
            )
            pass
    return prompt


def check_openai_env():
    api_key = os.environ["OPENAI_API_KEY"]
    if api_key is None:
        return False
    else:
        return True


# 根据手机型号model code, 返回手机型号名称及其CPU芯片
def query_model_and_chipsets(model):
    # Prepare OpenAI env
    if check_openai_env is False:
        raise Exception("OpenAI API key not found.")

    openai_api_model = os.environ["OPENAI_API_MODEL"]
    openai_api_deployment = os.environ["OPENAI_API_DEPLOYMENT"]

    # Prepare OpenAI API
    llm = AzureChatOpenAI(
        openai_api_type="azure",
        deployment_name=openai_api_deployment,
        model_name=openai_api_model,
        temperature=0
    )

    # Search more info from google
    search_keywords = '\"{model}\" chipsets'.format(model=model)
    print('search_keyword:' + search_keywords)

    google_search_result = queryToPrompt(
        search_keywords
    )

    if len(google_search_result) < 5:
        search_keywords = '\"{model}\"'.format(model=model)
        google_search_result += queryToPrompt(
            search_keywords
        )

    if len(google_search_result) < 5:
        return '''{"product name": "unknown", "chipsets": "unknown"}'''

    # Generate full prompt
    symbol_template = PromptTemplate(
        input_variables=["symbol", "google_search_result"],
        template="""Based on the information below, tell me what the product name and the chipsets of the device whose model code is {symbol}.

                        ----------------------------------------
                        {google_search_result} 
                        ----------------------------------------

                        Return responses as a valid JSON object with two keys: 
                        The first key is the product name, a string.
                        The second key is its chipsets, a string.
                        """,
    )

    symbol_chain = LLMChain(
        llm=llm, prompt=symbol_template, verbose=True
    )  # , output_key='title'

    input = {"symbol": model, "google_search_result": google_search_result}
    res = symbol_chain.run(input)

    return res


def generate_query_prompt(model):
    # Search more info from google
    google_search_result = queryToPrompt(model + ' chipsets')

    # Generate full prompt
    symbol_template = PromptTemplate(
        input_variables=["symbol", "google_search_result"],
        template="""Based on the information below, tell me what the product name and the chipsets of the device whose model code is {symbol}.

                        ----------------------------------------
                        {google_search_result} 
                        ----------------------------------------

                        Return responses as a valid JSON object with two keys: 
                        The first key is the product name, a string.
                        The second key is its chipsets, a string.
                        """,
    )

    return symbol_template.format(
        symbol=model,
        google_search_result=google_search_result,
    )

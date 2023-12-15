import os
import re
from langchain.llms import OpenAI
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

    retryCount = 0
    while retryCount < 3:
        try:
            results = search(
                query,
                num_results=10,
                sleep_interval=1,
                lang="en",
                timeout=10,
            )
            break
        except:
            retryCount += 1
            sleep(5)

    if retryCount == 3:
        # fallback to baidu search
        utils.exceptionLog(
            pkg_path,
            filename,
            "Google search failed, fallback to Baidu search.",
        )

    return results


def queryToPrompt(model):
    results = googleSearch(model + " chipsets")
    prompt = []
    for result in results:
        try:
            response = requests.get(result)
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.title.string if soup.title else ""
            snippet = soup.find("meta", attrs={"name": "description"})
            snippet = snippet["content"] if snippet else ""
            prompt.append(f"Title: {title}\nSnippet: {snippet}")
            # st.write(f"Title: {title}")
            # st.write(f"Snippet: {snippet}")
        # except requests.exceptions.SSLError:
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

    # Prepare OpenAI API
    llm = OpenAI(temperature=0)

    # Search more info from google
    google_search_result = queryToPrompt(model)

    # Generate full prompt
    symbol_template = PromptTemplate(
        input_variables=["symbol", "google_search_result"],
        template="""Based on the information below, tell me what the product name and the chipsets of the device whose model code is {symbol}.
                        ----------------------------------------
                        {google_search_result} 
                        ----------------------------------------
                        For your final answer, please provide only the product name and its chipsets, separated by commas.""",
    )

    symbol_chain = LLMChain(
        llm=llm, prompt=symbol_template, verbose=True
    )  # , output_key='title'

    input = {"symbol": model, "google_search_result": google_search_result}
    res = symbol_chain.run(input)

    return res

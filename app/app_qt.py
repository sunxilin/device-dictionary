# -*- coding: UTF-8 -*-


def main():
    """Main function for the app."""
    import os
    import re
    import streamlit as st
    from langchain.llms import OpenAI
    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain, SequentialChain
    from langchain.memory import ConversationBufferMemory
    from time import sleep
    from langchain.utilities import WikipediaAPIWrapper
    from bs4 import BeautifulSoup
    import requests
    from importlib import reload
    from . import utils  # relative import

    utils = reload(utils)

    # Error log
    pkg_path = utils.pkg_path
    filename = re.findall("(.*).py", os.path.basename(__file__))
    utils.errorLog(pkg_path, filename)

    # OpenAI API key
    openai_apikey = utils.loadJSON(json_name="openaiapi")["key"]
    os.environ["OPENAI_API_KEY"] = openai_apikey

    # App framework
    st.title("Phone model info")
    query = st.text_input("请输入你想了解的手机型号代码:")

    # Leveraging google search results via streamlit.
    def googleSearch(query):
        """Return Google search results."""
        from .google_search import search

        results = []

        proxies = {"https": "http://127.0.0.1:7890", "http": "http://127.0.0.1:7890"}

        retryCount = 0
        while retryCount < 3:
            try:
                search_results = search(
                    query, num_results=5, sleep_interval=1, lang="en", proxies=proxies
                )
                break
            except Exception as e:
                retryCount += 1
                sleep(5)

        if retryCount == 3:
            # fallback to baidu search
            utils.exceptionLog(
                pkg_path,
                filename,
                func_name=googleSearch.__name__,
                error=e,
                loop_item="nothing(not a loop)",
            )

        for j in search_results:
            results.append(j)
        return results

    # Specify search inputs and parse results with bs4.
    def queryToPrompt():
        results = googleSearch(query + " processor")
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

    # Show stuff to the screen if there's a user input query
    if query:
        google_search_result = queryToPrompt()
        # Prompt templates: combining user input(a.k.a. symbol) and google search results for specified outputs in nature syntax prompt.
        symbol_template = PromptTemplate(
            input_variables=["symbol", "google_search_result"],
            template="""Based on the information below, tell me what the product name and processor model specific to the model code of {symbol} are.
                        {google_search_result} 
                        For your final answer, please provide only the product name and processor model, separated by commas.""",
        )

        # LLMs
        llm = OpenAI(temperature=0)
        symbol_chain = LLMChain(
            llm=llm, prompt=symbol_template, verbose=True
        )  # , output_key='title'

        st.write(google_search_result)

        input = {"symbol": query, "google_search_result": google_search_result}
        title = symbol_chain.run(input)

        st.write(title)

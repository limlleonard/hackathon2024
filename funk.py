from llama_index.llms.openai import OpenAI
from llama_index.llms.ollama import Ollama # pip install llama-index-llms-ollama
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.embeddings.jinaai import JinaEmbedding # pip install llama-index-embeddings-jinaai

from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine

import openai
import os
import re
from dotenv import load_dotenv
load_dotenv()

prompt_sys='Answer the question only based on the given context with original sentence(s) in the provided context in German. Keep the answer short. If you dont know the answer, say "I dont know". '

class Embeder:
    def __init__(self, dir1='datei3', k_top=3):
        """zusammenfassung tool, todos mit few_shot zu optimieren"""
        self.dir1=dir1
        self.k_top=k_top
        self.engine=None
        self.inited=None
    def valid_api(self, api):
        client = openai.OpenAI(api_key=api)
        try:
            client.models.list()
        except openai.AuthenticationError:
            return False
        else:
            return True
    def init_llama(self, api=''):
        os.environ["OPENAI_API_KEY"] = api
        Settings.llm = OpenAI(temperature=0.2) # max_tokens=256 (output), Settings.context_window = 4096, model="gpt-4o"

        Settings.chunk_size = 512
        Settings.chunk_overlap = 50
        Settings.system_prompt=prompt_sys
        self.inited=True

    def embed(self):
        documents = SimpleDirectoryReader(self.dir1, filename_as_id=True, ).load_data()
        index = VectorStoreIndex.from_documents(documents=documents)
        self.engine=index.as_query_engine(similarity_top_k=self.k_top, )
        # tmpl1 = PromptTemplate(str_tmpl1) # prompt template auf Deutsch
        # self.engine.update_prompts({"response_synthesizer:text_qa_template": tmpl1})
        retriever = VectorIndexRetriever(index=index, similarity_top_k=self.k_top) # try multiple response
        self.engine1 = RetrieverQueryEngine.from_args(retriever, response_mode='accumulate')
        
    # def init_retriever(self, index):
    def qa(self, frage, multi=False):
        if self.engine is None or self.engine1 is None:
            return None
        response=self.engine1.query(frage) if multi else self.engine.query(frage)
        lst_ant=[r1[12:] for r1 in re.split(r'\n-+\n', str(response))]
        return lst_ant[0]

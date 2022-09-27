import logging

logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
logging.getLogger("haystack").setLevel(logging.INFO)

from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import TfidfRetriever
from haystack.nodes import FARMReader
from haystack.pipelines import ExtractiveQAPipeline
from haystack.utils import clean_wiki_text, convert_files_to_docs, fetch_archive_from_http
from pprint import pprint
from rasaweb.utils.utils import print_answers

data_location= r"C:\py\blog-master\blog-master\rasa\sample_data"
question = ""
document_store = InMemoryDocumentStore()
docs = convert_files_to_docs(dir_path=data_location, clean_func=clean_wiki_text, split_paragraphs=True)
document_store.write_documents(docs)
retriever = TfidfRetriever(document_store=document_store)
reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2",num_processes=1)
pipe = ExtractiveQAPipeline(reader, retriever)

def get_answer(question):

    prediction = pipe.run(query=question, params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 5}})
    ans = "Search"
    # pprint(prediction)
    if len(prediction['answers']) >0:
        if prediction['answers'][0].score > 0.90:
            ans = print_answers(prediction, details="minimum")
    # print(ans)
    return ans

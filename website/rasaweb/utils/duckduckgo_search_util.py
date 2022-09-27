# website/rasaweb/utils/duckduckgo_search_util.py
# __author__='Lokesh Kuncham'

from duckduckgo_search import ddg


keywords = "Share pricer of hathway"

def search_duckduckgo(search_key):
    results = ddg(search_key, region='wt-wt', safesearch='Moderate', time='y', max_results=1)
    result  = results[0]['body']
    if ". " in result:
        result_list = result.split(". ")
        if '...' in result_list[-1]:
            del result_list[-1]
        result = '. '.join(result_list)
    return result
# print(search_duckduckgo(keywords))
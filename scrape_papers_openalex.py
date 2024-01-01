import pyalex
from pyalex import Works
import json

pyalex.config.email = "1kevin.huang@gmail.com"

search_term = "antibody antigen binding affinity prediction"
num_papers = 500
results_pager = Works().search(search_term) \
    .paginate(per_page=200)
    # .sort(cited_by_count="desc") \

top_results = []
for i, page in enumerate(results_pager):
    top_results += page
    print(len(page), len(top_results))

    if len(top_results) >= num_papers:
        break

# Link in  doi, or pdf
with open('openalex_papers.json', 'w') as f:
    json.dump(top_results, f, indent=4)
# finetuned_research_proposals
Research project to fine-tune a LLM on research proposals, given a research goal.

# How to use
1. Data collection. Edit 'scrape_papers_openalex.py' to set your search term (search_term) to what papers you want to fine-tune on and the number of papers (num_papers) you want. Then, run 'python scrape_papers_openalex.py'

Expected result: openalex_papers.json should appear in your root directory containing open paper metadata.

2. Scrape full-text or landing page if possible. Run 'scrape_papers.ipynb'. Set NUM_PAPERS_TO_SCRAPE to the number of papers you want to scrape (assuming it's lower than in the metadata).

Expected result: You should see scraped text in 'autoscious_logs' directory.

3. Use a LLM to create the 1) research goal prompt and 2) research hypothesis output that you want. Run "prep_training_dataset.ipynb"

Expected result: You should end with a "autoscious_logs_complete_cleaned.csv" that can be used for fine-tuning.

4. For fine-tuning, use Google Colab's free GPU. Run this notebook here: https://colab.research.google.com/drive/1T47NgQS-50PVAz9tW0I9e42KKrkfeceh#scrollTo=iwsMn_ax4hoO
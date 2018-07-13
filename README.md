# fastai_reddit

Here, we'll use [Fast.ai's Language Model](https://github.com/fastai/fastai/blob/master/courses/dl1/lesson4-imdb.ipynb) to imitate another Reddit user.

Initially, I plan to create an iPython notebook similar to Fast.ai's.  Later, I might release .py libraries.

You'll need to setup API access in your Reddit account [according to these instructions](http://www.storybench.org/how-to-scrape-reddit-with-python/) and put the API keys in a file named "credentials.key".

You can see a sample credential file in "sample_credentials.key".

## Requirements:

- [fast.ai](http://github.com/fastai/fastai) (make sure you also 'activate fastai')
- [praw](https://github.com/praw-dev/praw)
- spacy
  - ```conda install spacy (or pip install spacy)```
  - ```python -m spacy download en ``` (may need to run this as admin in Windows)


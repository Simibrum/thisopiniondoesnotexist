# This Opinion Does Not Exist

Using generative API to produce content that does not exist.

## Initialising the Project

Create a `.env` file in the root directory of the project. The file should contain the following:

```
# Twitter
TWITTER_KEY=[YOUR KEY]
TWITTER_SECRET=[YOUR SECRET]
TWITTER_BEARER=[YOUR BEARER]
TWITTER_ACCESS_TOKEN=[YOUR ACCESS TOKEN]
TWITTER_TOKEN_SECRET=[YOUR TOKEN SECRET]

# Google Cloud BigQuery - set path for .json service account key
GOOGLE_APPLICATION_CREDENTIALS=[PATH TO .json FILE]

# OpenAI
OPENAI_API_KEY=[YOUR API KEY]

# Stability AI / DreamStudio
STABILITY_KEY=[YOUR KEY]
```

Aerich is used to handle database migrations. Run the code below to initialise. 
```bash
aerich init -t app.db.config.TORTOISE_ORM

aerich init-db
```

Then after making any changes to the models run the following to generate a migration:
```bash
aerich migrate --name "migration name"
aerich upgrade
```

## Running the project

You can use uvicorn to run the project:

```bash
uvicorn app.main:app --reload
```

If the database does not exist, it will be created automatically.

## Adding Authors

You can add authors to the database by running the following command:

```bash
python -m app.cli add-authors --num_authors 1
```

The variable `--num-authors` is the number of authors to add to the database. 
It defaults to 10 if not supplied.

## Adding Posts

You can add posts to the database by running the following command:

```bash
python -m app.cli add-post --date "13 January 2023" --topics "politics,technology" \
--num_paragraphs 4
```
```

Resources:
* [FastAPI](https://fastapi.tiangolo.com/)
* https://testdriven.io/blog/fastapi-crud/
* https://tortoise-orm.readthedocs.io/en/latest/examples/fastapi.html
* https://medium.com/nerd-for-tech/python-tortoise-orm-integration-with-fastapi-c3751d248ce1
* https://testdriven.io/blog/developing-a-single-page-app-with-fastapi-and-vuejs/
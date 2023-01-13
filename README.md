# This Opinion Does Not Exist

Using generative API to produce content that does not exist.

## Initialising the Project

Aerich is used to handle database migrations. Run the code below to initialise. 
```bash
aerich init -t app.db.config.TORTOISE_ORM
aerich init-db
```

## Running the project

You can use uvicorn to run the project:

```bash
uvicorn app:app --reload
```

If the database does not exist, it will be created automatically.

## Adding Authors

You can add authors to the database by running the following command:

```bash
python -m app.cli add-authors --num_authors 1
```

The variable `--num-authors` is the number of authors to add to the database. 
It defaults to 10 if not supplied.



Resources:
* [FastAPI](https://fastapi.tiangolo.com/)
* https://testdriven.io/blog/fastapi-crud/
* https://tortoise-orm.readthedocs.io/en/latest/examples/fastapi.html
* https://medium.com/nerd-for-tech/python-tortoise-orm-integration-with-fastapi-c3751d248ce1
* https://testdriven.io/blog/developing-a-single-page-app-with-fastapi-and-vuejs/
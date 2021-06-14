import json
from behave import *
from features.queries.demo_sql.demo_mysql import ScriptPyonSchema as SqlSample


@given('that "{database_schema}" is connected')
def step_given_that_database_schema_is_connected(context, database_schema):
    db_connection = {
        "db_schema": database_schema,
        "db_user": "root",
        "db_password": "Py0n33r!",
        "db_host": "localhost",
        "db_name": "pyon_schema_tests",
        "db_type": "mysql",
        "db_driver_abs_path": "",
    }
    context.db_connection = json.dumps(db_connection)


@when("user drops the database")
def step_user_drops_the_database(context):
    SqlSample.query_destroy_database(context.db_connection)


@when("user creates the database")
def step_user_creates_the_database(context):
    SqlSample.query_create_database(context.db_connection)


@then("user can have the database ready to be used")
def step_user_creates_the_database(context):
    SqlSample.query_select_and_use_database(context.db_connection)

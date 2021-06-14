from behave import *
from features.queries.demo_sql.demo_mysql import ScriptPyonSchema as SqlSample


@given("that the tables tb_test_resource, tb_test_type, tb_category and tb_feature are created")
def step_given_that_the_tables_test_resource_test_type_category_and_feature_are_created(context):
    SqlSample.query_create_tables(context.db_connection)


@when("user populates these tables")
def step_when_user_populates_these_tables(context):
    SqlSample.query_populate(context.db_connection)


@then("the user can select with a join between tb_feature, tb_test_type and tb_category tables")
def step_then_the_user_can_select_with_join_between_tables_feature_test_type_and_category(context):
    expected_rows = [
        ("API TEST", "Automated", "The planets from Star Wars Universe API"),
        ("MOBILE TEST", "Automated", "The user can search something on Google Search"),
        ("WEB TEST", "Automated", "The user can add a product to cart"),
        ("WEB TEST", "Manual", "The app can be created by the user after he chooses the mode"),
    ]
    SqlSample.query_select_feature_categories(context.db_connection, expected_rows)


@then("the feature registers are showed")
def step_then_the_feature_registers_are_showed(context):
    expected_rows = 4
    SqlSample.query_select_count_feature_categories(context.db_connection, expected_rows)

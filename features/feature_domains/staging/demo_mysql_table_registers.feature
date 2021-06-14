@demo-mysql
Feature: Selecting registers from Pyon Schema Tests tables

    Background: Cleaning up the 'pyon_schema_tests' database
        Given that "pyon_schema_tests" is connected

    @demo-mysql-tables
    Scenario: The user can create tables, populate and select registers
        Given that the tables tb_test_resource, tb_test_type, tb_category and tb_feature are created
        When user populates these tables
        Then the user can select with a join between tb_feature, tb_test_type and tb_category tables
        And the feature registers are showed

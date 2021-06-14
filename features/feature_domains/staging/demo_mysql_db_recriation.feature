@demo-mysql
Feature: MySQL Database provisioning for Pyon Schema Tests

    @demo-mysql-cleanup
    Scenario: Cleaning up the 'pyon_schema_tests' database
        Given that "pyon_schema_tests" is connected
        When user drops the database
        And user creates the database
        Then user can have the database ready to be used


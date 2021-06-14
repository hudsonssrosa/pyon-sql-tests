import json
import time
from settings.environment_data_provider import EnvSettings as Conf


class SQLTestConnection:

    @staticmethod
    def main():
        db_connection = {
              "db_user": "hudsenberg",
              "db_password": "Huds3nb3rg@qa",
              "db_host": "localhost",
              "db_name": "pyon_schema_tests",
              "db_type": "MySQL",
              "db_driver_abs_path": ""
        }
        connect = json.dumps(db_connection)
        SQLTestConnection.query_drop_tables(connect)
        SQLTestConnection.query_destroy_database(connect)
        SQLTestConnection.query_create_database(connect)
        SQLTestConnection.query_create_tables(connect)
        SQLTestConnection.query_populate(connect)
        SQLTestConnection.query_select_test_type_resources(connect)
        SQLTestConnection.query_select_feature_categories(connect)
        SQLTestConnection.query_select_count_feature_categories(connect)

    @staticmethod
    def query_drop_tables(db_connection):
        drop_table_tb_feature = """
            DROP TABLE IF EXISTS tb_feature;
        """
        drop_table_tb_category = """
            DROP TABLE IF EXISTS tb_category;          
        """
        drop_table_tb_test_type = """        
            DROP TABLE IF EXISTS tb_test_type;          
        """
        drop_table_tb_test_resource = """
            DROP TABLE IF EXISTS tb_test_resource; 
        """
        Conf.execute_sql(drop_table_tb_feature, db_connection)
        Conf.execute_sql(drop_table_tb_category, db_connection)
        Conf.execute_sql(drop_table_tb_test_type, db_connection)
        Conf.execute_sql(drop_table_tb_test_resource, db_connection)

    @staticmethod
    def query_destroy_database(db_connection):
        drop_database_pyon_schema_tests = """
            DROP DATABASE IF EXISTS pyon_schema_tests; 
        """
        Conf.execute_sql(drop_database_pyon_schema_tests, db_connection)

    @staticmethod
    def query_create_database(db_connection):
        create_database_pyon_schema_tests = """
            create database pyon_schema_tests;  
        """
        select_database = """
            SELECT DATABASE();
        """
        use_database = """
            USE pyon_schema_tests;     
        """
        Conf.execute_sql(create_database_pyon_schema_tests, db_connection)
        time.sleep(2)
        # Conf.execute_sql(select_database, db_connection)
        Conf.execute_sql(use_database, db_connection)

    @staticmethod
    def query_create_tables(db_connection):
        create_tb_test_resource = """
            CREATE TABLE IF NOT EXISTS tb_test_resource (
                id_test_resource int NOT NULL primary key,
                resource_name varchar(200) NOT NULL    
            );  
        """
        create_tb_test_type = """
            CREATE TABLE IF NOT EXISTS tb_test_type (
                id_test_type int NOT NULL primary key,
                type_name varchar(200) NOT NULL,
                id_test_resource int(3) NOT NULL,
                constraint fk_tb_test_type__id_test_resource foreign key (id_test_resource)
                references tb_test_resource (id_test_resource)
                ON DELETE cascade ON UPDATE cascade
            );
        """
        create_tb_category = """
            CREATE TABLE IF NOT EXISTS tb_category (
                id_test_category int NOT NULL primary key,
                category_name varchar(200) NOT NULL    
            );           
        """
        create_tb_feature = """
            CREATE TABLE IF NOT EXISTS tb_feature (
                id_feature int(6) unsigned NOT NULL auto_increment primary key,
                id_test_type int(3) NOT NULL,
                id_test_category int(3) NOT NULL,
                test_description varchar(200) NOT NULL,
                constraint fk_tb_feature__id_test_type foreign key (id_test_type)
                    references tb_test_type (id_test_type)
                    ON DELETE cascade ON UPDATE cascade,
                constraint fk_tb_feature__id_test_category foreign key (id_test_category)
                    references tb_category (id_test_category)
                    ON DELETE cascade ON UPDATE cascade    
            );             
        """
        Conf.execute_sql(create_tb_test_resource, db_connection)
        Conf.execute_sql(create_tb_test_type, db_connection)
        Conf.execute_sql(create_tb_category, db_connection)
        Conf.execute_sql(create_tb_feature, db_connection)

    @staticmethod
    def query_populate(db_connection):
        insert_tb_test_resource = """
            INSERT INTO tb_test_resource (id_test_resource, resource_name) VALUES
                ('1', 'HTTP Request'),
                ('2', 'User Interface'),
                ('3', 'Unit'),
                ('4', 'Integration'),
                ('5', 'Acceptation'),
                ('6', 'Regression'),
                ('7', 'Smoke test'),
                ('8', 'Performance - Load/Stress'),
                ('9', 'Functional'),
                ('10', 'Exploratory');
        """
        insert_tb_test_type = """
            INSERT INTO tb_test_type (id_test_type, type_name, id_test_resource) VALUES
                ('1', 'API TEST', '1'),
                ('2', 'WEB TEST', '2'),
                ('3', 'MOBILE TEST', '2');
        """
        insert_tb_category = """
            INSERT INTO tb_category (id_test_category, category_name) VALUES
                ('1', 'Manual'),
                ('2', 'Automated');
        """
        insert_tb_feature = """
            INSERT INTO tb_feature (id_test_type, id_test_category, test_description) VALUES
                ('3', '2', 'The user can search something on Google Search'),
                ('1', '2', 'The planets from Star Wars Universe API'),
                ('2', '2', 'The user can add a product to cart'),
                ('2', '1', 'The app can be created by the user after he chooses the mode');
        """
        Conf.execute_sql(insert_tb_test_resource, db_connection)
        Conf.execute_sql(insert_tb_test_type, db_connection)
        Conf.execute_sql(insert_tb_category, db_connection)
        Conf.execute_sql(insert_tb_feature, db_connection)

    @staticmethod
    def query_select_test_type_resources(db_connection):
        select_tb_test_type__resources = """
            SELECT tt.id_test_type, tt.type_name, tr.resource_name 
            FROM tb_test_type tt 
            JOIN tb_test_resource tr 
            ON tt.id_test_resource  = tr.id_test_resource 
            ORDER BY tt.type_name;
        """
        Conf.execute_sql(select_tb_test_type__resources, db_connection)

    @staticmethod
    def query_select_feature_categories(db_connection):
        select_tb_feature__categories = """
            SELECT tt.type_name, tc.category_name, tf.test_description
            FROM tb_feature tf 
            JOIN tb_test_type tt 
            ON tf.id_test_type = tt.id_test_type
            JOIN tb_category tc
            ON tf.id_test_category = tc.id_test_category
            ORDER BY tt.type_name;
        """
        Conf.execute_sql(select_tb_feature__categories, db_connection)

    @staticmethod
    def query_select_count_feature_categories(db_connection):
        select_tb_feature__categories = """
            SELECT COUNT(1) FROM tb_feature tf 
            JOIN tb_test_type tt 
            ON tf.id_test_type = tt.id_test_type
            JOIN tb_category tc 
            ON tf.id_test_category = tc.id_test_category
            ORDER BY tt.type_name;
        """
        Conf.execute_sql(select_tb_feature__categories, db_connection)


if __name__ == "__main__":
    SQLTestConnection().main()

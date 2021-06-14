import os
import json
import time
import cx_Oracle
import mysql.connector as mysql
from factory.base_context import BaseContext as Bctx
from factory.handling.base_logging import BaseLogging as Log
from factory.handling.running_exception import RunningException as Rexc
from factory.handling.assertion import Assertion as Assert
from factory.utils.StringsUtil import StringUtil
from settings.environment_data_provider import EnvSettings as Conf


UTF8_UPPER = "UTF-8"
UTF8 = "utf-8"


class BaseSQL(Log):
    @staticmethod
    def assert_that(comparative_value=""):
        return Assert(comparative_value)

    def new_db_connection(json_db_config):
        if json_db_config is not None:
            return json.load(json_db_config)

    @staticmethod
    def execute_sql(any_sql, json_connection, validate_content=None):
        rdbms = str(Bctx.flag_mode.get())
        if json_connection is not None:
            new_db_connection: object = json.loads(json_connection)
            user = new_db_connection["db_user"]
            password = new_db_connection["db_password"]
            host = new_db_connection["db_host"]
            db = new_db_connection["db_name"]
            driver_path = os.path.abspath(new_db_connection["db_driver_abs_path"])
            db_type = new_db_connection["db_type"]
        else:
            user = Conf.get_db_user
            password = Conf.get_db_password
            host = Conf.get_db_host
            db = Conf.get_db_name
            driver_path = Conf.get_db_driver_abs_path
            db_type = rdbms
        try:
            if str(db_type).lower() == "oracle":
                BaseSQL.connect_to_oracle(
                    user, password, host, db, driver_path, str(any_sql).strip()
                )
            if str(db_type).lower() == "mysql":
                BaseSQL.connect_to_mysql(
                    user, password, host, db, driver_path, str(any_sql).strip(), validate_content
                )
        except Exception as ex:
            Rexc.raise_exception_error("Impossible to connect with the database!", ex)

    @staticmethod
    def connect_to_oracle(user, password, host, db, driver_path, any_sql):
        os.chdir(driver_path)
        os.environ["NLS_LANG"] = ".utf8"
        conn = cx_Oracle.connect(
            f"{user}/{password}@{host}/{db}", encoding=UTF8_UPPER, nencoding=UTF8_UPPER
        )
        version = conn.version
        Log.info(
            f"\nOracle version is: {version} -- Encoding {conn.encoding}; Nencoding {conn.nencoding}"
        )
        sqlline = str(any_sql).encode(UTF8).strip()
        BaseSQL.select_cursor(conn, sqlline)
        conn.commit()
        conn.close()

    @staticmethod
    def connect_to_mysql(user, password, host, db, driver_path, any_sql, validate_content):
        if str(driver_path) != "":
            os.chdir(driver_path)
        os.environ["NLS_LANG"] = ".utf8"
        conn = None
        try:
            conn = mysql.connect(host=host, user=user, password=password, database=db)
        except:
            conn = mysql.connect(host=host, user=user, password=password)
        finally:
            version = conn.get_server_info()
            Log.info(f"\nMySql version is: {version}")
            BaseSQL.select_cursor(conn, any_sql, validate_content)
            conn.commit()
            conn.close()

    @staticmethod
    def select_cursor(conn, any_sql, validate_content):
        cursor_ = conn.cursor(buffered=True)
        time.sleep(0.5)
        try:
            if str(any_sql) is not None:
                Log.info(f"Executing statement:\n {any_sql}")
                any_sql = StringUtil.remove_multispaces(str(any_sql).replace("\n", "").strip())
                cursor_.execute(any_sql)
                time.sleep(1)
                BaseSQL.check_results(cursor_, validate_content)
        except Exception as e:
            Log.error(e)
            raise e
        finally:
            cursor_.close()

    @staticmethod
    def check_results(cursor_, validate_content):
        Log.info("\n------------- The query has been executed ------------")
        try:
            if validate_content is not None:
                records = cursor_.fetchone()
                if str(validate_content).isdigit():
                    Log.info(f"Total rows: {len(records)}")
                    BaseSQL.assert_that(records[0]).is_equals_to(
                        int(validate_content), "Total rows found"
                    )
                else:
                    for row in records:
                        BaseSQL.assert_that(row).contains_the(
                            validate_content, "Results fetched (Array_size)"
                        )
        except Exception as error:
            Rexc.raise_assertion_error("Failed to read data from table", error)

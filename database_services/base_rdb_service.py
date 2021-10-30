import pymysql
import json
import logging

import sys

sys.path.append('../')
import middleware.context as context

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class BaseDataResource:

    def __init__(self):
        pass

    @classmethod
    def get_db_connection(cls):

        db_info = context.get_db_info()

        logger.info("BaseDataResource.get_db_connection:")
        logger.info("\t HOST = " + db_info['host'])

        db_connection = pymysql.connect(
            **db_info,
            autocommit=True
        )
        return db_connection

    @classmethod
    def run_sql(cls, sql_statement, args, fetch=False):

        conn = BaseDataResource.get_db_connection()

        try:
            cur = conn.cursor()
            print('args: ', args)
            print(sql_statement)
            res = cur.execute(sql_statement, args=args)
            if fetch:
                res = cur.fetchall()
        except Exception as e:
            conn.close()
            raise e

        return res

    @classmethod
    def get_by_prefix(cls, db_schema, table_name, column_name, value_prefix):

        conn = BaseDataResource.get_db_connection()
        cur = conn.cursor()

        sql = "SELECT * FROM " + db_schema + "." + table_name + " WHERE " + \
              column_name + " LIKE " + "'" + value_prefix + "%'" + " AND is_deleted = 0"
        print("SQL Statement = " + cur.mogrify(sql, None))

        res = cur.execute(sql)
        res = cur.fetchall()

        conn.close()

        return res

    @classmethod
    def get_where_clause_args(cls, template):

        terms = []
        args = []
        clause = None

        if template is None or template == {}:
            clause = ""
            args = None
        else:
            for k, v in template.items():
                terms.append(k + "=%s")
                args.append(v)

            clause = " WHERE " + " AND ".join(terms)

        return clause, args

    @classmethod
    def find_by_template(cls, db_schema, table_name, template):

        wc, args = BaseDataResource.get_where_clause_args(template)

        conn = BaseDataResource.get_db_connection()
        cur = conn.cursor()

        sql = "SELECT * FROM " + db_schema + "." + table_name + " " + wc

        res = cur.execute(sql, args=args)
        res = cur.fetchall()

        conn.close()

        return res

    @classmethod
    def create(cls, db_schema, table_name, create_data):

        cols = []
        vals = []
        args = []

        for k, v in create_data.items():
            cols.append(k)
            vals.append('%s')
            args.append(v)

        cols_clause = "(" + ",".join(cols) + ")"
        vals_clause = "values (" + ",".join(vals) + ")"

        sql_stmt = "insert into " + db_schema + "." + table_name + " " + cols_clause + \
                   " " + vals_clause

        res = BaseDataResource.run_sql(sql_stmt, args)

        return res

    @classmethod
    def update(cls, db_schema, table_name, update_data, template):

        wc, wc_args = BaseDataResource.get_where_clause_args(template)

        cols = []
        # vals = []
        args = []

        for k, v in update_data.items():
            cols.append(k + '=%s')
            # vals.append('%s')
            args.append(v)

        cols_clause = ",".join(cols)

        sql_stmt = "UPDATE " + db_schema + "." + table_name + " SET " + cols_clause + " " + wc

        args.extend(wc_args)

        res = BaseDataResource.run_sql(sql_stmt, args)

        return res

    @classmethod
    def delete(cls, db_schema, table_name, template):
        wc, args = BaseDataResource.get_where_clause_args(template)

        conn = BaseDataResource.get_db_connection()
        cur = conn.cursor()

        sql = "DELETE FROM " + db_schema + "." + table_name + " " + wc

        res = cur.execute(sql, args=args)
        res = cur.fetchall()

        conn.close()

        return res
    
    @classmethod
    def find_in_condition(cls, db_schema, table_name, select_vars, in_variable, in_values):

        conn = BaseDataResource.get_db_connection()
        cur = conn.cursor()

        select_clause = "*"
        if select_vars is not None:
            select_clause = ",".join(select_vars)
        for i in range(len(in_values)):
            in_values[i] = '"' + in_values[i] + '"'

        in_values_clause = ",".join(in_values)
        sql = "SELECT " + select_clause + " FROM " + db_schema + "." + table_name + " WHERE " + \
              in_variable + " in (" + in_values_clause + ")"
        print(sql)
        res = cur.execute(sql)
        res = cur.fetchall()

        conn.close()

        return res 

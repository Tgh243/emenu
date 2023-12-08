import os
from contextlib import contextmanager
import logging as logger

import pymysql.cursors as cursors
import pymysql
import yaml
cwd = os.path.dirname(__file__)
config = yaml.safe_load(open(f"{cwd}/../config.yaml"))


@contextmanager
def get_connection(config_file="config.yaml", cursorclass=cursors.DictCursor):
    conn = pymysql.connect(**yaml.safe_load(open(config_file))["credentials"], cursorclass=cursorclass)
    try:
        yield conn
    except pymysql.Error as e:
        logger.error(f"Database error: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        conn.close()


def execute_query(query, args=None):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, args)
            return cursor.fetchall()
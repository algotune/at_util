# -*- coding: utf-8 -*-
from functools import partial
import os
import MySQLdb
import warnings
from sqlalchemy import create_engine, event, exc
from sqlalchemy.orm import scoped_session, sessionmaker
import logging
import numpy as np


def add_engine_pidguard(engine):
    """
    Add multiprocessing guards.

    Forces a connection to be reconnected if it is detected
    as having been shared to a sub-process.
    """

    @event.listens_for(engine, "connect")
    def connect(dbapi_connection, connection_record):
        connection_record.info['pid'] = os.getpid()

    @event.listens_for(engine, "checkout")
    def checkout(dbapi_connection, connection_record, connection_proxy):
        pid = os.getpid()
        if connection_record.info['pid'] != pid:
            # substitute log.debug() or similar here as desired
            warnings.warn(
                "Parent process %(orig)s forked (%(newproc)s) with an open "
                "database connection, "
                "which is being discarded and recreated." %
                {"newproc": pid, "orig": connection_record.info['pid']})
            connection_record.connection = connection_proxy.connection = None
            raise exc.DisconnectionError(
                "Connection record belongs to pid %s, "
                "attempting to check out in pid %s" %
                (connection_record.info['pid'], pid)
            )


def gen_session(in_host, in_user, in_pass, in_db_name,
                in_db_engine_type, in_pool_recycle=3600, in_pool_size=10):
    db_engine = gen_engine(in_host, in_user, in_pass, in_db_name, in_db_engine_type, in_pool_recycle=in_pool_recycle,
                           in_pool_size=in_pool_size)
    add_engine_pidguard(db_engine)
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=db_engine))
    return session


def gen_engine(in_host, in_user, in_pass, in_db_name, in_db_engine_type, in_pool_recycle=3600, in_pool_size=10):
    conn_bh = partial(gen_connection,
                      host=in_host,
                      user=in_user,
                      password=in_pass,
                      db_name=in_db_name,
                      db_type=in_db_engine_type)

    db_engine = create_engine("{0}://".format(in_db_engine_type), creator=conn_bh, pool_recycle=in_pool_recycle,
                              pool_size=in_pool_size, encoding="utf-8")
    return db_engine


def gen_connection(host, user, password, db_name, db_type='mysql'):
    conn = None
    if db_type == 'mysql':
        conn = MySQLdb.connect(host, user, password, db_name)
    return conn


def get_session_from_env(env_host, env_user, env_pass, env_db_name):
    if not np.all([x in os.environ.keys() for x in [env_host, env_user, env_pass, env_db_name]]):
        result_session = None
        logging.info('environment variables missing')
    else:
        default_dict = {
            'in_user': os.environ[env_user],
            'in_pass': os.environ[env_pass],
            'in_host': os.environ[env_host],
            'in_db_engine_type': 'mysql',
            'in_db_name': os.environ[env_db_name],
            'in_pool_recycle': 3600,
            'in_pool_size': 10
        }
        result_session = gen_session(**default_dict)
        logging.info('session [{}] created'.format(env_db_name))
    return result_session

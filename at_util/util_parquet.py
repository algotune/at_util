"""
generic functions for handling parquet file
TODO: may consider move to util_io.py

"""
from typing import List

import pandas as pd
import os
import pyarrow as pa
import pyarrow.parquet as pq
import uuid
import logging


def to_parquet_table_from_df(input_df: pd.DataFrame, file_path: str = None,
                             file_name: str = None, arg_dict: dict = None) -> str:
    """

    :param arg_dict:
    :param input_df:
    :param file_path:
    :param file_name:
    usage:
        >>> input_df = pd.DataFrame({'a':[1,2, 3],'b':[2, 3, 4]})
        >>> file_path = None
        >>> file_name = None

        >>> file_path = '/Users/b3yang/workspace/at_data/'
        >>> file_name = 'blah.parquet'
    """
    logger = logging.getLogger(__name__)
    f_path = '.' if file_path is None else file_path
    f_name = '{}.parquet'.format(str(uuid.uuid1())) if file_name is None else file_name
    args = {} if arg_dict is None else arg_dict

    final_path = os.path.join(f_path, f_name)
    try:
        table = pa.Table.from_pandas(input_df)
        pq.write_table(table, final_path, **args)

    except Exception as e:
        logger.error(e)
    logger.info('[{}] written'.format(final_path))
    return final_path

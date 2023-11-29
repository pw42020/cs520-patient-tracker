"""db.py

various database functions for program to use
that are more general compared to ones in specific .py files"""

import os
import pymongo
from pymongo import MongoClient


def ping_database() -> str:
    """initialization to ensure that app is running
    and database can be grabbed

    Returns
    -------
    str
        ping if successful

    Raises
    ------
    InternalServerError
        if unsuccessful"""
    try:
        client = get_database("users")
        return "Pinged your deployment. You successfully connected to MongoDB!"
    except Exception as e:
        return e, 500


def get_database(collection: str) -> MongoClient:
    """gets database from MongoDB

    Parameters
    ----------
    collection : str
        collection to grab from

    Returns
    -------
    MongoClient
        database if successful

    Raises
    ------
    Exception
        if unsuccessful"""
    client = MongoClient(os.getenv("MONGODB_URI"))

    return client[collection]

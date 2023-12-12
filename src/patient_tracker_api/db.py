"""db.py

various database functions for program to use
that are more general compared to ones in specific .py files"""

import os
from dotenv import load_dotenv
import pymongo
from pymongo import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()  # loading .env (REQUIRED)


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
        client = MongoClient(
            os.getenv("MONGODB_URI"), tls=True, server_api=ServerApi("1")
        )
        client.admin.command("ping")
        return "Pinged your deployment. You successfully connected to MongoDB!"
    except Exception as e:
        return e, 500


def get_database(db_name: str) -> MongoClient:
    """gets database from MongoDB

    Parameters
    ----------
    db_name : str
        database to grab

    Returns
    -------
    MongoClient
        database if successful

    Raises
    ------
    Exception
        if unsuccessful"""
    client = MongoClient(os.getenv("MONGODB_URI"), tls=True)

    collection = client.Cluster0  # hard-coded at the moment

    return collection[db_name]

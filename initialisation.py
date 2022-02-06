"""Constant declaration"""

from tinydb import TinyDB
from pathlib import Path

DATE_FORMAT = ('%d/%m/%Y', 'jj/mm/aaaa')

TOURNAMENTS_DATABASE_NAME = "Tournaments"
DEFAULT_NUMBER_OF_TURNS = 4

# Save in DataBase at Roots
DB = TinyDB(Path(__file__).resolve().parent / 'db.json', indent=4)
PLAYERS_TABLE = DB.table("Players")
TOURNAMENTS_TABLE = DB.table("Tournaments")


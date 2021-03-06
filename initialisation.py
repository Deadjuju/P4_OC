"""Constant declaration"""

from tinydb import TinyDB
from pathlib import Path


# The number of rounds and players can be changed here
DEFAULT_NUMBER_OF_TURNS = 4
NUMBERS_OF_PLAYERS = 8

DATE_FORMAT = ('%d/%m/%Y', 'jj/mm/aaaa')
HOURS_FORMAT = "%Hh%M"

# Save in DataBase at Roots
DB = TinyDB(Path(__file__).resolve().parent / 'db.json', indent=4)
PLAYERS_TABLE = DB.table("Players")
TOURNAMENTS_TABLE = DB.table("Tournaments")
TURNS_TABLE = DB.table("Turns")
MATCHS_TABLE = DB.table("Matchs")

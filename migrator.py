import argparse
from arnold import main
from peewee import *

parser = argparse.ArgumentParser(description='down up')
parser.add_argument('direction', help='the direction to go')

args = parser.parse_args()
main(
    direction=args.direction,
    database=SqliteDatabase('firstaidkit.db'),
    directory="migrations",
    migration_module="migrations"
)

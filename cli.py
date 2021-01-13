# cli.py
import os
import argparse
from firebase import firebase
import random
import string
from dotenv import load_dotenv

load_dotenv()
DATABASE = os.getenv('DATABASE_URL')

firebase = firebase.FirebaseApplication(DATABASE, None)

parser = argparse.ArgumentParser(
    description="create/accept/modify/delete/settle bets.")
parser.add_argument(
    "-n",
    help="create new bet with given terms",
)
parser.add_argument(
    "-s",
    help="set stakes",
)
parser.add_argument(
    "-d",
    help="set expiration date (duration)",
)
parser.add_argument(
    "-u",
    help="set user",
)
parser.add_argument(
    "-a",
    help="accept bet"
)

args = parser.parse_args()
if args.n:
    key = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    put1 = firebase.put('/bets/' + key, "Bet", args.n)
    put2 = firebase.put('/bets/' + key, "Predictor", args.u)
    put3 = firebase.put('/bets/' + key, "Stakes", args.s)
    put4 = firebase.put('/bets/' + key, "Duration", args.d)
    put5 = firebase.put('/bets/' + key, "Status", "Awaiting challenger")
    put6 = firebase.put('/bets/' + key, "Challenger", "")

if args.a:
    put1 = firebase.put('/bets/' + args.a, "Challenger", args.u)
    put2 = firebase.put('/bets/' + args.a, "Status", "Active")

if args.d:
    delete = firebase.delete('/bets/', args.d)

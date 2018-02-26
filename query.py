# -*- coding: utf-8 -*-
"""
We used (https://mtgjson.com/json/PD2.json) for our data. It's a list of
every card in the 2010 Fire and Lightning Series of Magic The Gathering.
Every card has the following fields:
  id                        The unique SHA1 hash of setCode + cardName + cardImageName
  layout                    How this card is formatted. Possible values: normal, split, flip, double-faced, token, plane, scheme, phenomenon, leveler, vanguard, meld
  name                      The string name of this card.
  names                     An array of names if this is a split or double-sided card. Not always present.
  manaCost                  A string of the mana cost symbols. Every symbol is in {} and is either a number(colorless) or a one-letter abbreviation of the colored mana.
  cmc                       This is a number called the Converted Mana Cost. It is the sum of all the mana required to play this card.
  colors                    This is a list of color names derived from the mana cost.
  colorIdentity             An array of one-letter abbreviations for all the colors mentioned on this card.
  type                      This is the card's type. Consists of "supertypes types — subtypes" like "Legendary Creature — Angel"
  rarity                    How rare this card is. One of Common, Uncommon, Rare, Mythic Rare, Special, Basic Land
  text                      The text of the card. Describes its abilities.
  flavor                    Some cards have this. It's a quote to add flavor to the card.
  artist                    The name of the artist who drew this card.
  power                     The offense. This is a number in a string.
  toughness                 The defense. This is a number in a string.
The data was put into the 'deck' collection of the its2010again' database
of the 'homer.stuy.edu' server. It is contained in PD2.json in this repo,
and was parsed by create.py which loaded the json and inserted it into db
"""

import pymongo

#Given a query document, returns a cursor object containing the results of the search on the deck collection
def query(document):
    connection = pymongo.MongoClient("homer.stuy.edu")
    db = connection["its2010again"]
    collection = db["deck"]
    return collection.find(document)

#Given a mongo cursor object, returns a python list of dictionaries
def cursorToList(c):
    l = []
    for e in c:
        l.append(e)
    return l

#Given a MTG card id, will return the one card with this id or None
def get_by_id(id):
    result = query({"id": id})
    for card in result:
        return card

#Given a string name, will return the one card with this name or None
def get_by_name(name):
    result = query({"name": name})
    for card in result:
        return card

#Given a color name like Red, Green, Blue, White or Black, will return a list of cards that have this color in their mana cost
def get_cards_with_color(c):
    return cursorToList(query({"colors": c}))

#Given two numbers, will return a list of cards with a converted mana cost between the two numbers, inclusive
def get_mana_range(minCMC, maxCMC):
    return cursorToList(query({"cmc": {"$lte": int(maxCMC), "$gte": int(minCMC)}}))

#Given an artist name, returns a list of cards drawn by that artist
def get_by_artist(artist):
    return cursorToList(query({"artist": artist}))

#Given a toughness/defense number, will return a list of cards >= this number
def get_tougher_than(defense):
    return cursorToList(query({"toughness": {"$gte": str(defense)}}))

#Given a power/attack number, will return a list of cards >= this number
def get_stronger_than(attack):
    return cursorToList(query({"power": {"$gte": str(attack)}}))

#Given a number mana cost and a toughness/defense, will return all cards cheaper than the cmc and tougher than this number
def get_cheaper_tougher(cmc, defense):
    return cursorToList(query({"cmc": {"$lte": int(cmc)}, "toughness": {"$gte": str(defense)}}))

#Given a number mana cost and a power/attack, will return all cards cheaper than the cmc and more powerful than this number
def get_cheaper_stronger(cmc, attack):
    return cursorToList(query({"cmc": {"$lte": int(cmc)}, "power": {"$gte": str(attack)}}))

#Returns a list of cards with both power >= attack AND toughness >= defense
def get_min_stats(attack, defense):
    return cursorToList(query({"toughness": {"$gte": str(attack)}, "power": {"$gte": str(defense)}}))

print "get_by_name Spark Elemental"
print get_by_name("Spark Elemental")
print ""
print "get_cards_with_color Red"
print len(get_cards_with_color("Red"))
print ""
print "get_mana_range(3, 4)"
print len(get_mana_range(3, 4))
print ""
print "get_by_artist Michael Sutfin"
print get_by_artist("Michael Sutfin")[:2]
print ""
print "get_min_stats(2, 2)"
print len(get_min_stats(2, 2))
print ""
print "get_cheaper_tougher(3, 2)"
print len(get_cheaper_tougher(3, 2))
print ""
print "get_cheaper_stronger(3, 2)"
print len(get_cheaper_stronger(3, 2))
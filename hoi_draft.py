from constants import *
from country_data import db
from random import choice, shuffle

ideology_na = na
ideology_fa = fa
ideology_co = co
ideology_de = de

def filter_fact(stat, target):
  return list(filter(lambda x: db[x][stat] == target, db))

def _nonaligned():
  return filter_fact('ideo', ideology_na)

def _democracies():
  return filter_fact('ideo', ideology_de)

def _fascis():
  return filter_fact('ideo', ideology_fa)

def _commies():
  return filter_fact('ideo', ideology_co)

def _jokes():
  return filter_fact('status', jk)

def _minors():
  return filter_fact('status', min)

def _majors():
  return filter_fact('status', maj)

def _america():
  # is target in south, central or north america ?
  return list(filter(lambda x: db[x]['loc'] in (SA, CE, NA), db))

def _normalize(target):
  target = target.lower()
  if target in country_alias:
    return target
  for k in country_alias:
    if target in country_alias[k]:
      return k
    


pool = {}
ban_list = []
def regen_pool():
  global pool
  pool = {
    jk: _jokes(),
    min: _minors(),
    maj: _majors(),
    # location
    EU: filter_fact('loc', EU),
    AM: filter_fact('loc', AM),
    NA: filter_fact('loc', NA),
    CA: filter_fact('loc', CA),
    SA: filter_fact('loc', SA),
    AS: filter_fact('loc', AS),
    OC: filter_fact('loc', OC),
    AF: filter_fact('loc', AF),
    ME: filter_fact('loc', ME),
    # ideologies
    na: _nonaligned(),
    de: _democracies(),
    fa: _fascis(),
    co: _commies()
  }
  # shuffle the lists
  for key in pool:
    shuffle(pool[key])

def _remove_from_pools(target):
  if target is None:
      return False
  _info = db[target]
  # remove from all pools country may belong to
  for _type in _info.values():
      if _type in pool and target in pool[_type]:
          # print(f'removing {target} from {_type} pool')
          _index = pool[_type].index(target)
          del pool[_type][_index]
  return True

def _get(_type):
  if _type not in pool or len(pool[_type]) == 0:
      return None
  target = pool[_type].pop()
  _remove_from_pools(target)
  return target.capitalize()

def get_major():
  return _get(maj)

def get_minor():
  return _get(min)

def get_europe():
  return _get(EU)

def get_asia():
  return _get(AS)

def get_midle_east():
  return _get(ME)

def get_africa():
  return _get(AF)

def get_oceania():
  return _get(OC)

def get_america():
  return _get(AM)

def get_namerica():
  return _get(NA)

def get_camerica():
  return _get(CA)

def get_samerica():
  return _get(SA)

def get_jokes():
  return _get(jk)

# ideologies
def get_democracies():
  return _get(SA)

def get_fascis():
  return _get(ideology_fa)

def get_commies():
  return _get(ideology_co)

def get_democracies():
  return _get(ideology_de)

def get_nonaligned():
  return _get(ideology_na)

def ban(country):
  return _remove_from_pools(_normalize(country))


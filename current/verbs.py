"""
verbs.py
Code for handling verbs and conjugation.
"""

from utils import *
from eng_base import *

def base(verb):
  return verb

def add_s(verb):
  if (
    any(verb.endswith(e) for e in ["s", "z", "ch", "sh"])
  or
    verb[-2] in consonants and verb[-1] == "o"
  ):
    return verb + "es"
  elif verb[-2] in consonants and verb[-1] == "y":
    return verb[:-1] + "ies"
  else:
    return verb + "s"

def add_ed(verb):
  # TODO: Final consonant doubling?
  if verb.endswith("e"):
    return verb + "d"
  elif verb[-2] in consonants and verb[-1] == "y":
    return verb[:-1] + "ied"
  else:
    return verb + "ed"

def add_ing(verb):
  # TODO: Consonant doubling here as well?
  if verb.endswith("ie"):
    return verb[:-2] + "ying"
  elif verb.endswith("e") and len(verb) > 2:
    return verb[:-1] + "ing"
  else:
    return verb + "ing"

FORM_DEFAULTS = [
  ("present", "singular", "first", base),
  ("present", "singular", "second", base),
  ("present", "singular", "third", add_s),

  ("present", "plural", "any", base),

  ("past", "any", "any", add_ed),

  ("infinitive", "any", "any", base),

  ("imperative", "any", "any", base),

  ("present participle", "any", "any", add_ing),

  ("past participle", "any", "any", add_ed),
]

# TODO: Modal verbs!
IRREGULAR = {
  "be": [
    ("present", "singular", "first", "am"),
    ("present", "singular", "second", "are"),
    ("present", "singular", "third", "is"),

    ("present", "plural", "any", "are"),

    ("past", "singular", "first", "was"),
    ("past", "singular", "second", "were"),
    ("past", "singular", "third", "was"),

    ("past", "plural", "any", "were"),

    ("past participle", "any", "any", "been"),
  ],
  "do": [
    ("past", "any", "any", "did"),
    ("past participle", "any", "any", "done"),
  ],
  "have": [
    ("present", "singular", "third", "has"),
    ("past", "any", "any", "had"),
    ("past participle", "any", "any", "had"),
  ],
  "will": [
    ("present", "any", "any", "will"),
    ("past", "any", "any", "would"),
    ("infinitive", "any", "any", None),
    ("imperative", "any", "any", None),
    ("present participle", "any", "any", None),
    ("past participle", "any", "any", None),
  ],
  "can": [
    ("present", "any", "any", "can"),

    ("past", "any", "any", "could"),

    ("imperative", "any", "any", None),

    ("present participle", "any", "any", None),

    ("past participle", "any", "any", None),
  ],
  "might": [
    ("present", "any", "any", "might"),
    ("past", "any", "any", "might"),
    ("infinitive", "any", "any", None),
    ("imperative", "any", "any", None),
    ("present participle", "any", "any", None),
    ("past participle", "any", "any", None),
  ],
  "give": [
    ("present", "singular", "first", "give"),
    ("present", "singular", "second", "give"),
    ("present", "singular", "third", "gives"),

    ("present", "plural", "any", "give"),

    ("past", "any", "any", "gave"),

    ("present participle", "any", "any", "giving"),

    ("past participle", "any", "any", "given"),
  ],
  "come": [
    ("present", "singular", "first", "come"),
    ("present", "singular", "second", "come"),
    ("present", "singular", "third", "comes"),

    ("present", "plural", "any", "come"),

    ("past", "any", "any", "came"),

    ("present participle", "any", "any", "coming"),

    ("past participle", "any", "any", "come"),
  ],
  "become": [
    ("present", "singular", "first", "become"),
    ("present", "singular", "second", "become"),
    ("present", "singular", "third", "becomes"),

    ("present", "plural", "any", "become"),

    ("past", "any", "any", "became"),

    ("present participle", "any", "any", "becoming"),

    ("past participle", "any", "any", "become"),
  ],
  "bring": [
    ("present", "singular", "first", "bring"),
    ("present", "singular", "second", "bring"),
    ("present", "singular", "third", "brings"),
    ("present", "plural", "any", "bring"),

    ("past", "any", "any", "brought"),

    ("present participle", "any", "any", "bringing"),

    ("past participle", "any", "any", "brought"),
  ],
  "cannot": [
    ("present", "singular", "first", "cannot"),
    ("present", "singular", "second", "cannot"),
    ("present", "singular", "third", "cannot"),

    ("present", "plural", "any", "cannot"),

    ("past", "any", "any", "could not"),

    ("present participle", "any", "any", None),

    ("past participle", "any", "any", None),
  ],
  "can't": [
    ("present", "singular", "first", "can't"),
    ("present", "singular", "second", "can't"),
    ("present", "singular", "third", "can't"),

    ("present", "plural", "any", "can't"),

    ("past", "any", "any", "couldn't"),

    ("present participle", "any", "any", None),

    ("past participle", "any", "any", None),
  ],
  "don't": [
    ("present", "singular", "first", "don't"),
    ("present", "singular", "second", "don't"),
    ("present", "singular", "third", "doesn't"),

    ("present", "plural", "any", "don't"),

    ("past", "any", "any", "didn't"),

    ("present participle", "any", "any", None),

    ("past participle", "any", "any", None),
  ],
  "strike": [
    ("past", "any", "any", "struck"),
    ("past participle", "any", "any", "struck"),
  ],
  "fight": [
    ("past", "any", "any", "fought"),
    ("past participle", "any", "any", "fought"),
  ],
}

TIMESHIFTS = [
  "future",
  "past",
  "infinitive",
  "raw infinitive"
]
TIMESHIFT = {
  "present": {
    "future": "future",
    "past": "past",
    "infinitive": "infinitive",
    "raw infinitive": "raw infinitive",
  },
  "present continuous": {
    "future": "future continuous",
    "past": "past continuous",
    "infinitive": "present continuous",
    "raw infinitive": "present continuous",
  },
  "present participle": {
    "future": "present participle", # TODO: is this correct?
    "past": "present participle",
    "infinitive": "present participle",
    "raw infinitive": "present participle",
  },
  "past": {
    "future": "future perfect",
    "past": "past perfect",
    "infinitive": "past",
    "raw infinitive": "past",
  },
  "past continuous": {
    "future": "future perfect continuous",
    "past": "past perfect continuous",
    "infinitive": "past continuous",
    "raw infinitive": "past continuous",
  },
  "past participle": {
    "future": "past participle", # TODO: is this correct?
    "past": "past participle",
    "infinitive": "past participle",
    "raw infinitive": "past participle",
  },
  "future": {
    "future": "future", # does this work?
    "past": "past future", # TODO: I GIVE UP!
    "infinitive": "future",
    "raw infinitive": "future",
  },
  "future continuous": {
    "future": "future continuous",
    "past": "past future continuous",
    "infinitive": "future continuous",
    "raw infinitive": "future continuous",
  },
  "raw infinitive": {
    "future": "raw infinitive",
    "past": "raw infinitive",
    "infinitive": "raw infinitive",
    "raw infinitive": "raw infinitive",
  },
  "infinitive": {
    "future": "infinitive",
    "past": "infinitive",
    "infinitive": "infinitive",
    "raw infinitive": "infinitive",
  },
  "imperative": {
    "future": "imperative",
    "past": "imperative",
    "infinitive": "imperative",
    "raw infinitive": "imperative",
  },
  "present perfect": {
    "future": "future perfect",
    "past": "past perfect",
    "infinitive": "present perfect",
    "raw infinitive": "present perfect",
  },
  "present perfect continuous": {
    "future": "future perfect continuous",
    "past": "past perfect continuous",
    "infinitive": "present perfect continuous",
    "raw infinitive": "present perfect continuous",
  },
  "past perfect": {
    "future": "future perfect", # TODO: is this right? (and below)
    "past": "past perfect",
    "infinitive": "past perfect",
    "raw infinitive": "past perfect",
  },
  "past perfect continuous": {
    "future": "future perfect continuous",
    "past": "past perfect continuous",
    "infinitive": "past perfect continuous",
    "raw infinitive": "past perfect continuous",
  },
  "future perfect": {
    "future": "future perfect",
    "past": "past future perfect",
    "infinitive": "future perfect",
    "raw infinitive": "future perfect",
  },
  "future perfect continuous": {
    "future": "future perfect continuous",
    "past": "past future perfect continuous",
    "infinitive": "future perfect continuous",
    "raw infinitive": "future perfect continuous",
  },
  # Made-up tenses:
  "past future": {
    "future": "ERROR: future past future",
    "past": "ERROR: past past future",
    "infinitive": "ERROR: infinitive past future",
    "raw infinitive": "ERROR: raw infinitive past future",
  },
  "past future continuous": {
    "future": "ERROR: future past future continuous",
    "past": "ERROR: past past future continuous",
    "infinitive": "ERROR: infinitive past future continuous",
    "raw infinitive": "ERROR: raw infinitive past future continuous",
  },
  "past future perfect": {
    "future": "ERROR: future past future perfect",
    "past": "ERROR: past past future perfect",
    "infinitive": "ERROR: infinitive past future perfect",
    "raw infinitive": "ERROR: raw infinitive past future perfect",
  },
  "past future perfect continuous": {
    "future": "ERROR: future past future perfect continuous",
    "past": "ERROR: past past future perfect continuous",
    "infinitive": "ERROR: infinitive past future perfect continuous",
    "raw infinitive": "ERROR: raw infinitive past future perfect continuous",
  },
}

CONJUGATION = {} # redefined later

def verb_form(verb, tns="present", nmbr="any", per="any"):
  """
  Figures out the form of the given verb and returns it.
  """
  lookup = (tns, nmbr, per)
  if verb in IRREGULAR:
    irr = table_match(IRREGULAR[verb], lookup)
    if irr:
      return irr
    # else fall out:
  return table_match(FORM_DEFAULTS, lookup)(verb)

def conjugation(verb, tns="present", nmbr="any", per="any", timeshift=None):
  """
  If "timeshift" is given it throws the verb into the appropriate relative
  "future" or "past" tense.
  """
  if timeshift:
    tns = TIMESHIFT[tns][timeshift]
  return CONJUGATION[tns](verb, nmbr, per)

def conj_ref(thing, verb, tns, timeshift=None):
  """
  Uses the given noun to help conjugate the given verb (but still needs a tense
  of course).
  """
  return conjugation(verb, tns, thing.number, thing.person, timeshift)

CONJUGATION = {
  "present":
    lambda v, n, p: verb_form(v, "present", n, p),
  "present continuous":
    lambda v, n, p:
      verb_form("be", "present", n, p) + " " +
      verb_form(v, "present participle", n, p),
  "present participle":
    lambda v, n, p:
      verb_form(v, "present participle", n, p),
  "past":
    lambda v, n, p: verb_form(v, "past", n, p),
  "past continuous":
    lambda v, n, p:
      verb_form("be", "past", n, p) + " " +
      verb_form(v, "present participle", n, p),
  "past participle":
    lambda v, n, p:
      verb_form(v, "past participle", n, p),
  "future":
    lambda v, n, p:
      verb_form("will", "present", n, p) + " " +
      verb_form(v, "infinitive", n, p),
  "future continuous":
    lambda v, n, p:
      conjugation("be", "future", n, p) + " " +
      verb_form(v, "present participle", n, p),
  "raw infinitive":
    lambda v, n, p:
      verb_form(v, "infinitive", n, p),
  "infinitive":
    lambda v, n, p:
      "to " + verb_form(v, "infinitive", n, p),
  "imperative":
    lambda v, n, p:
      verb_form(v, "imperative", n, p),
  "present perfect":
    lambda v, n, p:
      verb_form("have", "present", n, p) + " " +
      verb_form(v, "past participle", n, p),
  "present perfect continuous":
    lambda v, n, p:
      conjugation("be", "present perfect", n, p) + " " +
      verb_form(v, "present participle", n, p),
  "past perfect":
    lambda v, n, p:
      verb_form("have", "past", n, p) + " " +
      verb_form(v, "past participle", n, p),
  "past perfect continuous":
    lambda v, n, p:
      conjugation("be", "past perfect", n, p) + " " +
      verb_form(v, "present participle", n, p),
  "future perfect":
    lambda v, n, p:
      conjugation("have", "future", n, p) + " " +
      verb_form(v, "past participle", n, p),
  "future perfect continuous":
    lambda v, n, p:
      conjugation("be", "future perfect", n, p) + " " +
      verb_form(v, "present participle", n, p),
  # Some made-up tenses:
  "past future":
    lambda v, n, p:
      verb_form("will", "past", n, p) + " " +
      verb_form(v, "infinitive", n, p),
  "past future continuous":
    lambda v, n, p:
      conjugation("be", "past future", n, p) + " " +
      verb_form(v, "present participle", n, p),
  "past future perfect":
    lambda v, n, p:
      conjugation("have", "past future", n, p) + " " +
      verb_form(v, "past participle", n, p),
  "past future perfect continuous":
    lambda v, n, p:
      conjugation("have", "past future perfect", n, p) + " " +
      verb_form(v, "present participle", n, p),
}

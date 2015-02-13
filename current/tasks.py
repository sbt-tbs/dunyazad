"""
tasks.py
"""

import os
import random

import asp
import ans

from ans import Pr, Vr, PVr, SbT

# Defines where to search for global rules:
GLOBAL_RULES_DIR = "rules"

# shortcut:
opj = os.path.join

# Base source files:
BASE_SOURCES = [
  "utils.lp",
  opj("story", "core.lp"),
  opj("story", "setup.lp"),
  opj("story", "symbols.lp"),
  opj("story", "the_party.lp"),
  opj("story", "skills.lp"),
  opj("story", "items.lp"),
  opj("story", "settings.lp"),
  opj("story", "potential.lp"),
  opj("story", "grow.lp"),
  opj("story", "eval.lp"),
  opj("story", "vignettes.lp"),
  opj("story", "choice_structure.lp"),
  opj("story", "surface.lp"),
]

CONTENT_DIR = opj("story", "content")

CONTENT_SOURCES = [
  opj(GLOBAL_RULES_DIR, CONTENT_DIR, f)
    for f in os.listdir(opj(GLOBAL_RULES_DIR, CONTENT_DIR))
    if f.endswith(".lp")
]

ALL_SOURCES = [
  opj(GLOBAL_RULES_DIR, path) for path in BASE_SOURCES
] + CONTENT_SOURCES

SEP = '\n' + '%'*80 + '\n'

BASE_SRC = SEP + "% Base source code start." + SEP
for s in ALL_SOURCES:
  with open(s) as fin:
    BASE_SRC += fin.read() + SEP
BASE_SRC += "% Base source code end." + SEP

FRAGMENTS_DIR = "fragments"

FR_CACHE = {}
def fr(name):
  if name in FR_CACHE:
    return FR_CACHE[name]
  else:
    code = ""
    fl = opj(*(name.split('.'))) + ".lp"
    with open(opj(FRAGMENTS_DIR, fl)) as fin:
      code = fin.read()
    FR_CACHE[name] = code
    return code

SC = {
  "story_node": Pr("story_node", Vr("Node")),
  "node_type": Pr("node_type", Vr("Node"), Vr("Type")),
  "option": Pr("at", Vr("Node"), Pr("option", Vr("Opt"))),
  "successor": Pr("successor", Vr("From"), Pr("option", Vr("Opt")), Vr("To")),
  "setup": PVr("setup", "setup", Vr("Node"), Vr("Which")),
  "polished": Pr("node_status", Vr("Node"), Pr("polished")),
  "unique_key_used": Pr("unique_key_used", Vr("Key")),
  "max_unique": Pr("max_unique", Vr("Key")),
}

KEEP = {
  "at": PVr("at", "at", Vr("Node"), SbT("Fluent")),
  "st": PVr("st", "st", Vr("Node"), SbT("Fluent")),

  "story_node": PVr("story_node", "story_node", Vr("Node")),
  "story_root": PVr("story_root", "story_root", Vr("Node")),
  "node_type": PVr("node_type", "node_type", Vr("Node"), Vr("Type")),
  "node_status_reached":
    PVr("node_status_reached", "node_status_reached", Vr("Node"), Vr("Status")),
  "successor":
    PVr(
      "successor", "successor",
      Vr("From"),
      Pr("option", Vr("Opt")),
      Vr("To"),
    ),
  "path_length": PVr("path_length", "path_length", Vr("Node"), Vr("Count")),

  "vignette": PVr("vignette", "vignette", Vr("Node"), Vr("Root")),
  "setting": PVr("setting", "setting", Vr("Node"), Vr("Setting")),

  "setup": PVr("setup", "setup", Vr("Node"), Vr("Which")),
  "spontaneous":
    PVr("spontaneous", "spontaneous", Pr("st", Vr("Node"), SbT("State"))),
  "unresolved_potential":
    PVr(
      "unresolved_potential", "unresolved_potential",
      Vr("Node"),
      Pr("option", Vr("Opt")),
      SbT("Potential"),
    ),
  "resolves_vignette":
    PVr(
      "resolves_vignette", "resolves_vignette", 
      Vr("Node"),
      Pr("option", Vr("Opt")),
    ),

  "intro_text":
    PVr("intro_text", "intro_text", Vr("Node"), Vr("Setup"), Vr("Text")),
  "potential_text":
    PVr("potential_text", "potential_text", Vr("Node"), Vr("Text")),
}

def runfr(story, name, extra = ""):
  program = SEP.join(
    [
      BASE_SRC,
      '\n'.join(str(pr) + '.' for pr in story),
      fr(name),
      extra
    ]
  )
  return program, asp.solve(program)

def filter_keep(story):
  result = []
  for sch, bnd in ans.bindings(KEEP, story):
    result.append(bnd[sch])
  # Unique key handling:
  max_unique_key = None
  for pr in story:
    b = ans.bind(SC["unique_key_used"], pr)
    if b:
      k = int(str(b["unique_key_used.Key"]))
      if max_unique_key == None or k > max_unique_key:
        max_unique_key = k
    b = ans.bind(SC["max_unique"], pr)
    if b:
      k = int(str(b["max_unique.Key"]))
      if max_unique_key == None or k > max_unique_key:
        max_unique_key = k
  if max_unique_key == None:
    result.append(Pr("max_unique", Pr(0)))
  else:
    result.append(Pr("max_unique", Pr(max_unique_key)))
  return result

def all_nodes(story):
  for pr in story:
    b = ans.bind(SC["story_node"], pr)
    if b:
      yield b["story_node.Node"]

def all_polished_nodes(story):
  for pr in story:
    b = ans.bind(SC["status_polished"], pr)
    if b:
      yield b["status_polished.Node"]

def all_endings(story):
  for pr in story:
    b = ans.bind(SC["node_type"], pr)
    if b and str(b["node_type.Type"]) == "ending":
      yield b["node_type.Node"]

def all_vignette_beginnings(story):
  # TODO: Fix me!
  for pr in story:
    b = ans.bind(SC["setup"], pr)
    if b:
      yield b["setup.Node"]

def all_options(story):
  for pr in story:
    b = ans.bind(SC["option"], pr)
    if b:
      yield (b["at.Node"], b["at.option.Opt"])

def all_successors(story):
  for pr in story:
    b = ans.bind(SC["successor"], pr)
    if b:
      yield (b["successor.From"], b["successor.option.Opt"], b["successor.To"])

def all_polished_nodes(story):
  for pr in story:
    b = ans.bind(SC["polished"], pr)
    if b:
      yield b["node_status.Node"]

def all_uninstantiated_nodes(story):
  an = all_nodes(story)
  ao = list(all_options(story))
  for n in an:
    hit = False
    for node, opt in ao:
      if n == node:
        hit = True
        break
    if not hit:
      yield n

def all_unfinished_options(story):
  ao = all_options(story)
  ae = list(all_endings(story))
  an = list(all_nodes(story))
  asc = list(all_successors(story))
  for n, opt in ao:
    if n in ae:
      continue
    hit = False
    for node, option, nxt in asc:
      if n == node and opt == option:
        hit = True
        break
    if not hit:
      yield (n, opt)

# Tasks:

def setup_story(story, extra=""):
  program, solution = runfr(story, "setup", extra)
  return program, filter_keep(solution)

def instantiate_node(story, n, extra=""):
  program, solution = runfr(
    story,
    "instantiate",
    extra + "\ntarget_node({}).".format(n)
  )
  return program, filter_keep(solution)

def branch_node(story, n, extra=""):
  program, solution = runfr(
    story,
    "branch",
    extra + "\ntarget_node({}).".format(n)
  )
  return program, filter_keep(solution)

def polish_ending(story, n, extra=""):
  program, solution = runfr(
    story,
    "branch",
    extra + "\ntarget_node({}).".format(n)
  )
  return program, filter_keep(solution)

def random_uninstantiated(story):
  l = list(all_uninstantiated_nodes(story))
  if l:
    return random.choice(l)
  else:
    print("Random uninstantiated: none left!")
    return None

def random_unbranched(story):
  l = list(all_unfinished_options(story))
  if l:
    return random.choice(l)[0]
  else:
    print("Random unbranched: none left!")
    return None

def random_ending(story):
  l = list(all_endings(story))
  if l:
    return random.choice(l)
  else:
    print("Random ending: none left!")
    return None

def random_unpolished_ending(story):
  l = list(all_endings(story))
  p = set(all_polished_nodes(story))
  upe = [ e for e in l if e not in p ]
  if upe:
    return random.choice(upe)
  else:
    print("Random unpolished ending: none left!")
    return None

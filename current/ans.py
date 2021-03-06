"""
ans.py
Answer set data structures.
"""

from utils import *

import re
import string

import packrat

@instance
class Tokens:
  """
  An object containing regular expressions for various tokens.
  """
  QUERY_MARK = packrat.Token(re.compile(r"\?"))
  CONS = packrat.Token(re.compile(r":-"))
  WCONS = packrat.Token(re.compile(r":~"))
  DOT = packrat.Token(re.compile(r"\.((?=[^.])|$)"))
    # Matches a period NOT followed by another, but doesn't eat the following
    # character.
  AT = packrat.Token(re.compile(r"@"))
  OR = packrat.Token(re.compile(r"\|"))
  NAF = packrat.Token(re.compile(r"not"))

  COMMA = packrat.Token(re.compile(r","))
  COLON = packrat.Token(re.compile(r":"))
  SEMICOLON = packrat.Token(re.compile(r";"))

  OP_PLUS = packrat.Token(re.compile(r"\+"))
  OP_MINUS = packrat.Token(re.compile(r"-"))
  OP_TIMES = packrat.Token(re.compile(r"\*((?=[^*])|$)"))
  OP_DIV = packrat.Token(re.compile(r"/"))
  OP_MOD = packrat.Token(re.compile(r"\\"))
  OP_POW = packrat.Token(re.compile(r"\*\*"))
  OP_BITWISE_AND = packrat.Token(re.compile(r"&"))
  OP_BITWISE_OR = packrat.Token(re.compile(r"\?"))
  OP_BITWISE_XOR = packrat.Token(re.compile(r"\^"))
  OP_BITWISE_NEG = packrat.Token(re.compile(r"~"))

  CMP_EQ = packrat.Token(re.compile(r"="))
  CMP_NEQ = packrat.Token(re.compile(r"(<>)|(!=)"))
  CMP_GT = packrat.Token(re.compile(r">((?=[^=])|$)"))
  CMP_LT = packrat.Token(re.compile(r"<((?=[^=])|$)"))
  CMP_GE = packrat.Token(re.compile(r">="))
  CMP_LE = packrat.Token(re.compile(r"<="))

  INTERVAL = packrat.Token(re.compile(r"\.\."))

  ANONYMOUS = packrat.Token(re.compile(r"_((?=[^a-zA-Z0-9_])|$)"))
    # Matches an underscore NOT followed any further word characters, but
    # doesn't eat the following character.

  NUMBER = packrat.Token(re.compile(r"0|([1-9][0-9]*)"))

  ID = packrat.Token(re.compile(r"[a-z_][A-Za-z0-9_]*"))
  VARIABLE = packrat.Token(re.compile(r"[A-Z][A-Za-z0-9_]*"))

  STRING = packrat.Token(re.compile(r'"([^\\"]|(\\.))*"'))
    # Matches a starting quote, followed by any number of tokens which are
    # either non-backslash, non-quote characters or which are escape codes ('\'
    # plus any character), finished by an ending quote.

  SCRIPT_TYPE_LUA = packrat.Token(re.compile(r"lua"))
  SCRIPT_TYPE_PYTHON = packrat.Token(re.compile(r"python"))

  SCRIPT_BODY = packrat.Token(re.compile(r"(.|\n)*#end(?=\.)", re.MULTILINE))
    # Matches any number of characters until the string "#end." and doesn't eat
    # the final period in "#end."

  DIR_HIDE = packrat.Token(re.compile(r"#hide"))
  DIR_SHOW = packrat.Token(re.compile(r"#show"))
  DIR_CONST = packrat.Token(re.compile(r"#const"))
  DIR_DOMAIN = packrat.Token(re.compile(r"#domain"))
  DIR_EXTERNAL = packrat.Token(re.compile(r"#external"))
  DIR_SCRIPT = packrat.Token(re.compile(r"#script"))

  DIRECTIVE_BODY = packrat.Token(re.compile(r"[^.]*(?=\.)"))
    # Matches any number of non-period characters followed by a period, but
    # doesn't eat the period.

  ABS = packrat.Token(re.compile(r"\|"))
  PAREN_OPEN = packrat.Token(re.compile(r"\("))
  PAREN_CLOSE = packrat.Token(re.compile(r"\)"))
  CURLY_OPEN = packrat.Token(re.compile(r"\{"))
  CURLY_CLOSE = packrat.Token(re.compile(r"\}"))
  SQUARE_OPEN = packrat.Token(re.compile(r"\["))
  SQUARE_CLOSE = packrat.Token(re.compile(r"\]"))

  KW_AGGREGATE_COUNT = packrat.Token(re.compile(r"#count"))
  KW_AGGREGATE_MIN = packrat.Token(re.compile(r"#min"))
  KW_AGGREGATE_MAX = packrat.Token(re.compile(r"#max"))
  KW_AGGREGATE_SUM = packrat.Token(re.compile(r"#sum"))

  KW_MAXIMIZE = packrat.Token(re.compile(r"#maximi[sz]e"))
  KW_MINIMIZE = packrat.Token(re.compile(r"#minimi[sz]e"))

  LOOSE_CONSTANT = packrat.Token(re.compile(r"_*[a-z][a-zA-Z0-9_]*"))
  LOOSE_VARIABLE = packrat.Token(re.compile(r"_*[A-Z][a-zA-Z0-9_]*"))
    # Matches some number of optional starting underscores, a first-position
    # alphabetic character, and then any number of alphanumerics and/or
    # underscores.

  LOOSE_INTEGER = packrat.Token(re.compile(r"-?[0-9]+"))

  KW_INFIMUM = packrat.Token(re.compile(r"#infimum"))
  KW_SUPREMUM = packrat.Token(re.compile(r"#supremum"))

  COMMENT = packrat.Token(re.compile(r"%([^*\n][^\n]*)?\n"))
    # Matches a percent possibly followed by some junk and then a newline.
    # The junk doesn't begin with either a * or a newline and it doesn't
    # contain any newlines.

  MULTI_LINE_COMMENT = packrat.Token(re.compile(r"%\*([^*]|(\*[^%]))*\*%"))
    # Matches %* followed by some junk which is composed entirely of either
    # non-asterisk characters or pairs of characters that begin with an
    # asterisk and end with a non-% character. All of this ends with *%.

  BLANK = packrat.Token(re.compile(r"[ \t\n]+"))

  @instance
  class Ignore:
    '''
    A place to store ignored versions of the normal attributes.
    '''
    pass

for attr in Tokens.__dict__:
  if not attr.startswith("__") and not attr.endswith("__") and attr != "Ignore":
    val = Tokens.__dict__[attr]
    if isinstance(val, packrat.StrToken):
      setattr(Tokens.Ignore, attr, packrat.StrToken(val.string, preserve=False))
    elif isinstance(val, packrat.REToken):
      setattr(Tokens.Ignore, attr, packrat.REToken(val.expression, omit=True))
    else:
      setattr(Tokens.Ignore, attr, packrat.Omit(val))

class Predicate:
  """
  A Predicate represents a predicate structure, something like:

    foo(bar, baz(xyzzy))

  Each Predicate object has a name and 0 or more arguments. Generally, unless
  the name begins and ends with a '"' character, it should only contain
  characters from the class [a-zA-Z0-9_] and its first character should be in
  [a-z]. This is not a strict rule however.
  """
  def __init__(self, name="_", *args):
    self.name = name
    self.args = args
    self._polish()

  def __str__(self):
    if self.args:
      return "{}({})".format(self.name, ', '.join(str(a) for a in self.args))
    else:
      return str(self.name)

  def unquoted(self):
    if self.args:
      return "{}({})".format(
        dequote(self.name),
        ', '.join(a.unquoted() for a in self.args)
      )
    else:
      return dequote(str(self.name))

  def __repr__(self):
    return "Predicate({}{})".format(
      repr(self.name),
      ', '.join([""] + [repr(a) for a in self.args])
    )

  def __hash__(self):
    return 47 * (
      47 * (
        31 + hash(self.args)
      ) + hash(self.name)
    )

  def __eq__(self, other):
    return (
      (type(self) == type(other))
    and
      (self.name == other.name)
    and
      (len(self.args) == len(other.args))
    and
      all(self.args[i] == other.args[i] for i in range(len(self.args)))
    )

  def __ne__(self, other):
    return not self == other

  def matches(self, other):
    return self.name == other.name and len(self.args) == len(other.args)

  def _polish(self):
    self.args = tuple(self.args)

Predicate.grammar = packrat.Package(
  Predicate,
  packrat.OneOf(
    packrat.Seq(
      packrat.Attr(
        "name",
        packrat.Munge(
          lambda x: ''.join(x),
          packrat.Seq(
            packrat.Opt( Tokens.AT ),
            packrat.OneOf( Tokens.STRING, Tokens.LOOSE_CONSTANT )
          )
        )
      ),
      packrat.Opt(
        packrat.Seq(
          Tokens.Ignore.PAREN_OPEN,
          packrat.Attr(
            "args",
            packrat.SepList( Predicate, sep=Tokens.Ignore.COMMA )
          ),
          Tokens.Ignore.PAREN_CLOSE,
        )
      )
    ),
    packrat.Attr(
      "name",
      packrat.OneOf(
        Tokens.ANONYMOUS,
        packrat.Munge(
          int,
          Tokens.LOOSE_INTEGER,
        ),
        Tokens.KW_INFIMUM,
        Tokens.KW_SUPREMUM,
      )
    ),
  ),
  "_polish"
)

PredicateStatement = packrat.Munge(
  lambda r: r[0],
  packrat.Seq(
    Predicate,
    Tokens.Ignore.DOT
  )
)


class Variable(Predicate):
  """
  Variables can be inserted into predicate structures to do predicate binding.
  Generally their names should begin with uppercase letters (class [A-Z]) but
  should otherwise follow the conventions for Predicate names. A normal
  variable matches any predicate with the same number of arguments as it.
  """
  def __str__(self):
    if self.args:
      return "var<{}({})>".format(
        self.name,
        ', '.join(str(a) for a in self.args)
      )
    else:
      return "var<{}>".format(self.name)

  def __hash__(self):
    return 7 * hash(super())

  def matches(self, other):
    return len(self.args) == len(other.args)

class PatternVariable(Variable):
  """
  A PatternVariable is like a normal variable but to match a predicate it must
  also satisfy a regular expression match (it must match fully).
  """
  def __init__(self, name, pattern, *args):
    super().__init__(name, *args)
    self.re = re.compile(pattern)

  def __str__(self):
    if self.args:
      return "cvar<{}:'{}'({})>".format(
        self.name,
        self.re.pattern,
        ', '.join(str(a) for a in self.args)
      )
    else:
      return "cvar<{}:'{}'>".format(self.name, self.re.pattern)

  def __hash__(self):
    return 27 * (
      17 + hash(self.re.pattern)
    ) + hash(super())

  def __eq__(self, other):
    return type(self) == type(other) \
        and self.name == other.name \
        and self.re.pattern == other.re.pattern \
        and self.args == other.args

  def matches(self, other):
    return len(self.args) == len(other.args) \
        and self.re.fullmatch(other.name)

class Subtree(Variable):
  """
  A subtree is like a normal variable, but it matches an entire subtree with a
  single node, no matter what structure that subtree has. For this reason,
  Subtrees can't have arguments, unlike the other variable types.
  """
  def __init__(self, name):
    super().__init__(name)

  def __str__(self):
    return "subtree<{}>".format(self.name)

  def __hash__(self):
    return 51 * (
      11 + hash(self.name)
    )

  def __eq__(self, other):
    return type(self) == type(other) and self.name == other.name

  def matches(self, other):
    return True

# How to represent arbitrary values as predicates

def as_predicate(value):
  if type(value) == int:
    return Predicate(value)
  elif type(value) == Predicate:
    return value
  else:
    return Predicate(quote(str(value)))

def build_schema(predicate):
  """
  Takes the given pure-Predicate structure and converts all predicates whose
  names start with uppercase letters into simple Variable objects, thus
  producing a schema.
  """
  new_args = []
  for arg in predicate.args:
    new_args.append(build_schema(arg))
  predicate.args = tuple(new_args)
  if type(predicate.name) == str \
  and predicate.name[0] in string.ascii_uppercase:
    return Variable(predicate.name, *predicate.args)
  else:
    return predicate

def build_fancy_schema(predicate):
  """
  Just like build_schema, but converts predicates that start with 'ST' into
  Subtree objects instead of normal Variables. Their arguments are ignored.
  """
  if isinstance(predicate, SimpleTerm):
    if predicate.terms:
      predicate = Predicate(predicate.id, *predicate.terms)
    else:
      predicate = Predicate(predicate.id)
  new_args = []
  for arg in predicate.args:
    new_args.append(build_fancy_schema(arg))
  predicate.args = tuple(new_args)
  if type(predicate.name) == str \
  and predicate.name[0] in string.ascii_uppercase:
    if predicate.name[:2] == "ST":
      return Subtree(predicate.name)
    else:
      return Variable(predicate.name, *predicate.args)
  else:
    return predicate

def bind(schema, predicate, prefix=""):
  """
  Takes a schema (see build_schema for a convenient way to produce one) and a
  predicate and tries to bind each Variable in the given schema to part of the
  given Predicate. If it succeeds, it returns a binding dictionary which maps
  variable names (using a dotted format to specify them absolutely relative to
  the root of the schema) to Predicate objects. So for example if we tried to
  bind:

    Unknown(foo, bar, Var(3, vwe(Baz)))

  against:

    xyzzy(foo, bar, twee(3, vwe(4)))

  the resulting binding dictionary would look like this:

    {
      "Unknown": xyzzy(foo, bar, twee(3, vwe(4))),
      "Unknown.Var": twee(3, vwe(4)),
      "Unknown.Var.vwe.Baz": 4,
    }

  keeping in mind that the above unquoted text represents Predicate objects. If
  the binding fails it returns None. Note that the prefix argument can be used
  to add a prefix to each binding in the result.
  """
  if not schema.matches(predicate):
    return None

  if prefix:
    prefix = prefix + '.' + str(schema.name)
  else:
    prefix = str(schema.name)
  result = {}

  if isinstance(schema, Variable):
    result[prefix] = predicate
    if isinstance(schema, Subtree):
      # Don't recurse further in this case...
      return result

  for i in range(len(schema.args)):
    b = bind(schema.args[i], predicate.args[i], prefix)
    if b == None:
      return None
    result.update(b)

  return result

# shortcuts:
Pr = Predicate
Vr = Variable
PVr = PatternVariable
SbT = Subtree

def bindings(schemas, predicates):
  """
  Takes a dictionary of schemas (each indexed by a string) and an iterable of
  predicates and generates all successful bindings of schemas in the dictionary
  to predicates in the iterable. The schemas are matched against each predicate
  in sort order of their keys, and more than one binding per predicate may be
  generated. Empty (but not failed) bindings may be generated for schemas with
  no variables in them. Each value yielded is a tuple containing the key for
  the schema that generated it and then the binding result (see the bind
  function above).
  """
  skeys = sorted(schemas.keys())
  for p in predicates:
    for k in skeys:
      b = bind(schemas[k], p)
      if b != None:
        yield (k, b)

def filter(predicates, require=[], forbid=[]):
  """
  Filters the given predicate set according to the given require and/or forbid
  lists. Each predicate which matches all schemas in the require list (if any
  are given) and which matches none of the filters in the forbid list is kept,
  all other predicates are dropped.
  """
  for p in predicates:
    if all(bind(schema, p) != None for schema in require) \
    and all(bind(schema, p) == None for schema in forbid):
      yield p

# Class definitions for answer set elements:
# Based almost entirely on the ASP-CORE language specification (and probably
# missing some gringo-specific constructions).
# https://www.mat.unical.it/aspcomp2013/files/ASP-CORE-2.03b.pdf

@attr_object("negated", "op", "lhs", "rhs")
class Expression:
  def __str__(self):
    if self.rhs:
      return "{}({} {} {})".format(
        '-' if self.negated else '',
        self.lhs,
        self.op,
        self.rhs
      )
    elif self.op:
      return "{}{}({})".format(
        '-' if self.negated else '',
        self.op,
        self.lhs
      )
    else:
      return "{}({})".format(
        '-' if self.negated else '',
        self.lhs
      )

@attr_object("id", "terms")
class SimpleTerm:
  def __str__(self):
    if self.terms:
      return "{}({})".format(
        self.id,
        ', '.join(str(t) for t in self.terms)
      )
    else:
      return "{}".format(self.id)

@attr_object("lower", "upper")
class Interval:
  def __str__(self):
    return "{}..{}".format(self.lower, self.upper)

@attr_object("function", "args")
class ScriptCall:
  def __str__(self):
    return "@{}({})".format(
      self.function,
      ', '.join(str(a) for a in self.args)
    )

@attr_object("negated", "id", "terms")
class ClassicalLiteral:
  def __str__(self):
    if self.terms:
      return "{}{}({})".format(
        '-' if self.negated else '',
        self.id,
        ', '.join(str(t) for t in self.terms)
      )
    else:
      return "{}{}".format(
        '-' if self.negated else '',
        self.id
      )

@attr_object("op", "lhs", "rhs")
class BuiltinAtom:
  def __str__(self):
    return "{} {} {}".format(self.lhs, self.op, self.rhs)

@attr_object("negated", "contents")
class NafLiteral:
  def __str__(self):
    if self.negated:
      return "not {}".format(self.contents)
    else:
      return str(self.contents)

@attr_object("weight", "level", "terms")
class WeightAtLevel:
  def __str__(self):
    return "{}@{}, {}".format(
      self.weight,
      self.level,
      ', '.join(str(t) for t in self.terms)
    )

@attr_object("terms", "constraints")
class AggregateElement:
  def __str__(self):
    if self.constraints:
      return "{} : {}".format(
        ', '.join(str(t) for t in self.terms),
        ', '.join(str(c) for c in self.constraints),
      )
    else:
      return ', '.join(str(t) for t in self.terms)

@attr_object("negated", "l", "lop", "function", "elements", "uop", "u")
class Aggregate:
  def __str__(self):
    return "{n}{l}{lop}{function} {{ {elements} }}{uop}{u}".format(
      n="not " if self.negated else "",
      l=(self.l and (str(self.l) + ' ')) or '',
      lop=(self.lop and (str(self.lop) + ' ')) or '',
      function=self.function,
      elements='; '.join(str(e) for e in self.elements),
      uop=(self.uop and (' ' + str(self.uop))) or '',
      u=(self.u and (' ' + str(self.u))) or '',
    )

@attr_object("literal", "constraints")
class ChoiceElement:
  def __str__(self):
    if self.constraints:
      return "{} : {}".format(
        self.literal,
        ', '.join(str(c) for c in self.constraints)
      )
    else:
      return str(self.literal)

@attr_object("l", "lop", "elements", "uop", "u")
class Choice:
  def __str__(self):
    return "{l}{lop}{{ {elements} }}{uop}{u}".format(
      l=(self.l and (str(self.l) + ' ')) or '',
      lop=(self.lop and (str(self.lop) + ' ')) or '',
      elements='; '.join(str(e) for e in (self.elements or [])),
      uop=(self.uop and (str(self.uop) + ' ')) or '',
      u=(self.u and (str(self.u) + ' ')) or '',
    )

@attr_object("elements")
class Disjunction:
  def __str__(self):
    return ' | '.join(str(e) for e in self.elements)


@attr_object("weightlevel", "literals")
class OptimizeElement:
  def __str__(self):
    if self.literals:
      return "{} : {}".format(
        self.weightlevel,
        ', '.join(str(l) for l in self.literals)
      )
    else:
      return str(self.weightlevel)

@attr_object("function", "elements")
class Optimization:
  def __str__(self):
    return "{} {{ {} }}.".format(
      self.function,
      '; '.join(str(e) for e in (self.elements or []))
    )

@attr_object("body", "weightlevel")
class WeakConstraint:
  def __str__(self):
    return ":~ {}. [ {}@{}, {} ]".format(
      ', '.join(str(l) for l in self.body),
      self.weight,
      self.level,
      ', '.join(str(t) for t in self.terms)
    )

@attr_object("head", "body")
class Rule:
  def __str__(self):
    if self.head:
      if self.body:
        return "{} :- {}.".format(
          self.head,
          ', '.join(str(e) for e in self.body)
        )
      else:
        return "{}.".format(self.head)
    else:
      return ":- {}.".format(', '.join(str(e) for e in self.body))

@attr_object("literal")
class Query:
  def __str__(self):
    return "{}?".format(self.literal)

@attr_object("language", "contents")
class Script:
  def __str__(self):
    return "#script ({})\n{}.".format(self.language, self.contents)

@attr_object("directive", "contents")
class Directive:
  def __str__(self):
    return "{} {}.".format(self.directive, self.contents)

@attr_object("text")
class Comment:
  def __str__(self):
    return "%* {} *%".format(self.text)

@attr_object("statements", "query")
class Program:
  def __str__(self):
    return "{}{}".format(
      '\n'.join(str(s) for s in self.statements),
      '\n' + str(self.query) if self.query else ''
    )

# Grammar definitions for answer set elements:

ArithOp = packrat.OneOf(
  Tokens.OP_PLUS,
  Tokens.OP_MINUS,
  Tokens.OP_TIMES,
  Tokens.OP_DIV,
  Tokens.OP_MOD,
  Tokens.OP_POW,
  Tokens.OP_BITWISE_AND,
  Tokens.OP_BITWISE_OR,
  Tokens.OP_BITWISE_XOR,
  Tokens.OP_BITWISE_NEG,
)

Comparator = packrat.OneOf(
  Tokens.CMP_EQ,
  Tokens.CMP_NEQ,
  Tokens.CMP_LT,
  Tokens.CMP_GT,
  Tokens.CMP_LE,
  Tokens.CMP_GE,
)

Term = packrat.OneOf(
  Interval,
  Expression,
  SimpleTerm,
  ScriptCall,
)

# Because this element is directly recursive it can't be defined as part of the
# initial definition of Term, so we have to hack it in like this:
Term.elements = tuple_with(
  Term.elements,
  packrat.Seq(
    Tokens.Ignore.PAREN_OPEN,
    Term,
    Tokens.Ignore.PAREN_CLOSE,
  )
)

Terms = packrat.SepList(Term, sep=Tokens.Ignore.COMMA)

Interval.grammar = packrat.Package(
  Interval,
  packrat.Seq(
    packrat.Attr("lower", SimpleTerm),
    Tokens.INTERVAL,
    packrat.Attr("upper", SimpleTerm),
  ),
)

SimpleTerm.grammar = packrat.Package(
  SimpleTerm,
  packrat.OneOf(
    packrat.Seq(
      packrat.Attr("id", Tokens.ID),
      packrat.Opt(
        packrat.Seq(
          Tokens.Ignore.PAREN_OPEN,
          packrat.Opt(
            packrat.Attr("terms", Terms),
          ),
          Tokens.Ignore.PAREN_CLOSE,
        )
      )
    ),
    packrat.Attr(
      "id",
      packrat.OneOf(
        Tokens.NUMBER,
        Tokens.STRING,
        Tokens.VARIABLE,
        Tokens.ANONYMOUS,
      )
    ),
  ),
)

Expression.grammar = packrat.Package(
  Expression,
  packrat.OneOf(
    packrat.Seq(
      packrat.Flag("negated", Tokens.OP_MINUS),
      packrat.OneOf(
        packrat.Seq(
          packrat.Seq(
            Tokens.Ignore.PAREN_OPEN,
            packrat.Attr(
              "lhs",
              Term,
            ),
            Tokens.Ignore.PAREN_CLOSE,
          ),
          packrat.Attr("op", ArithOp),
          packrat.Attr("rhs", Term)
        ),
        packrat.Seq(
          packrat.Attr("lhs", SimpleTerm),
          packrat.Attr("op", ArithOp),
          packrat.Attr("rhs", Term)
        ),
      )
    ),
    packrat.Seq(
      packrat.RequiredFlag("negated", Tokens.OP_MINUS),
      packrat.Attr("lhs", SimpleTerm),
    ),
  )
)

ScriptCall.grammar = packrat.Package(
  ScriptCall,
  packrat.Seq(
    Tokens.Ignore.AT,
    packrat.Attr("function", Tokens.ID),
    Tokens.Ignore.PAREN_OPEN,
    packrat.Opt(
      packrat.Attr("args", Terms),
    ),
    Tokens.Ignore.PAREN_CLOSE,
  )
)

ClassicalLiteral.grammar = packrat.Package(
  ClassicalLiteral,
  packrat.Seq(
    packrat.Flag("negated", Tokens.OP_MINUS),
    packrat.Attr("id", Tokens.ID),
    packrat.Opt(
      packrat.Seq(
        Tokens.Ignore.PAREN_OPEN,
        packrat.Opt(
          packrat.Attr("terms", Terms),
        ),
        Tokens.Ignore.PAREN_CLOSE,
      )
    )
  )
)

BuiltinAtom.grammar = packrat.Package(
  BuiltinAtom,
  packrat.Seq(
    packrat.Attr("lhs", Term),
    packrat.Attr("op", Comparator),
    packrat.Attr("rhs", Term),
  )
)

NafLiteral.grammar = packrat.Package(
  NafLiteral,
  packrat.Seq(
    packrat.Flag("negated", Tokens.NAF),
    packrat.Attr(
      "contents",
      packrat.OneOf(
        BuiltinAtom,
        ScriptCall,
        ClassicalLiteral,
      )
    )
  )
)

WeightAtLevel.grammar = packrat.Package(
  WeightAtLevel,
  packrat.Seq(
    packrat.Attr("weight", Term),
    packrat.Opt(
      packrat.Seq(
        Tokens.Ignore.AT,
        packrat.Attr("level", Term),
      )
    ),
    packrat.Opt(
      packrat.Seq(
        Tokens.Ignore.COMMA,
        packrat.Attr("terms", Terms)
      )
    )
  )
)

AggregateElement.grammar = packrat.Package(
  AggregateElement,
  packrat.Seq(
    packrat.Attr(
      "terms",
      packrat.SepList(packrat.OneOf(NafLiteral, Term), sep=Tokens.Ignore.COMMA)
    ),
    packrat.Opt(
      packrat.Seq(
        Tokens.Ignore.COLON,
        packrat.Attr(
          "constraints",
          packrat.SepList(NafLiteral, sep=Tokens.Ignore.COMMA)
        )
      )
    )
  )
)

Aggregate.grammar = packrat.Package(
  Aggregate,
  packrat.Seq(
    packrat.Flag("negated", Tokens.NAF),
    packrat.Opt(
      packrat.Seq(
        packrat.Attr("l", Term),
        packrat.Attr("lop", Comparator),
      )
    ),
    packrat.OneOf(
      packrat.Attr(
        "function",
        packrat.OneOf(
          Tokens.KW_AGGREGATE_COUNT,
          Tokens.KW_AGGREGATE_MAX,
          Tokens.KW_AGGREGATE_MIN,
          Tokens.KW_AGGREGATE_SUM,
        )
      ),
      packrat.Attr(
        "function",
        packrat.Omit(),
        value="#count"
      )
    ),
    Tokens.Ignore.CURLY_OPEN,
    packrat.Opt(
      packrat.Attr(
        "elements",
        packrat.SepList(AggregateElement, sep=Tokens.Ignore.SEMICOLON),
      )
    ),
    Tokens.Ignore.CURLY_CLOSE,
    packrat.Opt(
      packrat.Seq(
        packrat.Attr("uop", Comparator),
        packrat.Attr("u", Term),
      )
    ),
  )
)

ChoiceElement.grammar = packrat.Package(
  ChoiceElement,
  packrat.Seq(
    packrat.Attr(
      "literal",
      packrat.OneOf( ClassicalLiteral, ScriptCall )
    ),
    packrat.Opt(
      packrat.Seq(
        Tokens.Ignore.COLON,
        packrat.Attr(
          "constraints",
          packrat.SepList(NafLiteral, sep=Tokens.Ignore.COMMA)
        )
      )
    )
  )
)

Choice.grammar = packrat.Package(
  Choice,
  packrat.Seq(
    packrat.Opt(
      packrat.Seq(
        packrat.Attr("l", Term),
        packrat.Attr("lop", Comparator),
      )
    ),
    Tokens.Ignore.CURLY_OPEN,
    packrat.Opt(
      packrat.Attr(
        "elements",
        packrat.SepList(ChoiceElement, sep=Tokens.Ignore.SEMICOLON)
      )
    ),
    Tokens.Ignore.CURLY_CLOSE,
    packrat.Opt(
      packrat.Seq(
        packrat.Attr("uop", Comparator),
        packrat.Attr("u", Term),
      )
    ),
  )
)

Disjunction.grammar = packrat.Package(
  Disjunction,
  packrat.Attr(
    "elements",
    packrat.SepList(
      packrat.OneOf( ClassicalLiteral, ScriptCall ),
      sep=Tokens.Ignore.OR,
      require_multiple=True,
    )
  )
)

Head = packrat.OneOf(
  Disjunction,
  Choice,
  ClassicalLiteral,
  ScriptCall,
)

Body = packrat.SepList(
  packrat.OneOf(
    NafLiteral,
    Aggregate
  ),
  sep=Tokens.Ignore.COMMA
)

OptimizeElement.grammar = packrat.Package(
  OptimizeElement,
  packrat.Seq(
    packrat.Attr("weightlevel", WeightAtLevel),
    packrat.Opt(
      packrat.Seq(
        Tokens.Ignore.COLON,
        packrat.Attr(
          "literals",
          packrat.SepList(NafLiteral, sep=Tokens.Ignore.COMMA)
        )
      )
    )
  )
)

OptimizeFunction = packrat.OneOf( Tokens.KW_MAXIMIZE, Tokens.KW_MINIMIZE )

Optimization.grammar = packrat.Package(
  Optimization,
  packrat.Seq(
    packrat.Attr("function", OptimizeFunction),
    Tokens.Ignore.CURLY_OPEN,
    packrat.Attr(
      "elements",
      packrat.SepList(OptimizeElement, sep=Tokens.Ignore.SEMICOLON)
    ),
    Tokens.Ignore.CURLY_CLOSE,
    Tokens.Ignore.DOT,
  )
)

WeakConstraint.grammar = packrat.Package(
  WeakConstraint,
  packrat.Seq(
    Tokens.Ignore.WCONS,
    packrat.Opt(
      packrat.Attr("body", Body),
    ),
    Tokens.Ignore.DOT,
    Tokens.Ignore.SQUARE_OPEN,
    packrat.Attr("weightlevel", WeightAtLevel),
    Tokens.Ignore.SQUARE_CLOSE,
  )
)

Rule.grammar = packrat.Package(
  Rule,
  packrat.OneOf(
    packrat.Seq(
      Tokens.Ignore.CONS,
      packrat.Attr("body", Body),
      Tokens.Ignore.DOT
    ),
    packrat.Seq(
      packrat.Attr("head", Head),
      packrat.Opt(
        packrat.Seq(
          Tokens.Ignore.CONS,
          packrat.Attr("body", Body),
        )
      ),
      Tokens.Ignore.DOT
    ),
  )
)

Script.grammar = packrat.Package(
  Script,
  packrat.Seq(
    Tokens.Ignore.DIR_SCRIPT,
    Tokens.Ignore.PAREN_OPEN,
    packrat.Attr(
      "language",
      packrat.OneOf(
        Tokens.SCRIPT_TYPE_LUA,
        Tokens.SCRIPT_TYPE_PYTHON
      )
    ),
    Tokens.Ignore.PAREN_CLOSE,
    packrat.Attr("contents", Tokens.SCRIPT_BODY),
    Tokens.Ignore.DOT
  )
)

Directive.grammar = packrat.Package(
  Directive,
  packrat.Seq(
    packrat.Attr(
      "directive",
      packrat.OneOf(
        Tokens.DIR_HIDE,
        Tokens.DIR_SHOW,
        Tokens.DIR_CONST,
        Tokens.DIR_DOMAIN,
        Tokens.DIR_EXTERNAL,
      )
    ),
    packrat.Attr(
      "contents",
      Tokens.DIRECTIVE_BODY
    ),
    Tokens.Ignore.DOT
  ),
)

Statement = packrat.OneOf(
  Rule,
  WeakConstraint,
  Optimization,
  Directive,
  Script,
)

Query.grammar = packrat.Package(
  Query,
  packrat.Seq(
    packrat.Attr("literal", packrat.OneOf( ClassicalLiteral, ScriptCall )),
    Tokens.Ignore.QUERY_MARK
  )
)

Comment.grammar = None

Program.grammar = packrat.Package(
  Program,
  packrat.Seq(
    packrat.Attr("statements", packrat.Rep( Statement )),
    packrat.Opt( packrat.Attr("query", Query) ),
  )
)

# Parsing setup:

def devour_asp(text):
  """
  A devour function for ASP that eats whitespace and comments.
  """
  ate_something = True
  while ate_something:
    ate_something = False
    for r in (
      Tokens.BLANK.expression,
      Tokens.COMMENT.expression,
      Tokens.MULTI_LINE_COMMENT.expression,
    ):
      m = r.match(text)
      if m:
        text = text[len(m.group(0)):]
        ate_something = True
  return text

def parse_ans(text):
  """
  Parses the given text as an answer set, i.e., a sequence of predicate
  statements. Returns a (possibly empty) tuple of Predicate objects.
  """
  return packrat.parse_completely(
    text,
    packrat.Rep(PredicateStatement),
    devour=devour_asp
  )

def parse_ans_fast(text):
  """
  Parses the given text as an answer set quickly, assuming normal clingo output
  constraints.
  """
  qsplit = re.compile(r'("(?:[^\\"]|(?:\\.))*")')
  # First, split up the output into a list of predicate strings, being
  # careful of quotes:
  prstrings = [""]
  qregions = re.split(qsplit, text)
  for r in qregions:
    if re.fullmatch(qsplit, r):
      prstrings[-1] += r
    else:
      prparts = r.split(" ")
      for part in prparts[:-1]:
        prstrings[-1] += part
        prstrings.append("")
      prstrings[-1] += prparts[-1]
  # Now parse each predicate string individually:
  predicates = []
  for p in prstrings:
    predicates.append(packrat.parse_completely(p, Predicate, devour=devour_asp))
  return predicates

def parse_fans_fast(text):
  """
  Parses the given text as an answer set quickly, assuming formatted clingo
  output (i.e., facts suitable for clingo input, one per line with periods, but
  no rules or other non-predicate statements).
  """
  # Parse each line as a predicate individually:
  lines = text.split('\n')
  predicates = []
  for l in lines:
    if not l:
      continue
    if l[-1] != '.':
      raise packrat.ParseError("Line lacks trailing '.':\n{}".format(l))
    predicates.append(
      packrat.parse_completely(l[:-1], Predicate, devour=devour_asp)
    )
  return predicates

def parse_asp(text):
  """
  Parses the given text as an answer set program, i.e., a Program (see above).
  Returns a Program object.
  """
  return packrat.parse_completely(
    text,
    Program,
    devour=devour_asp
  )

def ruleset(*programs):
  """
  Takes zero or more Program objects and returns a set() containing all of the
  Statements from those programs (Queries are ignored). If no programs are
  given, an empty set is returned.
  """
  result = set()
  for p in programs:
    for s in p.statements:
      result.add(s)
  return result

def concatenate_programs(*progs):
  """
  Takes one or more Program objects and returns a single unified Program object
  that combines them. Raises a ValueError if there is more than one Query
  object between the programs given.
  """
  statements = []
  query = None
  for p in progs:
    statements.extend(p.statements)
    if p.query:
      if query == None:
        query = p.query
      else:
        raise ValueError(
          "Cannot create a merged program with more than one query."
        )
  return Program(tuple(statements), query)

def load_logic_files(files):
  """
  Loads all of the given files as Program objects and returns a ruleset
  distilled from all of them.
  """
  return ruleset(*process_file_contents(files, parse_asp))

def load_logic_dir(dir):
  """
  Loads all .lp files in the given directory (and its subdirectories) as
  Program objects and returns a ruleset distilled from all of them.
  """
  return ruleset(
    *process_dir_file_contents(
      dir,
      parse_asp,
      include=lambda f: f.endswith(".lp"),
    )
  )

# Testing:

def _test_parse_as_predicate(text):
  return packrat.parse(text, Predicate)

def _test_parse_as_predicate_statement(text):
  return packrat.parse(text, PredicateStatement)

def _test_parse_completely_as_term(text):
  return packrat.parse_completely(text, Term)

def _test_parse_completely_as_builtinatom(text):
  return packrat.parse_completely(text, BuiltinAtom)

def _test_parse_completely_as_nafliteral(text):
  return packrat.parse_completely(text, NafLiteral)

def _test_parse_completely_as_statement(text):
  return packrat.parse_completely(text, Statement)


def _test_restring_predicate(text):
  return str(packrat.parse_completely(text, Predicate))

def _test_restring_term(text):
  return str(packrat.parse_completely(text, Term))

def _test_restring_statement(text):
  return str(packrat.parse_completely(text, Statement))

def _test_restring_program(text):
  return str(packrat.parse_completely(text, Program))


def _test_bad_fact(text):
  try:
    packrat.parse_completely(text, Predicate)
  except packrat.ParseError:
    return True
  return False

_test_cases = [
  (
    _test_parse_as_predicate,
    "test",
    (Predicate("test"), '')
  ),
  (
    _test_parse_as_predicate,
    "two_part",
    (Predicate("two_part"), '')
  ),
  (
    _test_parse_completely_as_term,
    "Capitalized",
    SimpleTerm("Capitalized")
  ),
  (
    _test_parse_as_predicate,
    "with_period.",
    (Predicate("with_period"), '.')
  ),
  (
    _test_parse_as_predicate_statement,
    "with_period.",
    (Predicate("with_period"), '')
  ),
  (
    _test_parse_as_predicate,
    "_",
    (Predicate("_"), '')
  ),
  (
    _test_parse_as_predicate,
    "-15",
    (Predicate(-15), '')
  ),
  (
    lambda x: x, # test predicate equality
    Pr(
      "p",
      Pr(
        "p",
        Pr(2)
      ),
      Pr("v",
        Pr(3),
        Pr(4),
        Pr("s")
      ),
      Pr("z")
    ),
    Pr(
      "p",
      Pr(
        "p",
        Pr(2)
      ),
      Pr("v",
        Pr(3),
        Pr(4),
        Pr("s")
      ),
      Pr("z")
    ),
  ),
  (
    _test_parse_as_predicate,
    "p(p(2), v(3, 4, s), z)",
    (
      Pr(
        "p",
        Pr(
          "p",
          Pr(2)
        ),
        Pr("v",
          Pr(3),
          Pr(4),
          Pr("s")
        ),
        Pr("z")
      ),
      ''
    )
  ),
  (
    _test_restring_predicate,
    "p(p(2), v(3, 4, s), z)",
    "p(p(2), v(3, 4, s), z)",
  ),
  (
    _test_parse_as_predicate,
    '"quoted"',
    (Predicate('"quoted"'), '')
  ),
  (
    _test_parse_as_predicate,
    '"negative(-3).bar"',
    (Predicate('"negative(-3).bar"'), '')
  ),
  (
    _test_parse_as_predicate,
    'negative(-3)',
    (Predicate("negative", Predicate(-3)), '')
  ),
  (
    _test_parse_as_predicate,
    '"qp"(test, "qp2")',
    (
      Pr(
        '"qp"',
        Pr("test"),
        Pr('"qp2"')
      ),
      ''
    )
  ),
  (
    _test_parse_as_predicate,
    'slot(n("P2.AgitatedInsult","S1"),to,empty).',
    (
      Pr(
        "slot",
        Pr(
          "n",
          Pr('"P2.AgitatedInsult"'),
          Pr('"S1"'),
        ),
        Pr("to"),
        Pr("empty"),
      ),
      '.'
    )
  ),
  (
    _test_parse_as_predicate_statement,
    'slot(n("P2.AgitatedInsult","S1"),to,empty).',
    (
      Pr(
        "slot",
        Pr(
          "n",
          Pr('"P2.AgitatedInsult"'),
          Pr('"S1"'),
        ),
        Pr("to"),
        Pr("empty"),
      ),
      ''
    )
  ),
  (_test_bad_fact, "3(v)", True),
  (_test_bad_fact, "_(1)", True),
  (
    _test_parse_as_predicate,
    'p(p(2), v(3, 4, s), z, "myeh myeh \\"jyeh, )")',
    (
      Pr(
        "p",
        Pr(
          "p",
          Pr(2)
        ),
        Pr("v",
          Pr(3),
          Pr(4),
          Pr("s")
        ),
        Pr("z"),
        Pr('"myeh myeh \\"jyeh, )"')
      ),
      ''
    )
  ),
  (
    str,
    Pr(
      "p",
      Pr(
        "p",
        Pr(2)
      ),
      Pr("v",
        Pr(3),
        Pr(4),
        Pr("s")
      ),
      Pr("z"),
      Pr('"myeh myeh \\"jyeh, )"')
    ),
    'p(p(2), v(3, 4, s), z, "myeh myeh \\"jyeh, )")',
  ),
  (
    _test_parse_as_predicate,
    "value(5,6,9,tr(2,-1,tr(6,1,tr(1,1,tr(3,-1,tr(3,1,none))))))).",
    (
      Pr(
        "value",
        Pr(5),
        Pr(6),
        Pr(9),
        Pr(
          "tr",
          Pr(2),
          Pr(-1),
          Pr(
            "tr",
            Pr(6),
            Pr(1),
            Pr(
              "tr",
              Pr(1),
              Pr(1),
              Pr(
                "tr",
                Pr(3),
                Pr(-1),
                Pr(
                  "tr",
                  Pr(3),
                  Pr(1),
                  Pr("none")
                )
              )
            )
          )
        )
      ),
      ').'
    )
  ),
  (
    str,
    Pr(
      "value",
      Pr(5),
      Pr(6),
      Pr(9),
      Pr(
        "tr",
        Pr(2),
        Pr(-1),
        Pr(
          "tr",
          Pr(6),
          Pr(1),
          Pr(
            "tr",
            Pr(1),
            Pr(1),
            Pr(
              "tr",
              Pr(3),
              Pr(-1),
              Pr(
                "tr",
                Pr(3),
                Pr(1),
                Pr("none")
              )
            )
          )
        )
      )
    ),
    "value(5, 6, 9, tr(2, -1, tr(6, 1, tr(1, 1, tr(3, -1, tr(3, 1, none))))))",
  ),
  (
    build_schema,
    Pr(
      "foo",
      Pr("Bar"),
      Pr(
        "Baz",
        Pr(3),
        Pr("hoho"),
        Pr("Jig")
      )
    ),
    Pr(
      "foo",
      Vr("Bar"),
      Vr(
        "Baz",
        Pr(3),
        Pr("hoho"),
        Vr("Jig")
      )
    )
  ),
  (
    bind,
    (
      Pr(
        "foo",
        Vr("Bar"),
        Vr(
          "Baz",
          Pr(3),
          Pr("hoho"),
          Vr("Jig")
        )
      ),
      Pr(
        "foo",
        Pr("gah"),
        Pr(
          "ehhh",
          Pr(3),
          Pr("hoho"),
          Pr("lee")
        )
      )
    ),
    {
      "foo.Bar": Pr("gah"),
      "foo.Baz": Pr(
        "ehhh",
        Pr(3),
        Pr("hoho"),
        Pr("lee")
      ),
      "foo.Baz.Jig": Pr("lee")
    }
  ),
  (
    bind,
    (
      Pr(
        "foo",
        Vr("X"),
        Vr("X"),
      ),
      Pr(
        "foo",
        Pr("bar"),
        Pr("bar"),
      ),
    ),
    {
      "foo.X": Pr("bar")
    }
  ),
  (
    bind,
    (
      Pr(
        "foo",
        Vr("X"),
        Vr("X"),
      ),
      Pr(
        "foo",
        Pr("bar"),
        Pr("baz"),
      ),
    ),
    {
      "foo.X": Pr("baz")
    }
  ),
  # TODO: add more tests for binding with pattern variables and subtrees.
  (
    _test_parse_completely_as_term,
    "foo",
    SimpleTerm("foo"),
  ),
  (
    _test_parse_completely_as_term,
    "foo(bar, 5)",
    SimpleTerm(
      "foo",
      (
        SimpleTerm("bar"),
        SimpleTerm("5")
      )
    ),
  ),
  (
    _test_parse_completely_as_term,
    "foo + 5",
    Expression(
      False,
      "+",
      SimpleTerm("foo"),
      SimpleTerm("5")
    )
  ),
  (
    _test_parse_completely_as_term,
    "foo * 5 - 3",
    Expression(
      False,
      "*",
      SimpleTerm("foo"),
      Expression(
        False,
        "-",
        SimpleTerm("5"),
        SimpleTerm("3")
      )
    )
  ),
  (
    _test_parse_completely_as_term,
    "baz(X, X+1)",
    SimpleTerm(
      "baz",
      (
        SimpleTerm("X"),
        Expression(
          False,
          "+",
          SimpleTerm("X"),
          SimpleTerm("1"),
        )
      )
    ),
  ),
  (
    _test_parse_completely_as_term,
    "bar(Var)",
    SimpleTerm( "bar", ( SimpleTerm("Var"), )),
  ),
  (
    _test_parse_completely_as_term,
    "foo(bar(Var), baz(X, X+1))",
    SimpleTerm(
      "foo",
      (
        SimpleTerm( "bar", ( SimpleTerm("Var"), )),
        SimpleTerm(
          "baz",
          (
            SimpleTerm("X"),
            Expression(
              False,
              "+",
              SimpleTerm("X"),
              SimpleTerm("1"),
            )
          )
        ),
      )
    ),
  ),
  (
    _test_parse_completely_as_term,
    "foo(bar(Var), baz(X, X+1)) / bar(Zed)",
    Expression(
      False,
      "/",
      SimpleTerm(
        "foo",
        (
          SimpleTerm( "bar", ( SimpleTerm("Var"), )),
          SimpleTerm(
            "baz",
            (
              SimpleTerm("X"),
              Expression(
                False,
                "+",
                SimpleTerm("X"),
                SimpleTerm("1"),
              )
            )
          ),
        )
      ),
      SimpleTerm( "bar", ( SimpleTerm("Zed"), ))
    ),
  ),
  (
    _test_parse_completely_as_term,
    "-(x + 3) / 5 - 4", # Note awful operator binding x2
    Expression(
      True,
      "/",
      Expression(
        False,
        "+",
        SimpleTerm("x"),
        SimpleTerm("3"),
      ),
      Expression(
        False,
        "-",
        SimpleTerm("5"),
        SimpleTerm("4"),
      )
    ),
  ),
  (
    _test_parse_completely_as_term,
    "X * Y - -Z", # Note again bad operator binding
    Expression(
      False,
      "*",
      SimpleTerm("X"),
      Expression(
        False,
        "-",
        SimpleTerm("Y"),
        Expression(
          True,
          None,
          SimpleTerm("Z")
        )
      )
    )
  ),
  (
    _test_restring_term,
    "X * Y - -Z",
    "(X * (Y - -(Z)))"
  ),
  (
    _test_restring_term,
    "-(x + 3) / 5 - 4 * 3 - 1",
    "-((x + 3) / (5 - (4 * (3 - 1))))"
  ),
  (
    _test_restring_term,
    "foo(bar, baz(Zed))",
    "foo(bar, baz(Zed))",
  ),
  (
    _test_parse_completely_as_statement,
    "foo(bar, baz).",
    Rule(
      ClassicalLiteral(
        False,
        "foo",
        (
          SimpleTerm("bar"),
          SimpleTerm("baz"),
        )
      ),
      None
    ),
  ),
  (
    _test_parse_completely_as_statement,
    "foo(bar, baz) :- a, not b.",
    Rule(
      ClassicalLiteral(
        False,
        "foo",
        (
          SimpleTerm("bar"),
          SimpleTerm("baz"),
        )
      ),
      (
        NafLiteral(
          False,
          ClassicalLiteral(
            False,
            "a"
          )
        ),
        NafLiteral(
          True,
          ClassicalLiteral(
            False,
            "b"
          )
        )
      )
    ),
  ),
  (
    packrat._test_parse(ClassicalLiteral),
    "-xyzzy", 
    ClassicalLiteral(
      True,
      "xyzzy"
    ),
  ),
  (
    packrat._test_parse(Disjunction, leftovers=''),
    "foo(bar, baz) | -xyzzy", 
    Disjunction(
      (
        ClassicalLiteral(
          False,
          "foo",
          (
            SimpleTerm("bar"),
            SimpleTerm("baz"),
          )
        ),
        ClassicalLiteral(
          True,
          "xyzzy"
        ),
      )
    ),
  ),
  (
    _test_parse_completely_as_statement,
    "foo(bar, baz) | -xyzzy :- a, not b.",
    Rule(
      Disjunction(
        (
          ClassicalLiteral(
            False,
            "foo",
            (
              SimpleTerm("bar"),
              SimpleTerm("baz"),
            )
          ),
          ClassicalLiteral(
            True,
            "xyzzy"
          ),
        )
      ),
      (
        NafLiteral(
          False,
          ClassicalLiteral(
            False,
            "a"
          )
        ),
        NafLiteral(
          True,
          ClassicalLiteral(
            False,
            "b"
          )
        )
      )
    ),
  ),
  (
    packrat._test_parse(Choice),
    "1 <= { x(T) : not T < 3 ; y(T) }",
    Choice(
      SimpleTerm("1"),
      "<=",
      (
        ChoiceElement(
          ClassicalLiteral(
            False,
            "x",
            ( SimpleTerm("T"), )
          ),
          (
            NafLiteral(
              True,
              BuiltinAtom(
                "<",
                SimpleTerm("T"),
                SimpleTerm("3")
              )
            ),
          )
        ),
        ChoiceElement(
          ClassicalLiteral(
            False,
            "y",
            ( SimpleTerm("T"), )
          )
        )
      ),
    )
  ),
  (
    _test_parse_completely_as_statement,
    """\
1 <= { x(T) : not T < 3 ; y(T) } :-
  -3 < #count {
    -X, Y+5, foobar(X) : X = 3;
    other;
    a, b : c, not d
  } < 7,
  other.""",
    Rule(
      Choice(
        SimpleTerm("1"),
        "<=",
        (
          ChoiceElement(
            ClassicalLiteral(
              False,
              "x",
              ( SimpleTerm("T"),)
            ),
            (
              NafLiteral(
                True,
                BuiltinAtom(
                  "<",
                  SimpleTerm("T"),
                  SimpleTerm("3")
                )
              ),
            )
          ),
          ChoiceElement(
            ClassicalLiteral(
              False,
              "y",
              ( SimpleTerm("T"),)
            )
          )
        ),
      ),
      ( # rule-body
        Aggregate(
          False,
          Expression(
            True,
            None,
            SimpleTerm("3")
          ),
          "<",
          "#count",
          (
            AggregateElement(
              (
                Expression(True, None, SimpleTerm("X")),
                Expression(False, "+", SimpleTerm("Y"), SimpleTerm("5")),
                NafLiteral(
                  False,
                  ClassicalLiteral(
                    False,
                    "foobar",
                    ( SimpleTerm("X"), )
                  )
                ),
              ),
              (
                NafLiteral(
                  False,
                  BuiltinAtom(
                    "=",
                    SimpleTerm("X"),
                    SimpleTerm("3")
                  )
                ),
              )
            ),
            AggregateElement(
              ( NafLiteral(False, ClassicalLiteral(False, "other")), )
            ),
            AggregateElement(
              (
                NafLiteral(False, ClassicalLiteral(False, "a")),
                NafLiteral(False, ClassicalLiteral(False, "b")),
              ),
              (
                NafLiteral(False, ClassicalLiteral(False, "c")),
                NafLiteral(True, ClassicalLiteral(False, "d")),
              )
            ),
          ),
          "<",
          SimpleTerm("7"),
        ),
        NafLiteral(False, ClassicalLiteral(False, "other"))
      )   
    ),
  ),
  (
    _test_restring_statement,
    "foo(bar, baz).",
    "foo(bar, baz).",
  ),
  (
    _test_restring_statement,
    "foo(bar, baz) | -xyzzy :- a, not b.",
    "foo(bar, baz) | -xyzzy :- a, not b.",
  ),
  (
    _test_restring_statement,
    """\
1 <= { x(T) : not T < 3 ; y(T) } :-
  -3 < #count {
    -X, Y+5, foobar(X) : X = 3;
    other;
    a, b : c, not d
  } < 7,
  other.""",
    "1 <= { x(T) : not T < 3; y(T) } :- -(3) < #count { -(X), (Y + 5), "\
    "foobar(X) : X = 3; other; a, b : c, not d } < 7, other.",
  ),
  (
    parse_asp,
    """\
a.
b.
q :- a, b.
    """,
    Program(
      (
        Rule( ClassicalLiteral(False, "a") ),
        Rule( ClassicalLiteral(False, "b") ),
        Rule(
          ClassicalLiteral(False, "q"),
          (
            NafLiteral(False, ClassicalLiteral(False, "a")),
            NafLiteral(False, ClassicalLiteral(False, "b")),
          )
        )
      )
    ),
  ),
  (
    parse_asp,
    """\
foo(3, 4).
bar(X, Y+1) :- foo(X, Y), not bar(X, Y-1).
bar(3, 5)?
    """,
    Program(
      (
        Rule(
          ClassicalLiteral(
            False,
            "foo",
            ( SimpleTerm("3"), SimpleTerm("4") )
          )
        ),
        Rule(
          ClassicalLiteral(
            False,
            "bar",
            (
              SimpleTerm("X"),
              Expression(
                False,
                "+",
                SimpleTerm("Y"),
                SimpleTerm("1")
              )
            )
          ),
          (
            NafLiteral(
              False,
              ClassicalLiteral(
                False,
                "foo",
                 ( SimpleTerm("X"), SimpleTerm("Y") )
              )
            ),
            NafLiteral(
              True,
              ClassicalLiteral(
                False,
                "bar",
                (
                  SimpleTerm("X"),
                  Expression(
                    False,
                    "-",
                    SimpleTerm("Y"),
                    SimpleTerm("1")
                  )
                )
              )
            )
          )
        )
      ),
      Query(
        ClassicalLiteral(
          False,
          "bar",
          (
            SimpleTerm("3"),
            SimpleTerm("5"),
          )
        )
      )
    ),
  ),
  (
    parse_asp,
    """\
a. %comment b.
    """,
    Program(
      (
        Rule(
          ClassicalLiteral(
            False,
            "a"
          ),
        ),
      ),
    ),
  ),
  (
    parse_asp,
    """\
% comment
a. %comment b.
    """,
    Program(
      (
        Rule(
          ClassicalLiteral(
            False,
            "a"
          ),
        ),
      ),
    ),
  ),
  (
    packrat._test_parse(Interval),
    "1..X",
    Interval(
      SimpleTerm("1"),
      SimpleTerm("X")
    )
  ),
  (
    parse_asp,
    """\
time(1..1000).
    """,
    Program(
      (
        Rule(
          ClassicalLiteral(
            False,
            "time",
            (
              Interval(
                SimpleTerm("1"),
                SimpleTerm("1000")
              ),
            )
          ),
        ),
      ),
    ),
  ),
  (
    parse_asp,
    """\
% comment
bar(X, Y+1) %* interrupt *%:-
  foo(X, Y),
  not bar(X, Y-1).
    """,
    Program(
      (
        Rule(
          ClassicalLiteral(
            False,
            "bar",
            (
              SimpleTerm("X"),
              Expression(
                False,
                "+",
                SimpleTerm("Y"),
                SimpleTerm("1")
              )
            )
          ),
          (
            NafLiteral(
              False,
              ClassicalLiteral(
                False,
                "foo",
                ( SimpleTerm("X"), SimpleTerm("Y") )
              )
            ),
            NafLiteral(
              True,
              ClassicalLiteral(
                False,
                "bar",
                (
                  SimpleTerm("X"),
                  Expression(
                    False,
                    "-",
                    SimpleTerm("Y"),
                    SimpleTerm("1")
                  )
                )
              )
            )
          )
        ),
      ),
    ),
  ),
  (
    parse_asp,
    """\
% comment
bar(X, Y+1) %* interrupt *%:-
  foo(X, Y),
  not bar(X, Y-1).
bar(
  3, % annoying
  5
)?
    """,
    Program(
      (
        Rule(
          ClassicalLiteral(
            False,
            "bar",
            (
              SimpleTerm("X"),
              Expression(
                False,
                "+",
                SimpleTerm("Y"),
                SimpleTerm("1")
              )
            )
          ),
          (
            NafLiteral(
              False,
              ClassicalLiteral(
                False,
                "foo",
                ( SimpleTerm("X"), SimpleTerm("Y") )
              )
            ),
            NafLiteral(
              True,
              ClassicalLiteral(
                False,
                "bar",
                (
                  SimpleTerm("X"),
                  Expression(
                    False,
                    "-",
                    SimpleTerm("Y"),
                    SimpleTerm("1")
                  )
                )
              )
            )
          )
        ),
      ),
      Query(
        ClassicalLiteral(
          False,
          "bar",
          (
            SimpleTerm("3"),
            SimpleTerm("5"),
          )
        )
      )
    ),
  ),
  (
    parse_asp,
    """\
foo(3, 4).
% comment
bar(X, Y+1) %* interrupt *%:- foo(X, Y), %* multi-
line
comment
*% not bar(X, Y-1).
bar(
  3, % annoying
  5
)?
    """,
    Program(
      (
        Rule(
          ClassicalLiteral(
            False,
            "foo",
            ( SimpleTerm("3"), SimpleTerm("4") )
          )
        ),
        Rule(
          ClassicalLiteral(
            False,
            "bar",
            (
              SimpleTerm("X"),
              Expression(
                False,
                "+",
                SimpleTerm("Y"),
                SimpleTerm("1")
              )
            )
          ),
          (
            NafLiteral(
              False,
              ClassicalLiteral(
                False,
                "foo",
                ( SimpleTerm("X"), SimpleTerm("Y") )
              )
            ),
            NafLiteral(
              True,
              ClassicalLiteral(
                False,
                "bar",
                (
                  SimpleTerm("X"),
                  Expression(
                    False,
                    "-",
                    SimpleTerm("Y"),
                    SimpleTerm("1")
                  )
                )
              )
            )
          )
        )
      ),
      Query(
        ClassicalLiteral(
          False,
          "bar",
          (
            SimpleTerm("3"),
            SimpleTerm("5"),
          )
        )
      )
    ),
  ),
  (
    _test_restring_program,
    """\
a.
b.
q :- a, b.
    """,
    """\
a.
b.
q :- a, b.\
""",
  ),
  (
    _test_restring_program,
    """\
foo(3, 4).
bar(X, Y+1) :- foo(X, Y), not bar(X, Y-1).
bar(3, 5)?
    """,
    """\
foo(3, 4).
bar(X, (Y + 1)) :- foo(X, Y), not bar(X, (Y - 1)).
bar(3, 5)?""",
  ),
  (
    _test_restring_program,
    "#minimize { 1@0, test(Foo) : test(Foo) }.",
    "#minimize { 1@0, test(Foo) : test(Foo) }.",
  ),
  (
    _test_parse_completely_as_term,
    "at(Now,outcome(option(Opt),o(success,victory)))",
    SimpleTerm(
      "at",
      (
        SimpleTerm("Now"),
        SimpleTerm(
          "outcome",
          (
            SimpleTerm("option", ( SimpleTerm("Opt"), )),
            SimpleTerm(
              "o",
              (
                SimpleTerm("success"),
                SimpleTerm("victory"),
              )
            ),
          )
        ),
      )
   ),
  ),
  (
    _test_parse_as_predicate,
    "@call(function)",
    (
      Pr("@call", Pr("function")),
      ''
    )
  ),
  (
    packrat._test_parse(ScriptCall, leftovers=''),
    "@call(function)",
    ScriptCall("call", ( SimpleTerm("function"), )),
  ),
  (
    _test_restring_program,
    "@call(function).",
    "@call(function).",
  ),
  (
    _test_restring_program,
    """\
#script (python)
#end.
    """,
    "#script (python)\n#end.",
  ),
  (
    packrat._test_parse(
      Script,
      leftovers='\n    '
    ),
    """\
#script (python)
def foo(x):
  return x
#end.
    """,
    Script("python", "def foo(x):\n  return x\n#end")
  ),
  (
    _test_restring_program,
    """\
test(X).
#script (python)
def join(x, y):
  return "{}{}".format(x, y)
#end.
a(@join(foo, bar)).
    """,
    """\
test(X).
#script (python)
def join(x, y):
  return "{}{}".format(x, y)
#end.
a(@join(foo, bar)).""",
  ),
  (
    packrat._test_parse(Choice, leftovers=''),
    "1 = { l_selected(P) : provocation(P) } = 1",
    Choice(
      SimpleTerm("1"),
      "=",
      (
        ChoiceElement(
          ClassicalLiteral(
            False,
            "l_selected",
            ( SimpleTerm("P"),)
          ),
          (
            NafLiteral(
              False,
              ClassicalLiteral(
                False,
                "provocation",
                ( SimpleTerm("P"), )
              )
            ),
          ),
        ),
      ),
      "=",
      SimpleTerm("1")
    ),
  ),
  (
    parse_asp,
    "1 = { l_selected(P) : provocation(P) } = 1.",
    Program(
      (
        Rule(
          Choice(
            SimpleTerm("1"),
            "=",
            (
              ChoiceElement(
                ClassicalLiteral(
                  False,
                  "l_selected",
                  ( SimpleTerm("P"),)
                ),
                (
                  NafLiteral(
                    False,
                    ClassicalLiteral(
                      False,
                      "provocation",
                      ( SimpleTerm("P"), )
                    )
                  ),
                ),
              ),
            ),
            "=",
            SimpleTerm("1")
          ),
        ),
      )
    )
  ),
  (
    parse_asp,
    "next_chr_id(1) :- { character(_) } = 0.",
    Program(
      (
        Rule(
          ClassicalLiteral(
            False,
            "next_chr_id",
            ( SimpleTerm("1"),)
          ),
          (
            Aggregate(
              False,
              None,
              None,
              "#count",
              (
                AggregateElement(
                  (
                    NafLiteral(
                      False,
                      ClassicalLiteral(
                        False,
                        "character",
                        ( SimpleTerm("_"), )
                      )
                    ),
                  ),
                ),
              ),
              "=",
              SimpleTerm("0")
            ),
          )
        ),
      )
    )
  ),
  (
    parse_asp,
    """\
1 = {
  bound(Ref, id(Type, ID)) :
    proposed(id(Type, ID)),
    not story(id(Type, ID))
} :-
  edit(new, Type, Ref).
    """,
    Program(
      (
        Rule(
          Choice(
            SimpleTerm('1', None),
            '=',
            (
              ChoiceElement(
                ClassicalLiteral(
                  False,
                  'bound',
                  (
                    SimpleTerm('Ref', None),
                    SimpleTerm(
                      'id',
                      (
                        SimpleTerm('Type', None),
                        SimpleTerm('ID', None)
                      )
                    )
                  )
                ),
                (
                  NafLiteral(
                    False,
                    ClassicalLiteral(
                      False,
                      'proposed',
                      (
                        SimpleTerm(
                          'id',
                          (
                            SimpleTerm('Type', None),
                            SimpleTerm('ID', None)
                          )
                        ),
                      )
                    )
                  ),
                  NafLiteral(
                    True,
                    ClassicalLiteral(
                      False,
                      'story',
                      (
                        SimpleTerm(
                          'id',
                          (
                            SimpleTerm('Type', None),
                            SimpleTerm('ID', None)
                          )
                        ),
                      )
                    )
                  )
                )
              ),
            ),
            None,
            None
          ),
          (
            NafLiteral(
              False,
              ClassicalLiteral(
                False,
                'edit',
                (
                  SimpleTerm('new', None),
                  SimpleTerm('Type', None),
                  SimpleTerm('Ref', None)
                )
              )
            ),
          )
        ),
      ),
      None
    )
  ),
  (
    parse_asp,
    """\
:- 1 < { current_ending(T) : time(T) }.
    """,
    Program(
      (
        Rule(
          None,
          (
            Aggregate(
              False,
              SimpleTerm('1', None),
              '<',
              '#count',
              (
                AggregateElement(
                  (
                    NafLiteral(
                      False,
                      ClassicalLiteral(
                        False,
                        "current_ending",
                        ( SimpleTerm("T"), )
                      )
                    ),
                  ),
                  (
                    NafLiteral(
                      False,
                      ClassicalLiteral(
                        False,
                        'time',
                        (
                          SimpleTerm('T', None),
                        )
                      )
                    ),
                  )
                ),
              ),
              None,
              None
            ),
          )
        ),
      ),
      None
    )
  ),
  (
    parse_asp,
    """\
error(m("Unordered event.", ID)) :-
  story(Story, id(evt, ID)),
  0 = { story(Story, happens(T, id(evt, ID))) : time(T) }.
    """,
    Program(
      (
        Rule(
          ClassicalLiteral(
            False,
            'error',
            (
              SimpleTerm(
                'm',
                (
                  SimpleTerm('"Unordered event."', None),
                  SimpleTerm('ID', None)
                )
              ),
            )
          ),
          (
            NafLiteral(
              False,
              ClassicalLiteral(
                False,
                'story',
                (
                  SimpleTerm('Story', None),
                  SimpleTerm(
                    'id',
                    (
                      SimpleTerm('evt', None),
                      SimpleTerm('ID', None)
                    )
                  )
                )
              )
            ),
            Aggregate(
              False,
              SimpleTerm('0', None),
              '=',
              '#count',
              (
                AggregateElement(
                  (
                    NafLiteral(
                      False,
                      ClassicalLiteral(
                        False,
                        "story",
                        (
                          SimpleTerm('Story', None),
                          SimpleTerm(
                            'happens',
                            (
                              SimpleTerm('T', None),
                              SimpleTerm(
                                'id',
                                (
                                  SimpleTerm('evt', None),
                                  SimpleTerm('ID', None)
                                )
                              )
                            )
                          )
                        )
                      )
                    ),
                  ),
                  (
                    NafLiteral(
                      False,
                      ClassicalLiteral(
                        False,
                        'time',
                        (
                          SimpleTerm('T', None),
                        )
                      )
                    ),
                  )
                ),
              ),
              None,
              None
            )
          )
        ),
      ),
      None
    )
  ),
  (
    parse_asp,
    """\
caused_by(changed(T, status(Subj, Status)), Act) :-
  event(T, Act),
  outcome(T, Outcome),
  causes(T, Act, Outcome, status(Arg, NewStatus)),
  argument(T, Arg, Subj),
  at(T, status(Subj, Status)),
  1 <= { NewStatus = _not(Status); Status = _not(NewStatus) }.
    """,
    Program((Rule(ClassicalLiteral(False, 'caused_by', (SimpleTerm('changed', (SimpleTerm('T', None), SimpleTerm('status', (SimpleTerm('Subj', None), SimpleTerm('Status', None))))), SimpleTerm('Act', None))), (NafLiteral(False, ClassicalLiteral(False, 'event', (SimpleTerm('T', None), SimpleTerm('Act', None)))), NafLiteral(False, ClassicalLiteral(False, 'outcome', (SimpleTerm('T', None), SimpleTerm('Outcome', None)))), NafLiteral(False, ClassicalLiteral(False, 'causes', (SimpleTerm('T', None), SimpleTerm('Act', None), SimpleTerm('Outcome', None), SimpleTerm('status', (SimpleTerm('Arg', None), SimpleTerm('NewStatus', None)))))), NafLiteral(False, ClassicalLiteral(False, 'argument', (SimpleTerm('T', None), SimpleTerm('Arg', None), SimpleTerm('Subj', None)))), NafLiteral(False, ClassicalLiteral(False, 'at', (SimpleTerm('T', None), SimpleTerm('status', (SimpleTerm('Subj', None), SimpleTerm('Status', None)))))), Aggregate(False, SimpleTerm('1', None), '<=', '#count', (AggregateElement((NafLiteral(False, BuiltinAtom('=', SimpleTerm('NewStatus', None), SimpleTerm('_not', (SimpleTerm('Status', None),)))),), None), AggregateElement((NafLiteral(False, BuiltinAtom('=', SimpleTerm('Status', None), SimpleTerm('_not', (SimpleTerm('NewStatus', None),)))),), None)), None, None))),), None)
  ),
  (
    parse_asp,
    """\
1 = {
  error(m("Unable to assign relation.", T, id(T1, ID), id(T2, To), Rel));
  at(T, rel(id(T1, ID), id(T2, To), Rel, Value)) : value(Rel, Value)
} :-
  id(T1, ID),
  id(T2, To),
  relation(T1, T2, Rel),
  time(T),
  1 <= { id(T1, ID) != id(T2, To); not nonreflexive(T1, T2, Rel) }.
    """,
    Program((Rule(Choice(SimpleTerm('1', None), '=', (ChoiceElement(ClassicalLiteral(False, 'error', (SimpleTerm('m', (SimpleTerm('"Unable to assign relation."', None), SimpleTerm('T', None), SimpleTerm('id', (SimpleTerm('T1', None), SimpleTerm('ID', None))), SimpleTerm('id', (SimpleTerm('T2', None), SimpleTerm('To', None))), SimpleTerm('Rel', None))),)), None), ChoiceElement(ClassicalLiteral(False, 'at', (SimpleTerm('T', None), SimpleTerm('rel', (SimpleTerm('id', (SimpleTerm('T1', None), SimpleTerm('ID', None))), SimpleTerm('id', (SimpleTerm('T2', None), SimpleTerm('To', None))), SimpleTerm('Rel', None), SimpleTerm('Value', None))))), (NafLiteral(False, ClassicalLiteral(False, 'value', (SimpleTerm('Rel', None), SimpleTerm('Value', None)))),))), None, None), (NafLiteral(False, ClassicalLiteral(False, 'id', (SimpleTerm('T1', None), SimpleTerm('ID', None)))), NafLiteral(False, ClassicalLiteral(False, 'id', (SimpleTerm('T2', None), SimpleTerm('To', None)))), NafLiteral(False, ClassicalLiteral(False, 'relation', (SimpleTerm('T1', None), SimpleTerm('T2', None), SimpleTerm('Rel', None)))), NafLiteral(False, ClassicalLiteral(False, 'time', (SimpleTerm('T', None),))), Aggregate(False, SimpleTerm('1', None), '<=', '#count', (AggregateElement((NafLiteral(False, BuiltinAtom('!=', SimpleTerm('id', (SimpleTerm('T1', None), SimpleTerm('ID', None))), SimpleTerm('id', (SimpleTerm('T2', None), SimpleTerm('To', None))))),), None), AggregateElement((NafLiteral(True, ClassicalLiteral(False, 'nonreflexive', (SimpleTerm('T1', None), SimpleTerm('T2', None), SimpleTerm('Rel', None)))),), None)), None, None))),), None)
  ),
  (
    _test_parse_completely_as_builtinatom,
    "id(T1, ID) < id(T2, To)",
    BuiltinAtom(
      '<',
      SimpleTerm(
        'id',
        (
          SimpleTerm('T1', None),
          SimpleTerm('ID', None)
        )
      ),
      SimpleTerm(
        'id',
        (
          SimpleTerm('T2', None),
          SimpleTerm('To', None)
        )
      )
    )
  ),
  (
    _test_parse_completely_as_nafliteral,
    "id(T1, ID) < id(T2, To)",
    NafLiteral(
      False,
      BuiltinAtom(
        '<',
        SimpleTerm(
          'id',
          (
            SimpleTerm('T1', None),
            SimpleTerm('ID', None)
          )
        ),
        SimpleTerm(
          'id',
          (
            SimpleTerm('T2', None),
            SimpleTerm('To', None)
          )
        )
      )
    )
  ),
  (
    lambda x: packrat.parse_completely(x, packrat.SepList(SimpleTerm, sep=';')),
    "st(Now,relation(has_item,inst(actor,monster_57),inst(item,Item)));st(Now,relation(stolen_from,inst(actor,Victim),inst(item,Item)))",
    (
      SimpleTerm(
        'st',
        (
          SimpleTerm('Now', None),
          SimpleTerm(
            'relation',
            (
              SimpleTerm('has_item', None),
              SimpleTerm(
                'inst',
                (
                  SimpleTerm('actor', None),
                  SimpleTerm('monster_57', None)
                )
              ),
              SimpleTerm(
                'inst',
                (
                  SimpleTerm('item', None),
                  SimpleTerm('Item', None)
                )
              ),
            )
          ),
        )
      ),
      SimpleTerm(
        'st',
        (
          SimpleTerm('Now', None),
          SimpleTerm(
            'relation',
            (
              SimpleTerm('stolen_from', None),
              SimpleTerm(
                'inst',
                (
                  SimpleTerm('actor', None),
                  SimpleTerm('Victim', None)
                )
              ),
              SimpleTerm(
                'inst',
                (
                  SimpleTerm('item', None),
                  SimpleTerm('Item', None)
                )
              ),
            ),
          )
        )
      )
    )
  )
]

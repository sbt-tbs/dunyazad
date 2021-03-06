% attack
action(attack).

chaotic(attack).

% arguments

argument(attack, aggressor, actor).
argument(attack, target, actor).
initiator(attack, aggressor).
default_intent(attack, o(success, victory)).

% outcomes

outcome_val(attack, aggressor_state, unharmed).
outcome_val(attack, aggressor_state, injured).
outcome_val(attack, aggressor_state, killed).

outcome_val(attack, target_state, unharmed).
outcome_val(attack, target_state, injured).
outcome_val(attack, target_state, killed).

outcome_val(attack, get_loot, loot).
outcome_val(attack, get_loot, nothing).

outcome_val(attack, success, victory).
outcome_val(attack, success, defeat).
outcome_val(attack, success, tie).

outcome_excludes(
  attack,
  o(success, victory),
  o(aggressor_state, killed)
).
outcome_excludes(
  attack,
  o(success, defeat),
  o(target_state, killed)
).

outcome_excludes(attack, o(success, tie), o(aggressor_state, killed)).

outcome_excludes(attack, o(success, tie), o(get_loot, loot)).
outcome_excludes(attack, o(success, defeat), o(get_loot, loot)).

outcome_excludes(
  attack,
  o(success, tie),
  o(target_state, killed)
).

outcome_excludes(
  attack,
  o(aggressor_state, unharmed),
  o(target_state, unharmed)
).

outcome_excludes(
  attack,
  o(target_state, unharmed),
  o(aggressor_state, unharmed)
).

% skills:

skill_link(
  fighting, contest, tool,
  attack,
  between(aggressor, target),
  either(o(aggressor_state, unharmed), o(aggressor_state, injured))
).

skill_link(
  fighting, contest, tool,
  attack,
  between(aggressor, target),
  either(o(target_state, injured), o(target_state, unharmed))
).

skill_link(
  fighting, contest, tool,
  attack,
  between(aggressor, target),
  either(o(success, victory), o(success, defeat))
).

% attacking is one way to deal with a threat

at(
  N,
  consequence_of(
    X,
    o(success, victory),
    resolves,
    potential(problem, relation(threatening, Target, Someone))
  )
) :-
  at(N, action(X, attack)),
  at(N, arg(X, target, Target)),
  st(N, relation(threatening, Target, Someone)),
  story_op(N, build_options).

% no matter the outcome, an attack that winds up injuring a threat
% resolves the threat

at(
  N,
  consequence_of(
    X,
    o(aggressor_state, injured),
    resolves,
    potential(problem, relation(threatening, Aggressor, Someone))
  )
) :-
  at(N, action(X, attack)),
  at(N, arg(X, aggressor, Aggressor)),
  st(N, relation(threatening, Aggressor, Someone)),
  story_op(N, build_options).

at(
  N,
  consequence_of(
    X,
    o(aggressor_state, killed),
    resolves,
    potential(problem, relation(threatening, Aggressor, Someone))
  )
) :-
  at(N, action(X, attack)),
  at(N, arg(X, aggressor, Aggressor)),
  st(N, relation(threatening, Aggressor, Someone)),
  story_op(N, build_options).

at(
  N,
  consequence_of(
    X,
    o(target_state, injured),
    resolves,
    potential(problem, relation(threatening, Target, Someone))
  )
) :-
  at(N, action(X, attack)),
  at(N, arg(X, target, Target)),
  st(N, relation(threatening, Target, Someone)),
  story_op(N, build_options).

at(
  N,
  consequence_of(
    X,
    o(target_state, killed),
    resolves,
    potential(problem, relation(threatening, Target, Someone))
  )
) :-
  at(N, action(X, attack)),
  at(N, arg(X, target, Target)),
  st(N, relation(threatening, Target, Someone)),
  story_op(N, build_options).

at(
  N,
  consequence_of(
    X,
    o(success, Every),
    manifests,
    potential(problem, relation(threatening, Aggressor, Target))
  )
) :-
  outcome_val(attack, success, Every),
  at(N, action(X, attack)),
  at(N, arg(X, aggressor, Aggressor)),
  at(N, arg(X, target, Target)),
  st(N, relation(threatening, Aggressor, Target)),
  story_op(N, build_options).

% fighting is dangerous:
at(
  N,
  consequence_of(
    X,
    o(aggressor_state, injured),
    state(injured, Aggressor)
  )
) :-
  at(N, action(X, attack)),
  at(N, arg(X, aggressor, Aggressor)),
  story_op(N, build_options).

at(
  N,
  consequence_of(
    X,
    o(aggressor_state, killed),
    state(killed, Aggressor)
  )
) :-
  at(N, action(X, attack)),
  at(N, arg(X, aggressor, Aggressor)),
  story_op(N, build_options).

at(
  N,
  consequence_of(
    X,
    o(target_state, injured),
    state(injured, Target)
  )
) :-
  at(N, action(X, attack)),
  at(N, arg(X, target, Target)),
  story_op(N, build_options).

at(
  N,
  consequence_of(
    X,
    o(target_state, killed),
    state(killed, Target)
  )
) :-
  at(N, action(X, attack)),
  at(N, arg(X, target, Target)),
  story_op(N, build_options).

% Looting is a possibility:

1 = {
  at(
    N,
    consequence_of(
      X,
      o(get_loot, loot),
      relation(has_item, Aggressor, Item)
    )
  ) : st(N, relation(has_item, Aggressor, Item))
} :-
  at(N, action(X, attack)),
  at(N, arg(X, aggressor, Aggressor)),
  1 <= { st(N, relation(has_item, Aggressor, Item)) },
  story_op(N, build_options).

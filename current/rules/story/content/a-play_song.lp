% play_song
action(play_song).

% arguments

argument(play_song, musician, actor).
argument(play_song, audience, actor).
initiator(play_song, musician).
default_intent(play_song, o(quality, harmonious)).
% TODO: the instrument?

% outcomes

outcome_val(play_song, quality, harmonious).
outcome_val(play_song, quality, plain).
% TODO: add discordant?

% skills

skill_link(
  music, required, tool,
  play_song, musician,
  o(quality, harmonious)
).

error(m("Unintelligent musician.", N, X)) :-
  at(N, action(X, play_song)),
  at(N, arg(X, musician, Unintelligent)),
  st(N, property(has_skill, Unintelligent, unintelligent)),
  story_op(N, build_options).

error(m("Unintelligent audience.", N, X)) :-
  at(N, action(X, play_song)),
  at(N, arg(X, audience, Unintelligent)),
  st(N, property(has_skill, Unintelligent, unintelligent)),
  story_op(N, build_options).

% effects

at(
  N,
  consequence_of(
    X,
    o(quality, harmonious),
    resolves,
    potential(opportunity, state(bored, Audience))
  )
):-
  at(N, action(X, play_song)),
  at(N, arg(X, audience, Audience)),
  st(N, state(bored, Audience)),
  story_op(N, build_options).

at(
  N,
  consequence_of(
    X,
    o(quality, plain),
    nullifies,
    potential(opportunity, state(bored, Audience))
  )
):-
  at(N, action(X, play_song)),
  at(N, arg(X, audience, Audience)),
  st(N, state(bored, Audience)),
  story_op(N, build_options).


% TODO: angering the audience?

% TODO: Other effects?

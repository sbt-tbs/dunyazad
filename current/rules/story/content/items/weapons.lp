subclass(item, weapon).

subclass(weapon, artificial_weapon).
subclass(weapon, natural_weapon).

%item_def(sword, artificial_weapon, "sword", singular).
item_def(spear, artificial_weapon, "spear", singular).
%item_def(javelin, artificial_weapon, "javelin", singular).
%item_def(dagger, artificial_weapon, "daggers", plural).
%item_def(axe, artificial_weapon, "axe", singular).
%item_def(mace, artificial_weapon, "mace", singular).
%item_def(glaive, artificial_weapon, "glaive", singular).
%item_def(bow, artificial_weapon, "bow", singular).
%item_def(rapier, artificial_weapon, "rapier", singular).

tool_for(IType, fighting) :-
  item_def(IType, artificial_weapon, Name, Number).
tool_for(IType, fighting) :-
  item_def(IType, natural_weapon, Name, Number).

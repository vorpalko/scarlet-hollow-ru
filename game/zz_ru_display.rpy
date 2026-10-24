# Pure Russian display adapters for source-bound supplemental cases.
# English machine strings remain intact in story state and saves.

init 901 python:
    def ru_item(value, case="nom"):
        forms = {
            "chips": {"nom": "чипсы", "gen": "чипсов", "dat": "чипсам", "acc": "чипсы", "inst": "чипсами", "prep": "чипсах"},
            "beverage": {"nom": "напиток", "gen": "напитка", "dat": "напитку", "acc": "напиток", "inst": "напитком", "prep": "напитке"},
            "ice cream": {"nom": "мороженое", "gen": "мороженого", "dat": "мороженому", "acc": "мороженое", "inst": "мороженым", "prep": "мороженом"},
        }
        if not ru_text_is_active() or value not in forms:
            return value
        return forms[value][case]

    def ru_item_agree(value, plural, masculine, neuter):
        """Choose an authored phrase; unknown/absent values return the raw value."""
        if not ru_text_is_active():
            return value
        return {"chips": plural, "beverage": masculine, "ice cream": neuter}.get(value, value)

    def ru_trait(value):
        if not ru_text_is_active():
            return value
        return {"Keen Eye": "Зоркий глаз", "Street Smart": "Житейская хватка"}.get(value, value)

    def ru_identity(value, case="nom"):
        if not ru_text_is_active():
            return value
        if value == "Kaneeka":
            return {"nom": "Каника", "gen": "Каники", "dat": "Канике", "acc": "Канику", "inst": "Каникой", "prep": "Канике"}[case]
        if value in ("全体の一部", "何もない"):
            # Preserve intentional opaque identity codepoints. Only the font is scoped.
            return "{font=ru_support/fonts/NotoSerifJP/NotoSerifJP-Regular.otf}" + value + "{/font}"
        return value

    import builtins as _ru_display_builtin

    def _ru_display_pronoun(case, capital=False):
        if ru_text_is_active():
            return ru_pronoun(case, capital)
        # English templates do not reference these fields, but a direct display
        # caller still receives the original English dictionary value.
        if case == "nom":
            key = "singular_subject_cap" if capital else "singular_subject"
        elif case == "poss":
            key = "possessive"
        else:
            key = "singular_object"
        return getattr(renpy.store, "pronouns", {}).get(key, "")

    class _RuDisplayFields(_ru_display_builtin.object):
        # Ordinary init object, no cache or story-state writes. Existing saves
        # retain this init default; the object has no per-save mutable fields.
        __slots__ = ()

        @property
        def item_gen(self):
            return ru_item(getattr(renpy.store, "monday_store_item", None), "gen")

        @property
        def item_acc(self):
            return ru_item(getattr(renpy.store, "monday_store_item", None), "acc")

        @property
        def item_possessive(self):
            return ru_item_agree(getattr(renpy.store, "monday_store_item", None), "свои", "свой", "своё")

        @property
        def trait(self):
            return ru_trait(getattr(renpy.store, "street_insert", None))

        @property
        def identity_nom(self):
            return ru_identity(getattr(renpy.store, "kaneeka_insert", None))

        @property
        def identity_inst(self):
            return ru_identity(getattr(renpy.store, "kaneeka_insert", None), "inst")

        @property
        def identity_gen(self):
            return ru_identity(getattr(renpy.store, "kaneeka_insert", None), "gen")

        @property
        def identity_dat(self):
            return ru_identity(getattr(renpy.store, "kaneeka_insert", None), "dat")

        @property
        def identity_acc(self):
            return ru_identity(getattr(renpy.store, "kaneeka_insert", None), "acc")

        @property
        def pronoun_nom(self):
            return _ru_display_pronoun("nom")

        @property
        def pronoun_nom_cap(self):
            return _ru_display_pronoun("nom", capital=True)

        @property
        def pronoun_gen(self):
            return _ru_display_pronoun("gen")

        @property
        def pronoun_dat(self):
            return _ru_display_pronoun("dat")

        @property
        def pronoun_acc(self):
            return _ru_display_pronoun("acc")

        @property
        def pronoun_inst(self):
            return _ru_display_pronoun("inst")

        @property
        def pronoun_prep(self):
            return _ru_display_pronoun("prep")

        @property
        def pronoun_poss(self):
            return _ru_display_pronoun("poss")

        @property
        def was_going_home(self):
            # Finite past-progressive phrase for one reviewed source token.
            # No story variables, English pronoun dictionary, or saves change.
            if not ru_text_is_active():
                return getattr(renpy.store, "pronouns", {}).get("pronoun_was", "they were") + " going home"
            return {"male": "он шёл домой", "female": "она шла домой"}.get(
                getattr(renpy.store, "gender", "enby"), "они шли домой")

        @property
        def came_to_town(self):
            # Completed arrival with the original subject, selected at display.
            if not ru_text_is_active():
                return getattr(renpy.store, "pronouns", {}).get("singular_subject_cap", "They") + " came into town"
            return {"male": "Он приехал в город", "female": "Она приехала в город"}.get(
                getattr(renpy.store, "gender", "enby"), "Они приехали в город")

        @property
        def was_nervous_verb(self):
            if not ru_text_is_active():
                # The source subject is the unchanged proper name, not they.
                return "was nervous"
            return {"male": "нервничал", "female": "нервничала"}.get(
                getattr(renpy.store, "gender", "enby"), "нервничали")

        @property
        def still_asleep(self):
            # Subject and number agree in the bounded Episode 2 sleep statement.
            if not ru_text_is_active():
                return getattr(renpy.store, "pronouns", {}).get("pronoun_is_conj", "they're") + " still asleep"
            return {"male": "он ещё спит", "female": "она ещё спит"}.get(
                getattr(renpy.store, "gender", "enby"), "они ещё спят")

        @property
        def went_past(self):
            # The unchanged player name is the subject of four reviewed clauses.
            if not ru_text_is_active():
                return "went"
            return {"male": "пошёл", "female": "пошла"}.get(
                getattr(renpy.store, "gender", "enby"), "пошли")

        @property
        def found_past(self):
            # Finite completed discovery; the source subject stays unchanged.
            if not ru_text_is_active():
                return "found"
            return {"male": "нашёл", "female": "нашла"}.get(
                getattr(renpy.store, "gender", "enby"), "нашли")

        @property
        def rest_future(self):
            # Third-person agreement after the unchanged player name.
            if not ru_text_is_active():
                return "rest"
            return "отдохнёт" if getattr(renpy.store, "gender", "enby") in ("male", "female") else "отдохнут"

        @property
        def called_past(self):
            # Completed third-person call after the unchanged proper name.
            if not ru_text_is_active():
                return "called"
            return {"male": "позвонил", "female": "позвонила"}.get(
                getattr(renpy.store, "gender", "enby"), "позвонили")

        @property
        def planned_past(self):
            # Named player's intended action; display agreement only.
            if not ru_text_is_active():
                return "planned"
            return {"male": "задумал", "female": "задумала"}.get(
                getattr(renpy.store, "gender", "enby"), "задумали")

        @property
        def go_future(self):
            # Named player's future movement; display agreement only.
            if not ru_text_is_active():
                return "will go"
            return {"male": "пойдёт", "female": "пойдёт"}.get(
                getattr(renpy.store, "gender", "enby"), "пойдут")

        @property
        def invited_past(self):
            # Completed invitation by the unchanged named player; display only.
            if not ru_text_is_active():
                return "invited"
            return {"male": "пригласил", "female": "пригласила"}.get(
                getattr(renpy.store, "gender", "enby"), "пригласили")

        @property
        def animal_odd_present(self):
            # Three bounded Episode 3 predicates keep agreement with the name.
            if not ru_text_is_active():
                return "is a little odd"
            return "немного чудит" if getattr(renpy.store, "gender", "enby") in ("male", "female") else "немного чудят"

        @property
        def likes_talk_animals_present(self):
            if not ru_text_is_active():
                return "likes"
            return "любит" if getattr(renpy.store, "gender", "enby") in ("male", "female") else "любят"

        @property
        def animal_weird_present(self):
            if not ru_text_is_active():
                return "is weird"
            return "странно себя ведёт" if getattr(renpy.store, "gender", "enby") in ("male", "female") else "странно себя ведут"

        @property
        def implies_present(self):
            # Exact named-player attribution without changing the addressee.
            if not ru_text_is_active():
                return "is implying"
            return "намекает" if getattr(renpy.store, "gender", "enby") in ("male", "female") else "намекают"

        @property
        def speak_present(self):
            # Let the named player speak, preserving the original addressee.
            if not ru_text_is_active():
                return "speak"
            return "говорит" if getattr(renpy.store, "gender", "enby") in ("male", "female") else "говорят"

        @property
        def told_past(self):
            # Completed speech about the unchanged named player, not the addressee.
            if not ru_text_is_active():
                return "told"
            return {"male": "рассказал", "female": "рассказала"}.get(
                getattr(renpy.store, "gender", "enby"), "рассказали")

        @property
        def banished_past(self):
            # Completed action by the unchanged named player.
            if not ru_text_is_active():
                return "banished"
            return {"male": "изгнал", "female": "изгнала"}.get(
                getattr(renpy.store, "gender", "enby"), "изгнали")

        @property
        def lost_past(self):
            if not ru_text_is_active():
                return "lost"
            return {"male": "потерял", "female": "потеряла"}.get(
                getattr(renpy.store, "gender", "enby"), "потеряли")

        @property
        def endured_past(self):
            if not ru_text_is_active():
                return "has been through"
            return {"male": "пережил", "female": "пережила"}.get(
                getattr(renpy.store, "gender", "enby"), "пережили")

        @property
        def must_present(self):
            if not ru_text_is_active():
                return "must"
            return {"male": "должен", "female": "должна"}.get(
                getattr(renpy.store, "gender", "enby"), "должны")

        @property
        def tried_past(self):
            if not ru_text_is_active():
                return "was trying"
            return {"male": "пытался", "female": "пыталась"}.get(
                getattr(renpy.store, "gender", "enby"), "пытались")

        @property
        def thinks_up_present(self):
            if not ru_text_is_active():
                return "thinks up"
            return {"male": "придумывает", "female": "придумывает"}.get(
                getattr(renpy.store, "gender", "enby"), "придумывают")

        @property
        def can_present(self):
            if not ru_text_is_active():
                return "can"
            return "может" if getattr(renpy.store, "gender", "enby") in ("male", "female") else "могут"

        @property
        def handled_past(self):
            if not ru_text_is_active():
                return "took care of things"
            return {"male": "разобрался", "female": "разобралась"}.get(
                getattr(renpy.store, "gender", "enby"), "разобрались")

        @property
        def teases_present(self):
            if not ru_text_is_active():
                return "is pulling your leg"
            return {"male": "разыгрывает", "female": "разыгрывает"}.get(
                getattr(renpy.store, "gender", "enby"), "разыгрывают")

        @property
        def meant_past(self):
            if not ru_text_is_active():
                return "meant"
            return {"male": "имел в виду", "female": "имела в виду"}.get(
                getattr(renpy.store, "gender", "enby"), "имели в виду")

        @property
        def leper_inst(self):
            if not ru_text_is_active():
                return "a leper"
            return {"male": "прокажённым", "female": "прокажённой"}.get(
                getattr(renpy.store, "gender", "enby"), "прокажёнными")

        @property
        def was_right_past(self):
            if not ru_text_is_active():
                return "was right"
            return {"male": "был прав", "female": "была права"}.get(
                getattr(renpy.store, "gender", "enby"), "были правы")

        @property
        def infected_past(self):
            if not ru_text_is_active():
                return "infected"
            return {"male": "заразил", "female": "заразила"}.get(
                getattr(renpy.store, "gender", "enby"), "заразили")

        @property
        def tries_present(self):
            if not ru_text_is_active():
                return "is trying"
            return {"male": "пытается", "female": "пытается"}.get(
                getattr(renpy.store, "gender", "enby"), "пытаются")

        @property
        def worried_past(self):
            if not ru_text_is_active():
                return "was worried"
            return {"male": "волновался", "female": "волновалась"}.get(
                getattr(renpy.store, "gender", "enby"), "волновались")

        @property
        def did_past(self):
            if not ru_text_is_active():
                return "did"
            return {"male": "сделал", "female": "сделала"}.get(
                getattr(renpy.store, "gender", "enby"), "сделали")

        @property
        def speaker_title_nom(self):
            # Source title for the player; keep its meaning and grammatical gender.
            if not ru_text_is_active():
                return "Speaker"
            return {"male": "Говорящий", "female": "Говорящая"}.get(
                getattr(renpy.store, "gender", "enby"), "Говорящие")

        @property
        def speaker_title_gen(self):
            if not ru_text_is_active():
                return "Speaker"
            return {"male": "Говорящего", "female": "Говорящей"}.get(
                getattr(renpy.store, "gender", "enby"), "Говорящих")

        @property
        def speaker_title_inst(self):
            if not ru_text_is_active():
                return "Speaker"
            return {"male": "Говорящим", "female": "Говорящей"}.get(
                getattr(renpy.store, "gender", "enby"), "Говорящими")

        @property
        def will_feel(self):
            if not ru_text_is_active():
                return "will feel"
            return ru_form("будет чувствовать", "будет чувствовать", "будут чувствовать")

        @property
        def is_listening(self):
            if not ru_text_is_active():
                return "is listening"
            return ru_form("слушает", "слушает", "слушают")

        @property
        def said_past(self):
            # Completed speech by the unchanged named player; no story-state writes.
            if not ru_text_is_active():
                return "said"
            return {"male": "сказал", "female": "сказала"}.get(
                getattr(renpy.store, "gender", "enby"), "сказали")

        @property
        def confused_past(self):
            if not ru_text_is_active():
                return "confused"
            return {"male": "запутал", "female": "запутала"}.get(
                getattr(renpy.store, "gender", "enby"), "запутали")

    ru_display = _RuDisplayFields()

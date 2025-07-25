from otree.api import *
import itertools


doc = """
This is my idea for a dice game
"""


class C(BaseConstants):
    NAME_IN_URL = 'BeesDice_app'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 2

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    bus_name = models.StringField(label="Your Business name:")
    fin_roll_one = models.CurrencyField(label='What is the value of the first dice?')
    #fin_roll_two = models.IntegerField(label='What is the value of the second dice?')
    #fin_roll_three = models.IntegerField(label='What is the value of the third dice?')
    #fin_roll_four = models.IntegerField(label='What is the value of the fourth dice?')
    #fin_roll_five = models.IntegerField(label='What is the value of the fifth dice?')
    acct_roll_one = models.CurrencyField(label='What is the value of the first dice?')
    #acct_roll_two = models.IntegerField(label='What is the value of the second dice?')
    #acct_roll_three = models.IntegerField(label='What is the value of the third dice?')
    #acct_roll_four = models.IntegerField(label='What is the value of the fourth dice?')
    #acct_roll_five = models.IntegerField(label='What is the value of the fifth dice?')
    earn = models.CurrencyField()
    tax = models.CurrencyField()
    net = models.CurrencyField()


# Functions:
def creating_session(subsession):
    treatment = itertools.cycle([1, 2, 3])
    for player in subsession.get_players():
        participant = player.participant
        participant.treatment = next(treatment)

def set_player_treatment(player):
    if player.id_in_group == 1:
        player.treatment = 'treatment_1'
    elif player.id_in_group == 2:
        player.treatment = 'treatment_2'
    else:
        player.treatment = 'treatment_3'
    player.participant.vars['treatment'] = player.treatment

def get_treatment(player):
    treatment = player.participant.vars.get('treatment')
    return treatment


# PAGES
class Intro(Page):
    form_model = 'player'
    form_fields = ['bus_name']

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

class FakeIntro(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

class Fin(Page):
    # making it simpler to play through for testing
    #form_model = 'player'
    #form_fields = ['fin_roll_one', 'fin_roll_two', 'fin_roll_three', 'fin_roll_four', 'fin_roll_five']

    form_model = 'player'
    form_fields = ['fin_roll_one']

class EarlyWaitPage(WaitPage):
    wait_for_all_groups = True

class Acct(Page):
    # Making it simpler for testing
    #form_model = 'player'
    #form_fields = ['acct_roll_one', 'acct_roll_two', 'acct_roll_three', 'acct_roll_four', 'acct_roll_five']
    form_model = 'player'
    form_fields = ['acct_roll_one']

class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        #earn= (player.fin_roll_one + player.fin_roll_two + player.fin_roll_three + player.fin_roll_four + player.fin_roll_five),
        #tax = ((player.acct_roll_one + player.acct_roll_two + player.acct_roll_three + player.acct_roll_four + player.acct_roll_five) * .25),
        #net = int(earn[0]) - int(tax[0]),
        earn = player.fin_roll_one * 100,
        tax = player.acct_roll_one * 25,
        player.net = cu(earn[0]) - cu(tax[0])
        return dict(
            earn=cu(earn[0]),
            tax=cu(tax[0]),
            net=cu(player.net)
        )

class LateWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        for p in group.get_players():
            p.payoff = p.net

class EndResults(Page):
    pass

page_sequence = [FakeIntro, Fin, Acct, EarlyWaitPage, Results, LateWaitPage, EndResults]

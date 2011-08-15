from django import forms
from archive.models import Game, GameStat


class ApiGameForm(forms.ModelForm):
	player_limit = forms.IntegerField(min_value=2, max_value=8)

	class Meta:
		model = Game
		fields = ('player_limit', 'score_limit', 'time_limit',
			'map', 'duration', 'opponent', 'opponent_lineup',
			'our_result', 'opponent_result', 'game_id')


class ApiGameStatForm(forms.ModelForm):

	class Meta:
		model = GameStat
		fields = ('game', 'nickname', 'points', 'kills', 'deaths', 'suicides',
			'best_spree', 'hammer_kills', 'hammer_deaths', 'pistol_kills',
			'pistol_deaths', 'shotgun_kills', 'shotgun_deaths', 'grenade_kills',
			'grenade_deaths', 'rifle_kills', 'rifle_deaths', 'carriers_killed',
			'kills_holding_flag', 'deaths_holding_flag')

from decimal import Decimal
from django.contrib.auth.models import User
from django.db import models
from django.utils import dateformat
from picklefield.fields import PickledObjectField


# http://stackoverflow.com/questions/394574/394807#394807
to_roman=lambda n:o[n]if n<10 else''.join(
	dict(zip('IVXLC','XLCDM'))[c]for c in to_roman(n//10))+o[n%10]
o=' I II III IV V VI VII VIII IX'.split(' ')


class Match(models.Model):
	"""Groups games into game sessions"""
	notes = models.CharField(max_length=255)

	# denormalized
	player_limit = models.PositiveIntegerField()
	score_limit = models.PositiveIntegerField()
	time_limit = models.PositiveIntegerField(default=0)
	map = models.CharField(max_length=25)

	# during save(), by self.get_our_clan_name()
	our_clan_name = models.CharField(max_length=2)

	opponent = models.ForeignKey(OpponentClan)

	# sum of wins/losses
	our_result = models.PositiveIntegerField()
	opponent_result = models.PositiveIntegerField()

	"""
	a match is a group of consecutive games
	with the same player_limit, score_limit, map and opponent
	"""

	def get_score_limit(self):
		return u"{0}on{0}".format(self.score_limit)

	def get_result_string(self):
		return u"{0}-{1}".format(to_roman(self.our_result),
			to_roman(self.opponent_result))

	def get_our_clan_name(self):
		stats = GameStat.objects.filter(game__in=self.games)
		return UserProfile.CLAN_KA if stats.filter(
			player__clan=UserProfile.CLAN_KA).count() / \
			stats.count() >= 0.5 else UserProfile.CLAN_QI

	def get_game_title(self):
		return u"{0} vs {1}, {2}, {3}".format(self.get_our_clan_name,
			self.opponent.tag, self.get_score_limit, self.get_result_string)



class Game(models.Model):
	created_at = models.DateTimeField(default=datetime.datetime.now)
	created_by = models.ForeignKey(User)

	# grouping
	match = models.ForeignKey(Match, related_name='games', blank=True, null=True)

	# game conditions
	player_limit = models.PositiveIntegerField() # 2-8
	score_limit = models.PositiveIntegerField() # forms: 600, 1000, custom
	time_limit = models.PositiveIntegerField(default=0) # in minutes, 0 - disabled
	map = models.CharField(max_length=25)
	duration = models.PositiveIntegerField() # in seconds

	# lineup
	opponent = models.ForeignKey(OpponentClan)
	
	# a list of strings
	# [u"Player1", u"Player2"]
	opponent_lineup = PickledObjectField()

	# emulating a list of strings
	@property
	def our_lineup(self):
		return GameStat.objects.filter(game=self) \
			.values_list('player', flat=True)

	# result
	our_result = models.IntegerField()
	opponent_result = models.IntegerField()

	# moderation
	is_verified = models.BooleanField(default=False)

	# unique game ID
	# sha1(game_start_tick + red_result + blue_result \
	#  + time.time() + game_end_tick + sum_of_all_players_score)
	game_id = models.CharField(max_length=32)

	# denormalized
	RESULT_LOSS = False
	RESULT_WIN = True
	RESULT_CHOICES = (
		(RESULT_LOSS, "Loss"),
		(RESULT_WIN, "Win"),
	)
	result = models.BooleanField(choices=RESULT_CHOICES)


class GameStat(models.Model):
	player = models.ForeignKey(Player)
	game = models.ForeignKey(Game, related_name='stats')

	points = models.IntegerField() # this is denormalized btw

	kills = models.PositiveIntegerField() # this is denormalized btw
	deaths = models.PositiveIntegerField() # this is denormalized btw
	suicides = models.PositiveIntegerField()

	best_spree = models.PositiveIntegerField()

	# weapon stuff
	hammer_kills = models.PositiveIntegerField()
	hammer_deaths = models.PositiveIntegerField()

	pistol_kills = models.PositiveIntegerField()
	pistol_deaths = models.PositiveIntegerField()

	shotgun_kills = models.PositiveIntegerField()
	shotgun_deaths = models.PositiveIntegerField()

	grenade_kills = models.PositiveIntegerField()
	grenade_deaths = models.PositiveIntegerField()

	rifle_kills = models.PositiveIntegerField()
	rifle_deaths = models.PositiveIntegerField()

	# ctf
	flag_touches = models.PositiveIntegerField()
	flag_captures = models.PositiveIntegerField()

	carriers_killed = models.PositiveIntegerField()
	kills_holding_flag = models.PositiveIntegerField()
	deaths_holding_flag = models.PositiveIntegerField()

	# denormalized

	# self.kills/self.game.duration
	kills_per_minute = models.DecimalField(max_digits=3, decimal_places=1) # up to 99.9

	# self.kills - self.deaths
	net_score = models.IntegerField()

	# ! ! ! ! ! ! ! ! ! ! ! ! ! !
	# BEWARE OF DIVISION BY ZERO!
	# store infinite ratio as None
	# ! ! ! ! ! ! ! ! ! ! ! ! ! !
	
	# self.kills/self.deaths
	ratio = models.DecimalField(max_digits=6, decimal_places=2, null=True) # up to 9999.99

	@property
	def has_positive_ratio(self):
		return True if self.ratio and self.ratio > Decimal(1) else False

	class Meta:

		unique_together = ('game', 'player')

	def __unicode__(self):
		return u"Stats of {0} v {1} [#{2}]".format(self.player,
			self.game.opponent, self.game.id)



class OpponentClan(models.Model):
	tag = models.CharField(max_length=11)
	full_name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.full_name


class Player(models.Model):
	nickname = models.CharField(max_length=15)
	user = models.OneToOneField(User, unique=True,
		related_name='player', blank=True, null=True)
	
	def __unicode__(self):
		return self.user if self.user else self.nickname


class AdditionalNickname(models.Model):
	nickname = models.CharField(max_length=15)
	player = models.ForeignKey(Player, related_name='additional_nicks')


class Screenshot(models.Model):
	game = models.ForeignKey(Game)
	sent_by = models.ForeignKey(User)
	
	TYPE_SCORE = 1
	TYPE_STATS = 2
	TYPE_CHOICES = (
		(TYPE_SCORE, "Scoreboard"),
		(TYPE_STATS, "Statboard"),
	)
	screenshot_type = models.PositiveIntegerField(choices=TYPE_CHOICES)

	def screenshot_filename(self, filename):
		del filename
		return 'uploads/shots/{0}/qi_vs_{1}_{2}.png'.format(
			self.get_screenshot_type_display(),
			self.game.opponent,
			dateformat.format(self.game.created_at, 'd-m-y_h-i'),
		).lower()
	screenshot_file = models.FileField(upload_to=screenshot_filename)

	class Meta:

		unique_together = ('game', 'screenshot_type')

	def get_absolute_url(self):
		return self.screenshot_file.url


class ClientDemo(models.Model):
	game = models.ForeignKey(Game)
	sent_by = models.ForeignKey(User)

	def demo_filename(self, filename):
		del filename
		return 'uploads/demos/client/{0}_vs_{1}_{2}_by_{3}.png'.format(
			self.match.our_clan_name,
			self.game.opponent,
			dateformat.format(self.game.created_at, 'd-m-y_h-i'),
			self.sent_by,
		).lower()
	demo_file = models.FileField(upload_to=demo_filename)

	class Meta:

		unique_together = ('game', 'sent_by')

	def get_absolute_url(self):
		return self.demo_file.url


class ClientDemo(models.Model):
	game = models.ForeignKey(Game, unique=True)
	sent_by = models.ForeignKey(Server)

	def demo_filename(self, filename):
		del filename
		return 'uploads/demos/server/{0}_vs_{1}_{2}_serverside.png'.format(
			self.match.our_clan_name,
			self.game.opponent,
			dateformat.format(self.game.created_at, 'd-m-y_h-i'),
		).lower()
	demo_file = models.FileField(upload_to=demo_filename)

	def get_absolute_url(self):
		return self.demo_file.url

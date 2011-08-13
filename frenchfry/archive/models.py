from decimal import Decimal
from django.contrib.auth.models import User
from django.db import models
from django.utils import dateformat


class Match(models.Model):
	"""Groups games into game sessions"""
	notes = models.CharField(max_length=255)

	# denormalized
	player_limit = models.PositiveIntegerField()
	score_limit = models.PositiveIntegerField()
	time_limit = models.PositiveIntegerField(default=0)
	map = models.CharField(max_length=25)

	opponent = models.CharField(max_length=25)
	# OR
	#opponent = models.ForeignKey(OpponentClan)


	# sum of wins/losses
	our_result = models.PositiveIntegerField()
	opponent_result = models.PositiveIntegerField()

	"""
	a match is a group of consecutive games
	with the same player_limit, score_limit, map and clan
	"""


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

	opponent = models.CharField(max_length=25)
	# OR
	#opponent = models.ForeignKey(OpponentClan)
	
	# result
	our_result = models.IntegerField()
	opponent_result = models.IntegerField()

	# moderation
	is_verified = models.BooleanField(default=False)

	# unique game ID
	#game_id = models.IntegerField()

	# denormalized
	RESULT_LOSS = False
	RESULT_WIN = True
	RESULT_CHOICES = (
		(RESULT_LOSS, "Loss"),
		(RESULT_WIN, "Win"),
	)
	result = models.BooleanField(choices=RESULT_CHOICES)


class GameStats(models.Model):
	player = models.ForeignKey(Player)
	game = models.ForeignKey(Game)

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
		return True if self.ratio and self.ratio > Decimal(1)

	def __unicode__(self):
		return u"Stats of {0} v {1} [#{2}]".format(self.player,
			self.game.opponent, self.game.id)


class Player(models.Model):
	nickname = models.CharField(max_length=25)
	user = models.OneToOneField(User, unique=True,
		related_name='player', blank=True, null=True)


class AdditionalNickname(models.Model):
	nickname = models.CharField(max_length=25)
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
		""" uploads/shots/scoreboard/qi_vs_ib_13-08-11_23-52.png """
		return 'uploads/shots/{0}/qi_vs_{1}_{2}.png'.format(
			self.get_screenshot_type_display(),
			self.game.opponent,
			dateformat.format(self.game.created_at, 'd-m-y_h-i'),
		).lower()
	screenshot = models.FileField(upload_to=screenshot_filename)

	class Meta:

		unique_together = ('game', 'screenshot_type')

	def get_absolute_url(self):
		return self.screenshot_file.url

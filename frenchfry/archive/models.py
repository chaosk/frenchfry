from decimal import Decimal
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db import models
from django.db.models import F
from django.utils import dateformat
from picklefield.fields import PickledObjectField


# http://stackoverflow.com/questions/394574/394807#394807
to_roman=lambda n:o[n]if n<10 else''.join(
	dict(zip('IVXLC','XLCDM'))[c]for c in to_roman(n//10))+o[n%10]
o=' I II III IV V VI VII VIII IX'.split(' ')


class Match(models.Model):
	created_at = models.DateTimeField(default=datetime.now)

	"""Groups games into game sessions"""
	notes = models.CharField(max_length=255)

	# denormalized
	player_limit = models.PositiveIntegerField()
	score_limit = models.PositiveIntegerField()
	time_limit = models.PositiveIntegerField(default=0)
	map = models.CharField(max_length=25)

	# during Game().save(), by self.set_our_clan_name()
	our_clan_name = models.IntegerField(max_length=1)

	opponent = models.ForeignKey('OpponentClan')

	# moderation
	is_verified = models.BooleanField(default=False)

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
		return Player.CLAN_KA_DISPLAY if stats.exclude(
			player__clan=Player.CLAN_QI).count() / \
			stats.count() >= 0.5 else Player.CLAN_QI_DISPLAY

	def set_our_clan_name(self):
		return self.get_our_clan_name()

	def get_game_title(self):
		return u"{0} vs {1}, {2}, {3}".format(self.our_clan_name,
			self.opponent.tag, self.get_score_limit, self.get_result_string)

	def refresh_results(self, commit=True):
		self.our_result = self.games.filter(result=Game.RESULT_WIN).count()
		self.opponent_result = self.games.filter(result=Game.RESULT_LOSS).count()
		if commit:
			self.save()

	def save(self, *args, **kwargs):
		self.refresh_results(commit=False)
		super(Match, self).save(*args, **kwargs)


class Game(models.Model):
	created_at = models.DateTimeField(default=datetime.now)
	created_by = models.ForeignKey(User)

	# grouping
	match = models.ForeignKey(Match, related_name='games', blank=True, null=True)

	# game conditions
	player_limit = models.PositiveSmallIntegerField() # 2-8
	score_limit = models.PositiveIntegerField() # forms: 600, 1000, custom
	time_limit = models.PositiveIntegerField(default=0) # in minutes, 0 - disabled
	map = models.CharField(max_length=25)
	duration = models.PositiveIntegerField() # in seconds

	# lineup
	opponent = models.ForeignKey('OpponentClan')
	
	# a list of strings
	# [u"Player1", u"Player2"]
	opponent_lineup = PickledObjectField(editable=True)

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
	#  + game_end_tick + sum_of_all_players_score)
	game_id = models.CharField(max_length=40, unique=True)

	# denormalized
	RESULT_LOSS = -1
	RESULT_DRAW = 0
	RESULT_WIN = 1
	RESULT_CHOICES = (
		(RESULT_LOSS, "Loss"),
		(RESULT_DRAW, "Draw"),
		(RESULT_WIN, "Win"),
	)
	result = models.SmallIntegerField(max_length=1, choices=RESULT_CHOICES)

	def has_all_stats(self):
		return self.stats.count() == self.player_limit*2

	def has_scoreboard(self):
		return self.screenshots.filter(
			screenshot_type=Screenshot.TYPE_SCORE).exists()

	def has_statboard(self):
		return self.screenshots.filter(
			screenshot_type=Screenshot.TYPE_STATS).exists()

	def save(self, *args, **kwargs):		
		# lookup matches from last 24 hours
		matches = Match.objects.filter(
			player_limit=self.player_limit,
			score_limit=self.score_limit,
			time_limit=self.time_limit,
			map=self.map,
			opponent=self.opponent,
			created_at__gte=F('created_at') - timedelta(days=1)
		)
		if not matches:
			self.match = Match.objects.create(
				player_limit=self.player_limit,
				score_limit=self.score_limit,
				time_limit=self.time_limit,
				map=self.map,
				opponent=self.opponent,
			)
		else:
			self.match = matches[0]
		

		# denormalization
		self.result = Game.RESULT_WIN \
			if self.our_result > self.opponent_result else Game.RESULT_DRAW \
			if self.our_result == self.opponent_result else Game.RESULT_LOSS
		super(Game, self).save(*args, **kwargs)
		self.match.set_our_clan_name()


class GameStat(models.Model):
	player = models.ForeignKey('Player')
	game = models.ForeignKey(Game, related_name='stats')

	# we store this here anyway, to have a little history
	nickname = models.CharField(max_length=15)

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
		return self.ratio and self.ratio > Decimal(1)

	class Meta:

		unique_together = ('game', 'player')

	def save(self, *args, **kwargs):
		# setting the player if we have an exact match
		# it can be changed later by reviewer
		try:
			self.player = Player.objects.get(nickname=self.nickname)
		except Player.DoesNotExist:
			pass

		# denormalization
		if self.game.duration != 0:
			self.kills_per_minute = self.kills / self.game.duration
		else:
			self.kills_per_minute = 0

		self.net_score = self.kills - self.deaths
		self.ratio = self.kills / self.deaths if self.deaths != 0 else None

		super(GameStat, self).save(*args, **kwargs)

	def __unicode__(self):
		return u"Stats of {0} v {1} [#{2}]".format(self.player,
			self.game.opponent, self.game.id)


class Screenshot(models.Model):
	game = models.ForeignKey(Game, related_name='screenshots')
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
	sent_by = models.ForeignKey('Server')

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


class OpponentClan(models.Model):
	tag = models.CharField(max_length=11)
	full_name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.full_name


class Player(models.Model):
	nickname = models.CharField(max_length=15, unique=True)
	user = models.OneToOneField(User, unique=True,
		related_name='player', blank=True, null=True)

	CLAN_QI = 1
	CLAN_QI_DISPLAY = "Qi"
	CLAN_KA = 2
	CLAN_KA_DISPLAY = "Ka"
	CLAN_NONE = 3
	CLAN_NONE_DISPLAY = "-"
	CLAN_CHOICES = (
		(CLAN_QI, CLAN_QI_DISPLAY),
		(CLAN_KA, CLAN_KA_DISPLAY),
		(CLAN_NONE, CLAN_NONE_DISPLAY) # recruit?
	)
	clan = models.IntegerField(max_length=1, choices=CLAN_CHOICES)

	def __unicode__(self):
		return self.user if self.user else self.nickname


class AdditionalNickname(models.Model):
	nickname = models.CharField(max_length=15)
	player = models.ForeignKey(Player, related_name='additional_nicks')



class Server(models.Model):
	name = models.CharField(max_length=50)
	# api key?

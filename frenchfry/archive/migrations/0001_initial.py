# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Match'
        db.create_table('archive_match', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('player_limit', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('score_limit', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('time_limit', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('map', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('our_clan_name', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
            ('opponent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.OpponentClan'])),
            ('is_verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('our_result', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('opponent_result', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('archive', ['Match'])

        # Adding model 'Game'
        db.create_table('archive_game', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('match', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='games', null=True, to=orm['archive.Match'])),
            ('player_limit', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('score_limit', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('time_limit', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('map', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('duration', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('opponent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.OpponentClan'])),
            ('opponent_lineup', self.gf('picklefield.fields.PickledObjectField')()),
            ('our_result', self.gf('django.db.models.fields.IntegerField')()),
            ('opponent_result', self.gf('django.db.models.fields.IntegerField')()),
            ('is_verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('game_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
            ('result', self.gf('django.db.models.fields.SmallIntegerField')(max_length=1)),
        ))
        db.send_create_signal('archive', ['Game'])

        # Adding model 'GameStat'
        db.create_table('archive_gamestat', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Player'])),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stats', to=orm['archive.Game'])),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('points', self.gf('django.db.models.fields.IntegerField')()),
            ('kills', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('deaths', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('suicides', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('best_spree', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('hammer_kills', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('hammer_deaths', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pistol_kills', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pistol_deaths', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('shotgun_kills', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('shotgun_deaths', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('grenade_kills', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('grenade_deaths', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('rifle_kills', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('rifle_deaths', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('flag_touches', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('flag_captures', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('carriers_killed', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('kills_holding_flag', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('deaths_holding_flag', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('kills_per_minute', self.gf('django.db.models.fields.DecimalField')(max_digits=3, decimal_places=1)),
            ('net_score', self.gf('django.db.models.fields.IntegerField')()),
            ('ratio', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2)),
        ))
        db.send_create_signal('archive', ['GameStat'])

        # Adding unique constraint on 'GameStat', fields ['game', 'player']
        db.create_unique('archive_gamestat', ['game_id', 'player_id'])

        # Adding model 'Screenshot'
        db.create_table('archive_screenshot', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(related_name='screenshots', to=orm['archive.Game'])),
            ('sent_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('screenshot_type', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('screenshot_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('archive', ['Screenshot'])

        # Adding unique constraint on 'Screenshot', fields ['game', 'screenshot_type']
        db.create_unique('archive_screenshot', ['game_id', 'screenshot_type'])

        # Adding model 'ClientDemo'
        db.create_table('archive_clientdemo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.Game'])),
            ('sent_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('demo_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('archive', ['ClientDemo'])

        # Adding unique constraint on 'ClientDemo', fields ['game', 'sent_by']
        db.create_unique('archive_clientdemo', ['game_id', 'sent_by_id'])

        # Adding model 'OpponentClan'
        db.create_table('archive_opponentclan', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('archive', ['OpponentClan'])

        # Adding model 'Player'
        db.create_table('archive_player', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nickname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=15)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='player', unique=True, null=True, to=orm['auth.User'])),
            ('clan', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
        ))
        db.send_create_signal('archive', ['Player'])

        # Adding model 'AdditionalNickname'
        db.create_table('archive_additionalnickname', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(related_name='additional_nicks', to=orm['archive.Player'])),
        ))
        db.send_create_signal('archive', ['AdditionalNickname'])

        # Adding model 'Server'
        db.create_table('archive_server', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('archive', ['Server'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'ClientDemo', fields ['game', 'sent_by']
        db.delete_unique('archive_clientdemo', ['game_id', 'sent_by_id'])

        # Removing unique constraint on 'Screenshot', fields ['game', 'screenshot_type']
        db.delete_unique('archive_screenshot', ['game_id', 'screenshot_type'])

        # Removing unique constraint on 'GameStat', fields ['game', 'player']
        db.delete_unique('archive_gamestat', ['game_id', 'player_id'])

        # Deleting model 'Match'
        db.delete_table('archive_match')

        # Deleting model 'Game'
        db.delete_table('archive_game')

        # Deleting model 'GameStat'
        db.delete_table('archive_gamestat')

        # Deleting model 'Screenshot'
        db.delete_table('archive_screenshot')

        # Deleting model 'ClientDemo'
        db.delete_table('archive_clientdemo')

        # Deleting model 'OpponentClan'
        db.delete_table('archive_opponentclan')

        # Deleting model 'Player'
        db.delete_table('archive_player')

        # Deleting model 'AdditionalNickname'
        db.delete_table('archive_additionalnickname')

        # Deleting model 'Server'
        db.delete_table('archive_server')


    models = {
        'archive.additionalnickname': {
            'Meta': {'object_name': 'AdditionalNickname'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'additional_nicks'", 'to': "orm['archive.Player']"})
        },
        'archive.clientdemo': {
            'Meta': {'unique_together': "(('game', 'sent_by'),)", 'object_name': 'ClientDemo'},
            'demo_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sent_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'archive.game': {
            'Meta': {'object_name': 'Game'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'duration': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'game_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'map': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'match': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'games'", 'null': 'True', 'to': "orm['archive.Match']"}),
            'opponent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.OpponentClan']"}),
            'opponent_lineup': ('picklefield.fields.PickledObjectField', [], {}),
            'opponent_result': ('django.db.models.fields.IntegerField', [], {}),
            'our_result': ('django.db.models.fields.IntegerField', [], {}),
            'player_limit': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'result': ('django.db.models.fields.SmallIntegerField', [], {'max_length': '1'}),
            'score_limit': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'time_limit': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'archive.gamestat': {
            'Meta': {'unique_together': "(('game', 'player'),)", 'object_name': 'GameStat'},
            'best_spree': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'carriers_killed': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'deaths': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'deaths_holding_flag': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'flag_captures': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'flag_touches': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stats'", 'to': "orm['archive.Game']"}),
            'grenade_deaths': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'grenade_kills': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'hammer_deaths': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'hammer_kills': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kills': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'kills_holding_flag': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'kills_per_minute': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '1'}),
            'net_score': ('django.db.models.fields.IntegerField', [], {}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'pistol_deaths': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pistol_kills': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Player']"}),
            'points': ('django.db.models.fields.IntegerField', [], {}),
            'ratio': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2'}),
            'rifle_deaths': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'rifle_kills': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'shotgun_deaths': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'shotgun_kills': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'suicides': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'archive.match': {
            'Meta': {'object_name': 'Match'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'map': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'opponent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.OpponentClan']"}),
            'opponent_result': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'our_clan_name': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            'our_result': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'player_limit': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'score_limit': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'time_limit': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'archive.opponentclan': {
            'Meta': {'object_name': 'OpponentClan'},
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '11'})
        },
        'archive.player': {
            'Meta': {'object_name': 'Player'},
            'clan': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'player'", 'unique': 'True', 'null': 'True', 'to': "orm['auth.User']"})
        },
        'archive.screenshot': {
            'Meta': {'unique_together': "(('game', 'screenshot_type'),)", 'object_name': 'Screenshot'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'screenshots'", 'to': "orm['archive.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'screenshot_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'screenshot_type': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'sent_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'archive.server': {
            'Meta': {'object_name': 'Server'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['archive']

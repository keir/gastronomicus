# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Meeting'
        db.create_table(u'gastronomicus_meeting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(unique=True)),
            ('treasurer_comments', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'gastronomicus', ['Meeting'])

        # Adding M2M table for field attendees on 'Meeting'
        m2m_table_name = db.shorten_name(u'gastronomicus_meeting_attendees')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('meeting', models.ForeignKey(orm[u'gastronomicus.meeting'], null=False)),
            ('attendee', models.ForeignKey(orm[u'gastronomicus.attendee'], null=False))
        ))
        db.create_unique(m2m_table_name, ['meeting_id', 'attendee_id'])

        # Adding model 'Dish'
        db.create_table(u'gastronomicus_dish', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'gastronomicus', ['Dish'])

        # Adding model 'Serving'
        db.create_table(u'gastronomicus_serving', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dish', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gastronomicus.Dish'])),
            ('meeting', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gastronomicus.Meeting'])),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('gift', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('giver', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='gifts', null=True, to=orm['gastronomicus.Attendee'])),
        ))
        db.send_create_signal(u'gastronomicus', ['Serving'])

        # Adding model 'Attendee'
        db.create_table(u'gastronomicus_attendee', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('membership_started', self.gf('django.db.models.fields.DateField')(db_index=True, null=True, blank=True)),
            ('membership_ended', self.gf('django.db.models.fields.DateField')(db_index=True, null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'gastronomicus', ['Attendee'])


    def backwards(self, orm):
        # Deleting model 'Meeting'
        db.delete_table(u'gastronomicus_meeting')

        # Removing M2M table for field attendees on 'Meeting'
        db.delete_table(db.shorten_name(u'gastronomicus_meeting_attendees'))

        # Deleting model 'Dish'
        db.delete_table(u'gastronomicus_dish')

        # Deleting model 'Serving'
        db.delete_table(u'gastronomicus_serving')

        # Deleting model 'Attendee'
        db.delete_table(u'gastronomicus_attendee')


    models = {
        u'gastronomicus.attendee': {
            'Meta': {'object_name': 'Attendee'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'membership_ended': ('django.db.models.fields.DateField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'membership_started': ('django.db.models.fields.DateField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'gastronomicus.dish': {
            'Meta': {'object_name': 'Dish'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'gastronomicus.meeting': {
            'Meta': {'object_name': 'Meeting'},
            'attendees': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'meetings'", 'symmetrical': 'False', 'to': u"orm['gastronomicus.Attendee']"}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'servings': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'meetings'", 'symmetrical': 'False', 'through': u"orm['gastronomicus.Serving']", 'to': u"orm['gastronomicus.Dish']"}),
            'treasurer_comments': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'gastronomicus.serving': {
            'Meta': {'object_name': 'Serving'},
            'dish': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gastronomicus.Dish']"}),
            'gift': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'giver': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'gifts'", 'null': 'True', 'to': u"orm['gastronomicus.Attendee']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meeting': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gastronomicus.Meeting']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['gastronomicus']
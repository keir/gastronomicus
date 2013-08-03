from django.db import models

class Meeting(models.Model):
    date               = models.DateField(unique=True)
    attendees          = models.ManyToManyField('Attendee', related_name='meetings')
    servings           = models.ManyToManyField('Dish', related_name='meetings', through='Serving')
    treasurer_comments = models.TextField(blank=True)
    comments           = models.TextField(blank=True)

    def __unicode__(self):
        return u'Meeting %s' % self.date

class Dish(models.Model):
    name               = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return self.name

class Serving(models.Model):
    dish               = models.ForeignKey('Dish')
    meeting            = models.ForeignKey('Meeting')
    quantity           = models.IntegerField(null=True, blank=True)
    gift               = models.BooleanField(default=False)
    giver              = models.ForeignKey('Attendee', related_name='gifts', null=True, blank=True)

    def __unicode__(self):
        ret = u'%s - %s' % (self.meeting.date, self.dish.name)
        if self.gift and self.giver:
            return '%s by %s' % (ret, self.giver.name)
        return ret

class Attendee(models.Model):
    membership_started = models.DateField(null=True, blank=True, db_index=True)
    membership_ended   = models.DateField(null=True, blank=True, db_index=True)
    first_name         = models.CharField(max_length=100, blank=True)
    last_name          = models.CharField(max_length=100, blank=True)
    title              = models.CharField(max_length=100, blank=True)
    notes              = models.TextField(blank=True)

    @property
    def name(self):
        if self.first_name and self.last_name:
            return (u'%s %s' % (self.first_name, self.last_name)).strip()
        return self.first_name or self.last_name

    def __unicode__(self):
        if self.title:
            return '%s %s' % (self.title, self.name)
        return self.name

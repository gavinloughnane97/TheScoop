from django.contrib import admin
from .models import Team, Matchup, Bet

# Register your models here.

admin.site.register(Team)
admin.site.register(Matchup)
admin.site.register(Bet)
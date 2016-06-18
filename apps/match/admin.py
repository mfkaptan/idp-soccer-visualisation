from django.contrib import admin

from .models import (Stadium, MatchStadium, Match, Team,
                     MatchTeam, Person, Player, MatchPlayer, Referee)

admin.site.register(Stadium)
admin.site.register(MatchStadium)
admin.site.register(Match)
admin.site.register(Team)
admin.site.register(MatchTeam)
admin.site.register(Person)
admin.site.register(Referee)
admin.site.register(Player)
admin.site.register(MatchPlayer)


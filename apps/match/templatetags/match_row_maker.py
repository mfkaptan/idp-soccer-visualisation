from django.template import Library

register = Library()


@register.inclusion_tag('match/partials/match_row.html')
def match_row(match):
    context = {}
    h, a = map(int, match.get_score().split(":"))
    if h > a:
        context["home_class"] = "table-success"
        context["away_class"] = "table-danger"
    elif h == a:
        context["home_class"] = "table-warning"
        context["away_class"] = "table-warning"
    elif h < a:
        context["home_class"] = "table-danger"
        context["away_class"] = "table-success"

    context["home_team"] = match.home_team
    context["away_team"] = match.away_team
    context["score"] = match.get_score
    context["url"] = "#"

    return context



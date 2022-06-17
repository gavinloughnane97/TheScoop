from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404
from gameInfo.models import Team, Matchup, Bet, Game
import pytz
import requests
import statsapi


# Create your views here.

def index(request):
    currentTime = datetime.now(tz=pytz.UTC)
    startTime = currentTime - timedelta(hours=4)
    endTime = currentTime + timedelta(days=1)
    all_matchups = list(Matchup.objects.filter(time__range=(startTime, endTime)))
    context = {'all_matchups': all_matchups}
    return render(request, 'gameInfo/index.html', context)


def detail(request, matchup_id):
    matchup = get_object_or_404(Matchup, pk=matchup_id)
    all_bets = list(Bet.objects.filter(matchup_id=matchup_id))
    home_wins = list(Game.objects.filter(winning_team=matchup.home_team))
    home_losses = list(Game.objects.filter(losing_team=matchup.home_team))
    away_wins = list(Game.objects.filter(winning_team=matchup.away_team))
    away_losses = list(Game.objects.filter(losing_team=matchup.away_team))

    home_all = list(Game.objects.filter(home_team=matchup.home_team) | Game.objects.filter(away_team=matchup.home_team).order_by("-game_date"))
    home_last_ten = list(home_all[0:10])
    home_wins_last_ten = 0
    home_losses_last_ten = 0
    for game in home_last_ten:
        if game.winning_team==matchup.home_team:
            home_wins_last_ten += 1
        else:
            home_losses_last_ten += 1

    away_all = list(Game.objects.filter(home_team=matchup.away_team) | Game.objects.filter(away_team=matchup.away_team))
    away_last_ten = list(away_all[0:10])
    away_wins_last_ten = 0
    away_losses_last_ten = 0
    for game in away_last_ten:
        if game.winning_team == matchup.away_team:
            away_wins_last_ten += 1
        else:
            away_losses_last_ten += 1

    context = {
        'matchup': matchup,
        'all_bets': all_bets,
        'home_wins': len(home_wins),
        'home_losses': len(home_losses),
        'away_wins': len(away_wins),
        'away_losses': len(away_losses),
        'home_wins_last_ten': home_wins_last_ten,
        'home_losses_last_ten': home_losses_last_ten,
        'away_wins_last_ten': away_wins_last_ten,
        'away_losses_last_ten': away_losses_last_ten
    }
    return render(request, 'gameInfo/details.html', context)


def query_matchups(request):
    # delete_all()
    matchup_count = 0
    lines_count = 0

    response = requests.get(
        "https://api.the-odds-api.com/v4/sports/baseball_mlb/odds?regions=us&oddsFormat=american&apiKey=c0aa754dea26ec43e744af01ee995f42")

    if response.status_code != 200:
        return HttpResponseNotFound("Error loading new games")

    for game in response.json():

        matchup_id = game.get('id')
        homeTeam = Team.objects.get(team_name=game.get('home_team'))
        awayTeam = Team.objects.get(team_name=game.get('away_team'))
        matchup_title = awayTeam.team_name + " Vs " + homeTeam.team_name
        date_string = format_date(game.get('commence_time'))
        date = datetime.strptime(date_string, "%Y-%m-%d%H:%M:%S")
        date = date.replace(tzinfo=pytz.UTC)
        date = date.replace()
        matchup = Matchup(matchup_id=matchup_id, home_team=homeTeam, away_team=awayTeam, matchup_title=matchup_title,
                          time=date)

        if not matchup_exists(matchup):
            print(
                matchup.home_team_id + "_v_" + matchup.away_team_id + " doesn't exist, creating it now: " + matchup.matchup_id)
            matchup.save()
            matchup_count += 1
        else:
            matchup = Matchup.objects.get(pk=matchup.matchup_id)

        lines_count = update_lines(game, matchup, lines_count)

    return HttpResponse("Loaded {} new matchups and {} new lines in system".format(matchup_count, lines_count))


def matchup_exists(matchup):
    try:
        existing_matchup = Matchup.objects.get(pk=matchup.matchup_id)
        print(
            existing_matchup.home_team_id + "_v_" + existing_matchup.away_team_id + " already exists: " + existing_matchup.matchup_id)
        return True
    except ObjectDoesNotExist:
        return False


def format_date(date_string):
    date_string = date_string.replace('T', '')
    date_string = date_string.replace('Z', '')
    return date_string


def update_lines(game, matchup, lines_count):
    listOfBets = {}
    for bookmaker in game.get(
            "bookmakers"):  # create dictionary of Bet objects with tuple(bookmaker, bet_type, selected_team) as key
        for market in bookmaker.get("markets"):
            for outcome in market.get("outcomes"):
                selectedTeam = Team.objects.get(team_name=outcome.get('name'))
                bookie = bookmaker.get("key")
                bet_type = market.get("key")

                date_string = format_date(bookmaker.get('last_update'))
                date = datetime.strptime(date_string, "%Y-%m-%d%H:%M:%S")
                date = date.replace(tzinfo=pytz.UTC)
                date = date.replace()

                bet = Bet(matchup_id=matchup, selected_team=selectedTeam, bookmaker=bookie,
                          bet_type=bet_type, last_updated=date, price=outcome.get("price"), version=1)
                listOfBets[(bookie, bet_type, selectedTeam.team_id)] = bet

    # for each existing bet, if it is in dictionary and dict's last_updated is ahead of database version - update
    # for everything left in dictionary: create as bet

    bets_query_set = Bet.objects.filter(matchup_id=matchup.matchup_id)
    for existing_bet in bets_query_set:
        try:
            updated_bet = listOfBets[(existing_bet.bookmaker, existing_bet.bet_type, existing_bet.selected_team_id)]
        except KeyError:  # Bet is no longer getting returned - must be outdated remove from system
            existing_bet.delete()
        else:
            del listOfBets[(existing_bet.bookmaker, existing_bet.bet_type, existing_bet.selected_team_id)]
            if updated_bet.last_updated > existing_bet.last_updated:  # Updated bet is more recent, update DB
                updated_bet.bet_id = existing_bet.bet_id
                updated_bet.version = existing_bet.version + 1
                updated_bet.save()
                lines_count += 1

    for remaining_bet in listOfBets.values():
        remaining_bet.save()
        lines_count += 1
    return lines_count


def delete_all():
    all_matchups = Matchup.objects.all()
    print("Deleting", all_matchups.count(), "matchups")
    all_matchups.delete()

def game_exists(game):
    try:
        existing_game = Game.objects.get(pk=game.game_id)
        print(
            str(existing_game.game_id) + " already exists")
        return True
    except ObjectDoesNotExist:
        return False


def query_games(request):
    gameDict = statsapi.schedule(date=None, start_date="2022-04-07", end_date="2022-06-16", team="", opponent="",
                                 sportId=1, game_id=None)
    gameLoadCount = 0
    for game in gameDict:
        game_type = game.get('game_type')
        if game_type == 'R' or game_type == 'F' or game_type == 'D' or game_type == 'L' or game_type == 'W':
            game_id = game.get('game_id')
            game_date = game.get('game_date')
            print(game.get('away_id'))
            print(game.get('away_name'))
            away_team = Team.objects.get(team_num_id=game.get('away_id'))
            home_team = Team.objects.get(team_num_id=game.get('home_id'))
            doubleheader = game.get('doubleheader')
            game_num = game.get('game_num')
            home_probable_pitcher = game.get('home_probable_pitcher')
            away_probable_pitcher = game.get('away_probable_pitcher')
            home_pitcher_note = game.get('home_pitcher_note')
            away_pitcher_note = game.get('away_pitcher_note')
            home_score = game.get('home_score')
            away_score = game.get('away_score')
            venue_id = game.get('venue_id')
            venue_name = game.get('venue_name')
            if home_score > away_score:
                winning_team = home_team
                losing_team = away_team
            else:
                winning_team = away_team
                losing_team = home_team
            winning_pitcher = game.get('winning_pitcher')
            losing_pitcher = game.get('losing_pitcher')
            save_pitcher = game.get('save_pitcher')
            summary = game.get('summary')

            game_model = Game(game_id=game_id,
                              game_date=game_date,
                              game_type=game_type,
                              away_team=away_team,
                              home_team=home_team,
                              doubleheader=doubleheader,
                              game_num=game_num,
                              home_probable_pitcher=home_probable_pitcher,
                              away_probable_pitcher=away_probable_pitcher,
                              home_pitcher_note=home_pitcher_note,
                              away_pitcher_note=away_pitcher_note,
                              home_score=home_score,
                              away_score=away_score,
                              venue_id=venue_id,
                              venue_name=venue_name,
                              winning_team=winning_team,
                              losing_team=losing_team,
                              winning_pitcher=winning_pitcher,
                              losing_pitcher=losing_pitcher,
                              save_pitcher=save_pitcher,
                              summary=summary)
            if not game_exists(game_model):
                game_model.save()
                gameLoadCount += 1

    all_games = Game.objects.all
    print(all_games)
    return HttpResponse("Loaded {} new games".format(gameLoadCount))

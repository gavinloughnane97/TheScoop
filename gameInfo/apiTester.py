import statsapi
from gameInfo.models import Game, Team

gameDict = statsapi.schedule(date=None, start_date="2021-04-07", end_date="2022-06-16", team="", opponent="", sportId=1, game_id=None)

for game in gameDict:
    game_id = game.get('game_id')
    game_date = game.get('date')
    game_type = game.get('game_type')
    away_team = Team.objects.get(team_num_id=game.get('away_id'))
    home_team = Team.objects.get(team_num_id=game.get('home_id'))
    doubleheader = game.get('doubleheader')
    game_num = game.get(game_num)
    home_probable_pitcher = game.get(home_probable_pitcher)
    away_probable_pitcher = game.get(away_probable_pitcher)
    home_pitcher_note = game.get(home_pitcher_note)
    away_pitcher_note = game.get(away_pitcher_note)
    home_score = game.get(home_score)
    away_score = game.get(away_score)
    venue_id = game.get(venue_id)
    venue_name = game.get(venue_name)
    winning_team = Team.objects.get(team_name=game.get('winning_team'))
    losing_team = Team.objects.get(team_name=game.get('losing_team'))
    winning_pitcher = game.get(winning_pitcher)
    losing_pitcher = game.get(losing_pitcher)
    save_pitcher = game.get(save_pitcher)
    summary = game.get(summary)

    game_model = Game(game_id = game_id,
        game_date = game_date,
        game_type = game_type,
        away_team = away_team,
        home_team = home_team,
        doubleheader = doubleheader,
        game_num = game_num,
        home_probable_pitcher = home_probable_pitcher,
        away_probable_pitcher = away_probable_pitcher,
        home_pitcher_note = home_pitcher_note,
        away_pitcher_note = away_pitcher_note,
        home_score = home_score,
        away_score = away_score,
        venue_id = venue_id,
        venue_name = venue_name,
        winning_team = winning_team,
        losing_team = losing_team,
        winning_pitcher = winning_pitcher,
        losing_pitcher = losing_pitcher,
        save_pitcher = save_pitcher,
        summary = summary)

    game_model.save()

all_games = Game.objects.all
print(all_games)

#print(gameDict)
#if game_type != 'S' && status == "Final"

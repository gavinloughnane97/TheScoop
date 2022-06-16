import statsapi

gameDict = statsapi.schedule(date=None, start_date="2021-04-07", end_date="2022-06-16", team="", opponent="", sportId=1, game_id=None)

print(gameDict)


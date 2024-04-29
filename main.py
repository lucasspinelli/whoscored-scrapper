from csv_handler import CSVHandler
from web_scraper_manager import WebScraperManager
from primeira import Primeira
from terceira import Terceira

# Lista de URLs e diretórios
urls = [
    ("https://1xbet.whoscored.com/Regions/81/Tournaments/3/Seasons/9649/Stages/22128/TeamStatistics/Germany"
     "-Bundesliga-2023-2024", Primeira, "/home/leviatan/Documentos/league-data/bundesliga", "bundesliga"),
    ("https://1xbet.whoscored.com/Regions/252/Tournaments/7/Seasons/9622/Stages/22080/TeamStatistics/England"
     "-Championship-2023-2024", Primeira, "/home/leviatan/Documentos/league-data/championship", "championship"),
    ("https://1xbet.whoscored.com/Regions/155/Tournaments/13/Seasons/9705/Stages/22225/TeamStatistics/Netherlands"
     "-Eredivisie-2023-2024", Primeira, "/home/leviatan/Documentos/league-data/eredivisie", "eredivisie"),
    ("https://1xbet.whoscored.com/Regions/206/Tournaments/4/Seasons/9682/Stages/22176/TeamStatistics/Spain-LaLiga"
     "-2023-2024", Primeira, "/home/leviatan/Documentos/league-data/la-liga", "la-liga"),
    ("https://1xbet.whoscored.com/Regions/74/Tournaments/22/Seasons/9635/Stages/22105/TeamStatistics/France-Ligue-1"
     "-2023-2024", Primeira, "/home/leviatan/Documentos/league-data/league-one", "league-one"),
    ("https://1xbet.whoscored.com/Regions/177/Tournaments/21/Seasons/9730/Stages/22254/TeamStatistics/Portugal-Liga"
     "-2023-2024", Primeira, "/home/leviatan/Documentos/league-data/liga-portugal", "liga-portugal"),
    ("https://1xbet.whoscored.com/Regions/233/Tournaments/85/Seasons/9927/Stages/22796/TeamStatistics/USA-Major"
     "-League-Soccer-2024", Primeira, "/home/leviatan/Documentos/league-data/mls", "mls"),
    ("https://1xbet.whoscored.com/Regions/252/Tournaments/2/Seasons/9618/Stages/22076/TeamStatistics/England-Premier"
     "-League-2023-2024", Primeira, "/home/leviatan/Documentos/league-data/premier-league", "premier-league"),
    ("https://1xbet.whoscored.com/Regions/108/Tournaments/5/Seasons/9659/Stages/22143/TeamStatistics/Italy-Serie-A"
     "-2023-2024", Primeira, "/home/leviatan/Documentos/league-data/serie-a", "serie-a"),
    ("https://1xbet.whoscored.com/Regions/31/Tournaments/95/Seasons/10003/Stages/22961/TeamStatistics/Brazil"
     "-Brasileir%C3%A3o-2024", Primeira, "/home/leviatan/Documentos/league-data/brasileirao", "brasileirao"),

    ("https://1xbet.whoscored.com/Regions/81/Tournaments/3/Seasons/9649/Stages/22128/TeamStatistics/Germany"
     "-Bundesliga-2023-2024", Terceira, "/home/leviatan/Documentos/league-data/bundesliga", "bundesliga"),
    ("https://1xbet.whoscored.com/Regions/252/Tournaments/7/Seasons/9622/Stages/22080/TeamStatistics/England"
     "-Championship-2023-2024", Terceira, "/home/leviatan/Documentos/league-data/championship", "championship"),
    ("https://1xbet.whoscored.com/Regions/155/Tournaments/13/Seasons/9705/Stages/22225/TeamStatistics/Netherlands"
     "-Eredivisie-2023-2024", Terceira, "/home/leviatan/Documentos/league-data/eredivisie", "eredivisie"),
    ("https://1xbet.whoscored.com/Regions/206/Tournaments/4/Seasons/9682/Stages/22176/TeamStatistics/Spain-LaLiga"
     "-2023-2024", Terceira, "/home/leviatan/Documentos/league-data/la-liga", "la-liga"),
    ("https://1xbet.whoscored.com/Regions/74/Tournaments/22/Seasons/9635/Stages/22105/TeamStatistics/France-Ligue-1"
     "-2023-2024", Terceira, "/home/leviatan/Documentos/league-data/league-one", "league-one"),
    ("https://1xbet.whoscored.com/Regions/177/Tournaments/21/Seasons/9730/Stages/22254/TeamStatistics/Portugal-Liga"
     "-2023-2024", Terceira, "/home/leviatan/Documentos/league-data/liga-portugal", "liga-portugal"),
    ("https://1xbet.whoscored.com/Regions/233/Tournaments/85/Seasons/9927/Stages/22796/TeamStatistics/USA-Major"
     "-League-Soccer-2024", Terceira, "/home/leviatan/Documentos/league-data/mls", "mls"),
    ("https://1xbet.whoscored.com/Regions/252/Tournaments/2/Seasons/9618/Stages/22076/TeamStatistics/England-Premier"
     "-League-2023-2024", Terceira, "/home/leviatan/Documentos/league-data/premier-league", "premier-league"),
    ("https://1xbet.whoscored.com/Regions/108/Tournaments/5/Seasons/9659/Stages/22143/TeamStatistics/Italy-Serie-A"
     "-2023-2024", Terceira, "/home/leviatan/Documentos/league-data/serie-a", "serie-a"),
    ("https://1xbet.whoscored.com/Regions/31/Tournaments/95/Seasons/10003/Stages/22961/TeamStatistics/Brazil"
     "-Brasileir%C3%A3o-2024", Terceira, "/home/leviatan/Documentos/league-data/brasileirao", "brasileirao"),

]

ligas = [
    ('/home/leviatan/Documentos/league-data/bundesliga', 'bundesliga'),
    ('/home/leviatan/Documentos/league-data/championship', 'championship'),
    ('/home/leviatan/Documentos/league-data/eredivisie', 'eredivisie'),
    ('/home/leviatan/Documentos/league-data/la-liga', 'la-liga'),
    ('/home/leviatan/Documentos/league-data/league-one', 'league-one'),
    ('/home/leviatan/Documentos/league-data/liga-portugal', 'liga-portugal'),
    ('/home/leviatan/Documentos/league-data/mls', 'mls'),
    ('/home/leviatan/Documentos/league-data/premier-league', 'premier-league'),
    ('/home/leviatan/Documentos/league-data/serie-a', 'serie-a'),
    ('/home/leviatan/Documentos/league-data/brasileirao', 'brasileirao'),

]

# Inicializando e configurando o gerenciador
scraper_manager = WebScraperManager()
for url, scraper_class, directory, file_name_pattern in urls:
    scraper_manager.add_config(scraper_class, url, directory, file_name_pattern)


scraper_manager.run_scrapers()


for csv_path, league_name in ligas:
    handler = CSVHandler(csv_path, league_name)
    handler.process_csv_directory()




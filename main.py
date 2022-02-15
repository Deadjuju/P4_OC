from menu.menu import MenuView, MainMenu
from views.player import PlayerView
from views.tournament import TournamentView
from views.reports import ReportsView


# views creation
menu_view = MenuView
player_view = PlayerView()
tournament_view = TournamentView()
reports_view = ReportsView()

# start program
main_menu = MainMenu(view=menu_view,
                     player_view=player_view,
                     tournament_view=tournament_view,
                     reports_view=reports_view)
main_menu.menu_run()

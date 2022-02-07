from models.person import Player
from initialisation import PLAYERS_TABLE


class GenerationOfPairs:

    def __init__(self, players_id_list):
        self.players_id_list = players_id_list

    def swiss_system(self):
        players_unsorted_list = []
        players_instance_list = []

        # get all player's instance but unsorted
        for player_id in self.players_id_list:
            player_dict: dict = PLAYERS_TABLE.get(doc_id=player_id)
            players_instance = Player(**player_dict)
            players_unsorted_list.append(players_instance)

        # tant qu'il y a des instances
        while len(players_unsorted_list) > 0:
            provisional_players_instance_list = []

            # Generate score list
            players_score_list = []
            for player in players_unsorted_list:
                players_score_list.append(player.tournament_score)
            # print(f"||DEBUG -> SCORE LIST: {players_score_list}")

            max_value = None
            ids_list = []

            # Get value max from Generate score list
            for player in players_score_list:
                if max_value is None or player > max_value:
                    max_value = player

            # Get indices == max value
            for i in range(len(players_score_list)):
                if players_score_list[i] == max_value:
                    ids_list.append(i)

            # put max player in provisional_players_instance_list and delete it from players_unsorted_list
            # sort provisional_players_instance_list
            # get this list in players_instance_list.append(provisional_players_instance_list)
            for i in range(len(players_unsorted_list), -1, -1):
                if i in ids_list:
                    player = players_unsorted_list.pop(i)
                    provisional_players_instance_list.append(player)

                provisional_players_instance_list.sort()

            players_instance_list += provisional_players_instance_list
            # print(f"||DEBUG -> LISTE: {players_instance_list}")

        # print(f"|| DEBUG ->\n"
        #       f"|| PLAYERS INSTANCE LIST: \n"
        #       f"|| {players_instance_list}\n")

        # cut players_instance_list in 2 lists: bests and worsts
        half_player_list_length = int(len(players_instance_list) / 2)
        best_players_list = players_instance_list[:half_player_list_length]
        worst_players_list = players_instance_list[half_player_list_length:]

        # Générer les paires
        # Le meilleur de chaque liste s'affronte et est retiré de la liste
        # -> Adversaire marqué dans la liste des adversaires
        # Et on recommence tant qu'il y a des joueurs

        print("-" * 50)
        pairs_list = []
        for _ in range(half_player_list_length):
            i = 0
            pair_find = False

            best1: Player = best_players_list.pop(0)
            best2 = None

            while not pair_find:

                player2 = worst_players_list[i]

                if player2 not in best1.already_faced:
                    best2 = worst_players_list.pop(0 + i)

                    best1.already_faced.append(best2)
                    best2.already_faced.append(best1)

                    pair_find = True
                else:
                    # print("Déjà rencontré")
                    i += 1

            pair = (best1, best2)
            print(pair)
            pairs_list.append(pair)

        # # DEBUG POINT
        # print(pairs_list)
        # print(" --------- PAIRS: ---------")
        # for pair in pairs_list:
        #     print(pair[0].__dict__)
        #     print(pair[1].__dict__)

        return pairs_list


if __name__ == '__main__':

    players_id_list = [1, 2, 6, 8, 3, 4, 5, 7]
    generating_pairs = GenerationOfPairs(players_id_list=players_id_list)
    pairs = generating_pairs.swiss_system()
    print(pairs)


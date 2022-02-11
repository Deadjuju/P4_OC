from models.person import Player
from initialisation import PLAYERS_TABLE


class GenerationOfPairs:

    def __init__(self, players_id_list):
        self.players_id_list = players_id_list

    # def get_instances_list(self) -> list:
    #     players_unsorted_list = []
    #     # get all player's instance but unsorted
    #     for player_id in self.players_id_list:
    #         player_dict: dict = PLAYERS_TABLE.get(doc_id=player_id)
    #         players_instance = Player(**player_dict)
    #         players_unsorted_list.append(players_instance)
    #     return players_unsorted_list
    #
    @classmethod
    def sort_the_list(cls, players_unsorted_list):

        players_instance_list_sorted = []

        while len(players_unsorted_list) > 0:
            provisional_players_instance_list = []

            # Generate score list
            players_score_list = []
            for player in players_unsorted_list:
                players_score_list.append(player.tournament_score)

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
            # get this list in players_instance_list_sorted
            for i in range(len(players_unsorted_list), -1, -1):
                if i in ids_list:
                    player = players_unsorted_list.pop(i)
                    provisional_players_instance_list.append(player)

                provisional_players_instance_list.sort()

            players_instance_list_sorted += provisional_players_instance_list
        return players_instance_list_sorted

    @classmethod
    def generate_pairs_list(cls, half_player_list_length, players_instance_list):
        # Générer les paires
        # Le meilleur de chaque liste s'affronte et est retiré de la liste
        # -> Adversaire marqué dans la liste des adversaires
        # Et on recommence tant qu'il y a des joueurs

        print("-" * 50)

        # Split player instances into two lists
        best_players_list = players_instance_list[:half_player_list_length]
        worst_players_list = players_instance_list[half_player_list_length:]

        # Create the pairs
        # Check if the players have not already faced each other
        pairs_list = []
        for _ in range(half_player_list_length):
            i = 0
            pair_find = False

            best1: Player = best_players_list.pop(0)
            player1_id = Player.search_player(first_name=best1.first_name,
                                              last_name=best1.last_name)[0].doc_id
            best2 = None

            while not pair_find:

                player2 = worst_players_list[i]
                player2_id = Player.search_player(first_name=player2.first_name,
                                                  last_name=player2.last_name)[0].doc_id
                print("PLAYER 2 ID")
                print(player2_id)

                if player2_id not in best1.already_faced:
                    best2 = worst_players_list.pop(0 + i)
                    print(best2)
                    print(best2.already_faced)
                    print(type(best2))

                    best1_already_faced = best1.already_faced
                    best2_already_faced = best2.already_faced

                    best1_already_faced.append(player2_id)
                    best2_already_faced.append(player1_id)

                    # save already_faced in db
                    attribute = "already_faced"
                    best1.update_attribute(
                        new_attribute_value=best1_already_faced,
                        attribute_name=attribute,
                        player_id=player1_id
                    )
                    best2.update_attribute(
                        new_attribute_value=best2_already_faced,
                        attribute_name=attribute,
                        player_id=player2_id
                    )

                    pair_find = True
                    i = 0
                else:
                    i += 1

            pair = (best1, best2)
            pairs_list.append(pair)

        return pairs_list

    def swiss_system(self):
        # players_unsorted_list = self.get_instances_list()
        players_unsorted_list = Player.get_players_instances_list(
            players_id_list=self.players_id_list
        )
        players_instance_list_sorted = self.sort_the_list(
            players_unsorted_list=players_unsorted_list
        )

        # cut players_instance_list_sorted in 2 lists: bests and worsts
        half_player_list_length = int(len(players_instance_list_sorted) / 2)

        pairs_list = self.generate_pairs_list(
            half_player_list_length=half_player_list_length,
            players_instance_list=players_instance_list_sorted
        )

        return pairs_list


if __name__ == '__main__':
    players_id_list = [1, 2, 6, 8, 3, 4, 5, 7]
    generating_pairs = GenerationOfPairs(players_id_list=players_id_list)
    pairs = generating_pairs.swiss_system()
    print(pairs)

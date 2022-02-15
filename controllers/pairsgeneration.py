from typing import List

from models.person import Player


class GenerationOfPairs:
    """ Generate player pairs """

    def __init__(self, players_id_list):
        self.players_id_list = players_id_list

    @classmethod
    def _sort_the_list(cls, players_unsorted_list: List[Player]):
        """Make action to edit a player or to delete it

                Args:
                    players_unsorted_list (list): List of player instances Unsorted
                Return:
                    players_instance_list_sorted (list): List of player instances Sorted
                                                         by their rank in a tournament
                                                         and their total rank
                """

        players_instance_list_sorted = []

        while len(players_unsorted_list) > 0:
            provisional_players_instance_list = []

            # Generate score list
            players_score_list = [player.tournament_score for player in players_unsorted_list]

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
    def _generate_pairs_list(cls,
                             half_player_list_length: int,
                             players_instance_list: List[Player]):
        """Generates new pairs of players according to their order

                Args:
                    half_player_list_length (int): Half length of players list
                    players_instance_list (list): List of worst players
                Return:
                    players_instance_list_sorted (list): List of player instances Sorted
                """

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

                if player2_id not in best1.already_faced:
                    best2 = worst_players_list.pop(0 + i)

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
        """Swiss System Algorithm

                Return:
                    List of player pairs
                """
        # players_unsorted_list = self.get_instances_list()
        players_unsorted_list = Player.get_players_instances_list(
            players_id_list=self.players_id_list
        )
        players_instance_list_sorted = self._sort_the_list(
            players_unsorted_list=players_unsorted_list
        )

        # cut players_instance_list_sorted in 2 lists: bests and worsts
        half_player_list_length = int(len(players_instance_list_sorted) / 2)

        pairs_list = self._generate_pairs_list(
            half_player_list_length=half_player_list_length,
            players_instance_list=players_instance_list_sorted
        )

        return pairs_list


if __name__ == '__main__':
    players_id_list_example = [1, 2, 6, 8, 3, 4, 5, 7]
    generating_pairs_for_test = GenerationOfPairs(players_id_list=players_id_list_example)
    pairs = generating_pairs_for_test.swiss_system()
    print(pairs)

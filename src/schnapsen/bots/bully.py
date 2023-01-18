from random import Random
from typing import Optional
from schnapsen.game import \
    Bot, PlayerPerspective, Move, SchnapsenTrickScorer


class BullyBot(Bot):
    def __init__(self, rand: Random) -> None:
        """
        Create a new bully bot.

        :param rand: the source of randomness for this Bot
        """
        self.rand = rand

    def get_move(
        self,
        player_perspective: PlayerPerspective,
        leader_move: Optional[Move],
    ) -> Move:
        """
        Gets the list of valid moves. If the bot is the leader, it will
        play a random card of the trump suit if it has one. If the bot
        is the follower, it will play a random card of the same suit of
        the card of the leader if it has one. Otherwise, it will play
        the card with the highest number of points.

        :param player_perspective: perspective bot has on the game state
        :param leader_move: move the leader has played
        :returns: a move
        """
        moves = player_perspective.valid_moves()
        scorer = SchnapsenTrickScorer()
        max_points = float('-inf')
        leader_suit_moves = []
        trump_suit_moves = []

        # TODO Remove code below if line 44 works
#        if leader_move:
#            leader_card = leader_move._cards()[0]
#        else:
#            leader_card = None

        leader_card = leader_move._cards()[0] if leader_move else None

        for move in moves:
            card = move._cards()[0]
            points = scorer.rank_to_points(card.rank)

            if leader_move and card.suit == leader_card.suit:
                leader_suit_moves.append(move)

            if card.suit == player_perspective.get_trump_suit():
                trump_suit_moves.append(move)

            if points > max_points:
                max_points = points
                max_point_move = move

        if trump_suit_moves and player_perspective.am_i_leader():
            return self.rand.choice(trump_suit_moves)
        elif leader_suit_moves and not player_perspective.am_i_leader():
            return self.rand.choice(leader_suit_moves)
        else:
            return max_point_move

    def __repr__(self) -> str:
        return f"BullyBot()"
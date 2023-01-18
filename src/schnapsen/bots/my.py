from random import Random
from typing import Optional
from schnapsen.game import \
    Bot, PlayerPerspective, Move, SchnapsenTrickScorer


class MyBot(Bot):
    def __init__(self, rand: Random) -> None:
        """
        Creates a new my bot.

        :param rand: the source of randomness for this Bot
        """
        self.rand = rand

    def get_move(
        self,
        player_perspective: PlayerPerspective,
        leader_move: Optional[Move],
    ) -> Move:
        """
        Gets the list of valid moves. If this bots' score is lowe than
        its opponent's, it tries to play a marriage or a trump exchange.
        If not, it tries to play the same suit it played in the previous
        turn, and picks the card with the lowest points if there are
        multiple of this suit. Otherwise, it plays a random valid move.

        :param player_perspective: perspective bot has on the game state
        :param leader_move: move the leader has played
        :returns: a move
        """
        moves = player_perspective.valid_moves()

        my_score = player_perspective.get_my_score().direct_points
        opponent_score = player_perspective.get_opponent_score().direct_points
        lower_score = my_score < opponent_score
        trump_suit = player_perspective.get_trump_suit()

        if not leader_move and lower_score:
            for move in moves:
                if move.is_marriage() and move.suit == trump_suit:
                    low_score_move = move
                    setattr(self, 'prev_move', low_score_move)

                    return low_score_move

                if move.is_trump_exchange():
                    low_score_move = move
                    setattr(self, 'prev_move', low_score_move)

                    return low_score_move

                if move.is_marriage():
                    low_score_move = move
                    setattr(self, 'prev_move', low_score_move)

                    return low_score_move

        try:
            prev_suit = self.prev_move._cards()[0].suit
        except:
            prev_suit = None

        prev_suit_moves = []

        scorer = SchnapsenTrickScorer()
        min_points = float('+inf')

        if prev_suit:
            for move in moves:
                card = move._cards()[0]

                if card.suit == prev_suit:
                    prev_suit_moves.append(move)

        if prev_suit_moves:
            for move in prev_suit_moves:
                card = move._cards()[0]
                points = scorer.rank_to_points(card.rank)

                if points < min_points:
                    min_points = points
                    min_point_move = move

            setattr(self, 'prev_move', min_point_move)

            return min_point_move
        else:
            rand_move = self.rand.choice(moves)
            setattr(self, 'prev_move', rand_move)

            return rand_move

    def __repr__(self) -> str:
        return f"MyBot()"
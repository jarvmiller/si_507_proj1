# Do not change import statements.
import unittest
from SI507F17_project1_cards import *

"""
Write your unit tests to test the cards code here.
You should test to ensure that everything explained in the code description
file works as that file says. If you have correctly written the tests, at
least 3 tests should fail. If more than 3 tests fail, it should be because
multiple of the test methods address the same problem in the code.
You may write as many TestSuite subclasses as you like, but you should try to
make these tests well-organized and easy to read the output.
You should invoke the tests with verbosity=2 (make sure you invoke them!)
"""
###########


class CardTest(unittest.TestCase):

    def test_init_default(self):
        card = Card()
        self.assertEqual(card.suit, "Diamonds")
        self.assertEqual(card.rank, 2)

    def test_rank_strings(self):
        rank_dict = {11: "Jack", 12: "Queen", 13: "King", 1: "Ace"}
        for rank_num, rank_str in rank_dict.items():
            card = Card(rank=rank_num)
            self.assertEqual(card.rank, rank_str)
            self.assertEqual(card.rank_num, rank_num)

    def test_str_method(self):
        # Should be an Ace of Diamonds
        card = Card(0, 1)
        self.assertTrue(card.__str__() == "Ace of Diamonds",
                        "Testing that card reads 'Ace of Diamonds'. " \
                        "it instead reads '%s'. This implies " \
                        "that testing the deck str method " \
                        "will also cause failure" %card.__str__())

class DeckTest(unittest.TestCase):

    def test_init(self):
        deck = Deck()
        # Ensure 52 different cards
        self.assertEqual(len(set(deck.cards)), 52)

    def test_shuffle(self):
        deck = Deck()
        cards = deck.cards.copy()
        deck.shuffle()
        # Ensure different order
        self.assertFalse(cards[0].__str__() == deck.cards[0].__str__())

        # Ensure both lists contain the same elts
        cards_intersect = list(set(cards) & set(deck.cards))
        self.assertEqual(len(cards_intersect), 52)

    def test_pop(self):
        deck = Deck()
        card_popped = deck.pop_card()

        # Ensure card_popped is of type Card
        self.assertTrue(isinstance(card_popped, Card))

        # Ensure 51 different cards
        self.assertEqual(len(set(deck.cards)), 51)

        # Ensure deck is empty after popping all cards
        for i in range(51):
            deck.pop_card()
        self.assertTrue(deck.cards == [])

    def test_replace(self):
        deck = Deck()
        card_popped = deck.pop_card()
        deck.replace_card(card_popped)
        self.assertTrue(card_popped in deck.cards)

        # Ensure deck isn't modified when adding card
        # to a full deck
        card_extra = deck.cards[0]
        cards = deck.cards.copy()
        deck.replace_card(card_extra)
        self.assertTrue(deck.cards == cards)

        # Ensure deck isn't modified when adding duplicate card
        # even though it is no longer full
        card_popped = deck.pop_card()
        cards = deck.cards.copy()
        card_extra = deck.cards[1]
        deck.replace_card(card_extra)
        self.assertTrue(deck.cards == cards)

        self.assertFalse(card_popped in deck.cards)

    def test_sort(self):
        deck = Deck()

        # Ensure in the order diamonds, clubs, hearts, spades
        for i in range(52):
            if i < 13:
                self.assertTrue(deck.cards[i].suit == "Diamonds")
            elif i < 26:
                self.assertTrue(deck.cards[i].suit == "Clubs")
            elif i < 39:
                self.assertTrue(deck.cards[i].suit == "Hearts")
            else:
                self.assertTrue(deck.cards[i].suit == "Spades")

        # sort after cards have been removed
        deck.sort_cards()
        first_two_cards = deck.cards[0:2].copy()

        # remove everything but the first two cards
        for i in range(50):
            deck.pop_card()
        deck.shuffle()
        deck.sort_cards()
        self.assertEqual(len(deck.cards), 2,
                         "Sort doesn't work for remaining cards, it just " \
                         "recreates the full deck")
        self.assertEqual(first_two_cards, deck.cards)

    def test_deal(self):
        deck = Deck()
        dealt_card = deck.deal_hand(1)
        self.assertTrue(isinstance(dealt_card, list))
        self.assertEqual(len(deck.cards), 51)
        deck.replace_card(dealt_card)
        """
        This fails with an index error. The error is probably because the
        programmer is popping deck.cards[i] while i ranges from 0 to 52.
        deck.cards is being depleted so after half the cards are gone,
        there is no 27th entry in the list. At least, this is my suspicion
        """
        cards = deck.deal_hand(27)


class WarGameTest(unittest.TestCase):

    def test_play_war_game(self):
        game_rslt = play_war_game(testing=True)
        self.assertTrue(isinstance(game_rslt, tuple))
        self.assertTrue(game_rslt[0], str)
        self.assertTrue(game_rslt[0] in ['Player1', 'Player2', "Tie"])

        # Be sure the game is fair
        if game_rslt[0] == "Player1":
            self.assertGreater(game_rslt[1], game_rslt[2])
        elif game_rslt[0] == "Player2":
            self.assertGreater(game_rslt[2], game_rslt[1])
        else:
            self.assertEqual(game_rslt[1], game_rslt[2])

class SongTest(unittest.TestCase):
    def test_show_song(self):
        song_input = 'Billie Jean'
        num_searches = 5
        song_list = [show_song(song_input) for i in range(num_searches)]
        self.assertTrue(isinstance(song_list[0], helper_functions.Song))
        search_worked = False
        for song in song_list:
            if song_input in str(song):
                search_worked = True
        if not search_worked:
            self.assertTrue(song_input in str(song_list[0]),
                            "Search term %s is not included in song title in" \
                            " any of the 5 searches. Function fails to work" \
                            " for any search term as described" % song_input)

unittest.main(verbosity=2)


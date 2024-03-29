import math


def set_score(group, score_dict):
    # Sets have all cards of the same value, and a minimum size of 2.
    if len(group) > 1 and all(card[0] == group[0][0] for card in group[1:]):
        # score = value * number!
        return score_dict[group[0][0]] * math.factorial(len(group))
    return 0


def run_score(cards, score_dict):
    suits = [[], []]  # Store values of cards, separated by suit colour. Index 0 is black cards.
    number_list = [0] * 21  # Store frequency of each possible score. Index is the score, value is the frequency.

    # Create lists containing the scores of red cards and black cards
    # Create bit-list with the frequency of each card score
    for card in cards:
        card_score = score_dict[card[0]]
        suits[int(card[1] in "HD")].append(card_score)
        number_list[card_score] += 1

    # Score for runs
    # Runs must have no more than one of each card value (excluding aces), and have a minimum length of 3.
    if len(cards) > 2 and all(number <= 1 for number in number_list[:-1]):
        # number_list must now contain only values 0 or 1 in all indexes except for 20.
        # Get first card index (first non-zero index in number_list)
        card_index = 0
        while number_list[card_index] != 1:
            card_index += 1
        # Store current suit as a boolean, so can flip between red and black with a single operation.
        current_suit = card_index in suits[1]

        score = card_index
        # get next cards
        for i in range(1, len(cards)):
            card_index += 1
            current_suit = not current_suit
            if not (number_list[card_index] == 1 and card_index in suits[current_suit]):
                # No consecutive card with correct colour.
                # Try using an ace of correct colour. Cannot use if in last position.
                if 20 in suits[current_suit] and i < len(cards) - 1:
                    suits[current_suit].remove(20)
                else:
                    # No aces available, cannot make the run
                    return 0
            # Made the run with either a normal card or an ace. Increase the score by the card value.
            score += card_index
        return score
    return 0


def get_group_score(group):
    score_dict = {
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "0": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 20
    }  # Lookup table for scores of each card
    score = 0

    # Check for set
    score += set_score(group, score_dict)

    # Check for run
    if score == 0:
        score += run_score(group, score_dict)

    # Score as single cards
    if score == 0:
        score += -sum(score_dict[card[0]] for card in group)

    return score


if __name__ == '__main__':
    groups = [
        ['2C'],
        ['2C', '2S'],
        ['4C', '4H', '4S'],
        ['4C', '4H', '3S'],
        ['4C', '4H', 'AS'],
        ['KC', 'KH', 'KS', 'KD'],
        ['2C', '3D', '4S'],
        ['4S', '2C', '3D'],
        ['2C', '3D', '4H'],
        ['2C', '3D'],
        ['2C', 'AD', '4S'],
        ['5H', '2C', 'AD', '4S'],
        ['3C', '4H', 'AS'],
        ['4H', '0H', 'JC', '2H', '7H'],
        ['2C', 'AD', 'AS', 'AH', '6C'],
        ['2C', 'AD', 'AS', 'AH', '7C'],
        ['2C', 'AD', 'AS', 'AC', '6C'],
    ]
    scores = [
        -2,
        4,
        24,
        -11,
        -28,
        312,
        9,
        9,
        -9,
        -5,
        9,
        14,
        -27,
        -34,
        20,
        -69,
        -68
    ]

    for test_index in range(len(groups)):
        assert len(groups) == len(scores), "{} != {}".format(len(groups), len(scores))
        assert get_group_score(groups[test_index]) == scores[test_index],\
            "failed on test {}: {}. {} != {}".format(test_index, groups[test_index], get_group_score(groups[test_index]), scores[test_index])

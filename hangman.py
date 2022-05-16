#################################################################
# FILE : hangman.py
# WRITER : orin pour , orin1 , 207377649
# EXERCISE : intro2cs2 ex4 2021
# DESCRIPTION:this file contain the hangman game
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED:https://www.w3schools.com/python/ref_string_isalpha.asp
# NOTES: ...
#################################################################
import hangman_helper as hp


def create_pattern(word):
    """" this function create a pattern of ____ from a given word"""
    pattern = '_' * len(word)
    return pattern


def game_restart(words_list):
    """" this function is restarting the game by selecting a new word
    the function return the selected word"""
    word = hp.get_random_word(words_list)
    return word


def user_input_checking(user_input, pattern, word, score,
                        wrong_guess_lst, words_list, message):
    """this function deal with each choice of input"""
    input_type, word_or_letter = user_input

    # input type is letter
    if input_type == hp.LETTER:
        message, pattern, score, wrong_guess_lst = input_is_letter(
            word_or_letter, pattern, word, score, wrong_guess_lst, message)
    # input type is word
    if input_type == hp.WORD:
        pattern, score, message = word_choice(word_or_letter, pattern, word,
                                              score, message)
    # input type is hint
    if input_type == hp.HINT:
        score, small_hint_list = input_is_hint(words_list, pattern,
                                               wrong_guess_lst, score)
    return score, pattern, wrong_guess_lst, message


def input_is_letter(word_or_letter, pattern, word, score,
                    wrong_guess_lst, message):
    """this function check if the letter is valid and than check if its in the
    word"""
    # if letter is invalid
    if check_letter_validation(word_or_letter) is False:
        message = "input is invalid"
        return message, pattern, score, wrong_guess_lst
    # if letter is valid
    else:
        return letter_choice(word_or_letter, pattern, word, score,
                             wrong_guess_lst, message)


def check_letter_validation(letter):
    """"this func check if the user input is valid
    # if letter contain more than 1 char> return false
    # if letter is upper cases> return false
    # if letter is not alphabet> return False"""
    if len(letter) != 1 or letter.isupper() or letter.isalpha() is False:
        return False
    return True


def letter_choice(letter, pattern, word, score, wrong_guess_lst, message):
    """" this function check if the letter guess is right or wrong and use the
    right function and present the score"""
    if not check_if_letter_was_already_chosen(letter, pattern,
                                              wrong_guess_lst):
        score -= 1
        letter_appears = letter_appears_number(letter, word)
        if letter_appears == 0:
            wrong_guess_lst = letter_guess_is_wrong(wrong_guess_lst, letter,
                                                    score)
        else:
            pattern, score = letter_guess_is_right(pattern, letter,
                                                   letter_appears, word, score)
    else:
        message = "letter was already chosen"
    return message, pattern, score, wrong_guess_lst


def check_if_letter_was_already_chosen(letter, pattern, wrong_guess_lst):
    """" this function check if the letter is already in the wrong guess list
    or in the word> return True"""
    if (letter in wrong_guess_lst) or (letter in pattern):
        return True
    return False


def letter_appears_number(letter, word):
    """" this function return the number of the letter appears in the word """
    letter_appears = 0
    # checking the number of letter appears
    for i in word:
        if letter == i:
            letter_appears += 1
    return letter_appears


def letter_guess_is_wrong(wrong_guess_lst, letter, score):
    """this function add the letter to the wrong_guess_lst and update the
    score"""
    wrong_guess_lst.append(letter)
    score -= 1
    return wrong_guess_lst


def letter_guess_is_right(pattern, letter, letter_appears, word, score):
    """this function update the word pattern and update the score according to
    the word appears"""
    pattern = update_word_pattern(word, pattern, letter)
    score += (letter_appears * (letter_appears + 1)) // 2
    return pattern, score


def update_word_pattern(word, pattern, letter):
    """" this function gets a word, a pattern and a letter and return the
     pattern with the letter in the right place"""
    new_pattern = ""
    for i in range(len(word)):
        if word[i] == letter:
            # replacing the char in the pattern with the letter
            new_pattern = new_pattern + letter
        else:
            new_pattern = new_pattern + pattern[i]
    return new_pattern


def word_choice(word_input, pattern, word, score, message):
    """" this function check if the word guess is right or wrong
    and return the score"""
    score -= 1
    if word_input == word:
        message = "your guess is right"
        pattern, score = word_guess_is_right(pattern, word_input, score)
    else:
        message = "your guess is wrong"
    return pattern, score, message


def word_guess_is_right(pattern, word_input, score):
    """this function update the score according to the letters appears"""
    letter_appears = 0
    for i in range(len(pattern)):
        if word_input[i] != pattern[i]:
            letter_appears += 1
    score += (letter_appears * (letter_appears + 1)) // 2
    pattern = word_input
    return pattern, score


def word_can_be_hint(single_word, pattern, wrong_guess_lst):
    """this func check if the word can be a hint:
    if the word has letters from the wrong_guess_lst or different letters from
     the pattern or has a letter in several places> return False"""
    if len(single_word) == len(pattern):
        for i in range(len(pattern)):
            # if the letter in the word is in the wrong_guess_lst
            if single_word[i] in wrong_guess_lst:
                return False
            # if the letter is in not in the pattern
            if (pattern[i] != '_') and (single_word[i] != pattern[i]):
                return False
            # if the letter appear in the word more than once in different
            # location than the pattern
            if (pattern[i] != '_') and (single_word.count(single_word[i]) !=
                                        pattern.count(pattern[i])):
                return False
        return True
    return False


def input_is_hint(words_list, pattern, wrong_guess_lst, score):
    """this func update the score and return an hint list and the score"""
    score -= 1
    small_hint_list = []
    hint_length = hp.HINT_LENGTH
    # create a filter words list
    hint_list = filter_words_list(words_list, pattern, wrong_guess_lst)
    n = len(hint_list)
    # if the hint list is bigger than hint_length parameter> make it smaller
    if n > hint_length:
        for i in range(hint_length):
            small_hint_list.append(hint_list[(i * n) // hint_length])
    else:
        # if the hint list is smaller than the hint_length parameter> return
        # the entire hint list
        small_hint_list = hint_list
        # present the hint suggestion
    hp.show_suggestions(small_hint_list)
    return score, small_hint_list


def filter_words_list(word_list, pattern, wrong_guess_lst):
    """this function check for each word in the word list if it can be an hint
    > if yes add it to the hint list"""
    hint_list = []
    for single_word in word_list:
        if word_can_be_hint(single_word, pattern, wrong_guess_lst):
            hint_list.append(single_word)
    return hint_list


def run_single_game(words_list, score):
    """this function run a single game with one word"""
    wrong_guess_lst = []
    # restart the game > select a new word
    word = game_restart(words_list)
    message = "game started"
    pattern = create_pattern(word)
    # if the player has points and didn't guess the word yet
    while score > 0 and pattern != word:
        # print the current state of the user
        hp.display_state(pattern, wrong_guess_lst, score, message)
        # ask for input
        score, pattern, wrong_guess_lst, message = user_input_checking(
                hp.get_input(), pattern, word, score, wrong_guess_lst,
                words_list,
                message)
    # if the player guessed the word
    if pattern == word:
        message = "you won"
    else:
        message = f"you loose, the word was: {word}"
    # print the current state of the user
    hp.display_state(pattern, wrong_guess_lst, score, message)
    return score


def main():
    games_num = 0
    score = hp.POINTS_INITIAL
    words_list = hp.load_words(file='words.txt')
    while score >= 0:
        games_num += 1
        score = run_single_game(words_list, score)
        if score == 0:
            message = f"number of games: {games_num}, your score is: {score}" \
                      f", would you like to start a new game?"
            games_num = 0
            score = hp.POINTS_INITIAL
        else:
            message = f"number of games: {games_num}, your score is: {score}" \
                      f", would you like to play again?"
        if not hp.play_again(message):
            break


if __name__ == "__main__":
    main()

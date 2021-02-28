import random


class Style():
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    RESET = '\033[0m'

    def show(self,sentence):
        sentence=str(sentence)
        lst=[ Style.RED, Style.GREEN, Style.YELLOW , Style.BLUE, Style.MAGENTA, Style.CYAN, Style.RESET]
        senc=""
        for word in sentence:
            new_word=""
            for char in word:
                rand_color=random.choice(lst)
                new_word+=(rand_color + char)
            senc+=new_word
        print(senc)





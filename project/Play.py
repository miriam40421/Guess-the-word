import random

# פונקציית הגרלת המילה
def random_word(num = int(input("enter number:"))):
    file = open("./Words", 'r')
    list_word = file.readlines()
    random.shuffle(list_word)
    word = list_word[num % list_word.__len__()]
    return word
import language_tool_python
from spellchecker import SpellChecker
spell = SpellChecker()

def make_correct(text):
    correct = ""
    char = [",",":","!","?","@","#","$","%","&","*","(",")","+","-"]
    list = text.split(" "); words_dic = {}; special_care = []
    for i in range(len(list)): words_dic[i] = list[i]
    for i in range(len(list)):
        if words_dic[i] != "" and (words_dic[i][len(words_dic[i])-1] in char):
            special_care.append(i)
    tool = language_tool_python.LanguageTool('en-US')
    tool.enable_spellchecking()
    for word in words_dic.keys():
        if word in special_care:
            correct += spell.correction(words_dic[word][:len(words_dic[word])-1])+words_dic[word][len(words_dic[word])-1]+" "
        else:
            correct += spell.correction(words_dic[word])+" "
    return tool.correct(correct)




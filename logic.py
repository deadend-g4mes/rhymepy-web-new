from pyscript import fetch, document
import re
import asyncio
import json

url='https://api.datamuse.com/words?'
rhymes_struct = {}
poem = []
rhyming_words = []
colors = ["Gold", "MediumTurquoise", "LightCoral", "LightGreen", "LawnGreen", "LightPink", "LightSalmon", "LightSkyBlue", "Orange", "Violet", "Plum", "PaleTurquoise", "Bisque"]

async def fetch_rhymes(word, option):
    datamuse_response = []
    rhymes_list = []

    if option == 0:
        response = await fetch(url + "rel_rhy=" + word, method="GET")
        datamuse_response = response.json()
    
    elif option == 1:
        response = await fetch(url + "rel_nry=" + word, method="GET")
        datamuse_response = response.json()
    
    else:
        response_nry = await fetch(url + "rel_nry=" + word, method="GET")
        response_rhy = await fetch(url + "rel_rhy=" + word, method="GET")
        datamuse_response = await response_nry.json() + await response_rhy.json()

    for entry in datamuse_response:
        rhymes_list.append(entry['word'])

    return rhymes_list

#generates highlighted poem
async def generate_rhyme_struct(input_text, option):
    global rhyming_words
    rhymes_struct.clear()
    rhyming_words.clear()
    poem.clear()
    poem_length = len(re.split(r'\s+', input_text))
    word_counter = 0
    percentage = 0 
    lines = re.split(r'\s+', input_text)
    for line in lines:
        poem.append(line.split(' '))

    #looks for a word in the rhymes_struct, and returns the key if it exists
    def exists(word):
        for key, values in rhymes_struct.items():
            if word in values:
                return {"state": True, "key": key}
        return {"state": False}
    
    count = 0
    for test_line, words in enumerate(poem):
        for test_word_index, test_word in enumerate(words):

            if not poem[test_line]:
                break

            test_word = re.sub(r'[^A-Za-z0-9_]', '', test_word).lower()
            first_test_word = exists(test_word)
            
            if not first_test_word["state"]:
                fetch_rhymes_task = asyncio.create_task(fetch_rhymes(test_word, option))
                rhyming_words = await fetch_rhymes_task

                for line_index, line in enumerate(poem):
                    for word_index, word in enumerate(line):
                        word = re.sub(r'[^A-Za-z0-9_]', '', word).lower()

                        if word in rhyming_words:
                            test_word_exists = exists(test_word)
                            word_exists = exists(word)

                            if test_word_exists["state"] and word_exists["state"]:
                                continue
                            elif test_word_exists["state"]:
                                rhymes_struct[test_word_exists["key"]].append(word)
                            elif word_exists["state"]:
                                rhymes_struct[word_exists["key"]].append(test_word)
                            else:
                                count += 1
                                rhymes_struct[count] = [test_word, word]
            
            #progress bar
            word_counter += 1
            percentage = (word_counter * 100) / poem_length
            document.querySelector('#progressbarText').innerText = str(word_counter) + ' / ' + str(poem_length) + ' words'
            document.querySelector('#progressbarPercentage').innerText = str(round(percentage)) + '%'
            document.querySelector('#progressbarInner').style.width = str(percentage) + "%"

    return rhymes_struct

def colorize_index(index):
    while index >= len(colors):
        index -= len(colors)
    return colors[index]


def colorize_words(matching_word_list, line_start, line_end, color_index):
    for i in range(line_start, line_end - 1):
        for j in range(len(poem[i])):
            if isinstance(poem[i][j], str) and re.sub(r'[^A-Za-z0-9_]', '', poem[i][j]).lower() in matching_word_list:
                poem[i][j] = {"word": poem[i][j], "color": colorize_index(color_index)}

def match_lines(lines):
    color_index = 0
    count = 0
    lines_block = []

    if not poem[-1]:
        poem.pop()
    
    for i, line in enumerate(poem):
        if line != "" and len(line) != 0:
            lines_block.extend(line)
            count += 1
        else:
            continue
        if count == lines or i == len(poem) - 1:
            lines_block = [re.sub(r'[^A-Za-z0-9_]', '', word).lower() for word in lines_block]

            for key, rhyming_words in rhymes_struct.items():
                matching_words = [word for word in rhyming_words if word in lines_block]
                if matching_words and len(matching_words) > 1:
                    color_index += 1
                    colorize_words(matching_words, 0, i + 2, color_index)
            
            count = 0
            lines_block = []


def match_stanzas():
    color_index = 0
    count = 0
    lines_block = []   

    poem.append([])
    for i, line in enumerate(poem):
        if line != "" and len(line) != 0:
            lines_block.extend(line)
        else:
            lines_block = [re.sub(r'[^A-Za-z0-9_]', '', word).lower() for word in lines_block]
            for key, rhymes in rhymes_struct.items():
                matching_words = [word for word in rhymes if word in lines_block]
                if matching_words and len(matching_words) > 1:
                    color_index += 1
                    colorize_words(matching_words, i-count, i+1, color_index)

def match_rhyming_words(rhyming_method, lines):
    if rhyming_method == 0:
        match_stanzas()
    elif rhyming_method == 1:
        if not lines:
            match_lines(4)
        else:
            match_lines(lines)
    else:
        #total number of words across all lines
        total_words = sum(len(line) for line in poem)
        match_lines(total_words)

def return_poem():
    return poem
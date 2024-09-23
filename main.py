#imports
from logic import colors, generate_rhyme_struct, match_rhyming_words, return_poem
import random
from pyscript import when, document, fetch
import asyncio

#variables
analyze_button = document.getElementById('analyze-button')
logo_text = document.getElementsByClassName('logo-text')[0]
spinner = document.getElementById('spinner')
progressbar = document.getElementById('progressbar')
rectangles = spinner.getElementsByTagName("div")
btns = document.getElementsByClassName('btn')
random_color = random.choice(colors)
textarea = document.getElementById('text')
output_container = document.getElementsByClassName('output-container')[0]
output = document.getElementsByClassName('output')[0]
reset_button = document.getElementById('reset-button')
text_reset = document.getElementById('text-reset')

#set a random color from the colors list as the logo's background color
logo_text.style.background = "linear-gradient(to top," + random_color +" 30%, transparent 30%)"
#set a random color from the colors list as the progressbar's color
progressbar.style.backgroundColor = random_color
#set a random color from the colors list as loading spinner's color
for rect in rectangles:
    rect.style.backgroundColor = random_color
#set a random color from the colors list as .btn background color
for btn in btns:
    btn.style.backgroundColor = random_color
#run on load to get right textarea height when page is refreshed
textarea.style.height = ""
textarea.style.height = str(textarea.scrollHeight + 3) + "px"

#get and convert an element's id as a string
def get_id(e):
    return "#" + e.getAttribute("id")

#replaces user inputted poem with rhyme highlighted version
def display_poem():
    
    #fetches highlighted poem from logic.py
    poem = return_poem()
    
    #seperates highlighted poem into lines
    for line in poem:
        
        #seperates each word from the lines
        for word_info in line:

            #creates new text element in input box
            word_span = document.createElement('span')
            empty_span = document.createElement('span')
            empty_span.textContent = ' '
            output.appendChild(word_span)
            output.appendChild(empty_span)
            
            if isinstance(word_info, str):
                word_span.textContent = word_info
                
            else:
                word_span.setAttribute('style', 'background-color:' + word_info['color'])
                word_span.textContent = word_info['word']
                
        output.appendChild(document.createElement('br'))
        
    output_container.classList.remove("hidden")
    textarea.classList.add("hidden")

#start rhymepy
@when("click", get_id(analyze_button))
async def anal_btn(e):
    textValue = textarea.value
    rhymingOption = document.querySelector('input[name="rhyming-options"]:checked').value 
    rhymingMethod = document.querySelector('input[name="rhyming-methods"]:checked').value
    lines = document.querySelector('input[name="lines-value"]').value
    
    #hide output and show input box
    output_container.classList.add("hidden")
    textarea.classList.remove("hidden")

    #check if textarea is not empty
    if len(textValue.strip()) != 0:
        analyze_button.disabled = True
        output.innerHTML = ""
        spinner.classList.remove("hidden")
        progressbar.classList.remove("hidden")
        await generate_rhyme_struct(textValue, rhymingOption)
        match_rhyming_words(rhymingMethod, lines)
        display_poem()
        spinner.classList.add("hidden")
        progressbar.classList.add("hidden")
        analyze_button.disabled = False
        progressbar.style.width = "1%"

#resize input box as user inputs lines
@when("input", get_id(textarea))
def user_typing(e):
    textarea.style.height = ""
    textarea.style.height = str(textarea.scrollHeight) + "px"
    
#reset button
@when("click", get_id(reset_button))
def reset_btn(e):
    output_container.classList.add("hidden")
    textarea.classList.remove("hidden")
    progressbar.classList.add("hidden")

#reset text
@when("click", get_id(reset_button))
def text_res(e):
    
    #Reset textarea height
    textarea.value = ""
    textarea.style.height = ""
    textarea.style.height = textarea.scrollHeight + 3 + "px"

    output_container.classList.add("hidden")
    textarea.classList.remove("hidden")

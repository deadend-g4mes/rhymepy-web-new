# imports
from logic import colors
import random
from pyscript import document, when

# variables
analyze_button = document.querySelector('.analyze-button')
logo_text = document.querySelector('.logo-text')
spinner = document.querySelector('#spinner')
progressbar = document.querySelector('#progressbar')
rectangles = spinner.querySelectorAll("div")
btns = document.querySelectorAll('.btn')
random_color = random.choice(colors)
textarea = document.querySelector('#text')
output_container = document.querySelector('.output-container')
output = document.querySelector('.output')
reset_button = document.querySelector('#reset-button')
text_reset = document.querySelector('#text-reset')

# Set a random color from the colors list as the logo's background color
logo_text.style.background = "linear-gradient(to top," + random_color +" 30%, transparent 30%)"
# Set a random color from the colors list as the progressbar's color
progressbar.style.backgroundColor = random_color
# Set a random color from the colors list as loading spinner's color
for rect in rectangles:
    rect.style.backgroundColor = random_color
# Set a random color from the colors list as .btn background color
for btn in btns:
    btn.style.backgroundColor = random_color
# Run on load to get right textarea height when page is refreshed
textarea.style.height = ""
textarea.style.height = str(textarea.scrollHeight + 3) + "px"

@when("input", textarea)
def userTyping(e):
    textarea.style.height = ""
    textarea.style.height = str(textarea.scrollHeight) + "px"

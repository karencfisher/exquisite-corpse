exquisite-corpse
================

Karen C Fisher 2023  
Contributions by Dan Wilcox, ZKM | Hertz-Lab 2023

MIT License.

Introduction
------------

**Exquisite corpse**, according to ChatGPT, 

"is a collaborative drawing or writing game invented by Surrealist artists in the 
early 20th century. The game involves a group of people creating a drawing or piece of writing 
together, but without seeing each other's contributions.

The game typically involves folding a piece of paper into sections, with each person drawing or 
writing in one section before passing the paper on to the next person to continue the process. The end
result is a collaborative work that is often unexpected and surreal, as each person's contribution 
is influenced by the preceding one, but is not fully aware of what has come before.

The name 'Exquisite Corpse' comes from the French phrase 'cadavre exquis', which was the original 
name given to the game by the Surrealists. It is said that the name was inspired by a phrase that was 
generated randomly using the game: 'Le cadavre exquis boira le vin nouveau' (The exquisite corpse 
will drink the new wine)."

That is as good a definition as I could come up with. So now, why not play this game of collaboration 
by writing some poetry with ChatGPT?

1) First, the human writes some verse. Clicks the "Fold" button (essentially folding the page). 
2) ChatGPT is prompted with only the last line of the human's contribution.  
3) The AI returns its contribution. The page is (virtually) folded, only the last line is visible.
4) Human continues the poem from that line. And folds again.
5) Repeat, until the human chooses to reveal the poem's entirety.

Feeling uninspired? If you just click the "Fold" button, ChatGPT will begin. (if it returns nothing,
try again). If you repeatedly click "Fold" ChatGPT will continue on from its last line.

And one need not necessarily write in English. It should work in any of the languages ChatGPT
speaks (this is not yet tested, however).

---

An example of a collaborative poem. ChatGPT's contributions are **bold**, human's *italic*.

---

<b>
Stirring the oceans into a frothy swoon.  

The stars are sprinkles on a cosmic cake,  
A celestial treat that we cannot fake. 

The sun is a blazing ball of fire,  
A radiant orb that never tires. 

But what of the
</b><br>
<i>entrance to the realms unborn?

Of selves untarnished by time and toil,  
worthiness of happiness and joy  
will they feel light and love?</i>
<b>  
Will they dance with the stars, or tangle with the trees,  
Will their hearts be set free, or forever bewitched with unease,  
The answers lie hidden, in the depths of the unknown,</b>  
<i>the oceans of sky withheld  
things only the whales know, and fish</i>  
<b>Tales of shipwrecks and lost treasures prized  
Echoes of mermaid songs that hypnotize  
Mysteries of the tides and their ebb and flow  
Silent whispers of creatures we'll never know
</b><br>
<i>alas, despite our endeavors.

In concupiscence of a days denouement</i>  
<b>As the sun sets and darkness proclaims.  
The night is young, our hearts are aflame,  
With the promise of adventure and no shame.  
We'll run wild, through the woods and the streams.</b>

---

Installation
------------

There are two options. 

### To run the application (Windows)

If you only wish to play the exquisite-corpse game to collaborate with the AI on some poetry, simply download the exquisite-corpse.zip file. Unzip the directory containing the application and related files, and follow the instructions in the readme.txt.

### Clone this repository

1) Clone this repository and change to the new directory. (You will need to have Git and [Git LFS](https://git-lfs.com) installed.)

```
git clone https://github.com/karencfisher/exquisite-corpse.git
cd exquisite-corpse
```

2) Install system dependencies

* Python3
* Tkinter

**Windows**: download Python and install from [python.org](https://www.python.org/downloads/windows/), Tkinter is included

**macOS**: it is recommended to install Python and Tkinter using [homebrew](https://brew.sh)

    brew install python3 python-tk

**Linux**: a version of Python3 should already be installed, install Tkinter using your package manager, for Debian it woudl be something like:

    sudo apt-get install python-tk

3) Create a Python virtual environment and install dependencies in requirements.txt, e.g.

With the Makefile:

    make

or manually:

    python -m venv venv
    ./venv/bin/activate
    pip -r requirements.txt

Locale Support
--------------

Optionally, install [GNU gettext](https://www.gnu.org/software/gettext) and build translation files for non-English locales.

**Windows**: not tested, can be installed if usinfg msys2 or as a separate installer(?)

**macOS**: install via Homebrew:

    brew install gettext`

**Linux**: install using your package manager, ie. for Debian:

    sudo apt-get install gettext

Generate translation files in the `locale` directory:

    make -C locale

See `locale/README.md` for more info.

_Note: ChatGPT will respond in English if using the default `instructions.txt`. Try translating the instructions or simply adding an additional instruction to respond on in the desired language, ie. "You are to respond only in German."_

Configuration
-------------

If you do not already have an account to use the OpenAI API, you will need to do so. As of 2023, you will initially have $18 credit for usage, which is good for 3 months. If you have used the free credits or they have expired after 3 months (which ever happens first), you will need to set up a paid account.

To do so, you can setup an account and obtain your key here:

https://platform.openai.com/signup

Once you have an OpenAI account, you can proceed to,

https://platform.openai.com/account/api-keys

You will then need to create an `.env` file containing your secret key.

```
SECRET_KEY = '<your secret key>'
```

Replacing `<your secret key>` with your key. BE CAREFUL TO **NOT** PUT THIS INFORMATION IN PUBLIC PLACES. (It's why its called "secret," after all.)

On a macOS or Linux console, to create the file and set the key in one line:

    echo "SECRET_KEY = ABC123..." > .env

_Note: As this file starts with a period `.`, it will be hidden by default on Linux and macOS. Don't forget it's there as it won't appear in Finder, etc!_

### Configuration Files

These are available to edit for your experimentation, if you like.

**instructions.txt** - the prompt for ChatGPT to instruct it to play its role in the collaboration.

**gpt_config.json** - Parameters for the language model. Such as temperature or maximum expected output in tokens.

Additionally, you can provide paths to separate copies of each file via command line args.

Running
-------

Run on the command line via the `exquisite` wrapper script:

	./exquisite

or manually by first activating the virtual environment:

	./venv/bin/activate

then running the main script:

	python exquisite.py

### Commandline Arguments

Additional options and behavior can be set via the commandline arguments.

Script `exquisite -h` help output:
~~~
usage: exquisite.py [-h] [--config CONFIGFILE] [--fontsize FONTSIZE] [-u] [-r] [--randomai RANDOM_AI] [-d] [-b] [-t] [-v] [INSTRUCT]

Exquisite Corpse, according to ChatGPT

positional arguments:
  INSTRUCT              custom ChatGPT instructions txt file

options:
  -h, --help            show this help message and exit
  --config CONFIGFILE   custom ChatGPT configuration json file
  --fontsize FONTSIZE   textbox font size in points, default: 12
  -u, --unfold          enable interim "unfolded" state to hide previous input, ie. when used within a group
  -r, --random          randomly choose between ai and human when folding
  --randomai RANDOM_AI  percent chance to get an ai response 0-100, default: 50
  -d, --dummyai         use dummy ai text instead of ChatGPT (saves money when testing)
  -b, --breaks          force line breaks between folds
  -t, --tags            prepend writer tag lines per fold: <ai> or <human>, adds Reveal Writers menu item
  -v, --verbose         enable verbose printing
~~~

For example, to enable unfold blanking, random AI responses, line breaks + writer tags, larger font, and a dummy AI response for testing (save $):

	./exquisite -urbt --fontsize 24 --dummyai $@

For custom instructions and ChatGPT configurations, either file can be given on the command line to be used in place of the default files:

    ./exquisite --config my_gpt_config.json my_instructions.txt

For the current chat completion model names for use in the JSON config, see the [OpenAI docs](https://platform.openai.com/docs/models/model-endpoint-compatibility).

### Default Behavior

The writer takes turns with ChatGPT on each fold. The text is kept plain without line breaks or writer tag annotation.

### Additional Behavior

Additional behavior has been added to allow for flexibility when used with multiple people ala round robin:

#### Unfold

The textbox is hidden ("blanked") after folding so the writer will not know if ChatGPT has responded. The next writer then unfolds to unhide the textbox. The fold button and menu item act as a toggle between "Fold" and "Unfold".

#### Random

Randomly choose to have ChatGPT respond to the last line, as opposed to *always* responding. The default is a 50% chance which can also be changed to allow for more or less AI responses.

#### Breaks

Prepend an empty line between folds. This should make it easier to delineate between responses, assuming there are no additional line breaks in the responses.

#### Tags

Prepend writer tags `<human>` or `<ai>` to each fold to denote the original writer. When set, Reveal Poem will show the poem text without tags. The show the tags use the additional Reveal Writers option afterwards. Writer tags are always saved with the text file, whether or not they are revealed in the textbox.

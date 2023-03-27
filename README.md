# exquisite-corpse

<h2>Introduction</h2>

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

Feeling uninspired? If you just click the "Fold" button, ChatGPT will begin. 

And one need not necessarily write in English. It should work in any of the languages ChatGPT
speaks (this is not yet tested, however).

<br><hr>
An example of a collaborative poem. ChatGPT's contributions are **bold**, human's *italic*.

*****

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
<hr><br>

<h2>Installation</h2>

There are two options. 

<h3>To run the application</h3>

If you only wish to play the exquisite-corpse game to collaborate with the AI on some poetry, simply download the exquieite-corpse.zip file. Unzip the directory containing the application and accesory files, and follow the instructions in the readme.txt.

<h3>Clone this repository</h3>

It is advisable to work in a virtual environment, as shown below.

1) Clone this repository, and change to the new directory. (You will need to have git and LFS installed.)

```
https://github.com/karencfisher/exquisite-corpse.git
cd exquisite-corpse
```

2) Create a Python virtual environment and activate it, e.g.,

```
python -m venv exq-env
exq-env\scripts\activate
```

3) Install dependencies using the requirements.txt file, e.g.,

```
pip -r requirements.txt
```


<h2>Configuration</h2>

If you do not already have an account to use the OpenAI API, you will need to do so. You will initially have $18 credit for usage, which is good for 3 months. If you have used the free credits or they have expired after 3 months (which ever happens first), you will need to set up a paid account.

To do so,
you can setup an account and obtain your key here:

https://platform.openai.com/signup

Once you have an OpenAI account, you can proceed to,

https://platform.openai.com/account/api-keys

You will then need to create a .env file containig your secret key.

```
SECRET_KEY = '<your secret key>'
```

Replacing <your secret key> with your key. BE CAREFUL TO **NOT** PUT THIS INFORMATION IN PUBLIC PLACES.
(It's why its called "secret," after all.)

<h3>Configuration Files</h3>

These are available to edit for your experimentation, if you like.

**instructions.txt** - the prompt for ChatGPT to instruct it to play its role in the collaboration.

**gpt_config.json** - Paramaters for the language model. Such as temperature or maximum expected output in tokens.

<h2>Running</h2>

Run on the command line:

```
python exquisite.py
```


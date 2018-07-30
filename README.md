# stock_picker
A stock selection and prediction tool for the next day using a variety of stacked LSTM neural networks

# Description: 

So. 

A while ago, in my own endevour to be a millionaire, I tried to create a tool to automatically predict and choose which stock would be the most successful for the next day.

At the time, I created a tool that would iteratively go through around 4000 different stock symbols, download historical pricing information, and then using a LSTM network (very simple, no stacking, single layer) tried to estimate what the next days value would be for that stock. And then after accumulating each stock prediction, gave a single result that would be the largest "winner" for that day.

... this failed after just a couple of days ... :(

[[https://i.imgflip.com/2ezldo.jpg|alt=meme]]
<div class="imagelink_wikilogo">[[meme|&nbsp;]]</div>

Fast forward several years, I came back to the same problem. I am fully aware of the chance of failure (as evidenced from my previous trial), but just to get the nagging off my shoulder I figure I try this again. Yay for stupidity! 

This time however, to avoid simple insanity, I changed the hypothesis. I fully expect the output of lstm.py (a price projection using a stacked lstm with a scale down in dimensions) is pretty much inaccurate (better than nothing but still inaccurate). Price prediction should not be the sole mechanism for determining the winner (or at least not in a straight forward method of numeric assessment following the price prediction). 

So since price project is NOT the purpose of this project, what is the purpose? 

Well to put it simply its "(hidden) pairs trading".

"if there exists stocks that will have a postive/negative impact on another stock somewhere, can we identify those traits of one stock and associate those traits to the largest swing stock (by percentage) for every single day for the last year?" ... across every single S&P500 stock

......

so in other words, there is no projection of the next days price (in the primary solution), but rather a 500 class classification with a window of 10 across 500 different classes


....


This also has a terrible accuracy, about .3% (with around 150-200 epochs) but in this model, i dont care about finding the "winner", i just care if the stock is green or not .....


over the last month so far ive had 15/18 matches (for being green)


we'll see where this goes.


runs best in linux


... YMMV :)



# Installation:

install python2.7 (or 3.6) ... whatever im a readme, not your mother

git clone https://github.com/quiteconfused/stock_picker

pip install tensorflow-gpu keras pandas matplotlib sklearn numpy

git clone https://github.com/Jamonek/Robinhood

cd Robinhood

pip install .

cd ../stock_picker

# Usage: 

Just run the test once and test it out for yourself:
python stacked_lstm.py -d 

Get an actual assessment running through the gauntlet of all model combinations
./run_test.sh
./process_output_log.sh output.log

# Credits: Alot of smart people at keras/google/pandas/and whoever would like to take credit for something they did in the past

# License: 


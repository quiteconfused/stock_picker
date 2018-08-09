# stock_picker
A stock selection and prediction tool for the next day using a variety of stacked LSTM neural networks

## Description: 
So. 

A while ago, in my own endevour to be a millionaire, I tried to create a tool to automatically predict and choose which stock would be the most successful for the next day.

At the time, I created a tool that would iteratively go through around 4000 different stock symbols, download historical pricing information, and then using a LSTM network (very simple, no stacking, single layer) tried to estimate what the next days value would be for that stock. And then after accumulating each stock prediction, gave a single result that would be the largest "winner" for that day.

This model failed after just a couple of days :(

![alt text](https://github.com/quiteconfused/stock_picker/blob/master/images/2ezldo.jpg "Obligatory Meme")

Fast forward several years, I came back to the same problem. I am fully aware of the chance of failure (as evidenced from my previous trial), but just to get the nagging off my shoulder I figure I try this again. Yay for stupidity! 

This time however, to avoid simple insanity, I changed the hypothesis. I fully expect the output of lstm.py (a price projection using a stacked lstm with a scale down in dimensions) is pretty much inaccurate (better than nothing but still inaccurate). Price prediction should not be the sole mechanism for determining the winner (or at least not in a straight forward method of numeric assessment following the price prediction). 

So since price project is NOT the purpose of this project, what is the purpose? 

Well to put it simply its "(hidden) pairs trading".

"If there exists a stock that will have a postive/negative impact on another stock somewhere, can we identify those traits of that one stock and associate those traits to the largest swing stock (by percentage) for every single day for the last year?" ... across every single S&P500 stock.

So in other words, there is no projection of the next days price (in the primary component), but rather a 500 class classification with a window of 10 across 500 different classes.

This also has a terrible accuracy, ~ 3% ( @ around 150-200 epochs). But in this model, I dont care about finding the "winner" (even though that is what I am training for), I just care if the stock is green or not. 

As my previous manager told me "its ok to try for the fences, just as long as you get on base."

We'll see where this goes.

The core component should run in either Linux or Windows but in my own experience this runs best in Linux.

YMMV :)

## Disclaimer:

And just to make sure everyone is aware. The author takes no responsibility for whatever investment choices are made in conjunction with predictions made with use of this software. Use at your own risk!!

## Installation:

### Install python2.7 (or 3.6) ... whatever I'm a readme, not your mother
```
sudo apt-get install python
```
### Install the stock_picker
```
git clone https://github.com/quiteconfused/stock_picker
```
### If you have a good video card (something that supports tensorflow)
```
pip install tensorflow-gpu keras pandas matplotlib sklearn numpy
```
### else
```
pip install tensorflow keras pandas matplotlib sklearn numpy
```
### Install other supporting libraries to download stock information
```
git clone https://github.com/Jamonek/Robinhood
cd Robinhood
pip install .
```
### Return to the stock_picker
```
cd ../stock_picker
```
## Usage: 

### Just run the test once and test it out for yourself*
```
python stacked_lstm.py -d 
```
* This generally consumes upwards 95% of my 1070 video cards ram, and about 11.5gb when running with the GPU

#### IT REALLY SAVES ALOT OF TIME USING THE GPU

### Get an actual assessment running through the gauntlet of all model combinations
```
./run_test.sh && ./process_output_log.sh output.log
```
### OR (when its past 6pm and the markets have closed ... projections are made to compensate for live values) 
```
./run_test_post_6pm.sh && ./process_output_log.sh output.log
```

### If you want to try running in CPU only mode*
```
CUDA_VISIBLE_DEVICES="" python stacked_lstm.py -d
```
* this generally consumes upwards of 10G on my laptop in CPU mode, 

## Credits: 
Alot of smart people at keras, google, pandas, Robinhood, Jamonek, and whoever would like to take credit for something they did in the past

oh my mother and God

_queues music_

## License: 


# Coinbase L2 Socket Lite

The purpose of this project was to create a lite websocket worker which can aggregate data from the Coinbase Pro API L2 book websocket. More information on that can be found here: https://docs.pro.coinbase.com/#channels

# Target Device

This project is being targeted for and tested on a Raspberry Pi 400. The specs are:

| Hardware | Spec |
|----------|------|
|CPU| Quad-core Cortex A-72 64-bit ARM SoC, 1.8GHz|
|RAM| 4GB LPDDR4-3200|
|Storage| 16GB Micro SD|
|OS| Raspberry Pi OS|
|Networking| 1 Gigabit 5.0GHz WiFi Connection|

# Current Results

So far, I've managed to achieve about 15% CPU usage on the target device while tracking the full L2 Orderbook of 10 coins/tokens and printing a 500 entry Pandas DataFrame every 1 second. 

The next step is to ensure that this can run side by side with Dash Plotly (https://dash.plotly.com/) as this projects ties in with my dashboard project (https://github.com/JoshLove-portfolio/Crypto_Dashboard).

# Installation

To begin, clone or download the zip for this repo. The dependencies are currently small to reduce the amount of storage required on the target device. First, change directory into the project and then dependencies can be installed using:

```python
pip install -r requirements.txt
```

# Usage

Currently, this project is not in the best state to be reconfigured. However, if you desire, it can be done by first editing the subscribe.json and including the ticket in the "product_ids" field. 

Next, you'll need to edit the on_message method within the CbSocket class to search for a new coin following the similar syntax:

```python
elif result['product_id'] == 'NEW-COIN-ID':
    adaBook = self.coins.get('NEW-COIN-ID')
    adaBook.set_dicts(result)
```

Where "NEW-COIN-ID" is the new asset you want to track. Next, you'll need to add the new coin to the CbSocket dictionary in the same syntax as the rest:

```python
self.coins = {
    'ETH-USD': Coin('ETH-USD'),
    'NEW-COIN-ID': Coin('NEW-COIN-ID')
}
```

Finally, this project currently runs out of ```__main__``` and thus you'll need to create a new CbSocket object within that. Currently, an object called ```new``` is provided. You'll then need to request the ```bids``` and ```asks``` from the object, as shown in the script currently, and do with those DataFrames what you will.

# Future

As it stands, the goal is to support my Dash Plotly dashboard to run on a Raspberry Pi with this data. I'll continue to optimize the code and improve it so anyone else can take advantage of it in the future. 


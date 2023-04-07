# Math
Models for pricing, insurance premiums, historical gas data, etc.

## Gas Price Model

We start by plotting the raw historical gas prices, as well as the sliding window maximum gas price over a fixed window (in this case 1 day).
![alt text](historical_gas_prices_raw.png "Historical Gas Prices (raw) - 1 day").

Next, we use the sliding window maximum gas price to generate a discrete histogram, allowing us to visualise the probability distribution in gas price space. After that, we fit parameters to our probability distribution to find a function that approximates the distribution. This serves as our future projection
![alt text](max_gas_price_pdf_fitted.png "Max Gas Price PDF (fitted)").

### Improvements

In the future, we can build a more sophisticated model that also takes into account other data not just historical gas data. For example, if we know there will be an upgrade to the network in 2 weeks or a big NFT sale, we can use this information to inform our model that the probability distribution will be skewed as a result.

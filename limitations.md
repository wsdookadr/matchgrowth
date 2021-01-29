Limitations
===========

The computed matches only give an lower bound approximation which doesn't replace a [more rigorous analysis](https://en.wikipedia.org/wiki/Analysis_of_algorithms).

The module can erroneously identify growth rates in the following cases:
- there aren't enough data points in the dataset and it can be identified as having polynomial growth instead of exponential
- the dataset contains a lot of noise which can mislead the curve fitting
- the [curve_fit](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html) algorithm has various biases depending on which
  bounds the coefficients are allowed to be in, and many times that can affect the growth rate detection quite a bit

See also:
- https://stackoverflow.com/q/3930360/827519
- https://stats.stackexchange.com/q/9334/90824
- https://math.stackexchange.com/a/350765/68328
- https://stats.stackexchange.com/a/391314/90824
- https://stats.stackexchange.com/a/9336/90824
- https://softwareengineering.stackexchange.com/a/347750/83470
- https://softwareengineering.stackexchange.com/a/347764/83470
- https://softwareengineering.stackexchange.com/a/164030/83470


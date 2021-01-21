Limitations
===========

The computed matches only give an approximation which doesn't replace a [more rigorous analysis](https://en.wikipedia.org/wiki/Analysis_of_algorithms).

The module can erroneously identify growth rates in the following cases:
- there aren't enough data points in the dataset and it can be identified as having polynomial growth instead of exponential
- the dataset contains a lot of noise which can mislead the curve fitting
- the [curve_fit](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html) algorithm has various biases depending on which
  bounds the coefficients are allowed to be in, and many times that can affect the growth rate detection quite a bit

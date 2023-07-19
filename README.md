# 2023 North American Einstein Toolkit Summer School

You can also access this repository using the shorter URL: https://tinyurl.com/analysiset2023

## Tutorial: Simulation Analysis

This repository contains example parameter files to illustrate how to use some
of the most common diagnostic thorns in the Einstein Toolkit, such as
`AHFinderDirect` and `QuasiLocalMeasures`. The parameter files do not tell the
whole story, and they are likely very different from the ones you will use to
perform production-quality simulations. Nevertheless, they were constructed
using only a minimal number of thorns which are required to perform the basic
tasks they are setup to do. Because of this, we hope they are significantly
shorter (and more organized) than typical parameter files, and we thus hope they
will be of valuable use to new users of the Einstein Toolkit.

This repository also contains scripts for processing simulation data. In
particular, we illustrate how to create movies of the density $\rho$ and the
radial velocity $v^{r}$, using `kuibit` to do most of the heavy lifting during
the post-processing stage. While `kuibit` (and in particular `motionpicture`)
can be used to generate the movies, we have not done it on the scripts because,
from experience, most high-performance computing systems do not have `ffmpeg`
installed. We thus opt to combine the images into a movie in a separate step.

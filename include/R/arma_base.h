#ifndef ARMA_BASE_H
#define ARMA_BASE_H

#include <my_cblas.h>

#define ARMA_DONT_USE_WRAPPER
#undef ARMA_BLAS_CAPITALS
#define ARMA_BLAS_UNDERSCORE

#include <RcppArmadillo.h>

using namespace arma;
using namespace std;

#endif

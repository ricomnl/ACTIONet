#' @export
fastColSums <- function(mat) {
    if (is.sparseMatrix(mat) && class(mat) != "dgCMatrix") {
        mat = as(mat, "dgCMatrix")
    }
    out = fast_column_sums(mat)
    return(out)
}

#' @export
fastRowSums <- function(mat) {
    if (is.sparseMatrix(mat) && class(mat) != "dgCMatrix") {
        mat = as(mat, "dgCMatrix")
    }
    out = fast_row_sums(mat)
    return(out)
}

#' @export
fastColMeans <- function(mat) {
    E = fastColSums(mat)/nrow(mat)
    return(E)
}

#' @export
fastRowMeans <- function(mat) {
    E = fastRowSums(mat)/ncol(mat)
    return(E)
}

#' @export
fastRowVars <- function(mat) {
    mat <- as(mat, "dgTMatrix")
    E = fastRowMeans(mat)
    V <- computeSparseRowVariances(mat@i + 1, mat@x, E, ncol(mat))
    return(V)
}

#' @export
fastBindSparse <- function(A, B, d = 1){
  d = d-1
  sp_mat = bind_sparse_mats(A, B, d)
  return(sp_mat)
}

is.sparseMatrix <- function(A) {
    return(length(which(is(A) == "sparseMatrix")) != 0)
}

rescale.matrix <- function(
  S,
  log_scale = FALSE,
  median_scale = FALSE
) {

    if (is.matrix(S)) {
        cs = fastColSums(S)
        cs[cs == 0] = 1
        B = Matrix::t(Matrix::t(S) / cs)

        if (median_scale == TRUE){
          B = B * median(cs)
        }

        if (log_scale == TRUE) {
            B = log1p(B)
        }

    } else {
        A = as(S, "dgTMatrix")
        cs = fastColSums(S)
        cs[cs == 0] = 1
        x = A@x/cs[A@j + 1]

        if (median_scale == TRUE){
          x = x * median(cs)
        }

        if (log_scale == TRUE) {
            x = log1p(x)
        }
        B = Matrix::sparseMatrix(
          i = A@i + 1,
          j = A@j + 1,
          x = x,
          dims = dim(A)
        )
    }

    return(B)
}

orthoProject <- function(A, S) {
    A = scale(A)
    S = scale(S)
    A_r = A - S %*% MASS::ginv(t(S) %*% S) %*% (t(S) %*% A)
    A_r = scale(A_r)
    return(A_r)
}

#' @export
revert_ace_as_sce <- function(ace) {
    sce = SingleCellExperiment::SingleCellExperiment(
      assays = SingleCellExperiment::assays(ace),
      colData = SingleCellExperiment::colData(ace),
      rowData = SingleCellExperiment::rowData(ace)
    )

    return(sce)
}

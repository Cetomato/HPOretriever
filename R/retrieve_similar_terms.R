#' Retrieve Similar Terms from HPO
#'
#' This function uses the Python FAISS library to retrieve similar terms from the HPO ontology based on mxbai-embed-large text embeddings.
#' @param query A character string representing the query word
#' @param k The number of similar terms to retrieve.
#' @return A data frame containing the HPO term IDs, names, and distances.
#' @import reticulate
#' @export
#' @examples
#' \dontrun{
#' # Example: Retrieve similar terms for the query "irritability"
#' library(HPOretriever)
#' retrieve_similar_terms("irritability", k = 3)
#' retrieve_similar_terms("tired", k = 3)
#' retrieve_similar_terms("swelling at the injection site", k = 3)
#' }
retrieve_similar_terms <- function(query, k = 3) {
  # Find the path to the Python script within the package
  python_script_path <- system.file("python", "hpo_retriever.py", package = "HPOretriever")

  # Source the Python script using reticulate
  reticulate::source_python(python_script_path)

  # Find the path to the pkl file within the package
  pkl_file_path <- system.file("extdata", "HPO_embed_db.pkl", package = "HPOretriever")

  # Load the HPO embedding database in Python
  py$load_hpo_embedding_db(pkl_file_path)

  # Call the Python function
  result <- py$retrieve_similar_terms(query, as.integer(k))

  # Convert the Python list of tuples to an R data frame
  similar_terms_df <- do.call(rbind, lapply(result, function(x) data.frame(ID = x[[1]], Name = x[[2]], Distance = x[[3]])))

  return(similar_terms_df)
}

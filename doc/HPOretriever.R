## ----setup, include=FALSE-----------------------------------------------------
knitr::opts_chunk$set(
  collapse = TRUE,
  comment = "#>"
)

## ----echo=T-------------------------------------------------------------------
reticulate::use_virtualenv(virtualenv='r-reticulate')
library(HPOretriever)
re = retrieve_similar_terms("irritability", k = 3)
print(re)
retrieve_similar_terms("tired", k = 3)
retrieve_similar_terms("swelling at the injection site", k = 3)
re = map_text_to_hpo("The most commonly reported reactions were pain at the injection site and headache.", k = 3)
print(re)
re = map_text_to_hpo("The most commonly reported solicited local and systemic adverse reactions in pregnant individuals (≥10%) were pain at the injection site (40.6%), headache (31.0%), muscle pain (26.5%), and nausea (20.0%). (6.1) • The most commonly reported solicited local and systemic adverse reactions in individuals 60 years of age and older (≥10%) were fatigue (15.5%), headache (12.8%), pain at the injection site (10.5%), and muscle pain (10.1%). ", k = 1)
print(re)


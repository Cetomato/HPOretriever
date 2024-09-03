On a Linux computer with at least 32GB of physical memory and an Nvidia graphics card with at least 16GB of VRAM, install the Nvidia drivers.

Start Ollama server, install llama3.1:8B model, stop proxy.

In R:

install.packages("reticulate")

reticulate::virtualenv_install("r-reticulate", packages = c("faiss", "numpy", "ollama", "requests", "pikle"))

install.packages("remotes")

remotes::install_github("Cetomato/HPOretriever")

library(HPOretriever)

retrieve_similar_terms("irritability", k = 3)

```r
#>           ID               Name    Distance
#> 1 HP:0000737       Irritability   0.0014415
#> 2 HP:0033628 Bowel irritability 125.8558502
#> 3 HP:0031588   Unhappy demeanor 130.1786652
```

retrieve_similar_terms("tired", k = 3)

```r
#>           ID       Name  Distance
#> 1 HP:0012378    Fatigue  90.20061
#> 2 HP:0002329 Drowsiness 126.78558
#> 3 HP:0001254   Lethargy 127.09422
```

map_text_to_hpo("The most commonly reported solicited local and systemic adverse reactions in pregnant individuals (≥10%) were pain at the injection site (40.6%), headache (31.0%), muscle pain (26.5%), and nausea (20.0%). (6.1) • The most commonly reported solicited local and systemic adverse reactions in individuals 60 years of age and older (≥10%) were fatigue (15.5%), headache (12.8%), pain at the injection site (10.5%), and muscle pain (10.1%). ", k = 1)

```r
#>                         word         ID           Name     Distance
#> 1 pain at the injection site HP:6000684 Radiating pain 1.540202e+02
#> 2                   headache HP:0002315       Headache 1.239755e-03
#> 3                muscle pain HP:0009763      Limb pain 9.780450e+01
#> 4                     nausea HP:0002018         Nausea 1.227577e-03
#> 5                    fatigue HP:0012378        Fatigue 1.030056e-03
#> 6                   headache HP:0002315       Headache 1.239755e-03
#> 7 pain at the injection site HP:6000684 Radiating pain 1.540202e+02
#> 8                muscle pain HP:0009763      Limb pain 9.780450e+01
```

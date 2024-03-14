CyberAML
==============================

Prractial Adversarial Attacks on Flow-Based Network Intrusion Detection Systems

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources (e.g., processed ready-to-use network traffic flow datasets).
    │   ├── interim        <- Intermediate data that has been transformed (e.g., raw pcaps after apllication of perturbation techniques).
    │   ├── processed      <- The final, canonical data sets for modeling (e.g., fully perturbed network traffic flow datasets).
    │   └── raw            <- The original, immutable data dump (e.g., raw pcaps).
    │
    ├── models             <- Trained and serialized models, resulting perturbation steps, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    └── src                <- Source code for use in this project.
        ├── __init__.py    <- Makes src a Python module
        │
        ├── data           <- Scripts to download or generate data
        │
        ├── pertubations   <- Scripts to turn raw pcaps into perturbed pcaps, or into ready network traffic flows
        │
        └── models         <- Scripts to train models and then use trained models to make predictions; generally to
                              find optimal perturbation steps
     



--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

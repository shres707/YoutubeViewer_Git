# -*- coding: utf-8 -*-
"""StreamLit_Launch.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19OqKc54HFo9x4zY3p1Fk0-LngZR0v5Lf
"""

!pip install streamlit

!pip install streamlit-pandas-profiling

!pip install https://github.com/pandas-profiling/pandas-profiling/archive/master.zip

!streamlit run multipage_main.py & npx localtunnel --port 8501

!python --version

!pip install pipreqs

!python -m pipreqs.pipreqs .

!pip freeze > requirements.txt
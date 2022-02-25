
## What is what in this repo?

1. Readme.md: this file as a summary of this project and telling you the structure of this repo files
2. Main.py: my codes in python saved without outputs to save your time viewing
3. climate_queries.ipynb: my codes (with outputs) that query data for analysis
4. app.py: my codes to make api/route via Flask
5. Outputs: the images of graphs, JSON-format outputs from api
6. Resources: data sources
7. temp_analysis_part1 | part_2: deeper analysis (unfinished) 

## What are the Project requirements?


Climate Analysis and Exploration: 

climate analysis and data exploration of the climate database of Hawaii | Honolulu (great place for vacation)

- Pricipitation (rainfall) analysis

- Temperature observations

- Station analysis: find out the most active station among data set, then look for the lowest, highest, and average temperature

- Climate apps: design a Flask API based on the above queries developed & return a JSON lists of stations and temperature observations. 


## Tools and languages used to get the job done: 

- SQLAlchemy | ORM | engine, automap_base
- sqlite
- Pandas
- Matplotlib
- Python 
- Flask
- t-test method 


## Some findings: (see more in my coding files)


![Rainfall_graph](https://user-images.githubusercontent.com/93897775/155198447-1984ed40-c3d6-4ad9-846a-7f7ee2279a41.png)

the data from 12 months observation in Hawaii shows the precipitation there were regularly high every 3 months and higher especially in the Fall and Spring seasons. 



![frequency_graph](https://user-images.githubusercontent.com/93897775/155198527-b9ef6ff9-9843-41d8-bd09-b41f7a620944.png)


When focus on specific station (code: ) to obserb the teperature for most recent year (Aug 2016 - Aug 2017), the data shows the most frequent temperature of Hawaii during this observation period were from 75F - 77F with more than 60 frequency occured; next to that was 73F - 75F with nearly 60 frequency. 

Sometimes Hawaii got hotter with 80F at nearly 30 times in the entire observed year.

The temperature were rarely cool down to 60F with below 10 times in the entire year. 


## Author: Tracie Bautista

Data Analyst

linkedin: https://www.linkedin.com/in/tracynguyen10/








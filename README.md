# Spotifiers   

Objective: To build music recommendation system based on user's music taste - recommendations based on genre, artists and audio features   

Steps:
Data analysis - we are using albums, artists, genres, audio features and tracks to process the data and using feature engineering to transform the raw data.   

Machine learning models used:   
- K means algorithm
- MiniBatchKMeans
- Birch    


Data Link: https://os.unil.cloud.switch.ch/fma/fma_metadata.zip


## APIs
`/prepare`
Prepare and process data
Processed data is saved as final.csv and metadata.csv

`/train`
Takes two arguments - ratio and model
Example - train KMeans model with 80% ratio:
`/train?ratio=80&model=KMeans`

`/recommend`
Music recommendations based on ratio and model
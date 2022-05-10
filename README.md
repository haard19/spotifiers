# Spotifiers   

### **Team Members**:
- [Haard Shah](http://github.com/haard19)
- [Neel Sojitra](https://github.com/nsojitra20)
- [Raj Choksi](https://github.com/rajchoksi1997)
- [Rishab Reddy](https://github.com/rishabreddyk)
- [Visva Suthar](https://github.com/visvasuthar)

### **Objective**: <br> 
To build music recommendation system based on user's music taste - recommendations based on genre, artists and audio features   

### **Steps**: <br>
Data analysis - we are using albums, artists, genres, audio features and tracks to process the data and using feature engineering to transform the raw data.   

### **Machine learning models used**:<br>   
- K means algorithm
- MiniBatchKMeans
- Birch    


### **Data Link**: <br>
https://os.unil.cloud.switch.ch/fma/fma_metadata.zip


### **APIs**

Endpoint | Description | Output
--- | --- | --
`/prepare` | Prepare and process data | Processed data is saved as final.csv and metadata.csv   
`/train` | Takes two arguments - ratio and model and trains it according to the inputs | Saves the trained model 
`/recommend` | Music recommendations based on ratio and model | Gives out a JSON object containing the recommended audio tracks

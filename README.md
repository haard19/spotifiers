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
- **K means algorithm**: 
  - Method of vector quantization, originally from signal processing, that aims to partition n observations into k clusters in which each observation belongs to the cluster with the nearest mean, serving as a prototype of the cluster. 
- **MiniBatchKMeans**
  - It uses small, random, fixed-size batches of data to store in memory, and then with each iteration, a random sample of the data is collected and used to update the clusters.
- **Birch**
  - Balanced Iterative Reducing and Clustering using Hierarchies (BIRCH) is a clustering algorithm that can cluster large datasets by first generating a small and compact summary of the the large dataset that retains as much information as possible.    


### **Data Link**: <br>
https://os.unil.cloud.switch.ch/fma/fma_metadata.zip


### **APIs**

Endpoint | Description | Output
--- | --- | --
`/prepare` | Prepare and process data | Processed data is saved as final.csv and metadata.csv   
`/train` | Takes two arguments - ratio and model and trains it according to the inputs | Saves the trained model 
`/recommend` | Music recommendations based on ratio and model | Gives out a JSON object containing the recommended audio tracks

### **Output**

- Flask app <br>
![alt text](./images/output1.png?raw=True)

- Prepare Features
![alt text](./images/output2.png?raw=True)

- Train Data
![alt text](./images/output3.png?raw=True)

- Recommend Songs
![alt text](./images/output4.png?raw=True)
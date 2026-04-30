This repositories describe the data cleaning process of the international trade dataset for DATS-SHU 235 Information Visualization final project.   
top10_trade_final.csv is the final CSV file after data processing.   
Please see the folder `data_processing` to see the detailed process of this data cleaning task.   
The original dataset contains annual international trade data from 1995 to 2024, with each year’s data stored in a separate CSV file. Due to the limitation of file size, the original data is not included here. You can download the dataset from this website: https://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37.   
`parse.py` is the code for the first step of data cleaning, where we extract the trade data between the top 10 economies from 30 CSV files and output them to a new CSV file. This CSV file is also too large and hard to visualize.   
`filter_output.py` is the code for the second step of data cleaning, where we only keep the data from 1995 to 2014, with non-zero quantity, and aggregate different types of commodities. In this way, the dataset is better suited for our visualization projects.   
After the two steps of data cleaning, top10_trade_final.csv is the final CSV file.

# MFC Batch Commenter

## What is this?
MFC Batch Commenter is designed to automatically comment on MyFigureCollection (MFC) product pages given a properly formatted CSV file. 
The script utilizes the MFC API's notify-availability request to add comments to each product's MFC page as specified in the CSV.

## Usage

Assuming you have python installed and have some knowledge of how to use python:

Create a .env file in the project directory and add your public and private keys to the file.
```
PUBLIC_KEY=your_public_key
PRIVATE_KEY=your_private_key
```
The script will not work if your keys are invalid.

Install the required dependencies using the following command:
```
pip install -r requirements.txt
```

Place your csv file into the project directory. 
Example csv:
```
status,jan,mfci,message,price,currency
1,1234567890123,123,This is a comment for product 1,2000,USD
0,9876543210987,456,Another comment for product 2,1500,EUR
```
The csv file must include the following headers as they are required parameters: jan, status.

Set this to False (line 18) so that the script is not in test mode.
```
sandbox_mode = True
```

Run the script with the following command:
```
python main.py
```
After running the script, "OK" in case of success and "FAILED" if unsuccessful will print for each item in the csv.
If you see "OK", you should be able to see your comments on the MFC product pages.

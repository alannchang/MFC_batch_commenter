### MFC Batch Commenter

## What is this?
MFC Batch Commenter is designed to automatically comment on MyFigureCollection (MFC) product pages given a properly formatted CSV file. 
The script utilizes the MFC API's notify-availability request to add comments to each product's MFC page as specified in the CSV.

API endpoint: https://myfigurecollection.net/papi.php?mode=notify-availability

## Usage

Create a .env file in the project directory and add your public and private keys to the file.
'''
PUBLIC_KEY=your_public_key
PRIVATE_KEY=your_private_key
'''
The script will not work if your keys are invalid.

Place your csv file into the project directory and run the python script.
'''
python main.py
'''

Example csv:
'''
status,jan,mfci,message,price,currency
1,1234567890123,MFCI123,This is a comment for product 1,2000,USD
0,9876543210987,MFCI456,Another comment for product 2,1500,EUR
'''
The csv file must include the following headers as they are required parameters: key, jan, status, s.
After running the script, "OK" in case of success and "FAILED" if unsuccessful will print for each item in the csv.
If you see "OK", you should be able to see your comments on the MFC product pages.

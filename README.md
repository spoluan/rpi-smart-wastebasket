# Descriptions
Install the dependencies \
`python -m pip install --user -r .\requirements\requirements.txt` 

Data collection (adjust the class that you want to collect inside soundcollection.py) \
`python .\codes\data-collection\soundcollection.py`

Train the model \
`python .\codes\train\train.py`

Test the model \
`python .\codes\test\test.py`

Run the program \
`python app.py`

To change your datasets, you can copy them into the `train` folder. The codes will automatically detect that the folder listed under the `train` folder is your class label.

# Datasets

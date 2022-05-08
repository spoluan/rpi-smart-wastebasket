# Descriptions

**The program was developed under the Raspberry Pi environment.**

Install the dependencies \
`python -m pip install --user -r .\requirements\requirements.txt` 

You will also need to install another dependency in the `.\requirements/installing_pyaudio.txt` file.

Train the model \
`python .\codes\train\train.py`

Test the model \
`python .\codes\test\test.py`

Run the program \
`python app.py`

# Datasets

Data collection (adjust the class that you want to collect inside soundcollection.py) \
`python .\codes\data-collection\soundcollection.py`


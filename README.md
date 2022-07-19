# Descriptions

**The program was developed under the Raspberry Pi environment.**

Install the dependencies \
`python -m pip install --user -r .\requirements\requirements.txt` 

You will also need to install another dependency in the `.\requirements/installing_pyaudio.txt` file.

Train the model \
`python .\codes\train\train.py`
 
In addition to training the model, melfrequency features will also be extracted into the pickle and saved for later use. In order to avoid re-extraction of features when retraining the model, you may wish to comment off line 54 of the `train.py` file. The process of extracting the features will take time.

<p align="center">
	<img src="img/training.jpg" width="800"/> 
</p>

The folder model contains a saved model. The following command can be executed to test the model with the available testing data.

`python .\codes\test\test.py`

<p align="center">
	<img src="img/testing.jpg" width="800"/> 
</p>

# Datasets

Data collection (adjust the class that you want to collect inside soundcollection.py) \
`python .\codes\data-collection\soundcollection.py`


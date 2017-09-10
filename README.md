### 1. Requrements:
 - Python>=3.4
 - Pillow>=3.2.0
 - beautifulsoup4>=4.4.0
 - Requests>=2.10.0

Note: PIL-1.1.7 comes with Pillow-2.3.0, as PIL has been
	depreciated.


### 2. How to Run:
    2.1 Clone the repository
	2.2 Install all the required dependencies.
`sudo pip3 install -r requirements.txt`

If it is unsuccessfull, install all the required dependencies manually.

	2.3 Generate Data set of alternative text from 200+ Indian University website:

`python3 urlcsvreader.py`

It will generate a file 'dataset.csv' in current directory.

	2.4 Build Feature Set from generated data set.
	
` python3 feature_builder.py`
	
	2.5 Train Model and visualize result.
`python3 classifier_plot.py`


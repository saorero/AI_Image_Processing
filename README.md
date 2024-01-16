The Images used in the training can be found in the shared drive link(https://drive.google.com/drive/folders/1Pu5Lut5eJGYv5gAi1BMRe7uWn74VaXO5?usp=sharing).
On how the scripts work refer to the text document INSTRUCTIONS
Other folders like test and train images are also available in drive... this includes the split 2016 images that were passed to the model to be able to detect lakes and come up with the detected bounding boxes that are stored in outputs folder found in  drive.
the custom model is in inferencegraph folder found in drive
Lake prediction was done in both 2015 and 2016 split images. Dimension of split - 500*500 split.py
The area of the lakes detected is calculated and converted to csv savingCSV.py
Classifying the lakes based on extent of vulnerability based on the area diffrence btwn 2016 and 2015 calculate_decrease.py

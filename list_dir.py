import os
dataset = os.listdir('dataset')

json_files = [ file for file in dataset if os.path.isfile(os.path.join('dataset',file)) and file.endswith('.json') ]

print(json_files)
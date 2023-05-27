import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('runs/detect/result0524_300/train/results.csv', 
                 usecols=[0, 1],
                 skiprows=1,
                 names=['X', 'Y'])

x_data = df['X']
y_data = df['Y']

plt.plot(x_data, y_data)
plt.xlabel('Rounds')
plt.ylabel('Box Loss')
plt.title('Data Diagram')
plt.show()
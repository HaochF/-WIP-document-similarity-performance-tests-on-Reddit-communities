from matplotlib import pyplot as plt

#plt.scatter([1,2,3,4,5,6], [6,3,6,1,2,3])
#plt.show()
def plotBarGraphWithDict(dict):
  x = []
  height = []
  for key, value in dict.items():
    x.append(key)
    height.append(value)
    
  plt.bar(x, height)
  plt.show()

if __name__ == "__main__":
  plt.bar(['a', 'b', 'c'], [1, 2, 3])
  plt.show()

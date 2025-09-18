import urllib.request

url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
try:
    response = urllib.request.urlopen(url, timeout=10)
    data = response.read()

    with open("iris.csv", "wb") as f:
        f.write(data)
except Exception as e:
    print(f"Error downloading or saving the file: {e}")

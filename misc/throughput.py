import requests
import json

def makeThroughputJson(source, destination):
    url = 'https://perfsonar.nautilus.optiputer.net/esmond/perfsonar/archive/'
    timeRange = 1728000
    headers = {'Content-Type': 'application/json'}

    m = requests.get('{0}?source={1}&destination={2}'.format(url,source,destination))

    returnJSON = m.json()
    JSONList = []
    for item in returnJSON:
        n = requests.get('{0}throughput/base?time-range={1}'.format(item['url'],timeRange), headers=headers)
        dataJSON = n.json()
        if dataJSON:
            JSONList.append(dataJSON)
    return JSONList

if __name__ == '__main__':
    source = "67.58.53.140"
    dest = "67.58.53.141"
    data = makeThroughputJson(source, dest)
    with open('dataPoints.json','w') as f:
        json.dump(data,f)
    f.close()

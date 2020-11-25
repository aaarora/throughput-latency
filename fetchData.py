import requests
import json
import time
import pickle

# Pull Latency JSON from Archive
def makeLatencyJson(source, destination): 
    url = 'https://perfsonar.nautilus.optiputer.net/esmond/perfsonar/archive/'
    timeRange = 10000
    headers = {'Content-Type': 'application/json'}

    m = requests.get('{0}?source={1}&destination={2}'.format(url,source,destination), headers=headers)

    returnJSON = m.json()

    for item in returnJSON:
        n = requests.get('{0}histogram-owdelay/statistics/0?time-range={1}'.format(item['url'],timeRange), headers=headers)
        dataJSON = n.json()
        if dataJSON:
            return dataJSON

# Pull Throughput JSON from Archive
def makeThroughputJson(source, destination):
    url = 'https://perfsonar.nautilus.optiputer.net/esmond/perfsonar/archive/'
    tool = 'xrootd-tpc-single-stream'
    timeRange = 259200
    headers = {'Content-Type': 'application/json'}

    m = requests.get('{0}?tool-name={1}&source={2}&destination={3}'.format(url,tool,source,destination), headers=headers)

    returnJSON = m.json()

    for item in returnJSON:
        n = requests.get('{0}throughput/base?time-range={1}'.format(item['url'],timeRange), headers=headers)
        dataJSON = n.json()
        if dataJSON:
            return dataJSON

# Parse Points from Latency JSON
def parseLatency(source, destination):
    latencyJSON = makeLatencyJson(source, destination)
    if latencyJSON is None:
        raise Exception
    total = 0
    count = 0
    for item in latencyJSON:
        total = total + float(item[u'val'][u'mean'])
        count = count + 1
    return total / count

# Avg Throughput
def parseThroughput(source, destination):
    throughputJSON = makeThroughputJson(source, destination)
    if throughputJSON is None:
        raise Exception
    total = 0
    count = 0
    for item in throughputJSON:
        total = total + float(item[u'val'])
        count = count + 1
    total = 8 * total / 8589934592.0 
    return total / count


if __name__ == "__main__":
    with open('internal.json','r') as f:
        conf = json.loads(f.read())
    f.close()
    parsedJSON = list()
    for (hostName1, hostIP1) in conf.items():
        for (hostName2, hostIP2) in conf.items():
            if (hostName1 == hostName2):
                continue
            try:
                latency = parseLatency(hostIP1,hostIP2)
                throughput = parseThroughput(hostName1,hostName2)
                parsedJSON.append((latency,throughput))
            except Exception:
                continue
    with open('dataPoints.txt','wb') as data:
        pickle.dump(parsedJSON,data)

import json

with open('forAashay.json','r') as f:
    data = json.loads(f.read())
f.close()

with open('conf.json','r') as c:
    conf = json.loads(c.read())
c.close()

items = data['items']

host = lambda i : items[i][u'spec'][u'nodeName']
ip = lambda i : items[i][u'metadata'][u'annotations'][u'cni.projectcalico.org/podIP'].split('/32')[0]

d = dict()
for i in range(len(items)):
    try:
        if(host(i) in conf.keys()):
            d.update({host(i): ip(i)})
    except:
        continue

with open('internal.json','w') as internal:
    json.dump(d,internal,indent=1)
    internal.write('\n')
internal.close()

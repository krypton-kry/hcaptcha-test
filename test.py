import random
from uuid import uuid4
import requests
from datetime import datetime
import asyncio
import urllib.parse
import urllib.request
import urllib3
import js2py
session = requests.Session()

def randomFromRange(start, end):
    return round(random.random() * (end - start) + start)


def getRandomUserAgent():
    return 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'

def uuid(a):
    (a^((random.random() * 16) >> (a/4)))
def getMouseMovements(timestamp):

    lastMovement = timestamp
    motionCount = randomFromRange(1000, 10000)
    mouseMovements = []
    for i in range(0 , motionCount):
        lastMovement += randomFromRange(0,10)
        mouseMovements.append([randomFromRange(0,500),randomFromRange(0,500), lastMovement])
    return mouseMovements


async def hsl(req):
    hsl = session.get('https://assets.hcaptcha.com/c/500c658/hsl.js').text
    # print(req)
    code = "const vm = require('vm');\
    code = `var self = {};\
    \
    function atob(a) {\
        return new Buffer(a, 'base64').toString('binary');\
    }\
    \n"+hsl+"\nhsl('"+req+"')`\n\
    vm.runInNewContext(code,{Buffer}).then(r=>{console.log(r)});"

    command = ['node','-e',code]

    process = await asyncio.create_subprocess_exec(*command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await process.communicate()

    return stdout.decode().strip()


async def tryToSolve(sitekey, host):
    userAgent = getRandomUserAgent()
    header = {
        'User-Agent': str(userAgent),
        'Accept':'application/json',
        'Content-type':'application/x-www-form-urlencoded',
        'host':'hcaptcha.com',
        'Accept-Language':'en-US,en;q=0.5',
        'Connection':'keep-alive',
        'Origin':'https://assets.hcaptcha.com',
        }

    response = session.get(f'https://hcaptcha.com/checksiteconfig?host={host}&sitekey={sitekey}&sc=1&swa=0',headers=header).json()
    timestamp = int(datetime.now().timestamp() * 1000) + randomFromRange(30, 120)
    print(response['c']['req'])
    re = await hsl(response['c']['req'])
    print(re)
    data = {
        'sitekey':str(sitekey),
        'host':'kwik.cx',
        'n':str(re) ,
        'c': str(response['c']),
        'motionData':{
            'st': str(timestamp),
            'dct':str(timestamp),
            'mm': str(getMouseMovements(timestamp))
        }
    }
    #req = urllib.request.Request('https://hcaptcha.com/getcaptcha',data=data)
    #resp = urllib.request.urlopen(req)
    resp = requests.post('https://hcaptcha.com/getcaptcha',data=data, headers=header)
    #http = urllib3.PoolManager()
    #resp = http.urlopen('POST','https://hcaptcha.com/getcaptcha',
    #        body=data,headers={'Content-Type':'application/json'})
    '''
    command = ['node','get_it.js',str(sitekey),str(re)]
    process = await asyncio.create_subprocess_exec(*command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await process.communicate()
    print(stdout.decode().strip(),stderr.decode().strip())
    '''
    print(resp.text)
loop = asyncio.get_event_loop()
loop.run_until_complete(tryToSolve(uuid4(),'kwik.cx'))
loop.close()


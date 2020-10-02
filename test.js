const request = require('request-promise-native');
const Url = require('url');
const vm = require('vm');
//const req = request.defaults({'proxy':'https://127.0.0.1:8888'})
function randomFromRange(start, end) {
    return Math.round(Math.random() * (end - start) + start);
  }
  
  function randomTrueFalse() {
    return randomFromRange(0, 1) ? 'true' : 'false';
  }
  
  const delay = (ms) => new Promise((r) => setTimeout(r, ms));
  
  function uuid(a) {
    return a
      ? (a ^ ((Math.random() * 16) >> (a / 4))).toString(16)
      : ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, uuid);
  }
  
  function getRandomUserAgent() {
    // TODO
    return 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36';
  }

  function getMouseMovements(timestamp) {
    let lastMovement = timestamp;
    const motionCount = randomFromRange(1000, 10000);
    const mouseMovements = [];
    for (let i = 0; i < motionCount; i++) {
      lastMovement += randomFromRange(0, 10);
      mouseMovements.push([randomFromRange(0, 500), randomFromRange(0, 500), lastMovement]);
    }
    return mouseMovements;
  }
  async function hsl(req) {
    const hsl = await request.get('https://assets.hcaptcha.com/c/500c658/hsl.js');
    return new Promise((resolve, reject) => {
      const code = `
      var self = {};
      function atob(a) {
        return new Buffer(a, 'base64').toString('binary');
      }
    
      ${hsl}
    
      hsl('${req}').then(resolve).catch(reject)
      `;
      vm.runInNewContext(code, {
        Buffer,
        resolve,
        reject,
      });
    });
  }
  async function tryToSolve(sitekey, host) {
    const userAgent = getRandomUserAgent();
    const headers = {
      'User-Agent': userAgent
    };
    
    let response = await request({
      method: 'get',
      headers,
      json: true,
      url: `http://hcaptcha.com/checksiteconfig?host=${host}&sitekey=${sitekey}&sc=1&swa=0`
    })
    let timestamp = Date.now() + randomFromRange(30, 120);
    //console.log(response)
  response = await request({
    method: 'post',
    headers,
    json: true,
    url: 'https://hcaptcha.com/getcaptcha',
    form: {
      sitekey,
      host,
      n: await hsl(response.c.req),
      c: JSON.stringify(response.c),
      motionData: {
        st: timestamp,
        dct: timestamp,
        mm: getMouseMovements(timestamp)
      }
    }
  });
console.log(response)
  
}

tryToSolve(uuid(),'kwik.cx')
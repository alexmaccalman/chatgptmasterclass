/*
 * Copyright (c) Microsoft Corporation. All rights reserved. Licensed under the MIT license.
 * See LICENSE in the project root for license information.
 */

/* global document, Office */

Office.onReady((info) => {
  if (info.host === Office.HostType.Outlook) {
    document.getElementById("sideload-msg").style.display = "none";
    document.getElementById("app-body").style.display = "flex";
    document.getElementById("run").onclick = run;
  }
});

export async function run() {
  /**
   * Insert your Outlook code here
   */

  let body = ''

  async function outputResult(body){
    console.log(body)
    let response = await runAzure(body)
    console.log(response.output)
    document.getElementById('app-body').innerHTML = "<b> Summary: </b> <br/> " + response.output
  }

  async function getBody() {
    Office.context.mailbox.item.body.getAsync("text", function (result) {
      if (result.status === Office.AsyncResultStatus.Succeeded) {
        body = result.value
        outputResult(body)
      }
    })
  } 

  async function runAzure(body) {

    const Url = 'https://chatgptmasterclass-apim.azure-api.net/completionapi';
    const bodyjson = '{"model":"text-davinci-003", "prompt":"summarize the following in 50 words or less: ' + body.replace(/['"]+/g, '').trim().replace(/(\r\n|\n|\r)/gm, "") + '", "max_tokens":200, "temperature":0}'
    console.log(bodyjson)
    const otherParam = {
      body: bodyjson,
      method: 'POST'
    };

    const response = await fetch(Url, otherParam);
    var output = await response.text()

    return {output}

  }

  await getBody()

}

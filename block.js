const puppeteer = require('puppeteer')
const url = `https://www.douban.com/group/685388/members`



const sleep = time => new Promise(resolve=>{
    setTimeout(resolve,time)
})




;(async()=>{

    console.log('开始数据的爬取')
    const browser = await puppeteer.launch({
        args:['--no-sandbox'],
        dumpio:false,
    })

    const page = await browser.newPage()
    var cookies = await page.cookies()

    await page.goto(url,{
        waitUntil:'networkidle2'
    })

    await sleep(1000)

    //await page.waitForSelector('.more')

    /*
    for (let index = 0; index < 1; index++) {
        await sleep(1000)

        await page.click('.more')
    }
    */

    const result = await page.evaluate(()=>{
        var $ = window.$
        var items = $('li .name a')

        var links = [];
        let ck = cookies.ck
        var name = "ck=";
        console.log('start')

            items.each((index,item)=>{
                let it = $(item)
                let member_id = item.href.split('/people/')[1].replace('/', '')

                links.push({
                    member_id,
                    ck
                })

            })
        return links
    })

    browser.close()
    console.log(result)

})()

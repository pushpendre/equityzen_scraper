/**
 * @name EquityZen Scraper
 *
 * @desc Scrapes new EquityZen investments. Provide your username and password as environment variables when running the script, i.e:

 *
 * https://github.com/checkly/puppeteer-examples/search?q=for&type=code
 */

const puppeteer = require('puppeteer')
const fs = require('fs')
const screenshot = 'equityzen.png';
const useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36';
const email = process.env.EMAIL;
const password = process.env.PASSWORD;
const companies = JSON.parse(fs.readFileSync(process.env.COMPANY_LIST, 'utf8'));

(async () => {
  const browser = await puppeteer.launch({ headless: true })
  const page = await browser.newPage()

  // set user agent (override the default headless User Agent)
  await page.setUserAgent(useragent);

  // Login
  await page.goto('https://equityzen.com/accounts/login/')
  await page.type('#email', email)
  await page.type('#password', password)
  await page.click('button')
  await page.waitForNavigation({ waitUntil: ['networkidle2'] })

  // Scrape
  await page.setViewport({ width: 1366, height: 768});
  for (const company of companies) {
    console.log(company)
    await page.goto(company, {waitUntil: 'networkidle2'})
    await page.waitForSelector('.DealOfferings')
    const tbody = await page.$eval('.DealOfferings tbody', el => el.innerHTML)
          .catch(function (error) {'empty';})
    console.log(tbody)
    console.log('')
  }

  // Take Screenshot
  // await page.screenshot({ path: screenshot })

  // Close
  browser.close()
})()

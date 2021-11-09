import aiohttp
import asyncio
import humanize


TIMEOUT = 7


#  myfin.by
async def parse_data_myfin(data):
    rate = data.split('"birzha_info_head_rates">')[1].split('$')[0].strip()
    print('a ------', float(rate))
    return humanize.intcomma('%.2f' % float(rate))


async def requests_course_myfin(session, url):
    async with session.get(url) as resp:
        print("Status myfin:", resp.status)
        data = await resp.text()
        if resp.status != 200:
            return
        return await parse_data_myfin(data)


async def client_myfin(list_url):
    print('^^^^^^^client_myfin')
    timeout = aiohttp.ClientTimeout(total=TIMEOUT)
    async with aiohttp.ClientSession(timeout=timeout, connector=aiohttp.TCPConnector(limit=64, ssl=False)) as session:
        requests = [requests_course_myfin(session, url) for url in list_url]
        results = await asyncio.gather(*requests, return_exceptions=True)
        print('!!!!!!!!results', results)

    return handler_result(results)


# bitinfocharts.com
async def parse_data_bitinfo(data):
    rate = data.split('"price"')[1].split('>')[1].split('<')[0].strip().replace(',', '')
    print('b ------', rate)
    return humanize.intcomma('%.2f' % float(rate))


async def requests_course_bitinfo(session, url):
    async with session.get(url) as resp:
        print("Status bitinfo:", resp.status)
        data = await resp.text()
        if resp.status != 200:
            return
        return await parse_data_bitinfo(data)


async def client_bitinfo(list_url):
    print('^^^^^^^client_bitinfo')
    timeout = aiohttp.ClientTimeout(total=TIMEOUT)
    async with aiohttp.ClientSession(timeout=timeout, connector=aiohttp.TCPConnector(limit=64, ssl=False)) as session:
        requests = [requests_course_bitinfo(session, url) for url in list_url]
        results = await asyncio.gather(*requests, return_exceptions=True)
        print('!!!!!!!!results', results)

    return handler_result(results)



# bitstat.top
async def parse_data_bitstat(data):
    rate = data.split('"ticker_usd">')[1].split('$')[0].replace(' ', '')
    print('c ------', rate)
    return humanize.intcomma('%.2f' % float(rate))


async def requests_course_bitstat(session, url):
    async with session.get(url) as resp:
        print("Status bitstat:", resp.status)
        data = await resp.text()
        if resp.status != 200:
            return
        return await parse_data_bitstat(data)


async def client_bitstat(list_url):
    print('^^^^^^^client_bitstat')
    timeout = aiohttp.ClientTimeout(total=TIMEOUT)
    async with aiohttp.ClientSession(timeout=timeout, connector=aiohttp.TCPConnector(limit=64, ssl=False)) as session:
        requests = [requests_course_bitstat(session, url) for url in list_url]
        results = await asyncio.gather(*requests, return_exceptions=True)
        print('!!!!!!!!results', results)

    return handler_result(results)


def handler_result(results):
    result_no_exception = list()
    for result in results:
        if isinstance(result, Exception):
            result_no_exception.append('')
        else:
            result_no_exception.append(result)
    bitcoin, ethereum, bitcoin_cash = result_no_exception
    return {'bitcoin': bitcoin, 'ethereum': ethereum, 'bitcoin_cash': bitcoin_cash}
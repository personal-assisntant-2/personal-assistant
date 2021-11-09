from .handlers import client_bitinfo, client_bitstat, client_myfin



# Resources
URL_BITCOIN_MYFIN = 'https://myfin.by/crypto-rates/bitcoin'
URL_ETHEREUM_MYFIN = 'https://myfin.by/crypto-rates/ethereum'
URL_BITCOINCASH_MYFIN = 'https://myfin.by/crypto-rates/bitcoincash'
URL_BITCOIN_BITINFOCHARTS = 'https://bitinfocharts.com/ru/bitcoin/'
URL_ETHEREUM_BITINFOCHARTS = 'https://bitinfocharts.com/ru/ethereum/'
URL_BITCOINCASH_BITINFOCHARTS = 'https://bitinfocharts.com/ru/bitcoin%20cash/'
URL_BITCOIN_BITSTAT = 'https://bitstat.top/coin.php?id_coin=1'
URL_ETHEREUM_BITSTAT = 'https://bitstat.top/coin.php?id_coin=2'
URL_BITCOINCASH_BITSTAT = 'https://bitstat.top/coin.php?id_coin=11'


# LIST URL in this order: ['bitcoin', 'ethereum', 'bitcoin_cash']!!!
handlers = {
    'rates_bitstat': client_bitstat([URL_BITCOIN_BITSTAT, URL_ETHEREUM_BITSTAT, URL_BITCOINCASH_BITSTAT]),
    'rates_myfin': client_myfin([URL_BITCOIN_MYFIN, URL_ETHEREUM_MYFIN, URL_BITCOINCASH_MYFIN]),
    'rates_bitinfo': client_bitinfo([URL_BITCOIN_BITINFOCHARTS, URL_ETHEREUM_BITINFOCHARTS, URL_BITCOINCASH_BITINFOCHARTS]),
     }


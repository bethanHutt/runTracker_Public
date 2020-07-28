from src import runtracker
from src import webscraper
from src import rundataclient
from src import datadisplayer
from src import dataconverter


def main():
    USE_MOCKS = False

    scraper = webscraper.WebScraper()
    client = rundataclient.Client()
    dconverter = dataconverter.DataConverter()
    ddisplayer = datadisplayer.DataDisplayer()

    rtracker = runtracker.RunTracker(
        use_mocks=USE_MOCKS,
        scraper=scraper,
        client=client,
        dconverter=dconverter,
        ddisplayer=ddisplayer)
    
    rtracker.run_runtracker()


if __name__ == '__main__':
    main()
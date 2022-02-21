from comics_scraper.main import main
from comics_scraper.comics import Series

if __name__ == '__main__':

    series = Series('civil-war-{issue}')
    series.add_issue('003-2009')

    main(series)

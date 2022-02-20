from comics_scraper.main import main
from comics_scraper.comics import Series

if __name__ == '__main__':

    series = Series('iron-man-v4-{issue}')
    series.add_issue('013')
    main(series)

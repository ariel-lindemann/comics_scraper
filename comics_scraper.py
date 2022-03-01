from comics_scraper.main import main
from comics_scraper.comics import Series

if __name__ == '__main__':

    series = Series('new-xmen-v1-{issue}')
    series.add_multiple_issues(range(133, 135))
    main(series)

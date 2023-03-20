from comics_scraper.downloader import download_issue, download_multiple_issues, find_links
from comics_scraper.comics import Issue, Series


def main(series: Series):

    issues = series.get_all_issues()
    download_multiple_issues(issues)

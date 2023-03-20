from downloader import download_issue, download_multiple_issues
from comics_scraper.comics import Issue, Series


def main(series: Series):

    issues = series.get_all_issues()
    download_multiple_issues(issues)

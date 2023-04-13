import cli
from comics_scraper import download_multiple_issues


if __name__ == '__main__':

    selected_issues = cli.cli_interaction()
    print(selected_issues)

    download_multiple_issues(selected_issues)
    print('Finished downloading')

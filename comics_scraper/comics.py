class Series:

    def __init__(self, url_sufix: str):
        self.url_suffix = url_sufix
        self.issues = dict()

    def add_issue(self, number):
        self.issues[number] = Issue(self.url_suffix, number)

    def get_issues_urls(self, issues: dict):
        issues_urls = []

        for i in issues.values():

            issues_urls.append(i.get_url())

        return issues_urls

    def get_issue(self, number):
        return self.issues[number]

    def get_all_issues(self):
        return self.issues

    def get_url(self):
        return self.url_suffix


class Issue:

    def __init__(self, series_url, number):
        self.number = number
        self.url = series_url.format(issue=number)
        self.downloaded = False
        self.read = False

    def set_downloaded(self, flag=True):
        self.downloaded = flag

    def get_url(self):
        return self.url

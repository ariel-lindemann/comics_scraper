class Series:

    def __init__(self, url_sufix: str):
        self.url_suffix = url_sufix
        self.issues = dict()

    def add_issue(self, number):
        self.issues[str(number)] = Issue(self.url_suffix, number)

    def add_multiple_issues(self, numbers):
        for n in numbers:
            self.add_issue(n)

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

    def increment_url(self):
        issue_num = self.url
        n = int(issue_num[-1])
        if n == 9:
            m = int(issue_num[-2])
            issue_num = issue_num[:-2] + f'{m+1}'
        issue_num += f'{(n+1)%10}'
        self.url = issue_num

    def set_downloaded(self, flag=True):
        self.downloaded = flag

    def get_url(self):
        return self.url

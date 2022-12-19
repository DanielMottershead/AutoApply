from dataclasses import dataclass

@dataclass
class SalaryRange:
    lower_bound: int
    upper_bound: int

    def get_average_salary(self) -> int:
        return (self.lower_bound + self.upper_bound) / 2

@dataclass
class JobPosting:
    job_id: str = ''
    job_title: str = ''
    posted: str = None
    salary_range: SalaryRange = None
    link: str = ''
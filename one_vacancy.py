class OneVacancy:
    def __init__(self, title, company_name, location, description, publication_time, vacancy_reference):
        self.title = title
        self.company_name = company_name
        self.location = location
        self.description = description
        self.publication_time = publication_time
        self.vacancy_reference = vacancy_reference

    def __str__(self):
        return f"\n\tTitle:            {self.title}" \
               f"\n\tCompany name:     {self.company_name}" \
               f"\n\tLocation:         {self.location}" \
               f"\n\tDescription:      {self.description}" \
               f"\n\tPublication time: {self.publication_time}" \
               f"\n\tReference:        {self.vacancy_reference}\n"

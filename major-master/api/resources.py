from import_export import resources, fields
from .models import Subject, StudentProfile

class SubjectAdminResource(resources.ModelResource):
    class Meta:
        model = Subject
        skip_unchanged = True
        report_skipped = True
        exclude = ('id',)
        import_id_fields = ( 'code', 'name', 'credit')

class StudentProfileAdminResource(resources.ModelResource):
    class Meta:
        model = StudentProfile
        skip_unchanged = True
        report_skipped = True
        exclude = ('id',)
        import_id_fields = ('usn', 'admission_year', 'admission_quota', 'placement')

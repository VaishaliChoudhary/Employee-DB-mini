import datetime
from django.db import models
from django.contrib.auth.models import User
import pandas as pd
import math
import threading
import time
from django.core.exceptions import ValidationError

# class FacultyProfile(models.Model):
#     # Additional information about the faculty
#     gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
#     qualification = models.CharField(max_length=255)
#     expertise = models.CharField(max_length=255)

#     def __str__(self):
#         return f'{self.faculty.name} Profile'

# class Faculty(models.Model):
#     # Basic information about the faculty
#     name = models.CharField(max_length=255)
#     short_form = models.CharField(max_length=50)  # Short form for the faculty
#     profile = models.OneToOneField(FacultyProfile, on_delete=models.CASCADE, null=True, blank=True)

#     def __str__(self):
#         return self.name

#     def clean(self):
#         # Additional validation to prevent duplicates
#         if Faculty.objects.filter(name=self.name, short_form=self.short_form).exists():
#             raise ValidationError(f'Faculty with name "{self.name}" and short form "{self.short_form}" already exists.')

#     class Meta:
#         unique_together = ('name', 'short_form')  # Ensuring name and short form combination is unique
#         verbose_name_plural="Faculties"


class Faculty(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]

    name = models.CharField(max_length=255)
    short_form = models.CharField(max_length=50,blank='True')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    qualification = models.CharField(max_length=255)
    designation=models.CharField(max_length=255,blank='True')
    expertise = models.CharField(max_length=255)

    class Meta:
        unique_together = ('name', 'short_form')  # Ensure that name and short form together are unique
        verbose_name_plural='Faculties'

    def __str__(self):
        return self.name

    def clean(self):
        if Faculty.objects.filter(name=self.name, short_form=self.short_form).exclude(id=self.id).exists():
            raise ValidationError(f'Faculty with name "{self.name}" and short form "{self.short_form}" already exists.')

    def save(self, *args, **kwargs):
        self.full_clean()  # This calls the clean method
        super(Faculty, self).save(*args, **kwargs)


class Publication(models.Model):
    PUBLICATION_TYPE_CHOICES = [
        ('JOURNAL', 'Journal'),
        ('CONFERENCE', 'Conference'),
        ('ARTICLE', 'Article'),
        ('BOOK','Book'),
        ('OTHER', 'Other')
    ]
    YEAR_CHOICES = [(str(r), str(r)) for r in range(1996, datetime.date.today().year+1)]
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Faculty, related_name='publications')
    publication_type = models.CharField(max_length=50, choices=PUBLICATION_TYPE_CHOICES)
    publication_date = models.DateField()
    # publication_year = models.PositiveIntegerField(choices=YEAR_CHOICES)
    publication_year = models.CharField(max_length=50,choices=YEAR_CHOICES)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

# Create your models here.
class Admission(models.Model):
    YEAR_CHOICES = [(str(r), str(r)) for r in range(2010, datetime.date.today().year+1)]
    admission_year = models.CharField(max_length=255, choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    CET = models.IntegerField(default = 0)
    comedk = models.IntegerField(default = 0)
    management = models.IntegerField(default = 0)
    snq = models.IntegerField(default = 0) 
    diploma = models.IntegerField(default = 0)
    CoB_incoming = models.IntegerField(default = 0)
    CoB_outgoing = models.IntegerField(default = 0) 
    total = models.IntegerField(default = 0, blank = True, null=True)

    def __str__(self):
        return "Batch: " + self.admission_year 
    
    def save(self):
        self.total = self.CET + self.comedk + self.management + self.diploma + self.CoB_incoming + self.snq + self.CoB_outgoing 
        return super(Admission, self).save()

    class Meta:
        verbose_name_plural = 'Admission'

class AdmissionFile(models.Model):
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE, related_name='admission')
    name = models.CharField(max_length=255)
    file = models.FileField()

    def __str__(self):
        return self.name

class Result(models.Model):
    YEAR_CHOICES = [(str(r), str(r)) for r in range(2010, datetime.date.today().year+1)]
    SEMESTER_CHOICES = [("1", "1"),("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"), ("6", "6"), ("7", "7"), ("8", "8")] 
    semester = models.CharField(max_length=255, choices=SEMESTER_CHOICES)
    admission_year = models.CharField(max_length=255, choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    without_backlog = models.IntegerField(default = 0)
    single_backlog = models.IntegerField(default = 0)
    double_backlog = models.IntegerField(default = 0)
    triple_backlog = models.IntegerField(default = 0)
    more_than_3_backlog = models.IntegerField(default = 0)
    dropouts = models.IntegerField(default = 0)

    def __str__(self):
        return "Batch: " + self.admission_year + " Sem: " + self.semester 

# class ResultFile(models.Model):
#     result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name='result')
#     name = models.CharField(max_length=255)
#     file = models.FileField()

#     def __str__(self):
#         return self.name 

class Placement(models.Model):
   YEAR_CHOICES = [(str(r), str(r)) for r in range(2010, datetime.date.today().year+1)] 
   admission_year = models.CharField(max_length=255, choices=YEAR_CHOICES, default=datetime.datetime.now().year)
   on_campus = models.IntegerField(default=0)
   off_campus = models.IntegerField(default=0)
   internship = models.IntegerField(default=0)

   def __str__(self):
        return self.admission_year

class PlacementFile(models.Model):
    placement = models.ForeignKey(Placement, on_delete=models.CASCADE, related_name="placement")
    name = models.CharField(max_length=255)
    file = models.FileField()

    def __str__(self):
        return self.name

class StudentProfile(models.Model):
    YEAR_CHOICES = [(str(r), str(r)) for r in range(2010, datetime.date.today().year+1)] 
    QUOTA_CHOICES = [('CET', 'CET'), ('MANAGEMENT', 'MANAGEMENT'), ('COMED-K', 'COMED-K'), ('SNQ', 'SNQ'), ('DIPLOMA', 'DIPLOMA')]
    PLACEMENT_CHOICES = [('ON_CAMPUS', 'ON_CAMPUS'), ('OFF_CAMPUS', 'OFF_CAMPUS'), ('INTERNSHIP', 'INTERNSHIP')]
    usn = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length = 255)
    admission_year = models.CharField(max_length=255, choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    admission_quota = models.CharField(max_length=255, choices=QUOTA_CHOICES) 
    placement = models.CharField(max_length=255, choices=PLACEMENT_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.usn

class Subject(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, primary_key=True)
    credit = models.IntegerField()

    def __str__(self):
        return self.name
   

class StudentResult(models.Model):
    GRADE_CHOICES = [('S', 'S'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('PP', 'PP'), ('NP', 'NP')]
    SEM_CHOICES = [('1', '1'), ('2', '2'), ('3', '3'), ('4','4'), ('5', '5'), ('6', '6'), ('7','7'), ('8', '8'), ('SUMMER 1 YEAR', 'SUMMER 1 YEAR'), ('SUMMER 2 YEAR', 'SUMMER 2 YEAR'), ('SUMMER 3 YEAR', 'SUMMER 3 YEAR'), ('SUMMER 4 YEAR', 'SUMMER 4 YEAR')]
    usn = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='result_usn')
    sem = models.CharField(max_length=255, choices=SEM_CHOICES)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject')
    grade = models.CharField(max_length=255, choices=GRADE_CHOICES)

    def __str__(self):
        return self.grade

class Template(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField()

    def __str__(self):
        return self.name

class ResultUpload(models.Model):
    YEAR_CHOICES = [(str(r), str(r)) for r in range(2010, datetime.date.today().year+1)]  
    SEM_CHOICES = [('1', '1'), ('2', '2'), ('3', '3'), ('4','4'), ('5', '5'), ('6', '6'), ('7','7'), ('8', '8'), ('SUMMER 1 YEAR', 'SUMMER 1 YEAR'), ('SUMMER 2 YEAR', 'SUMMER 2 YEAR'), ('SUMMER 3 YEAR', 'SUMMER 3 YEAR'), ('SUMMER 4 YEAR', 'SUMMER 4 YEAR')]
    admission_year = models.CharField(max_length=255, choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    sem = models.CharField(max_length=255, choices=SEM_CHOICES)
    file = models.FileField()
    uploading_done = models.BooleanField(default=True)
    error = models.TextField(blank=True, null=True, default='No Error')

    def __str__(self):
        return self.admission_year

    def save(self, *args, **kwargs):
        if self.file:
            # Access the uploaded file here
            uploaded_file = self.file
            print(uploaded_file)

            try:
                sheet_in_db = ResultUpload.objects.filter(admission_year = self.admission_year, sem = self.sem).update(file = self.file, uploading_done = False)
                print("This is filter and update", sheet_in_db)
                if not sheet_in_db:
                    self.uploading_done = False
                    super().save(*args, **kwargs) 
                # sheet_in_db.file = self.file
                # sheet_in_db.uploading_done = False
                # sheet_in_db.save()
            except:
                self.uploading_done = False
                super().save(*args, **kwargs)
                # ResultUpload.objects.create(admission_year = self.admission_year, sem = self.sem, file = self.file, uploading_done = False)
            # Process the file as needed
            # ...
            try:
                sheet_in_db = ResultUpload.objects.get(admission_year = self.admission_year, sem = self.sem)
                print("this is sheet in db", sheet_in_db.file, sheet_in_db.uploading_done)
            except:
                print("Not found in db")
            try:
                data_frame = pd.read_excel(uploaded_file, engine='openpyxl')
            except Exception as e:
                print(e)
                sheet_in_db = ResultUpload.objects.filter(admission_year = self.admission_year, sem = self.sem).update(uploading_done = False, error=e) 
                return 

            t = threading.Thread(target=ResultUpload.upload, args=(uploaded_file, data_frame, self.sem, self.admission_year), kwargs={})
            t.setDaemon(True)
            t.start()
            # data_frame = pd.read_excel(uploaded_file, engine='openpyxl')
            # column_names = data_frame.columns.tolist()
            # sem = self.sem

            # for col, row in data_frame.iterrows():
            #     try:
            #         usn = StudentProfile.objects.get(pk = row[0])
            #     except: 
            #         continue
            #     total_columns = len(column_names)
            #     for i in range(1, total_columns):
            #         try:
            #             print(f"Adding {i} column")
            #             if column_names[i].upper() == "PE" or column_names[i].upper() == "OE":
            #                 subject = Subject.objects.get(pk = row[i])
            #             elif column_names[i].upper() == "GRADE":
            #                 continue
            #             else:
            #                 subject = Subject.objects.get(pk = column_names[i])
            #         except:
            #             continue
            #         if str(row[i]) != "nan":
            #             if column_names[i].upper() == "PE" or column_names[i].upper() == "OE":
            #                 grade = row[i+1].upper()
            #             else:
            #                 grade = row[i].upper()
            #         else:
            #             continue
            #         try:
            #             result_in_db = StudentResult.objects.get(usn = usn, grade = grade, subject = subject, sem = sem)
            #             result_in_db.usn = usn
            #             result_in_db.grade = grade 
            #             result_in_db.subject =subject 
            #             result_in_db.sem =sem 
            #             result_in_db.save()
            #         except Exception as e:
            #             print(e)
            #             result = StudentResult(usn = usn, grade = grade, subject = subject, sem = sem)
            #             result.save()
                    # try:
                    #     sheet_in_db = ResultUpload.objects.get(admission_year = self.admission_year, sem = self.sem)
                    # except:
                    #     super().save(*args, **kwargs)
    
    def upload(uploaded_file, data_frame, student_sem, student_admission_year):
        print(uploaded_file, student_sem)
        try:
            column_names = data_frame.columns.tolist()
        except Exception as e:
            print(e)
            sheet_in_db = ResultUpload.objects.filter(admission_year = student_admission_year, sem = student_sem).update(uploading_done = False, error=e) 
            return
        sem = student_sem
        start = time.time()

        for col, row in data_frame.iterrows():
            try:
                usn = StudentProfile.objects.get(pk = row[0])
            except: 
                continue
            total_columns = len(column_names)
            for i in range(1, total_columns):
                try:
                    print(f"Adding {i} column")
                    if column_names[i].upper() == "PE" or column_names[i].upper() == "OE":
                        subject = Subject.objects.get(pk = row[i])
                    elif column_names[i].upper() == "GRADE":
                        continue
                    else:
                        subject = Subject.objects.get(pk = column_names[i])
                except:
                    continue
                if str(row[i]) != "nan":
                    if column_names[i].upper() == "PE" or column_names[i].upper() == "OE":
                        grade = row[i+1].upper()
                    else:
                        grade = row[i].upper()
                else:
                    continue
                try:
                    result_in_db = StudentResult.objects.get(usn = usn, grade = grade, subject = subject, sem = sem)
                    result_in_db.usn = usn
                    result_in_db.grade = grade 
                    result_in_db.subject =subject 
                    result_in_db.sem =sem 
                    result_in_db.save()
                except Exception as e:
                    print(e)
                    result = StudentResult(usn = usn, grade = grade, subject = subject, sem = sem)
                    result.save() 
        try:
            sheet_in_db = ResultUpload.objects.filter(admission_year = student_admission_year, sem = sem).update(uploading_done = True)
            end = time.time()
            time_taken = end - start
            print("Time take is", time_taken)
            print("This is filter and update", sheet_in_db)
        except:
            print("error while updating")
       










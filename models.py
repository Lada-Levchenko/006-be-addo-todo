import peewee as pw
from playhouse.fields import PasswordField
import datetime

db = pw.SqliteDatabase('database.db')


def initialize():
    User.create_table(fail_silently=True)
    Project.create_table(fail_silently=True)
    Task.create_table(fail_silently=True)
    try:
        user = User.create(
            username='root',
            password='123'
        )
    except pw.IntegrityError:
        pass


class BaseModel(pw.Model):

    class Meta:
        database = db


class User(BaseModel):
    username = pw.CharField(max_length=70, unique=True)
    password = PasswordField()
    state = pw.BooleanField(default=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.state

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % self.username


class Project(BaseModel):
    name = pw.CharField(max_length=100)
    color = pw.CharField(length=7)
    user = pw.ForeignKeyField(User, related_name="projects")

    def get_id(self):
        return self.id


class Task(BaseModel):
    PRIORITY_CHOICES = ((1, "high"), (2, "medium"), (3, "low"))
    name = pw.CharField(max_length=100)
    date = pw.DateField(default=datetime.date.today())
    priority = pw.IntegerField(choices=PRIORITY_CHOICES)
    project = pw.ForeignKeyField(Project, related_name="tasks")

    def get_id(self):
        return self.id







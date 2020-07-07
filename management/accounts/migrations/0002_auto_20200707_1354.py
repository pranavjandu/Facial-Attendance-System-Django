# Generated by Django 3.0.7 on 2020-07-07 08:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('attendance_date', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='AttendanceReport',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.BooleanField(default=False)),
                ('attendance_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Attendance')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('course_name', models.CharField(max_length=255)),
                ('session_start_date', models.DateField()),
                ('session_end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='NotificationInstructor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='NotificationStudent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='admin',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='student',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.DeleteModel(
            name='Courses',
        ),
        migrations.AddField(
            model_name='notificationstudent',
            name='student_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Student'),
        ),
        migrations.AddField(
            model_name='notificationinstructor',
            name='staff_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Instructor'),
        ),
        migrations.AddField(
            model_name='course',
            name='course_instructor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Instructor'),
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(to='accounts.Student'),
        ),
        migrations.AddField(
            model_name='attendancereport',
            name='student_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.Student'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='course_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.Course'),
        ),
    ]
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roomId', models.CharField(max_length=100, unique=True)),
                ('status', models.CharField(max_length=20, choices=[('waiting', 'Waiting'), ('in_progress', 'In Progress'), ('finished', 'Finished')], default='waiting')),
                ('currentSeq', models.IntegerField()),
                ('quizId', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]

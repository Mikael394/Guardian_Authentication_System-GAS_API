# Generated by Django 5.0.2 on 2024-05-01 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_gradeandsection_home_room_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactbook',
            name='hand_writing',
            field=models.CharField(blank=True, choices=[('Very Good', 'Very Good'), ('Good', 'Good'), ('Fair', 'Fair'), ('Need Improvement', 'Need Improvement')], max_length=20),
        ),
        migrations.AlterField(
            model_name='contactbook',
            name='parents_follow_up',
            field=models.CharField(choices=[('Very Good', 'Very Good'), ('Good', 'Good'), ('Fair', 'Fair'), ('Need Improvement', 'Need Improvement')], max_length=20, null=True),
        ),
    ]
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('predictor', '0002_alter_prediction_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('doctor', 'Médecin'), ('patient', 'Patient')], default='patient', max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='patient',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='patient_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='CDCPrediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('high_bp', models.IntegerField()),
                ('high_chol', models.IntegerField()),
                ('chol_check', models.IntegerField()),
                ('bmi', models.FloatField()),
                ('smoker', models.IntegerField()),
                ('stroke', models.IntegerField()),
                ('heart_disease', models.IntegerField()),
                ('phys_activity', models.IntegerField()),
                ('fruits', models.IntegerField()),
                ('veggies', models.IntegerField()),
                ('heavy_alcohol', models.IntegerField()),
                ('any_healthcare', models.IntegerField()),
                ('no_doc_cost', models.IntegerField()),
                ('gen_hlth', models.IntegerField()),
                ('ment_hlth', models.IntegerField()),
                ('phys_hlth', models.IntegerField()),
                ('diff_walk', models.IntegerField()),
                ('sex', models.IntegerField()),
                ('age_category', models.IntegerField()),
                ('education', models.IntegerField()),
                ('income', models.IntegerField()),
                ('probability', models.FloatField()),
                ('result', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cdc_predictions', to='predictor.patient')),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField()),
                ('medications', models.TextField(blank=True, null=True)),
                ('followup_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('prediction', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='treatment', to='predictor.cdcprediction')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='treatments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

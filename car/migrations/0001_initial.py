# Generated by Django 4.0.3 on 2022-03-13 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('hashkey', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('maker', models.CharField(db_index=True, max_length=255)),
                ('model', models.CharField(db_index=True, max_length=255)),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Market',
            fields=[
                ('code', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=25)),
                ('as24', models.CharField(max_length=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('hashkey', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('maker', models.CharField(max_length=255)),
                ('model', models.CharField(max_length=255, null=True)),
                ('frm', models.IntegerField(null=True)),
                ('to', models.IntegerField(null=True)),
                ('last', models.DateField()),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SearchLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('search', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='car.search')),
            ],
        ),
        migrations.CreateModel(
            name='CarVersion',
            fields=[
                ('hashkey', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('version', models.CharField(db_index=True, max_length=255)),
                ('year', models.IntegerField(db_index=True)),
                ('fuel', models.CharField(max_length=10, null=True)),
                ('gear', models.CharField(max_length=10, null=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('car_model', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='car.carmodel')),
            ],
        ),
        migrations.CreateModel(
            name='CarOffer',
            fields=[
                ('hashkey', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('source', models.CharField(choices=[('AS24', 'autoscout24.com'), ('SBT', 'subito.it')], db_index=True, max_length=4)),
                ('price', models.IntegerField(db_index=True)),
                ('seller', models.CharField(max_length=64, null=True)),
                ('miliage', models.IntegerField()),
                ('link', models.CharField(max_length=2048, null=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('car_version', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='car.carversion')),
                ('market', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='car.market')),
            ],
        ),
    ]

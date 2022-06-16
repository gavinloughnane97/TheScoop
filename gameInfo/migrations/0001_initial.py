# Generated by Django 4.0.4 on 2022-06-13 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('team_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('team_name', models.CharField(max_length=40)),
                ('location', models.CharField(max_length=40)),
                ('sport', models.CharField(max_length=40)),
                ('image_path', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Matchup',
            fields=[
                ('matchup_id', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('matchup_title', models.CharField(max_length=120)),
                ('time', models.DateTimeField(null=True)),
                ('away_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_team_id', to='gameInfo.team')),
                ('home_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_team_id', to='gameInfo.team')),
            ],
        ),
        migrations.CreateModel(
            name='Bet',
            fields=[
                ('bet_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('bookmaker', models.CharField(max_length=40)),
                ('bet_type', models.CharField(max_length=40)),
                ('last_updated', models.DateTimeField(null=True)),
                ('price', models.IntegerField()),
                ('version', models.IntegerField()),
                ('matchup_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gameInfo.matchup')),
                ('selected_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gameInfo.team')),
            ],
        ),
    ]
import csv
import click

from opinions_app import app, db
from opinions_app.models import Opinion
from opinions_app.utils.token_cleanup import cleanup_expired_tokens

@app.cli.command('load_opinions')
def load_opinions_command():
    """Функция загрузки мнений в базу данных."""
    with open('opinions_new.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        counter = 0
        for row in reader:
            opinion = Opinion(**row)
            db.session.add(opinion)
            db.session.commit()
            counter += 1
    click.echo(f'Загружено мнений: {counter}')


@app.cli.command('delete_opinions')
def delete_opinions_command():
    """Функция удаления мнений из базы данных."""
    counter = 0
    opinions = Opinion.query.all()
    for opinion in opinions:
        db.session.delete(opinion)
    db.session.commit()
    counter += 1
    click.echo(f'Удалено мнений: {counter}')


@app.cli.command('cleanup-tokens')
def cleanup_tokens_command():
    """Функция удаления старых токенов из базы данных."""

    count = cleanup_expired_tokens()
    click.echo(f"Старые токены удалены из базы данных (count: {count})")



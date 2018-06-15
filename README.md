## Configuration application

Create schema before running application: 
```text
CREATE SCHEMA `zarplata.ru-test` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
```

Change database connection in `config.py`
```text
SQLALCHEMY_DATABASE_URI = 'mysql://username:password@server/db'
```

Set up environment variable 
```bash
export FLASK_APP=run.py # for linux
set FLASK_APP=run.py # for Windows
```

Run migrations:
```bash
flask db upgrade
```

Load vacancies:
```bash
flask load-vacancies
```

Run application 
```
python run.py
```

For using API open url 
```
http://127.0.0.1:5000/vacancies/similar/<id>
```
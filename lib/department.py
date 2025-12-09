# lib/department.py
import sqlite3

CONN = sqlite3.connect('company.db')
CURSOR = CONN.cursor()

class Department:
    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY,
                name TEXT,
                location TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS departments"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        if self.id is None:
            sql = "INSERT INTO departments (name, location) VALUES (?, ?)"
            CURSOR.execute(sql, (self.name, self.location))
            CONN.commit()
            self.id = CURSOR.lastrowid
        else:
            self.update()
        return self

    @classmethod
    def create(cls, name, location):
        dept = cls(name, location)
        dept.save()
        return dept

    def update(self):
        sql = "UPDATE departments SET name = ?, location = ? WHERE id = ?"
        CURSOR.execute(sql, (self.name, self.location, self.id))
        CONN.commit()

    def delete(self):
        sql = "DELETE FROM departments WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        self.id = None

    @classmethod
    def instance_from_db(cls, row):
        if not row:
            return None
        return cls(row[1], row[2], id=row[0])

    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM departments"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        sql = "SELECT * FROM departments WHERE id = ?"
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row)

    @classmethod
    def find_by_name(cls, name):
        sql = "SELECT * FROM departments WHERE name = ?"
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row)

    def employees(self):
        from employee import Employee
        sql = "SELECT * FROM employees WHERE department_id = ?"
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Employee.instance_from_db(row) for row in rows]

    def __repr__(self):
        return f"<Department {self.id}: {self.name}, {self.location}>"
import sqlite3


class Database:
    __DB_PATH = "src/db/database.sqlite"

    # Устанавливаем соединение с базой данных
    def __init__(self, db_location: str | None = None):
        if db_location is not None:
            self.connection = sqlite3.connect(db_location)
        else:
            self.connection = sqlite3.connect(self.__DB_PATH)
        self.cur = self.connection.cursor()

    def __enter__(self):
        return self

    # Сохраняем изменения и закрываем соединение
    def __exit__(self, ext_type, exc_value, traceback):
        self.cur.close()
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()

    # Проверяем, является ли админом
    def is_admin(self, username: str) -> bool:
        self.cur.execute("SELECT COUNT(*) FROM admins WHERE username = ?", (username,))
        count = self.cur.fetchone()[0]
        return count > 0

    # Список администраторов
    def get_all_admins(self) -> list[str]:
        self.cur.execute("SELECT username FROM admins")
        return [row[0] for row in self.cur.fetchall()]

    # Добавляем нового админа
    def add_admin(self, username: str) -> None:
        self.cur.execute("INSERT INTO admins (username) VALUES (?)", (username,))

    # Удаляем админа
    def remove_admin(self, username: str) -> None:
        self.cur.execute("DELETE FROM admins WHERE username = ?", (username,))

    # Добавляем новую группу, в которой состоит бот
    def add_bot_group(self, group_id: int, title: str) -> None:
        self.cur.execute("INSERT INTO groups (group_id, title) VALUES (?, ?)", (group_id, title))

    # Удаляем группу, в которой бот больше не состоит
    def remove_bot_group(self, group_id: int) -> None:
        self.cur.execute("DELETE FROM groups WHERE group_id = ?", (group_id,))

    # Список всех групп с ботом
    def get_all_bot_groups(self) -> list:
        self.cur.execute("SELECT group_id, title FROM groups")
        return self.cur.fetchall()

import Db
from Entities.Project import Project


def create(project: Project):
    if _db_load_project(uid=project.uid) is not None:
        raise KeyError(f"Project {project.uid} already exists")

    Db.cursor.execute(f"""
        INSERT INTO projects VALUES('{project.uid}',
                                    '{project.name}',
                                    '{project.description}',
                                    '{project.location}',
                                    {project.is_location_coordinates},
                                    {project.is_shared},
                                    '{project.owner.uid if type(project.owner) is not str else project.owner}');
    """)

    Db.connection.commit()


def fetch(uid: str) -> Project | None:
    row = _db_load_project(uid=uid)

    if row is None:
        return None

    return Project.from_db(row)


def fetch_all() -> list[Project] | None:
    items: list[Project] = []

    rows = Db.cursor.execute("SELECT * FROM projects;").fetchall()

    if len(rows) == 0 or rows[0] is None:
        return None

    for row in rows:
        items.append(Project.from_db(row))

    return items


def update(project: Project):
    if _db_load_project(uid=project.uid) is None:
        raise KeyError(f"Project {project.uid} does not exist")

    Db.cursor.execute(f"""
        UPDATE projects WHERE uid='{project.uid}' SET ;
    """)

    Db.connection.commit()


def delete(uid: str):
    if _db_load_project(uid) is None:
        raise KeyError(f"Project {uid} does not exist")

    Db.cursor.execute(f"""
        DELETE FROM projects WHERE uid='{uid}';
    """)

    Db.connection.commit()


def _db_load_project(uid: str) -> tuple:
    return Db.cursor.execute(f"SELECT * FROM projects WHERE uid = '{uid}'").fetchone()


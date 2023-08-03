def fetch(databases) -> None:
    # 在处理完任意事件后自动保存所有已修改的数据库。
    for database in databases.values():
        if database.dirty:
            print("写入数据库", database)
            database.save()

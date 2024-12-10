import pg8000

class Triggers:
		def __init__(self, db_conn):
				self.conn = db_conn
				self.cursor = self.conn.cursor()
      
					
		def add(self, name, desc, price, size, brand_id):
				try:
						self.cursor.execute("INSERT INTO sneakers (name, desc, price, size, brand_id) VALUES (%s, %s, %s, %s, %s)", 
													(name, desc, price, size, brand_id))
						self.conn.commit()
						print("Запись успешно добавлена")
				except Exception as e:
						self.conn.rollback()
						print(e)
						
		def update(self, id, name, desc, price, size, brand_id):
				try:
						self.cursor.execute(
							'''
								UPDATE sneakers 
								SET 
									name = %s, 
									desc = %s, 
									price = %s, 
									size = %s, 
									brand_id = %s
								WHERE id = %s;
							''',
								(name, desc, price, size, brand_id, id.strip()))
						self.conn.commit()

						print("Запись успешно обновлена")
				except Exception as e:
						self.conn.rollback()
						print(e)
						

def show_menu():
		print("\033[31m\nМеню:\033[0m")
		print("\033[32m1\033[0m. Добавить запись")
		print("\033[32m2\033[0m. Обновить запись")
		print("\033[32m0\033[0m. Выйти")
        


def main():
		try:
			conn = pg8000.connect(database="db_pdfy", user="db_pdfy_user", password="lO76kHaDkk8cntFD0nabQR9aRU3aXB3g", host="dpg-ct8nm1tds78s73ce0kdg-a.oregon-postgres.render.com", port="5432")

			triggers = Triggers(conn)

			while True:
					show_menu()
					choice = input("\033[33mВыберите операцию: \033[0m")
					
					match choice.strip():
							case "1":
									name = input("Введите название кроссовка: ")
									desc = input("Введите описание кроссовка: ")
									price = input("Введите цену кроссовка: ")
									size = input("Введите размер кроссовка: ")
									brand_id = input("Введите id брэнда: ")
									triggers.add(name, desc, price, size, brand_id)
							case "2":
									id = input("Введите id кроссовка: ")
									name = input("Введите название кроссовка: ")
									desc = input("Введите описание кроссовка: ")
									price = input("Введите цену кроссовка: ")
									size = input("Введите размер кроссовка: ")
									brand_id = input("Введите id брэнда: ")
									triggers.update(id, name, desc, price, size, brand_id)
							case "0":
									print("\033[31mВыход из программы\033[0m")
									break
							case _:
									print("\033[31mЧто-то пошло не так\033[0m")
		except Exception as e:
				print(f"Ошибка при подключении к базе данных: {e}")
		finally:
			if conn:
				conn.close()




if __name__ == "__main__":
    main()
import pg8000

class ProceduresCrud:
		def __init__(self, db_conn):
				self.conn = db_conn
				self.cursor = self.conn.cursor()
      
					
		def add_provider(self, name, address, phone, email):
				try:
						self.cursor.execute("CALL add_provider(%s, %s, %s, %s)", (name, address, phone, email))
						self.conn.commit()
						print("Провайдер успешно добавлен")
				except Exception as e:
						self.conn.rollback()
						print(e)
						

		def get_all_providers(self):
				self.cursor.execute("SELECT * FROM get_all_providers()")
				rows = self.cursor.fetchall()
				max_length = [0] * len(rows[0])
				
				for row in rows:
						for i, value in enumerate(row):
								max_length[i] = max(max_length[i], len(str(value)))
				format_string = " ".join(["{:<" + str(length + 3) + "}" for length in max_length])

				for row in rows:
						print(format_string.format(*row))
						

		def get_provider_by_id(self, id):
				try:
						self.cursor.execute("SELECT * FROM get_provider_by_id(%s)", (id,))
						result = self.cursor.fetchone()
						if result:
								print("{:<20} {}".format("id:", result[0]))
								print("{:<20} {}".format("name:", result[1]))
								print("{:<20} {}".format("address:", result[2]))
								print("{:<20} {}".format("phone:", result[3]))
								print("{:<20} {}".format("email:", result[4]))
						else:
								print(f"Провайдер с id = {id} не найден")
				except Exception as e:
						self.conn.rollback()
						print(e)
						
						
		def update_provider(self, id, name, address, phone, email):
				try:
						self.cursor.execute("CALL update_provider(%s, %s, %s, %s, %s)",
								(id.strip(), name, address, phone, email))
						self.conn.commit()

						print("Провайдер успешно обновлен")
				except Exception as e:
						self.conn.rollback()
						print(e)
						

		def delete_provider(self, id):
				try:
						self.cursor.execute("CALL delete_provider(%s)", (id.strip(),))
						self.conn.commit()

						print("Провайдер успешно удален")
				except Exception as e:
						self.conn.rollback()
						print(e)
						

		def delete_list_providers(self, ids):
				try:
						self.cursor.execute("SELECT delete_list_providers(%s)", (ids,))
						deleted_count = self.cursor.fetchone()[0]
						self.conn.commit()

						print(f"Удалено провайдеров: {deleted_count}")
				except Exception as e:
						self.conn.rollback()
						print(e)
        


def show_menu():
		print("\033[31m\nМеню:\033[0m")
		print("\033[32m1\033[0m. Добавить провайдера")
		print("\033[32m2\033[0m. Вывести всех провайдеров")
		print("\033[32m3\033[0m. Вывести провайдера по id")
		print("\033[32m4\033[0m. Изменить провайдера по id")
		print("\033[32m5\033[0m. Удалить провайдера по id")
		print("\033[32m6\033[0m. Удалить список провайдеров")
		print("\033[32m0\033[0m. Выйти")
        


def main():
		conn = pg8000.connect(database="db_pdfy", user="db_pdfy_user", password="lO76kHaDkk8cntFD0nabQR9aRU3aXB3g", host="dpg-ct8nm1tds78s73ce0kdg-a.oregon-postgres.render.com", port="5432")

		crud = ProceduresCrud(conn)

		while True:
				show_menu()
				choice = input("\033[33mВыберите операцию: \033[0m")
				
				match choice.strip():
						case "1":
								name = input("Введите название провайдера: ")
								address = input("Введите адрес провайдера: ")
								phone = input("Введите номер провайдера: ")
								email = input("Введите почту провайдера: ")
								crud.add_provider(name, address, phone, email)
						case "2":
								crud.get_all_providers()
						case "3":
								id = input("Введите id провайдера: ")
								crud.get_provider_by_id(id)
						case "4":
								id = input("Введите id провайдера для обновления: ")
								name = input("Введите новое название провайдера: ")
								address = input("Введите новый адрес: ")
								phone = input("Введите новый номер: ")
								email = input("Введите новый email: ")
								crud.update_provider(id, name, address, phone, email)
						case "5":
								id = input("Введите id провайдера для удаления: ")
								crud.delete_provider(id)
						case "6":
								ids_input = input("Введите id провайдеров для удаления (через пробел): ")
								ids = ids_input.split()
								crud.delete_list_providers(ids)
						case "0":
								print("\033[31mВыход из программы\033[0m")
								break
						case _:
								print("\033[31mЧто-то пошло не так\033[0m")
						
		conn.close()




if __name__ == "__main__":
    main()
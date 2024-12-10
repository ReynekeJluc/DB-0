# import pg8000

# class Perfomances:
# 		def __init__(self, db_conn):
# 				self.conn = db_conn
# 				self.cursor = self.conn.cursor()
      
					
# 		def add(self, name, address, phone, email):
# 				try:
# 						self.cursor.execute("CALL add_provider(%s, %s, %s, %s)", (name, address, phone, email))
# 						self.conn.commit()
# 						print("Запись успешно добавлен")
# 				except Exception as e:
# 						self.conn.rollback()
# 						print(e)
						

# 		def get_all(self):
# 			self.cursor.execute("SELECT * FROM provider_payment_info")
# 			rows = self.cursor.fetchall()

# 			column_names = ["Order ID", "Payment ID", "Customer Name", "Order Date", "Payment Date", "Order Status", "Provider Name"]

# 			max_length = [len(col) for col in column_names]
			
# 			for row in rows:
# 					for i, value in enumerate(row):
# 							max_length[i] = max(max_length[i], len(str(value)))
# 			format_string = " ".join(["{:<" + str(length + 3) + "}" for length in max_length])

# 			print(format_string.format(*column_names))

# 			for row in rows:
# 					print(format_string.format(*row))


# 		def get_by_id(self, id):
# 				try:
# 						self.cursor.execute("SELECT * FROM provider_payment_info(%s)", (id,))
# 						result = self.cursor.fetchone()

# 						if result:
# 								print("{:<20} {}".format("order id:", result[0]))
# 								print("{:<20} {}".format("payment id:", result[1]))
# 								print("{:<20} {}".format("customer name:", result[2]))
# 								print("{:<20} {}".format("order date:", result[3]))
# 								print("{:<20} {}".format("payment date:", result[4]))
# 								print("{:<20} {}".format("order status:", result[5]))
# 								print("{:<20} {}".format("provider name:", result[6]))
# 						else:
# 								print(f"Запись с id = {id} не найдена")
# 				except Exception as e:
# 						self.conn.rollback()
# 						print(e)
						
						
# 		def update(self, id, name, address, phone, email):
# 				try:
# 						self.cursor.execute("CALL update_provider(%s, %s, %s, %s, %s)",
# 								(id.strip(), name, address, phone, email))
# 						self.conn.commit()

# 						print("Провайдер успешно обновлен")
# 				except Exception as e:
# 						self.conn.rollback()
# 						print(e)
						

# 		def delete(self, id):
# 				try:
# 						self.cursor.execute("CALL delete_provider(%s)", (id.strip(),))
# 						self.conn.commit()

# 						print("Запись успешно удален")
# 				except Exception as e:
# 						self.conn.rollback()
# 						print(e)


# def show_menu():
# 		print("\033[31m\nМеню:\033[0m")
# 		print("\033[32m1\033[0m. Добавить запись")
# 		print("\033[32m2\033[0m. Вывести все записи")
# 		print("\033[32m3\033[0m. Вывести запись по id")
# 		print("\033[32m4\033[0m. Изменить запись по id")
# 		print("\033[32m5\033[0m. Удалить запись по id")
# 		print("\033[32m0\033[0m. Выйти")
        


# def main():
# 		conn = pg8000.connect(database="db_pdfy", user="db_pdfy_user", password="lO76kHaDkk8cntFD0nabQR9aRU3aXB3g", host="dpg-ct8nm1tds78s73ce0kdg-a.oregon-postgres.render.com", port="5432")

# 		crud = Perfomances(conn)

# 		while True:
# 				show_menu()
# 				choice = input("\033[33mВыберите операцию: \033[0m")
				
# 				match choice.strip():
# 						case "1":
# 								name = input("Введите название провайдера: ")
# 								address = input("Введите адрес провайдера: ")
# 								phone = input("Введите номер провайдера: ")
# 								email = input("Введите почту провайдера: ")
# 								crud.add(name, address, phone, email)
# 						case "2":
# 								crud.get_all()
# 						case "3":
# 								id = input("Введите id провайдера: ")
# 								crud.get_by_id(id)
# 						case "4":
# 								id = input("Введите id провайдера для обновления: ")
# 								name = input("Введите новое название провайдера: ")
# 								address = input("Введите новый адрес: ")
# 								phone = input("Введите новый номер: ")
# 								email = input("Введите новый email: ")
# 								crud.update(id, name, address, phone, email)
# 						case "5":
# 								id = input("Введите id провайдера для удаления: ")
# 								crud.delete(id)
# 						case "0":
# 								print("\033[31mВыход из программы\033[0m")
# 								break
# 						case _:
# 								print("\033[31mЧто-то пошло не так\033[0m")
						
# 		conn.close()




# if __name__ == "__main__":
#     main()
import pg8000

class ShoeCategoryTree:   # класс методов для работы с деревом
    def __init__(self, db_conn):   # конструктор
      self.conn = db_conn
      self.cursor = self.conn.cursor()


		# Вывод дерева	
    def print_tree(self, category_id = 1, level = 0):
      self.cursor.execute("SELECT id, name, parent_id FROM categories WHERE id = %s", (category_id,))   # Сначала получаем категорию с данным category_id
      row = self.cursor.fetchone()
			
      if row:
        category_info = {'name': f"{'_' * level}{row[1]}", 'id': f"\033[32mid: {row[0]}\033[0m", 'parent_id': f"\033[33mparent_id:\033[0m {row[2]}"}
        print('{name:15} {id:20} {parent_id:20}'.format(**category_info))  # Выводим категорию с нужным отступом

			# Теперь получаем все потомки для текущей категории
      self.cursor.execute("SELECT id, name FROM categories WHERE parent_id = %s", (category_id,))
      rows = self.cursor.fetchall()
			
      for row in rows:
        self.print_tree(row[0], level + 1)  # Рекурсивно выводим дочерние категории с увеличенным отступом (row[0] - идентификатор дочерней категории)


		# Добавление листа
    def add_leaf(self, name, parent_id = None):
      row = get_node(self, parent_id)
      
      if row:
        try:
          self.cursor.execute("INSERT INTO categories (name, parent_id) VALUES (%s, %s) RETURNING id", (name, parent_id))
          self.conn.commit()
          
          category_id = self.cursor.fetchone()[0]
          print(f"\033[32mКатегория {name} добавлена с id = {category_id}\033[0m")
          
          return category_id
        except:
          self.conn.rollback()   # явный откат транзакции после перехвата ошибки
          print(f"\033[31mНеверный ввод имени\033[0m")
      else:
        print(f"\033[31mНеверный ввод родителя\033[0m") 



	  # Удаление листа
    def delete_leaf(self, category_id):
      row = get_node(self, category_id)
      
      if row:
        self.cursor.execute("SELECT COUNT(*) FROM categories WHERE parent_id = %s", (category_id,))    # проверка узла, является ли он узлом
        has_children = self.cursor.fetchone()[0] > 0

        if has_children:
          self.delete_non_leaf_node(category_id);
        else:
          self.cursor.execute("DELETE FROM categories WHERE id = %s", (category_id,))
          self.conn.commit()
		  	  
          print(f"\033[32mКатегория с id {category_id} удалена\033[0m")
      else:
        print(f"\033[31mКатегория с id '{category_id}' не найдена\033[0m")


    # Удаление узла без поддерева
    def delete_non_leaf_node(self, category_id):
      row = get_node(self, category_id)
      
      if row:
        self.cursor.execute("SELECT parent_id FROM categories WHERE id = %s", (category_id,))   # Найти родителя удаляемого узла
        parent_id = self.cursor.fetchone()[0]
    
        if parent_id is None:
            print(f"\033[33mКатегория с id = {category_id} является корнем и не может быть удалена таким образом\033[0m")
            return
    
        # Переназначить всех прямых потомков удаляемого узла его родителю
        self.cursor.execute("UPDATE categories SET parent_id = %s WHERE parent_id = %s", (parent_id, category_id))
        
        # Удалить узел
        self.cursor.execute("DELETE FROM categories WHERE id = %s", (category_id,))
        self.conn.commit()
    
        print(f"\033[32mКатегория с id = {category_id} удалена, её потомки переназначены категории с id = {parent_id}\033[0m")
      else:
        print(f"\033[31mКатегория с id '{category_id}' не найдена\033[0m")


    # Удаление поддерева для указанной категории
    def delete_subtree(self, parent_id):
      row = get_node(self, parent_id)
      
      if row:
        self.cursor.execute(
            """
            WITH RECURSIVE to_delete AS (
                SELECT id FROM categories WHERE id = %s
                UNION
                SELECT c.id FROM categories c
                INNER JOIN to_delete td ON c.parent_id = td.id
            )
            DELETE FROM categories WHERE id IN (SELECT id FROM to_delete)
            """,
            (parent_id,)
        )
        self.conn.commit()
        
        print(f"\033[32mПоддерево категории с id = {parent_id} удалено\033[0m")
      else:
        print(f"\033[31mКатегория с id '{parent_id}' не найдена\033[0m")


	  # Получение прямого родителя
    def get_parent(self, category_id):
      category_id = get_node(self, category_id);
      
      if category_id:
        self.cursor.execute("SELECT parent_id, name FROM categories WHERE id = %s", (category_id[0],))
        
        parent_id = self.cursor.fetchone()
        
        if parent_id[0] == None:
          print(f"\033[33mУ корня нет родителя\033[0m")
          return None
        
        print(f"\033[32mРодитель категории с id = {category_id[0]}\033[0m - \033[33mкатегория с id {parent_id[0]}: {parent_id[1]}\033[0m") 
      else:
        print(f"\033[31mНеверные входные данные - id: '{category_id}'\033[0m") 


    # Получение всех родителей категории
    def get_all_ancestors(self, category_id):
      category_id = get_node(self, category_id)

      if category_id:
        self.cursor.execute(
          """
            WITH RECURSIVE ancestors AS (
                SELECT id, name, parent_id 
                FROM categories 
                WHERE id = %s
                UNION
                SELECT c.id, c.name, c.parent_id 
                FROM categories c 
                INNER JOIN ancestors a ON c.id = a.parent_id
            ) 
            SELECT id, name, parent_id FROM ancestors WHERE parent_id IS NOT NULL
          """, 
          (category_id[0],)
        )
        rows = self.cursor.fetchall()
        
        if rows:
          print(f"\033[33mРодители категории с id = {category_id[0]}:\033[0m")
          for row in rows:
            category_info = {'id': f"Категория с id = \033[32m{row[0]}\033[0m", 'name': f"Название: \033[32m{row[1]}\033[0m", 'parent_id': f"Родительский id: \033[32m{row[2]}\033[0m"}
            print('{id:35} {name:30} {parent_id:25}'.format(**category_info))
        else:
          print(f"\033[31mДля категории с id = {category_id[0]} нет родителей\033[0m")
        
        return rows
      else:
        print(f"\033[31mНеверные входные данные - id: '{category_id}'\033[0m")


		# Получение прямых потомков для категории
    def get_children(self, parent_id):
      category_id = get_node(self, parent_id)

      if category_id:
        self.cursor.execute("SELECT id, name FROM categories WHERE parent_id = %s", (parent_id,))
        rows = self.cursor.fetchall()
  
        if rows:
          print(f"\033[33mПрямые потомки категории с id = {parent_id}:\033[0m")
          for row in rows:
            category_info = {'info': f"Категория с id = \033[32m{row[0]}\033[0m", 'name': f"имя: \033[33m{row[1]}\033[0m"}
            print('{info:30} {name:20}'.format(**category_info))
        else:
          print(f"\033[31mКатегория с id = {parent_id} не имеет прямых потомков.\033[0m")
      else:
        print(f"\033[31mНеверные входные данные - id: '{category_id}'\033[0m")


    # Получение всех потомков категории
    def get_all_descendants(self, parent_id):
      category_id = get_node(self, parent_id)

      if category_id:
        self.cursor.execute(
          """
            WITH RECURSIVE descendants AS (
                SELECT id, name, parent_id 
                FROM categories 
                WHERE parent_id = %s
                UNION
                SELECT c.id, c.name, c.parent_id 
                FROM categories c 
                INNER JOIN descendants d ON c.parent_id = d.id
            ) 
            SELECT id, name, parent_id FROM descendants
          """, 
          (parent_id,)
        )
        rows = self.cursor.fetchall()
        
        if rows:
          print(f"\033[33mПотомки категории с id = {parent_id}:\033[0m")
          for row in rows:
            category_info = {'id': f"Категория с id = \033[32m{row[0]}\033[0m", 'name': f"Название: \033[32m{row[1]}\033[0m", 'parent_id': f"Родительский id: \033[32m{row[2]}\033[0m"}
            print('{id:35} {name:30} {parent_id:25}'.format(**category_info))
        else:
          print(f"\033[31mДля категории с id = {parent_id} нет потомков\033[0m")
        
        return rows
      else:
        print(f"\033[31mНеверные входные данные - id: '{category_id}'\033[0m")



#! Вспомогательные функции

# Получение и вывод информации о категории по id
def get_node(self, category_id):
    try:
      category_id = int(category_id)
    except:
      print(f"\033[31mОшибка id - '{category_id}'\033[0m")
      return None
    
    self.cursor.execute("SELECT id, name, parent_id FROM categories WHERE id = %s", (category_id,))
    return self.cursor.fetchone()


def show_menu():
    print("\033[31m\nМеню:\033[0m")
    print("\033[32m1\033[0m. Вывести всё дерево")
    print("\033[32m2\033[0m. Вставить лист")
    print("\033[32m3\033[0m. Удалить лист")
    print("\033[32m4\033[0m. Получить прямого родителя категории")
    print("\033[32m5\033[0m. Получить прямых потомков категории")
    print("\033[32m6\033[0m. Получить всех родителей категории")
    print("\033[32m7\033[0m. Получить всех потомков категории")
    print("\033[32m8\033[0m. Удалить поддерево")
    print("\033[32m9\033[0m. Удалить узел без поддерева")
    print("\033[32m0\033[0m. Выйти")




def main():
    # задачи:
    # — добавление листа; +
		# — удаление листа; +
		# — удаление поддерева; +
		# — удаление узла без поддерева; +
		# — получение прямых потомков; +
		# — получение прямого родителя; +
		# — получение всех потомков; +
		# — получение всех родителей; +

    conn = pg8000.connect(database="db_a10c", user="db_a10c_user", password="A0khoNqbLhlUvzuv7hlR3aZAWp0au3s3", host="dpg-csksr2u8ii6s7380n160-a.oregon-postgres.render.com", port="5432")
    # postgresql://db_a10c_user:A0khoNqbLhlUvzuv7hlR3aZAWp0au3s3@dpg-csksr2u8ii6s7380n160-a.oregon-postgres.render.com/db_a10c
    
    tree = ShoeCategoryTree(conn)

    while True:
      show_menu()
      choice = input("\033[33mВыберите операцию: \033[0m")
      
      match choice:
        case "1":
          tree.print_tree()
        case "2":
          name = input("Введите название категории: ")
          parent_id = input("Введите id родительской категории: ")
          tree.add_leaf(name, parent_id)
        case "3":
          category_id = input("Введите id листа для удаления: ")
          tree.delete_leaf(category_id);
        case "4":
          category_id = input("Введите id категории, родителя которого хотите узнать: ")
          tree.get_parent(category_id);
        case "5":
          category_id = input("Введите id категории, потомков которого хотите узнать: ")
          tree.get_children(category_id);
        case "6":
          category_id = input("Введите id категории, всех родителей которого хотите узнать: ")
          tree.get_all_ancestors(category_id);
        case "7":
          category_id = input("Введите id категории, всех потомков которого хотите узнать: ")
          tree.get_all_descendants(category_id);
        case "8":
          category_id = input("Введите id категории, поддерево которого хотите удалить: ")
          tree.delete_subtree(category_id);
        case "9":
          category_id = input("Введите id категории для удаления: ")
          tree.delete_non_leaf_node(category_id);
        case "0":
          print("\033[32mВыход из программы\033[0m")
          break
        case _:
          print("\033[31mЧто-то пошло не так\033[0m")
            
    conn.close()




if __name__ == "__main__":
    main()
import pg8000

class CategoryTree:   # класс методов для работы с деревом
    def __init__(self, db_conn):   # конструктор
      self.conn = db_conn
      self.cursor = self.conn.cursor()


		# Добавление листа
    def add_leaf(self, name, parent_id = None):
      row = get_node(self, parent_id)
      
      if row:
        try:
          self.cursor.execute("INSERT INTO categories (name, parent_id) VALUES (%s, %s) RETURNING id", (name, parent_id))
          self.conn.commit()   # подтверждение изменений в базе
          
          category_id = self.cursor.fetchone()[0]
          print(f"\033[32mКатегория {name} добавлена с id = {category_id}\033[0m")
          
          #return category_id
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
        self.cursor.execute("DELETE FROM categories WHERE id = %s", (parent_id,))   # благодаря ограничению можем удалить просто по айди
        self.conn.commit()     #  фиксирует все изменения в базе, делая их постоянными
        
        print(f"\033[32mПоддерево категории с id = {parent_id} удалено\033[0m")
      else:
        print(f"\033[31mКатегория с id '{parent_id}' не найдена\033[0m")


	  # Получение прямого родителя
    def get_parent(self, category_id):
      category_id = get_node(self, category_id);
      
      if category_id:
        self.cursor.execute("SELECT id, name FROM categories WHERE id = %s", (category_id[2],))
        parent_id = self.cursor.fetchone()
        
        # print(parent_id)

        if not parent_id or parent_id[0] == None:
          print(f"\033[33mУ корня нет родителя\033[0m")
          return None
        
        print(f"\033[32mРодитель категории {category_id[1]} с id = {category_id[0]}\033[0m - \033[33mкатегория с id {parent_id[0]}: {parent_id[1]}\033[0m") 
      else:
        print(f"\033[31mНеверные входные данные - id: '{category_id}'\033[0m") 


    # Получение всех родителей категории
    def get_all_ancestors(self, category_id, level = 0):
      category_id = get_node(self, category_id)
  
      if category_id:
          # Начальный запрос - получение категории с введенным айди
          # Рекурсивный - находим для каждой категории ее родительские элементы и добавляем
          self.cursor.execute(
              """
                  WITH RECURSIVE ancestors AS (
                      SELECT id, name, parent_id 
                      FROM categories 
                      WHERE id = %s
                      UNION
                      SELECT c.id, c.name, c.parent_id 
                      FROM categories AS c 
                      INNER JOIN ancestors AS a ON c.id = a.parent_id
                  ) 
                  SELECT id, name, parent_id FROM ancestors
              """,
              (category_id[0],)
          )
          rows = list(self.cursor.fetchall())     # Преобразуем в список явно
  
          if rows:
              
              # for x in rows:
              #    print(x)

              rows.reverse()  # Для корректного порядка - корень вверху
              print(f"\033[33mРодители категории с id = {category_id[0]}:\033[0m")

              for row in rows:
                  category_info = {
                      'name': f"{'___' * level}{row[1]}",
                      'id': f"\033[32mid: {row[0]}\033[0m",
                      'parent_id': f"\033[33mparent_id:\033[0m {row[2]}"
                  }
                  print('{name:30} {id:20} {parent_id:20}'.format(**category_info))

                  level += 1
          else:
              print(f"\033[31mДля категории с id = {category_id[0]} нет родителей\033[0m")
      else:
          print(f"\033[31mНеверные входные данные - id: '{category_id}'\033[0m")

    
    # Получение прямых потомков
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
    def get_all_descendants(self, parent_id, level = 0):
      category_id = get_node(self, parent_id)
  
      if category_id:
          # Начальный запрос - получение категории с введенным айди
          # Рекурсивный - находим для каждой категории ее дочерние элементы и добавляем
          self.cursor.execute(
              """
                  WITH RECURSIVE descendants AS (
                      SELECT id, name, parent_id 
                      FROM categories 
                      WHERE id = %s
                      UNION
                      SELECT c.id, c.name, c.parent_id 
                      FROM categories AS c 
                      INNER JOIN descendants AS d ON c.parent_id = d.id
                  ) 
                  SELECT id, name, parent_id FROM descendants
              """,
              (category_id[0],)
          )
          rows = list(self.cursor.fetchall())  # Преобразуем в список явно
  
          if rows:
              rows_dict = {row[0]: {'name': row[1], 'parent_id': row[2]} for row in rows}   # преобразуем в словарь (для удобного поиска): id - ключ, имя и родитель - значение
              self._print_descendants_tree(rows_dict, category_id[0], level)   # рекурсивный вывод дерева
          else:
              print(f"\033[31mДля категории с id = {parent_id} нет потомков\033[0m")
      else:
          print(f"\033[31mНеверные входные данные - id: '{parent_id}'\033[0m")


    def _print_descendants_tree(self, rows_dict, current_id, level):
        current = rows_dict.get(current_id)   # пытамся получить (существует ли запись)

        if current:
            category_info = {
                'name': f"{'___' * level}{current['name']}",
                'id': f"\033[32mid: {current_id}\033[0m",
                'parent_id': f"\033[33mparent_id:\033[0m {current['parent_id']}"
            }
            print('{name:30} {id:20} {parent_id:20}'.format(**category_info))
    
            for child_id, child in rows_dict.items():
                if child['parent_id'] == current_id:
                    self._print_descendants_tree(rows_dict, child_id, level + 1)




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
    
    tree = CategoryTree(conn)

    while True:
      show_menu()
      choice = input("\033[33mВыберите операцию: \033[0m")
      
      match choice:
        case "1":
          tree.get_all_descendants(1)
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

import pg8000

class CategoryTree:   # класс методов для работы с деревом
    def __init__(self, db_conn):   # конструктор
      self.conn = db_conn
      self.cursor = self.conn.cursor()


    def print_tree(self, category_path="1", level=0, printed_paths=None):
      if printed_paths is None:
          printed_paths = set()  # Множество для отслеживания уже выведенных путей
  
      # Получаем категорию по path
      self.cursor.execute("SELECT id, name, path FROM categories WHERE path = %s", (category_path,))
      row = self.cursor.fetchone()
  
      if row:
          # Проверяем, если путь уже был выведен
          if row[2] in printed_paths:
              return
          printed_paths.add(row[2])
  
          category_info = {
              'name': f"{'___' * level}{row[1]}",
              'id': f"\033[32mid: {row[0]}\033[0m",
              'path': f"\033[33mpath:\033[0m {row[2]}"
          }
          print('{name:30} {id:20} {path:20}'.format(**category_info))  # Вывод категории с нужным отступом
  
          # Получаем дочерние категории (поиск по path с использованием LIKE)
          self.cursor.execute("SELECT id, name, path FROM categories WHERE path LIKE %s AND path != %s", 
                              (f"{category_path}/%", category_path))
          rows = self.cursor.fetchall()
  
          for row in rows:
              self.print_tree(row[2], level + 1, printed_paths)  # Передаем отслеживание путей


    # Добавление листа
    def add_leaf(self, name, parent_id=1):
      row = get_node(self, parent_id)
      
      if row:
        # Получаем путь родительской категории по parent_id
        self.cursor.execute("SELECT path FROM categories WHERE id = %s", (parent_id,))
        parent = self.cursor.fetchone()
    
        if parent:
            # Получаем следующий ID для новой категории
            self.cursor.execute("SELECT nextval('categories_id_seq')")  # Получаем следующий ID
            new_id = self.cursor.fetchone()[0]
    
            # Формируем новый путь с использованием родительского пути и нового ID
            new_path = f"{parent[0]}/{new_id}"
            
            # Вставляем новую категорию с этим путем
            try:
                self.cursor.execute("INSERT INTO categories (name, path) VALUES (%s, %s)", (name, new_path))
                self.conn.commit()
    
                print(f"\033[32mКатегория '{name}' добавлена с path = {new_path}\033[0m")
            except Exception as e:
                self.conn.rollback()
                print(f"\033[31mОшибка при добавлении категории: {e}\033[0m")
        else:
            print(f"\033[31mРодительская категория с id '{parent_id}' не найдена\033[0m")
      else:
        print(f"\033[31mНеверный ввод родителя\033[0m") 
    

    # Удаление листа
    def delete_leaf(self, category_id):
      row = get_node(self, category_id)
      
      if row:
        category_path = row[2]
        
        # Проверяем, есть ли потомки у данной категории по пути
        self.cursor.execute("SELECT COUNT(*) FROM categories WHERE path LIKE %s AND path != %s", (f"{category_path}/%", category_path))
        has_children = self.cursor.fetchone()[0] > 0

        if has_children:
            self.delete_non_leaf_node(category_id)
        else:
            # Удаляем категорию, если она является листом
            self.cursor.execute("DELETE FROM categories WHERE id = %s", (category_id,))
            self.conn.commit()
            
            print(f"\033[32mКатегория с id {category_id} удалена\033[0m")
      else:
        print(f"\033[31mКатегория с id '{category_id}' не найдена\033[0m")

    

    # Удаление поддерева
    def delete_subtree(self, category_path):
        self.cursor.execute("DELETE FROM categories WHERE path LIKE %s", (f"{category_path}/%",))
        self.cursor.execute("DELETE FROM categories WHERE path = %s", (category_path,))
        self.conn.commit()
        print(f"\033[32mПоддерево категории с path {category_path} удалено\033[0m")
    

		# Удаление узла без поддерева
    def delete_non_leaf_node(self, category_id):
      row = get_node(self, category_id)
      if not row:
          print(f"\033[31mКатегория с id '{category_id}' не найдена\033[0m")
          return
  
      # Проверяем, является ли узел корнем
      if row[2] is None:
          print(f"\033[33mКатегория с id = {category_id} является корнем и не может быть удалена\033[0m")
          return
  
      # Получаем parent_id и текущий path узла
      parent_id = row[2]
      self.cursor.execute("SELECT path FROM categories WHERE id = %s", (category_id,))
      current_path = self.cursor.fetchone()[0]
  
      # Получаем path родителя
      self.cursor.execute("SELECT path FROM categories WHERE id = %s", (parent_id,))
      parent_path = self.cursor.fetchone()[0]
  
      # Переназначаем потомков удаляемого узла его родителю
      self.cursor.execute(
          """
          	UPDATE categories
          	SET parent_id = %s, path = REPLACE(path, %s, %s)
          	WHERE path LIKE %s
          """,
          (parent_id, current_path, parent_path, f"{current_path}.%")
      )
  
      # Удаляем сам узел
      self.cursor.execute("DELETE FROM categories WHERE id = %s", (category_id,))
      self.conn.commit()
  
      print(f"\033[32mКатегория с id = {category_id} удалена, её потомки переназначены категории с id = {parent_id}\033[0m")
  
  
  
    # Получение прямого родителя
    def get_parent(self, category_path):
        self.cursor.execute("SELECT path FROM categories WHERE path = %s", (category_path,))
        row = self.cursor.fetchone()
    
        if row:
            parent_path = '/'.join(category_path.split('/')[:-1])
            if parent_path:
                self.cursor.execute("SELECT path, name FROM categories WHERE path = %s", (parent_path,))
                parent = self.cursor.fetchone()
                if parent:
                    print(f"\033[32mРодитель категории {category_path}: {parent[1]} с path = {parent[0]}\033[0m")
                else:
                    print("\033[33mРодитель отсутствует (корень дерева)\033[0m")
            else:
                print("\033[33mКорневая категория не имеет родителя\033[0m")
        else:
            print(f"\033[31mКатегория с path '{category_path}' не найдена\033[0m")
    

    # Получение всех родителей
    def get_all_ancestors(self, category_path):
        path_parts = category_path.split('/')
        if len(path_parts) <= 1:
            print("\033[33mКорень не имеет предков\033[0m")
            return
    
        for i in range(1, len(path_parts)):
            ancestor_path = '/'.join(path_parts[:i])
            self.cursor.execute("SELECT name, path FROM categories WHERE path = %s", (ancestor_path,))
            ancestor = self.cursor.fetchone()
            if ancestor:
                print(f"\033[32mПредок: {ancestor[0]} с path = {ancestor[1]}\033[0m")
    

    # Получение прямых потомков
    def get_children(self, category_path):
        self.cursor.execute("SELECT name, path FROM categories WHERE path LIKE %s AND LENGTH(path) = LENGTH(%s) + LENGTH(name) + 1", 
                            (f"{category_path}/%", category_path))
        rows = self.cursor.fetchall()
    
        if rows:
            print(f"\033[33mПрямые потомки категории {category_path}:\033[0m")
            for row in rows:
                print(f"\033[32mПотомок: {row[0]} с path = {row[1]}\033[0m")
        else:
            print(f"\033[31mКатегория {category_path} не имеет прямых потомков\033[0m")
    

    # Получение всех потомков
    def get_all_descendants(self, category_path):
        self.cursor.execute("SELECT name, path FROM categories WHERE path LIKE %s AND path != %s", (f"{category_path}/%", category_path))
        rows = self.cursor.fetchall()
    
        if rows:
            print(f"\033[33mВсе потомки категории {category_path}:\033[0m")
            for row in rows:
                indent = '___' * (row[1].count('/') - category_path.count('/') - 1)
                print(f"{indent}\033[32m{row[0]} с path = {row[1]}\033[0m")
        else:
            print(f"\033[31mКатегория {category_path} не имеет потомков\033[0m")
    



def get_node(self, category_id):
    try:
        category_id = int(category_id)
    except ValueError:
        print(f"\033[31mОшибка id - '{category_id}'\033[0m")
        return None

    self.cursor.execute("SELECT id, name, path FROM categories WHERE id = %s", (category_id,))
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
		# — удаление узла без поддерева; 
		# — получение прямых потомков; +
		# — получение прямого родителя; +
		# — получение всех потомков; +
		# — получение всех родителей; +
    
    conn = pg8000.connect(database="db_a10c", user="db_a10c_user", password="A0khoNqbLhlUvzuv7hlR3aZAWp0au3s3", host="dpg-csksr2u8ii6s7380n160-a.oregon-postgres.render.com", port="5432")
          
    tree = CategoryTree(conn)

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
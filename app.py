from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

class TreeNode:
    def __init__(self, name, due_date, tags, notes, priority):
        self.name = name
        self.due_date = due_date
        self.tags = tags
        self.notes = notes
        self.priority = priority  
        self.left = None
        self.right = None

class TaskManager:
    def __init__(self):
        self.root = None

    def add_task(self, name, due_date, tags, notes, priority):
        new_task = TreeNode(name, due_date, tags, notes, priority)
        if self.root is None:
            self.root = new_task
        else:
            self._add_task(self.root, new_task)

    def _add_task(self, current, new_task):
        if new_task.priority == 'baja':
            if current.right is None:
                current.right = new_task
            else:
                self._add_task(current.right, new_task)
        else:
            if current.left is None:
                current.left = new_task
            else:
                self._add_task(current.left, new_task)

    def search_tasks(self, query):
        results = []
        self._search_tasks(self.root, query, results)
        return results

    def _search_tasks(self, current, query, results):
        if current:
            if query.lower() in current.name.lower():
                results.append(current)
            self._search_tasks(current.left, query, results)
            self._search_tasks(current.right, query, results)

    def delete_task(self, name):
        self.root = self._delete_task(self.root, name)

    def _delete_task(self, current, name):
        if current is None:
            return current
        if name < current.name:
            current.left = self._delete_task(current.left, name)
        elif name > current.name:
            current.right = self._delete_task(current.right, name)
        else:
            if current.left is None:
                return current.right
            elif current.right is None:
                return current.left
            temp = self._min_value_node(current.right)
            current.name = temp.name
            current.right = self._delete_task(current.right, temp.name)
        return current

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def get_all_tasks(self):
        all_tasks = []
        self._inorder_traversal(self.root, all_tasks)
        return all_tasks

    def _inorder_traversal(self, node, all_tasks):
        if node is not None:
            if node != self.root:
                all_tasks.append(node)
            self._inorder_traversal(node.left, all_tasks)
            self._inorder_traversal(node.right, all_tasks)

task_manager = TaskManager()

@app.route('/')
def home():
    has_root = task_manager.root is not None
    return render_template('index.html', has_root=has_root)

@app.route('/add-root', methods=['GET', 'POST'])
def add_root():
    if request.method == 'POST':
        name = request.form['nombre']
        due_date = request.form['fecha']
        tags = request.form['etiquetas']
        notes = request.form['notas']
        priority = 'alta'
        task_manager.add_task(name, due_date, tags.split(','), notes, priority)
        return redirect(url_for('view_project'))
    return render_template('add_root.html')

@app.route('/view-project', methods=['GET', 'POST'])
def view_project():
    if request.method == 'POST':
        name = request.form['nombre']
        due_date = request.form['fecha']
        tags = request.form['etiquetas']
        notes = request.form['notas']
        priority = request.form['priority']
        task_manager.add_task(name, due_date, tags.split(','), notes, priority)
    all_tasks = task_manager.get_all_tasks()
    return render_template('view_project.html', project=task_manager.root, tasks=all_tasks)

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    results = task_manager.search_tasks(query)
    return render_template('view_project.html', project=task_manager.root, tasks=results)

@app.route('/eliminar', methods=['POST'])
def eliminar():
    task_name = request.form['task_name']
    task_manager.delete_task(task_name)
    return redirect(url_for('view_project'))

if __name__ == '__main__':
    app.run(debug=True)

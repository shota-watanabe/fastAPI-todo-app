'use client';

import { useState, useEffect, FormEvent } from 'react';
import { api } from '@/api/client';
import { components } from '@/api/types';

type Todo = components['schemas']['Todo']

export default function Home() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [newTodoContent, setNewTodoContent] = useState('');

  const fetchTodos = async () => {
    try {
      const response = await api.todos.list();
      setTodos(response);
    } catch (error) {
      console.error(error);
      alert('Todoリストの読み込みに失敗しました。');
    }
  };

  const addTodo = async (e: FormEvent) => {
    e.preventDefault(); // フォームのデフォルト送信を防ぐ
    // if (!newTodoContent.trim()) return; // 空の場合は追加しない

    try {
      await api.todos.create(newTodoContent)
      // 追加が成功したら、リストを再読み込みして表示を更新
      fetchTodos();
      setNewTodoContent(''); // 入力フォームをクリア
    } catch (error) {
      console.error(error);
      alert('Todoの追加に失敗しました。');
    }
  };

  // DELETE: Todoを削除する
  const deleteTodo = async (id: number) => {
    try {
      await api.todos.delete(id)
      // 削除が成功したら、リストを再読み込みして表示を更新
      fetchTodos();
    } catch (error) {
      console.error(error);
      alert('Todoの削除に失敗しました。');
    }
  };

  // コンポーネントが最初にマウントされたときにTodoリストを取得する
  useEffect(() => {
    fetchTodos();
  }, []);

  return (
    <main className="flex flex-col items-center min-h-screen bg-gray-100 p-4 sm:p-8">
      <div className="w-full max-w-2xl bg-white rounded-lg shadow-lg p-6">
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-6">
          Todo App
        </h1>

        {/* Todo追加フォーム */}
        <form onSubmit={addTodo} className="flex gap-2 mb-6">
          <input
            type="text"
            value={newTodoContent}
            onChange={(e) => setNewTodoContent(e.target.value)}
            placeholder="新しいTodoを入力"
            className="flex-grow p-3 border border-gray-300 rounded-lg text-black focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
          />
          <button
            type="submit"
            className="bg-blue-500 text-white font-semibold px-6 py-3 rounded-lg hover:bg-blue-600 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
          >
            追加
          </button>
        </form>

        {/* Todoリスト */}
        <ul className="space-y-3">
          {todos.map((todo) => (
            <li
              key={todo.id}
              className="flex items-center justify-between bg-gray-50 p-4 rounded-lg shadow-sm hover:bg-gray-100 transition-colors"
            >
              <span className="text-gray-700 text-lg">{todo.content}</span>
              <button
                onClick={() => deleteTodo(todo.id)}
                className="text-red-500 hover:text-red-700 font-semibold transition-colors focus:outline-none"
              >
                削除
              </button>
            </li>
          ))}
        </ul>
      </div>
    </main>
  );
}

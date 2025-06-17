import axios from 'axios';
import { components, operations } from './types';

// User型の定義を参照
type Todo = components['schemas']['Todo'];

const baseInfo = axios.create({
    baseURL: process.env.API_URL,
    headers: {
        'X-Requested-With': 'XMLHttpRequest',
    },
    withCredentials: true,
})

// APIクライアントの実装
export const api = {
  todos: {
    list: async (params?: operations['read_todos_todos__get']['parameters']['query']): Promise<Todo[]> => {
      const response = await baseInfo.get('/todos', { params });
      return response.data;
    },
    create: async (content: operations['create_todo_todos__post']['requestBody']['content']['application/json']['content']): Promise<Todo[]> => {
      const response = await baseInfo.post('/todos', { content });
      return response.data;
    },
    delete: async (id: operations['delete_todo_todos__todo_id__delete']['parameters']['path']['todo_id']): Promise<Todo[]> => {
      const response = await baseInfo.delete(`/todos/${id}`);
      return response.data;
    },
  }
};